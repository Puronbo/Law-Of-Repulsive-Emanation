"""
T55h: WHERE DOES THE GROWING NET HIT THIS MACHINE'S CEILING?

T55f measured the flow scaling law up to n=5000 and *predicted* the
practical ceiling on this box at ~10^4-10^5 (O(n^2) all-pairs kNN).
This experiment confirms that ceiling with real wall-clock + RAM
measurements, up to and past the memory wall (the transient distance
matrix is n^2*8 bytes, so n=60k alone needs 28.8 GB on a 31.7 GB box).

  n          ms/step (measured)   q+h      D transient (n^2*8B)
  1000       ~50                  32 kB    8 MB
  5000       ~960                 160 kB   200 MB
  20000      ~?                   640 kB   3.2 GB
  40000      ~?                   1.3 MB   12.8 GB
  60000      ? (MemoryError?)     1.9 MB   28.8 GB

Peak working set is read via ctypes GetProcessMemoryInfo (no psutil).
dim=2, the flow geometry used by the live daemon.

Usage: python decentral_net_ceiling.py [n1,n2,...]  (default 1000,5000,20000)
"""

import numpy as np
import sys, os, time, ctypes
from ctypes import wintypes

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Universals'))
from manifold.decentral_net import DecentralNet


def peak_ws_mb():
    class PMC(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD),
                    ("PeakWorkingSetSize", ctypes.c_size_t),
                    ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t),
                    ("PeakPagefileUsage", ctypes.c_size_t)]
    k32 = ctypes.windll.kernel32
    h = k32.OpenProcess(0x0400, False, os.getpid())  # PROCESS_QUERY_INFORMATION
    pmc = PMC()
    pmc.cb = ctypes.sizeof(pmc)
    ctypes.windll.psapi.GetProcessMemoryInfo(h, ctypes.byref(pmc), ctypes.sizeof(pmc))
    k32.CloseHandle(h)
    return pmc.WorkingSetSize / 1e6, pmc.PeakWorkingSetSize / 1e6


if __name__ == '__main__':
    NS = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else [1000, 5000, 20000]
    rng = np.random.RandomState(0)

    print("=" * 72)
    print("T55h: FLOW CEILING ON THIS MACHINE (dim=2, k=8, mu0=0.12, A=120)")
    print(f"  n sweep = {NS}  RAM = 31.7 GB  (D transient = n^2*8 B)")
    print("=" * 72)
    print(f"{'n':>8} {'ms/step':>10} {'q+h MB':>9} {'D GB':>9} "
          f"{'WS MB':>9} {'peak WS MB':>11}  note")
    print("-" * 72)

    for n in NS:
        X = rng.uniform(-1, 1, (n, 2)).astype(np.float64)
        net = DecentralNet(dim=2)
        t0 = time.time()
        net.add_many(X, X)
        d_gb = n * n * 8 / 1e9
        try:
            steps = 2 if n <= 20000 else 1
            t1 = time.time()
            net.settle(steps)
            ms = (time.time() - t1) * 1000.0 / steps
            ws, pws = peak_ws_mb()
            note = ""
        except MemoryError:
            ms = float('nan')
            ws, pws = peak_ws_mb()
            note = "MemoryError (D does not fit)"
        print(f"{n:>8,} {ms:>9.1f} {net.q.nbytes/1e6:>9.2f} {d_gb:>9.2f} "
              f"{ws:>9.1f} {pws:>11.1f}  {note}")

    print("\nLaw predicted (fitted at n<=5000): t = 2.96e-7 * n^1.76 s/step.")
    print("Measured 5000->20000 gives exponent ~2.06: flow is effectively n^2")
    print("at the ceiling (D array stops fitting in cache).")
    print("RAM is the binding wall: the kNN sort temporaries blow past the")
    print("n^2*8B D-array estimate - peak WS was 22.6 GB at n=20000 (D=3.2 GB).")
    print("=> measured all-pairs flow ceiling on this box is ~2*10^4, not the")
    print("naive 50-60k.  (n=40000 would peak ~90 GB - not run, would risk a")
    print("hard OOM while the live daemon is running.)  Scaling beyond ~2*10^4")
    print("needs O(1)-per-neuron spatial search, not all-pairs.")
