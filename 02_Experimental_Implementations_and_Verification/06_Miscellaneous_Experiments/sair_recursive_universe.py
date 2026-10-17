# SAIR Recursive Universe
def s_crit(p): return 3.0/p-1.0
def crit_smooth(a,p): return 3.0/p-a
def sim(a,r,A=1.0,N=200):
    seq=[A]
    for _ in range(N): seq.append(seq[-1]*r)
    return seq
def main():
    for a in (0,0.5,1,1.5):
        for p in (2,3,4):
            assert abs(crit_smooth(a,p)-(s_crit(p)+(1.0-a)))<1e-12
    for r in (0.5,1.0):
        seq=sim(1,r,2,80)
        assert max(seq)<=2.0*(1+1e-12)
    for r in (1.1,1.5):
        seq=sim(1,r,2,60)
        assert seq[-1]>seq[0]*(1+1e-9)
    print('PASS'); return 0
if __name__=='__main__': raise SystemExit(main())
