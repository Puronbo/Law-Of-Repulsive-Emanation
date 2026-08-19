"""
Regression suite pinning the solvable-theorem verdict artifacts (2026-08-08).

Each test loads a persisted verdict JSON from data/ and checks the headline
number so none of the resolved claims can silently drift:
  - continuum-limit drift converges to zero at first order
  - spectral C1/C3/C4 verdicts (100 modes, 120x120 grid)
  - Kawasaki 0.4866 reproduced and attributed to sampling scatter
  - PGT growth-form refutation at finite L
  - golden-ratio closure derived exactly (s(theta*)/s(TH) = 1/phi^2)
  - prime-time PAPER §8.4: uniform conservation; spectrum transient; recurrence unmeasurable
  - T-symmetry reversal error as a dt-dependent numerical bound
  - Bekenstein shift settled at n=100: significant raw, erased by index-matching
  - Wheeler-DeWitt constraint selects nothing (empty or C0-law relabeled)
  - fold-and-cut is not a unitary gate (non-injective, not norm-preserving)
  - Kawasaki is not a CTC/Novikov constraint (antecedent false)
  - C7 bridge extends to all primes trivially (no 2^n-k-special resonance)
   - Selberg paradigm not a concrete instance (Poisson, z(GOE)=-5.5/KS p=0.003; no zero overlap; no trace peaks vs matched null)
   - Riemann decimal perspective: 100 zeros (GUE, <r>=0.61) vs 100 disk modes (Poisson, <r>=0.37) on the unit interval - no shared spectrum (KS p=3e-7), zeros' decimals rigid ~9x, disk's random
   - Riemann-Siegel root engine: locates the first 100 zeros (max |t_RS - t_mpmath| < 1e-5, mean ~1e-7) by sign-change bisection on the real Z function (Gabcke remainder), WITHOUT zetazero; re-derives the decimal-perspective stats exactly (<r>=0.6108, residual 0.225, RvM max 0.9979); main-sum cutoff floor(sqrt(t/2pi)) = 6 terms at t_100 (6.3x condensation vs the t/2pi EM count) - not a test of RH
   - Riemann-Siegel certifier: rigorous interval-arithmetic + Turing certification that N(g_n) = 648 zeros <= g_n = 999.236 lie on Re(s)=1/2 and are simple - 654/654 brackets certified, signs OK at all 653 Gram points, zeta/Z containment PASS at 8 heights, theta (exact Stirling/Binet series, validated remainder bound) contained at all Gram points, max|S|=1, zetazero cross-check MATCH 648==648 - a finite verification, NOT a proof of RH
   - de Bruijn-Newman condensation: RH <=> Lambda <= 0 (Newman); the certified 648 zeros are the t=0 slice of the backward-heat flow H_t = int e^{tu^2} Phi(u) cos(zu) du; Phi even to 1.7e-51, H_0=(1/8)xi exact (rel 0 at z=10, 5e-48 at z=55); fast p-substitution evaluator tracks analytic xi to 4e-8 at z~223 and the independent v-substitution quadrature to 6e-7; measured merger law d(t)^2 = 4d^2 + 8t: P1 (gap 0.845) slope 7.377 (model 8), fit t_c -0.390 (model -0.357), merger confirmed between 0.90 and 1.05 of fit t_c; P2 (gap 1.219) fit t_c -0.942 (model -0.743); Polya direction holds (zeros persist and separate for t>0); certified global closest pair (gap 0.31043, idx 452) has local-model boundary t_c ~ -0.0482 at H_t ~ 1e-254, invisible to floats - a finite probe of the FINITE system, NOT a bound on Lambda, no proof of RH
   - merger-boundary creep t_c(N): the finite de Bruijn-Newman face is a stepping function of how many zeros are seen - a vectorized Riemann-Siegel scan re-locates 43851 consecutive zeros (t<36000, ~10s, count exact, zetazero match <=3e-6) and independently re-discovers the classical Lehmer pair (idx 6708, gap 0.0377 at gamma~7005) behind the Lambda >= -1.15e-11 bound; creep -0.0482 (N=648 certified) -> -7.11e-4 (N=10000, Lehmer) -> -6.23e-4 (N>=20000, record gap 0.03531 at gamma~17144); record-tight reduced gaps ~ N^(-1/3) (fit -0.36, GUE tail -1/3) bracketed by the Wigner expected-min null; direct H_t-eval face closes past gamma~1000 (e^{-pi gamma/4} ~ 1e-5847) while the zero-locations-only face is what the Lambda programme used - finite probe, located-not-certified beyond 648, NOT a bound on Lambda, no proof of RH
    - Connes footnote-14 Dirac reconstruction (the letter's claimed rank-one perturbation of the periodic Dirac operator with the Dirichlet kernel): reconstructed EXACTLY - fhat(z) = 4 z sin(zL/2) R(z) with R the rank-one secular function (verified to 5e-12), so the zeros are exactly {2 pi m/L : |m| > N} union {roots of R}, each root interlaced in its own pole gap; interlacing pins the FIRST eigenvalue into (0, 2.45] while gamma_1 = 14.1347 is 5.77 spacings up, so the claimed 2.6e-55 first-zero match is categorically impossible; the lattice part is exact at N=50 (m>N: 11 zeros at 2 pi m/L, |fhat| < 5e-15); the remaining roots miss the ordinates (median 0.82, 13/50 within 0.5); C_0 = V(q0) = H(q0,0) plays no role (scalar of an unrelated system, no trace formula); HONEST WALL: reproducing the structure is not the numbers, and neither direction speaks to RH
    - four-point coordinate lattice of 10262000 -> {10262000, 20001026, 20002610, 26102000}: exact finite arithmetic - gcd = 2 (the four span 2Z, Bezout 2 = -2238620*10262000 + 1148577*20001026); block structure 1026|2000, 2000|1026, 2000|2610, 2610|2000 closing the 4-cycle with step 1584 = 2^4*3^2*11; the full orbit of the digit multiset {0,0,0,0,1,2,2,6} is 840 points in three leading-digit clusters (1:210, 2:420, 6:210), none divisible by 3 (digit sum 11), 39 primes, anchors at ranks 470/532/543/729; the permutohedron has diameter 16, an EMPTY shell at distance 14, and (by S_8 transitivity) identical shells from every anchor; HONEST WALL: finite arithmetic, chance-level 2 pi/L proximity, no mechanism to zeta or RH
    - zeta-lattice alignment with an origin (the rigorous form of 'align the lattice with RH'): the ONLY honest spectral test is index-matched |gamma_k - (o + k s)| and the best FIXED lattice scores median error 10.5, 1/50 within 0.5, 0 within 0.05 (nearest-point metrics are trivially small at fine spacing and were rejected); the real 'origin' is adaptive - Weyl law residuals (mean 0.50, max 0.88) and Gram points (1/49 violations, offsets median 0.86, max 9.04 at gamma_1); the four anchors as origins on the 2 pi/L lattice sit inside the random-origin spread (uniform median 0.612, random 0.618, anchors 0.375..0.681; only 2/200 random origins beat the best anchor - selection noise, the expected number); any anchor rescaled to 61 points in [0,150] collapses to spacing 2.459 whatever its digits; PROVABLE negative theorem: interlacing pins the first rank-one eigenvalue to (0, 2.45], unreachable by gamma_1; HONEST WALL: RH is open, the provable content is negative classification, a positive proof needs mathematics outside this repository
    - zeta direct probe (the headline number tested head-on): at N=150 the letter's fhat is evaluated AT the ordinates at mpmath dps 60 - |fhat(gamma_1)| = 2.65e-3 while a true zero gives exactly 0 (claim 2.6e-55), the nearest zero to gamma_1 is 1.02 away (median 0.73 over n=1..50), |gamma_1 - r_1| = 13.09, and the closest any ordinate comes to a zero is |fhat| = 2.95e-5 at gamma_6 = 37.586 (the tight-match known from the matching stats); the identity fhat = 4 z sin(zL/2) R(z) holds on all 50 ordinates to the double-precision coefficient floor (5.4e-12); the interlacing theorem is verified at EVERY N in {50,100,150,200,300} - one root per pole gap, r_1 in (0, 2.45] (1.017..1.064 as N grows), gamma_1 = 5.77 w_1 for every N, min gap margin >= 5e-3, and N=100 cross-checks the persisted connes_dirac verdict to 8e-15; the WHOLE 840-point orbit is tested as origins - the best has q = 0.3734, exactly the expected extreme-value minimum of 840 random origins (min_mean 0.3734; random matches or beats it in 100% of trials), so no known point is a special origin; HONEST WALL: direct numbers confirm the impossibility, RH is open, negative classification only
    - zeta interlacing CERTIFIER (interval arithmetic): every pole gap of the letter's rank-one secular function R is certified to contain a root by validated-rounding IVT at both ends (N=100: 100/100 gaps, endpoint magnitudes >= 1.8e+0; N=150: 150/150; N=200: 200/200; N=246: 246/246) and the residues rho_k = c_k (-1)^k share one sign there, so R' = -2z sum rho_k/(z^2 - w_k^2)^2 is strictly one-signed on every gap and each IVT root is UNIQUE - exactly one root per pole gap for EVERY N <= 246 (numeric scan confirms 1 per gap); FINDING: the interlacing is NOT a theorem in N - the residues first fail to share a sign at N = 247 (flip between k = 246/247) and gap 246 then holds ZERO roots; at larger N the flips multiply, e.g. N=300 (flips between k = 153/154, 266/267, 267/268) where gap 153 keeps TWO roots hugging the poles (distances 3e-4/2e-4; its residues are tiny, ~4e-7), gaps 266 and 267 hold NONE, and every one of the other 297 gaps holds exactly one (histogram {0:2, 1:297, 2:1}, total 299) - the rule fails exactly where adjacent residues have opposite signs; the WALL still certifies at every N (first root enclosed to 2e-24 inside (0, 2.4496], gamma_1 = 14.1347 is 5.77 w_1's away, R and sin(gamma_1 L/2) certified nonzero at gamma_1) - the claimed 2.6e-55 first-zero match is certified impossible; an independent mp Newton iterate (dps 60, x0=1.5) lands inside the certified enclosure; float root-finders fail there because |R| ~ 1e-19 is below the float64 cancellation floor; HONEST WALL: negative certification of the letter's construction, RH remains open, no de Bruijn-Newman consequence, C_0 = V(q0) = H(q0,0) does not enter
    - riemann_siegel ordinate (gamma_1 re-derived): WHERE the number 14.1347251417... comes from, series-machinery ONLY (no zetazero, no mp.zeta, no mp.loggamma) - theta(t) by the Stirling/Binet series (validated factor-25 remainder bound) and zeta(1/2+it) by Euler-Maclaurin (Backlund remainder bound), both dps 60, Z = cos(theta)Re zeta - sin(theta)Im zeta; Z(0) = zeta(1/2) = -1.4603 < 0 < Z(g_0) = +2.3401 at the first Gram point g_0 = 17.8456 (theta = 0), and the RvM count N(g_0) = 1 (gamma_1 < g_0 < gamma_2) fixes that there is exactly one zero in (0, g_0]; the series scan over [13, g_0] (Stirling asymptotic only for t >= ~13) finds its single sign change, and bisection recovers gamma_1 with |diff| = 2.2e-39 vs zetazero; the certified-interval engine (validated regime, half-width 1e-8) encloses it with Z signs -1/+1; RvM: theta(gamma_1)/pi = -0.550253, S(gamma_1) = +0.550253 (S just below = -0.449747, the +1 jump at the simple zero), S(g_0) = 0; HONEST WALL: one ordinate derived to ~18 digits is a closed derivation of a number, NOT a statement about RH (open; rigorous verification to |t| <= 3e12, Platt-Trudgian)
    - s-function census (Littlewood's RH <==> S(t) = o(log t)): over the certified range 0 < t <= g_652 = 1005.43 (N(g_647) = 648 Turing-certified, extended by five Rosser blocks to N(g_652) = 653, every located bracket certified one on-line simple zero) the certified bound max|S(g_j)| = 1 holds at all 653 Gram points; an independent three-grid re-location reproduces the anchors exactly (654 located counts at grids 0.05/0.01/0.005; N(g_647) = 648, N(g_652) = 653) and exposes the classical Gram-violation pattern - S(g_j) takes values in {-1, 0, +1} (histogram {0:631, -1:13, +1:9}, nonzero at 22 points), with 609 Gram intervals holding exactly one zero, 22 holding a PAIR and 22 holding NONE; interior |S(t)| < 2 throughout (observed sup +1.133 / inf -1.110 on [14.5, 1005.43]; S(0+) -> -1); at the certified top the observed max|S|/log T = 0.164 sits below the minimum conceivable RH envelope sqrt(log T/log log T) = 1.891 (always >= sqrt(e) = 1.6487 since log t/log log t >= e) and far below the unconditional bound log T = 6.913; RESOLUTION LIMIT: the RH envelope reaches value k only at sqrt(log t/log log t) = k, i.e. log10 t = 3.74 / 13.41 / 29.26 for k = 2/3/4 with N ~ 1e4 / 1e14 / 1e30 - the k = 3 height needs ~1e14 certified zeros, ~2e11 x this repo's 648 and ~10 x the ENTIRE rigorous frontier (3e12, Platt-Trudgian, N ~ 1.3e13), k = 4 needs ~1e30, and no finite k-test can COMPLETE the o(log t) test; HONEST WALL: numerical search is a counterexample engine - it can find a disproof (an off-line zero, or S growing like c log t) but cannot prove RH, because every finite quiet census is compatible with a violation just beyond the frontier
    - mertens-psi census (Littlewood/von Koch prime-side equivalences): exact segmented sieve to x = 10^8 computes M(x), psi(x), pi(x) (mu verified against sympy mobius for n <= 10^6, zero mismatches; the classical Mertens table M(10^k) = -1, 1, 2, -23, -48, 212, 1037, 1928 reproduced exactly, OEIS A084237) - over x in [1000, 1e8] the Mertens-like ratio |M(x)|/sqrt(x) maxes at 0.4722 at x = 2803 and NEVER reaches 0.5 (only tiny x < 1000, e.g. x = 13, exceed it), max |psi(x)-x|/sqrt(x) = 0.7770 at x = 1422, RH-normalized max |psi(x)-x|/(sqrt(x) log^2 x) = 0.0147 at x = 1422, and pi(10^k) - Li(10^k) < 0 for every k = 1..8 (pi lags Li at every computable height); the EXPLICIT FORMULA psi_0(x) = x - sum_rho x^rho/rho - log(2 pi) - (1/2) log(1 - x^-2) evaluated with the repo's OWN located zeros (653/4520/10142/22491 for T = 1005.43/5k/10k/20k; 653 matches the certified N(g_652)) reproduces the sieve's exact psi(x) with residuals that shrink as T grows (at x = 100, -0.169 for T = 1005.43 vs -0.006 for T = 20000) - the zeros really DO count the primes; THE TWO PROVEN-BUT-NEVER-SEEN FAILURES: (a) the Mertens conjecture M(x) < sqrt(x) is PROVEN false (Odlyzko-te Riele 1985; Pintz: counterexample < exp(1.59e40)) yet no explicit x is known and |M(x)| < sqrt(x) holds for every x <= 1e16 computed, (b) pi(x) > Li(x) is PROVEN to occur (Skewes 1933/1955; first crossing < ~1.4e316 under RH, Bays-Hudson 2000) though pi(x) < Li(x) at every computable height - both finite-failure theorems whose empirical evidence points the WRONG way; RESOLUTION LIMIT: RH needs the supremum over ALL x (M(x) = O(x^(1/2+eps)), psi(x) = x + O(x^(1/2) log^2 x)) and the best unconditional state is Korobov-Vinogradov psi(x) = x + O(x exp(-c (log x)^(3/5)/(log log x)^(1/5))) - an exponential-in-log-distance gap from the RH exponent; HONEST WALL: the arithmetic side confirms the S-side conclusion - numerical search is a counterexample engine, RH remains open, the proof (if it exists) is not a computation
    - mertens sublinear census (the Mertens function at height): exact segmented mu-sieve to x = 1e10 (small-prime flips/zeroing + a vectorized large-cofactor step, n = m q with m squarefree <= sqrt(x), q prime > sqrt(x)) reproduces M(10^k) = -1, 1, 2, -23, -48, 212, 1037, 1928, -222, -33722 for k = 1..10 (OEIS A084237) and M(1e10) = -33722 - and finds the FIRST |M(x)|/sqrt(x) > 0.5 excursion at height, x = 7725038629 (M = 43947), record 0.5706 at x = 7766842813 (M = 50286), the first re-crossing since the trivial x = 13; the O(N^(2/3)) quotient-set recursion M(n) = 1 - sum M(floor(n/d)) (memoized over {floor(N/i)}, base = exact 1e9 prefix, self-checked by re-deriving M(10^5) = -48 and M(10^6) = 212) extends the census to M(10^11) = -87856, M(10^12) = 62366, M(10^13) = 599582, M(10^14) = -875575 - every value matching OEIS exactly, completing the published M(10^n) table n = 1..14; a free quotient-point scan of the recursion memo (11106 EXACT values x = floor(N/i) > 1e10, sampled not a census) finds two further 0.5 crossings at height, max 0.5132 at x = 108813928182 (M = 169281), still below the 7.7e9 exact record; THE PROVEN-BUT-NEVER-SEEN FAILURE: the Mertens conjecture is PROVEN false (Odlyzko-te Riele 1985; Pintz: counterexample < exp(1.59e40)) yet the first excursion appears at 7.7e9 while |M(x)| < sqrt(x) holds at every computed x <= 1e16; RESOLUTION LIMIT: RH needs the supremum over ALL x (M(x) = O(x^(1/2+eps)), Littlewood 1912) - a global statement no finite census decides; HONEST WALL: extending to 1e14 (or any finite height) is a counterexample search, not a proof, RH remains open, the proof (if it exists) is not a computation
    - mertens explicit formula at height (do the located zeros count the primes at 1e14?): the explicit formula M_0(x) = -2 + sum_{gamma<=T} 2 Re[x^(1/2+i gamma)/(rho zeta'(rho))] + trivial terms (constants pinned against the classical table M(100) = 1, M(1000) = 2), evaluated with the repo's OWN Riemann-Siegel located zeros in ONE pass to t = 20000 (22491 zeros, sliced per truncation; 653/4520/10142/22491 for T = 1005.43/5k/10k/20k) and mpmath zeta'(rho) at every zero, recovers ~98% of the exact M(x) from the sublinear census at every height: at x = 1e11 the T = 20000 value -86867 is off by +989 (1.13%), at x = 1e14 it is -860152 vs the exact -875575 (residual +15423, 1.76%), and at x = 100/1000 the truncation is essentially exact (3e-4 / 1.6e-3) - the same formula that nails psi at 1e8 carries ~98% of M at 1e14; THE REAL FACE OF THE HEIGHT: the Mertens explicit formula is only CONDITIONALLY convergent (pairing conjugate zeros) and the residuals are NON-monotone in T - at x = 1e12 the T = 20000 residual +1850 is WORSE than T = 10000's -61, and at x = 1e14 T = 5000 is worse than T = 1005.43 - so a hard cutoff at T does not guarantee a better value; the empirical tail bound E_T(x) = sum_{T<gamma<=20000} 2 sqrt(x)/(|rho||zeta'(rho)|) grossly overestimates the observed residual (at x = 1e12, E = 1.5e6 vs a residual ~1e3, a measured 1000x gap) because the terms cancel - the worst-case bound is not a predictor; RESOLUTION LIMIT: the identity holds only in the T -> infinity limit with the correct smooth/paired summation, no finite T certifies M(1e16) or beyond, and the tail past t = 20000 is not located; HONEST WALL: 22491 zeros carry ~98% of M(1e14) and the price of height is the residual's non-monotone walk - 'the zeros reproduce M' is a percent-level approximation with an unquantifiable conditional-convergence tail, not a proof of RH (open)
    - chebyshev psi explicit formula at height (the prime-side twin of the Mertens-at-height measurement): psi_0(x) = x - sum_{gamma<=T} 2 Re[x^(1/2+i gamma)/(1/2+i gamma)] - log(2 pi) - (1/2) log(1 - x^-2) evaluated with the repo's OWN Riemann-Siegel located zeros (22491 to t = 20000, sliced 653/4520/10142/22491) against EXACT psi(x) from a new quotient-set identity psi(x) = sum_{k<=V} log k * M(floor(x/k)) + sum_{w<=W} mu(w) * L(floor(x/w)) - M(W)*L(V) (V = isqrt(x), W = x//(V+1), L(n) = log(n!); M exact at every quotient point from the segmented 1e9 sieve + memoized quotient-set recursion, OEIS-verified; validated at psi(100) = 94.0453, psi(1000) = 996.6809, psi(1e6) = 999586.5975, psi(1e8) = 99998242.7966; mpmath loggamma for w < 2000, scipy gammaln vectorized for the rest, total rounding ~0.1 absolute): the exact psi(1e11..1e14) values are 100000058456.4 / 1000000040136.8 / 10000000171998.7 / 100000000618672.4 (psi(x) - x = +58456 / +40137 / +171999 / +618672, small fractions of sqrt(x) as RH would demand); at T = 20000 the formula residuals are -3645 / -19476 / +28854 / -88932 - at EVERY height LARGER than the Mertens formula's at the same truncation (+989 / +1850 / -13563 / +15423, factors ~3.7 / 10.5 / 2.1 / 5.8), exactly as the conditional-vs-absolute convergence theory predicts: psi's terms ~ sqrt(x)/gamma with sum 1/gamma divergent so NO tail bound exists (the located-tail magnitude sum_{T<gamma<=20000} 2 sqrt(x)/gamma = 6.3e7 at x = 1e14 is ~700x the observed residual - the tail cancels, it is context, NOT a bound, and it has no finite total as the horizon grows) while M's paired series is absolutely convergent (Titchmarsh); BOTH walks are NON-monotone in T (at x = 1e14 psi's best is T = 10000's -80364 vs T = 20000's -88932; M's T = 5000 is 30x worse than its T = 1005.43) - hard cutoffs are not ordered for either function; RESOLUTION LIMIT: no finite T certifies psi(1e16), the census truth stops at 1e14, the tail beyond t = 20000 is not located, and psi's truncation error is an unquantifiable oscillation with no tail bound at all; HONEST WALL: the located zeros influence the primes at 1e14 and the identity holds only as T -> infinity - a measured approximation (worse than M's, as the conditional convergence demands), NOT a proof of RH (open)
    - body fold symmetry (turning and folding the divisor hyperbola): the fold
      of the cartesian lattice {(a,b): a*b <= x} at the diagonal sqrt(x) is
      EXACT (D = U + L, L = U - d^2, commutativity) verified to x = 1e14; the
      breaking Delta(x) = D - (x log x + (2g-1)x) certifiably satisfies the
      proven Voronoi O(x^(1/3) log x) bound (ratio <= 0.006 at 1e14) but the
      conjectured x^(1/4) (half the critical 1/2 - the fold of the exponent) is
      not certified at any finite height (local exponent wanders -0.15..+0.81);
      the three convolution folds connect the field (1*1 = tau, 1*mu = delta
      with sum mu(d) floor(x/d) = 1 exact, mu*log = Lambda); tree growth: a
      regular tree (Calkin-Wilf) mirror is a tautology of regularity while the
      integer divisibility tree's depth-reversal mirror FAILS (median subtree
      ratios 2.0/2.0/2.0/1.0/0.5) and branch growth is linear tau(2^k) = k+1,
      not golden (tau(2^19)/phi^19 = 2.1e-3); HONEST WALL: arithmetic facts
      only; the body mapping is not committed; the divisor 1/4 is as open as
      RH (data/body_fold_symmetry_data.json)
    - zeta zero spectral match (which spectra resemble the zeros, and the time
      reading): the 22,491 located zeros (t <= 20000) are GUE-like - NNSD KS
      0.037 to the Wigner surmise vs 0.286 to Poisson, level repulsion beta
      1.64 (GUE 2 / GOE 1 / Poisson 0), number variance Sigma^2(L) 0.27-0.43
      tracking a simulated GUE ensemble and far below Poisson; the zeros are a
      determinantal process in log-time u = log x (the explicit formula is a
      Fourier sum in u with frequencies gamma; normalized gaps have lag-1
      autocorrelation -0.364 vs GUE -0.323 vs Poisson ~0); the S-walk
      max|S|/log t = 0.146 matches the persisted S-census (0.164); the repo's
      OWN spectra do NOT resemble the zeros (spectral_extended is Poisson,
      KS 0.074 to Poisson vs 0.354 to GUE; spectral_data sat ~10 units away);
      HONEST WALL: GUE resemblance is the conjectured Montgomery-Odlyzko law
      supported numerically, not a proof of RH, which remains open
      (data/zeta_zero_spectral_match_data.json)
    - C2 golden fold: retrace chain is not a phi/phi^2 ladder (1/4 rungs)
    - hierarchical C0 flow: SUPPORTED (NC parity with flat flow, router gain, 6 not 30 comps)
   - flow-guided active learning: margin-AL reaches targets with fewer labels than random; raw force-cancellation score is not the winner
   - balance survey: 50/50 is best shock absorber but NOT the layout optimum (PARTIAL)
   - balance scale (T54): scaling is a real confound (A* ~ n^1.086) but NOT the problem; dimension-independent shell
   - balance continual (T50): adaptive mu=0.5→0 schedule wins both axes; fixed balanced P5 is harmful
   - polysphere extensions: learned truths do not reproduce routing; S^2 repulsion does not preserve clustering (NOT SUPPORTED)
   - flow incremental: reflow buys separation (min_d) but not routing; random-add matches or beats (MIXED)
   - flow hier-incremental: hierarchical + incremental growth preserves old-class routing (no forgetting); hier beats flat (SUPPORTED)
   - polysphere use cases: classifier/anomaly/generator/continual claims hold at batch level; per-point weak; separation not bit-reproducible
   - polysphere routing: batch routing exact (identity confusion, chance 0.167); silhouette 0.943; per-point weak
   - golden survey: phi EXACT in cusp metric; golden rotation maxes min gap; static C0 packing has no golden structure; gap-filling does not lock to golden angle
   - fib stream (T52): Fibonacci-sized continual stream is steady; AD_phi (absorb on large terms) beats P0 on both axes in all 3 seeds; golden insertion washes out; no golden scaling signature
   - hamiltonian routing: C0 flow separates centroids (routing 0.420->0.765, nc reaches oracle 0.909); min pair dist barely moves; flow is not the ceiling
   - metric comparison: Poincare vs cusp geodesic from a 'stable' start blows up numerically in BOTH (Poincare NaN, cusp ~2e13; C0 broken, T-sym fails) - REFUTED at these settings
   - c0 crossing tsym: T-sym holds (err 0.066-0.226) but NO trajectory actually crossed the origin (closest approach = start dist) - PASS-with-caveat, crossing regime never exercised
   - c0 cusp flow: cusp-metric C0 geodesic at dt=0.005/5000 steps blows up (Poincare NaN, cusp escapes to ~2.7e23, drift 2.68e45, T-sym err 2.8e9) - REFUTED/unverifiable at settings
   - t39 cusp flow: cusp isometry w=log(q) verified EXACTLY (energy CV 3e-15, step ratio=phi exactly, w-plane R2=1.0 slope pi/(2 log phi), T-sym err 0) - SUPPORTED (deterministic)
   - van iterson T48a: NO golden-angle locking in ANY rule (discrete bisection, min-potential, min-dist, center+push-out; divergence 170-200 deg, r~n^0.4-0.5) - SUPPORTED negative, locking is an insertion-constraint special value
   - reverse pair gaps T57: NOT a reversal pair (reverse(10262)=26201 != 26102); 80-multiple + 11-sums hold but are plain arithmetic - REFUTED headline, census is ordinary
   - fibonacci spiral on disk: neither projection turns at golden angle (42.14 / 29.23 deg vs 137.51) and pseudo-energy not conserved (drift 1.00 / 11.81) - REFUTED, golden angle is a cusp-metric property
   - prime count from scratch T62: Lucy_Hedgehog pi exact at all chain points (pi(943901200001)=35575526191), endpoint prime, next gap 8 - SUPPORTED with corrections: 'gap 1 below' is wrong (measured 24), window max gap 176 exceeds own 40-100 note
   - fibonacci squares on disk: 90-deg turning is a square-construction artifact; pseudo-energy NOT conserved (drift 0.96, decay -0.357/step), escapes disk (r 1.117), T-sym fails (0.99 vs C0 6e-09) - REFUTED frictionless claim
   - rotation test T61: rotation preserves neighbor structure EXACTLY (overlap 1.0, sim corr 1.0, coords change 0.745); abs() drops overlap 1.0->0.426 but that is 6.5x chance, so 'collapse toward chance' overstated - SUPPORTED J1/J2 with J3 correction
   - clock test T59: calendar features nail the law at e0 (1.0000) but break at e0+15 (0.4167, BELOW chance -> anti-correlation), intrinsic mod-2/3/5/7 features survive both (1.0000) - SUPPORTED, convention carries then breaks
   - spring fold T58: mirror-fold area = 2*a^2*TH^3/6 EXACT, self-crosses at TH-pi; retrace fold closes EXACTLY to C0 (closure 0.00e+00, crease pi); golden fold ratio = phi EXACT but does NOT close to C0 (error 12.3); overcoil tucks end under start - SUPPORTED (by construction, deterministic)
   - eikonal fold T63: upwind viscosity solution of |r'|=a with C0 at both ends converges to the exact tent (err 3.3e-13); cut locus EXACT (0.00e+00); crease 0.0350*pi vs analytic 0.0318*pi (finite-diff approx); mirror area 2*a^2*TH^3/6 EXACT, retrace net area ~0 - SUPPORTED (deterministic; fold-as-integral semantics interpretive)
   - retrace boundary T64: equation + two pins admits infinitely many weak solutions (zig-zags all pass |r'|=a, r(0)=r(2TH)=0); viscosity selects the tent (all zig-zags fail at down-up corner); upwind from zig-zag converges to tent (err 5e-13); cut locus EXACT; reflection conserves |r'| to 3.6e-13 - SUPPORTED, retrace derived not assumed
   - fold optimizer T60: Hamiltonian spring conserves (drift 3.9e-3 bounded, area ratio 0.9921) and recurs to start (Poincare, min dist 3.3e-5); damped spring collapses (energy 0.00e+00 above min, area ratio ~0) and locks at x=+1 EXACT (stays 2000 steps) - SUPPORTED; 'cannot escape' is topological (shown by staying, not proved), mirror-fold=dissipation interpretive
   - t65 four-pack: P1 REFUTED (tau=1.4272 identical across all curiosity_drive, corr nan - knob has no effect); P2 REFUTED (ascent err 1.79-1.82, does not recover seed); P3 PARTIAL (2D proj MI 0.034 vs null 0.009 retains signal, but single coord already = 1.0, holography trivial); P4 REFUTED (converged fraction 0.00, max dist from final 0.45) - MIXED, mostly REFUTED
   - phi scheduler T53: FIB batching most robust on disk layouts (stream-old 0.912 best, final-old 0.910 at ~2.25 buffer); FIB+ABS buys final_all (+0.013) at old-routing cost (-0.063); P5 fixed mu=0.5 never usable (0.872); on MNIST scheduling NOT needed (NAIVE 0.953 > FIB 0.907 > FIB+ABS 0.887) - SUPPORTED with scope caveat (geometry-regime tool)
   - flow_regularized: flow regularizer at lambda=0.007 lifts routing 0.900->0.930 (+0.030) with test_acc 0.905 and sep 1.59x preserved, but the sweep is NON-MONOTONIC (0.003:+0.01, 0.005:-0.02, 0.007:+0.03, 0.01:-0.07, 0.015:+0.00) - SUPPORTED with narrow-window caveat, larger lambda clearly hurts routing
   - flow_hier_reg T48b: flow-REG does NOT stabilize - drift 6.616 (rel 0.686) vs baseline 6.549 (rel 0.647), forgetting -0.034 vs -0.029; flat routing worse (all 0.805 vs 0.885, old 0.873 vs 0.973); only hier routing better (all 0.790 vs 0.765, old 0.800 vs 0.760) - NOT SUPPORTED for stability headline, weak hier benefit only
   - flow_hier_reg_scaled T55b: n-scaling stage-2 reg per T54 A* law does NOT help materially - drift 6.5048 (rel 0.644) FIXED vs NSCAL 6.4636 (rel 0.640) and LIN 6.4573 (rel 0.640), a <=0.7% relative drift gain; ALL other metrics identical to 3 dp (acc 0.897/0.921, forget -0.031, route 0.895/0.933, hier 0.755/0.747); LIN nominally lowest - NOT SUPPORTED for a material effect
   - balance_auto T51: autonomous burst-detector regime switch does NOT deliver the claimed benefit - detector fires only on the explosive event, but AD ~= P0 on routing (MNIST old 0.990 vs 1.000, all 0.975 vs 0.985; synthetic burst 0.887 vs 0.873 old) and AD displacement slightly higher (1.816 vs 1.828); P5 constant-mu=0.5 decisively worse; on real MNIST embeddings reflow policy is nearly irrelevant (all >= 0.94, P0 best) - NOT SUPPORTED for the autonomous benefit (T50 absorb = one-shot recovery tool for a clean shell, not a stream policy)
   - self_balancing T55a: self-balancing router (fib batching + n-scaled absorb A=A*(n) + coherence gate) SUPPORTED in the geometry regime - the gate FIRES in a trapped crowded core: COH skips the absorb and lands exactly on P0 (old 0.900 ~ 0.900, all 0.860 = 0.860, disp 0.513 ~ 0.513) while ABS/ABS-SC pay the penalty (old 0.890, all 0.820-0.830); on the clean fib stream the all-routing gain survives (COH final_all 0.850 vs P0 0.770; multi-seed banner 0.880 vs 0.820) but seed-42 COH final_old 0.810 < ABS-SC 0.930 (banner tie 0.870/0.870 holds on average only); Part 4 MNIST adds NOTHING (COH final_all 0.873 < FIB 0.940); coherence is a shell-thickness signal, not a general crowding detector
   - polysphere_mnist: PolysphereRouter generalizes to REAL MNIST embeddings - mixed-batch routing 0.890 vs chance 0.100; anomaly gap 0.663 (in-dist 0.877 vs OOD 0.214); hierarchical end-to-end 0.753 vs combined chance ~0.111 (branching 10 -> 4); active learning flags unknowns 60% and routes 10/10 = 1.000 after faces added - SUPPORTED (embeddings are the MLP's own 2D bottleneck, single seed, hier below flat 0.890, threshold-dependent)
   - polysphere_nnflow_viz: three-extension probe - (1) learnable NN truths SUPPORTED: routing 0.880 (176/200) vs chance 0.100 on MLP embeddings (test_acc 0.885); (2) S^2 Hamiltonian flow NOT SUPPORTED: silhouette ~0.0 (intra ~= inter, no separation), only 3-4/6 faces self-route at low conf 0.24-0.56, repulsion destroys centroid structure (run-to-run variance: sil -0.016..0.022, 3-4 self-routed, part 2 draw not fully rng-seeded - verdict robust); (3) viz routing distribution tracks true per-class fractions within ~1-3 pts - PARTIAL
   - decentral_net T55c: fully local net (private home trap + k-NN repulsion + per-neuron steps, NO global mean/max/controller) SUPPORTED - decentralization ~free or better on old-routing (banner multi-seed: ABS-SC final_old 0.913 vs centralized 0.870; final_all 0.843 vs 0.853); shell EMERGES from local rules but needs the always-on home tether (without it collapses to rim 0.57 all-route -> 0.85 at mu0=0.12); self-heals with no repair unit (50% loss: spacing spread 0.16->0.11, regrown routing >= pre-damage 0.917 vs 0.877); MNIST part4 no collapse, ABS-SC final-all 0.813 > FIB 0.647; caveats: spacing gate never fired on clean stream (GATE ~ ABS-SC), k=4 worse than k=8, part4 single-seed
   - decentral_net_mnist T55d: no-dependency DecentralNet on real 64D MNIST embeddings SUPPORTED - local-settle routes at 0.810 vs nearest-centroid baseline 0.817 (within ~1 pt, no central controller); after killing 3/10 neurons survivors keep routing (0.834) and LOCAL heal alone restores spacing 0.562 -> 0.854 with routing preserved (0.822); regrow from fresh homes restores full 10-class net at 0.767 (~5 pts below grown 0.810); caveats: embeddings are the MLP's own 64D layer, single seed 42/4 epochs/disk radius 0.35
   - decentral_net_continual T55e: class-incremental LOCAL reflow on real 64D MNIST NOT SUPPORTED for the routing benefit - ADD old 0.805 vs raw-centroid CONTROL 0.863 (delta -0.057), all 0.647 vs 0.671 (homes ARE the data centroids, reflow cannot help); MIX (no reflow) collapses as the gauge freedom predicts - old 0.061/all 0.305, never mix frames; Part 2 tether NOT dimension-independent - mu0=0.12 2D-tuned over-drifts in 64D (0.49), mu0>=1 cuts drift to 0.11-0.21 but never beats CONTROL (best all 0.812 vs 0.817)
   - decentral_net_ceiling T55h: all-pairs kNN flow ceiling measured ~2*10^4 on this 31.7 GB box (dim=2, k=8) SUPPORTED - ms/step n^1.76 up to 5000 then exponent ~2.06 (D leaves cache); 66/1230/25422 ms/step at n=1k/5k/20k; peak WS 22.6 GB at n=20k vs D=3.2 GB (kNN sort temporaries blow past the estimate); n=40k would peak ~90 GB, not run - scaling beyond ~2*10^4 needs O(1) spatial search (T67)
   - decentral_net_t67: O(1)-per-neuron spatial search (uniform grid <=3D, scipy cKDTree >=4D) SUPPORTED - indexed flow BIT-IDENTICAL to exact all-pairs (grid 2D n=2000, tree 64D n=500) with spacing/predict equal and grid kNN == brute force on 3 seeds x 1D/2D/3D; 2D scaling exponent 1.11 (indexed) vs 1.92 (exact) - flow is now ~linear, and n=100k flows at 10.35 s/step where the all-pairs D would need 160 GB (10k real top-1M domains x 128D at 4.12 s/step, 102 GB) - the n^2 wall is gone for low-dim flow
   - decentral_net_live: the T55f live daemon's structural claims pinned by a bounded run - V1 population never exceeds CAP (30) through arrivals + damage + pruning (bounded O(CAP^2) cost); V2 after each random neuron death the local k-NN re-spread heals the survivors back into the healthy spacing band with NO repair unit (post-damage spacing within 0.5-2.0x of pre - removing a neuron legitimately enlarges mean k-NN distance, no clump, no rim blow-up; recovery ratio ~1.4); V3 the self-consistent routing probe stays 1.00 accurate through 3000-tick churn; V4 a checkpoint saved at tick 1500 and reloaded reproduces the uninterrupted trajectory bit-for-bit (positions identical, counters born/pruned/killed match, RNG stream carries on - the cycle is continuous with no damage) - all SUPPORTED on seeds 42/11/7, numpy-only DecentralNet, bounded ring memory, all as MECHANISM claims about the daemon design
    - bazaar_hybrid: the best-possible 4chan+reddit design (anonymity+bump-order honesty x reddit memory+curation, minus both status economies and central algorithms) verified as 6 structural claims on the repo's OWN machinery - C1 reason-tagged downvotes raise the brigade size to hide a good post 2.5x (reddit S50=8 free downvotes vs hybrid S50=20 pending-quorum-review; even then only HIDDEN, removal needs the quorum); C2 karma-free + tag-to-remove drops top-K spam frac 0.75->0.00 (reddit bot collusion saturates); C3 emergent DecentralNet mesh feed routes minority users 1.00 of their own community vs 0.30 on the global hot feed (overlap 1.0 -> local explicit clustering); C4 content-addressed ledger archive survives 50% node loss with retrieval 1.00 and tamper-evidence (verify() fails at seq 3); C5 9-guardian quorum collapses wrong-removal 0.20 -> 0.0031 at corruption p=0.20; C6 verified-vote-only membership (anonymity for cheap votes, EARNED mesh standing for the removal path) raises the brigade to suspend a good post 32x (S50 20 -> 640, sockpuppet standing 0.05 contributes ~nothing) and collapses quorum wrong-removal to 1e-08 (corrupt identity must ALSO hold guardian standing, 10% of population - a sockpuppet factory cannot mint guardians) at the honest cost of a removal-vote privacy leak - all SUPPORTED as MECHANISM claims (agent-based, no real users)
    - learn_creativity_test (T74): a test ascertaining LEARNED and CREATIVITY in a learning environment, one rubric (recognition/transfer for learned; novelty x appropriateness for creativity) re-used by a human protocol - L1 held-out probe accuracy climbs from near-chance 0.125 to >=0.90 as exemplar exposure grows 1..40/concept (a sparse stored-memory k-NN neighborhood is dominated by other concepts, a full one by the true concept); L2 first-taught concepts keep >=0.92 after every later concept is added (no forgetting under additive memory); C1 a measurable share of mid-size near-miss variations are simultaneously NOVEL and VALID (>=24% yield of never-presented new-but-right items); C2 random far nulls are ~100% novel but 0% creative (novelty alone is not creativity); C3 creative yield is interior-peaked over mutation size (too-close valid-but-not-novel, too-far novel-but-not-valid) - all SUPPORTED on seeds 42/11/7 as MECHANISM claims (stored-memory k-NN router over gaussian exemplars in a synthetic concept space)
    - learn_curve_scale (T75): the T74 acquisition curve is a density effect, not an artifact of its single operating point - S1 the sparse floor is chance: at one exemplar/concept held-out accuracy tracks 1/C and strictly decreases with curriculum size (0.50 -> 0.25 -> 0.125 -> ~0.07 for C = 2,4,8,16; a bigger curriculum is a denser confusion field); S2 the acquisition curve exists at every scale: the full-exposure ceiling holds >=0.90 for every C in {2,4,8}, so the dynamic range (ceiling - floor) grows with C (0.50 at C=2 -> 0.82 at C=8); S3 capacity saturation: beyond the well-separated regime the ceiling collapses once adjacent home separation reaches a few exemplar-sigma (0.94 at C=8 -> 0.61 -> 0.42 -> 0.30 at C=16,24,32), locating a real memory capacity C* ~= pi*HOME_R/(2*SIGMA) ~= 8 - all SUPPORTED on seeds 42/11/7 as MECHANISM claims, and the collapse tracks separation/sigma, not a magic C (SIGMA=0.03 holds 0.89 at C=16; SIGMA=0.10 collapses to 0.59 already at C=8)
    - human_trial_pilot: the T74 human protocol made concrete and validated - a trial package (teaching set, held-out probes, three-effort creativity prompts, pre-registered spacing thresholds and bars in data/human_trial_package.json) plus score_participant(), the SAME code that grades the machine, grading a human's recorded answers on the engine's bars; the pilot with simulated archetypes proves the instrument works: P1 a perfect participant attains every engine bar (L1 ceiling 1.0, L2 1.0, C1 mid creative ~0.24-0.36 >= 0.15, C2/C3 hold); P2 a random non-learner fails L1 (ceiling ~= 1/C) and C1 (yield ~= 0) - the bars are not passable by chance; P3 the joint criterion binds on both sides (trivial items valid-but-not-novel, wild items novel-but-not-valid, mid the only positive yield; a pure copycat scores exactly 0); P4 random far items grade ~100% novel but ~0% creative under the pre-registered thresholds - all SUPPORTED on seeds 42/11/7 as MECHANISM claims (simulated participants validate the instrument, not human behavior; a real trial hands the package to a human and scores with the same code)

Run:  python -m pytest tests/test_solvable_theorems.py -q
"""

import math
import os
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    with open(os.path.join(ROOT, 'data', name)) as fp:
        return json.load(fp)


def test_continuum_limit_first_order_convergence():
    d = load('continuum_limit_drift.json')
    assert d['verdict'].startswith('PASS')
    fit = d['convergence_fit']
    assert fit['order'] >= 0.8
    assert fit['r2'] >= 0.98
    assert d['interior_trajectory_fit']['order'] >= 0.8
    assert d['interior_clean'] is True


def test_spectral_extended_verdicts():
    d = load('spectral_extended_data.json')
    v = d['verdict']
    assert v['c3a'] == 'NOT SUPPORTED'
    assert v['c3b'].startswith('SUPPORTED')
    assert v['c4'].startswith('MEASURED')
    assert 'poisson' in v['c4']
    # the dozenal hit: r_12 vs ln(12), 0.53%
    c1 = {row['k']: row for row in d['c1']}
    assert math.isclose(c1[12]['r_mode'], math.log(12), rel_tol=0.02)
    assert d['c3b']['delta'] < 0.05
    assert d['c4']['r_mean'] < 0.45  # toward Poisson (0.386), away from GOE
    assert d['selberg_zeros']['min_dist'] > 5.0


def test_kawasaki_null_reproduced_and_attributed():
    d = load('kawasaki_null_data.json')
    assert d['verdict'].startswith('RESOLVED')
    m = d['measured']
    assert math.isclose(m['deviation'], 0.4866, abs_tol=1e-3)
    assert math.isclose(m['fraction_eps'], 0.724, abs_tol=1e-2)
    # the uniform-scatter control scatters MORE (0.8349), i.e. the 0.4866
    # is line-structure, not flat-foldability
    assert d['random_control']['deviation'] > m['deviation']
    assert d['exact_2line_vertices']['fraction_eps_0.5'] < 0.15  # 9.5%


def test_pgt_finite_l_refuted():
    d = load('pgt_finite_l_data.json')
    assert d['verdict'].startswith('finite-L RESULT')
    assert 'REFUTED' in d['verdict']
    assert d['growth_form']['slope_logN_vs_L'] < 0.1  # 0.002 vs 1.0
    assert 0.5 < d['sieve_ordering']['pearson_log_log'] < 0.9  # partial: 0.696


def test_fold_golden_closure_derived():
    d = load('fold_golden_closure_data.json')
    assert d['verdict'].startswith('DERIVED')
    assert math.isclose(d['measured'], 0.6137690167, abs_tol=1e-6)
    assert math.isclose(d['derived_at_TH_20'], d['measured'], rel_tol=1e-9)
    assert d['delta'] == 0.0
    assert math.isclose(d['asymptotic_limit']['1/phi'],
                        1.0 / (0.5 * (1 + math.sqrt(5))), rel_tol=1e-6)


def test_prime_time_uniform_and_unmeasurable():
    d = load('prime_time_data.json')
    v = d['verdict']
    assert 'uniform energy conservation' in v
    # drift at prime-indexed steps equals drift at all steps (nothing prime-special)
    assert math.isclose(d['c1']['drift_ratio_prime_vs_all'], 1.0, abs_tol=0.05)
    assert d['c1']['uniform'] is True
    # the claimed N=50 mu=0.065 is not reproduced, and the spectrum diverges by N~214
    assert d['c2']['mu_50'] < 0.05
    assert d['c2']['mu_N'] > 0.5
    # no near-recurrences before the flow escapes the disk
    assert d['c3']['n_recurrences'] == 0
    assert 'UNMEASURABLE' in v


def test_time_reversal_convergence_bound():
    d = load('time_reversal_convergence_data.json')
    # error superconverges to far below the PAPER's 0.003 at finer dt
    rows = {r['dt']: r for r in d['rows']}
    assert rows[0.0005]['ts_error'] < 0.01          # 8.9e-3
    assert rows[0.00025]['ts_error'] < 1e-3         # 7.2e-5
    assert rows[0.000125]['ts_error'] < 1e-4        # 5.9e-7
    assert d['superconvergent'] is True
    assert d['verdict'].startswith('the coarsest dt escapes')


def test_bekenstein_rerun_settled():
    d = load('bekenstein_rerun_data.json')
    fc, fm = d['frictionless_control'], d['frictionless_matched']
    # raw frictionless shift IS significant at n=100 (the old n=30 was underpowered)
    assert fc['n_trajectories'] >= 60
    assert fc['p_value_paired_t'] < 0.01
    assert fc['mean_diff'] > 0
    # but the index-matched control on the same trajectories erases it
    assert fm['p_value_paired_t'] > 0.05
    assert fm['bootstrap_95_ci'][0] < 0 < fm['bootstrap_95_ci'][1]
    assert abs(fm['mean_diff']) < 0.1 * fc['mean_diff']
    assert 'NOT REPRODUCED' in d['verdict']
    assert 'artifact' in d['verdict']


def test_wheeler_dewitt_selects_nothing():
    d = load('wheeler_dewitt_selection_data.json')
    v = d['verdict']
    assert 'EMPTY' in v or 'selects nothing' in v
    # unshifted |H|<eps is empty on every conservative trajectory at eps<=2
    for r in d['results']:
        if r['friction'] == 0.0:
            for row in r['rows']:
                if row['epsilon'] <= 2.0:
                    assert row['unshifted_fraction'] == 0.0
    # the PUM's 86.8% figure is not reproduced by the current filters
    assert d['scan_for_86.8pct']['reproduced'] is False


def test_fold_not_a_unitary_gate():
    d = load('fold_unitary_data.json')
    assert d['verdict'].startswith('NOT a unitary gate')
    c = d['checks']
    assert c['n_preimages'] == 2
    assert c['angle_collisions'] > 0
    assert abs(c['L_ratio'] - 0.5) < 0.05  # fold ~ half the development length


def test_kawasaki_not_a_ctc_constraint():
    d = load('kawasaki_ctc_data.json')
    assert d['verdict'].startswith('NOT a CTC constraint')
    assert d['satisfaction_at_null_rate'] is True
    assert d['input']['kawasaki_exact_2line_fraction_eps_0_5'] < 0.15
    # admission collapses with loop size exactly as the null does
    for V in ('4', '8', '16'):
        assert d['loop_sizes'][V]['binding'] is False


def test_bridge_extends_to_all_primes_trivially():
    d = load('bridge_extension_data.json')
    # census's own 6/186 resonance is NOT significant vs uniform null
    assert d['census']['binom_p_gt_uniform'] > 0.05
    # extended bridge: near-integer rate barely above the 2% uniform null
    ext = d['extended']
    assert 0.02 <= ext['near_int_rate'] <= 0.03
    # random-integer control reproduces most of the elevation
    ctrl = d['random_integer_control']['near_int_rate']
    assert ctrl >= 0.022
    # prime-specific residue is real but tiny (< 0.5pp)
    pv = d['prime_vs_random']
    assert pv['prime_specific'] is True
    assert pv['elevation'] < 0.005
    assert 'trivially extends' in d['verdict'] or 'trivial' in d['verdict']


def test_selberg_paradigm_not_a_concrete_instance():
    d = load('selberg_paradigm_data.json')
    assert d['a_level_stats']['verdict'].startswith('POISSON')
    # GOE excluded at >5 sigma at 100 modes, canonical constant 0.5307
    assert d['a_level_stats']['z_goe'] < -5.0
    assert d['a_level_stats']['ks_goe_p'] < 0.05
    assert d['a_level_stats']['ks_poisson_p'] > 0.05
    # no Riemann-zero correspondence is testable at this scale: the disk
    # t-range never reaches the first zero, and the Weyl densities differ
    assert d['b_zeros']['spectra_overlap'] is False
    assert d['b_zeros']['reach_gap'] > 5.0
    assert d['b_zeros']['density_ratio'] > 100
    assert d['b_zeros']['modes_needed_to_reach_t1'] > 100
    # Mersenne lengths produce no trace-formula signal vs a matched null
    assert d['c_form_factor']['mersenne_mean_abs_pctile'] < 95.0
    assert 40.0 < d['c_form_factor']['local_percentile_mean'] < 60.0
    assert d['verdict'].startswith('SELBERG PARADIGM NOT SUPPORTED')


def test_riemann_decimal_perspective_no_shared_spectrum():
    d = load('riemann_decimal_perspective_data.json')
    # 100 zeros (GUE, beta=2) on the decimal axis, not GOE
    z = d['zeros_decimalized']
    assert 0.55 < z['r_mean'] < 0.67
    assert z['z_vs_gue'] < 3.0
    assert z['z_vs_goe'] > 3.0
    assert z['ks_vs_exact_gue_p'] > 0.05
    # disk (real symmetric) is Poisson on the decimal axis
    dz = d['disk_decimalized']
    assert 0.30 < dz['r_mean'] < 0.45
    assert abs(dz['z_vs_poisson']) < 3.0
    assert dz['ks_vs_poisson_p'] > 0.05
    # the two normalized spectra are mutually excluded
    assert d['two_sample_ks']['p'] < 0.01
    # rigidity: the zeros' decimals are far closer to the ideal grid
    rg = d['decimal_rigidity']
    assert rg['zeros_residual_std'] < rg['disk_residual_std']
    assert rg['zeros_z_vs_null'] < -2.0
    assert d['verdict'].startswith('DECIMAL PERSPECTIVE')


def test_riemann_siegel_root_engine_reproduces_decimal_perspective():
    d = load('riemann_siegel_roots_data.json')
    # the engine locates the first 100 zeros on the real Z function alone
    zf = d['zeros_found']
    assert zf['n'] == 100
    assert zf['max_abs_error_vs_zetazero'] < 1e-5
    assert zf['mean_abs_error_vs_zetazero'] < 1e-6
    # the engine matches |zeta(1/2+it)| on the critical line
    assert d['engine_validation']['max_rel_error'] < 1e-3
    # the decimal-perspective verdict is reproduced from the RS-found roots
    ds = d['decimal_perspective_reproduced']
    assert 0.55 < ds['r_mean'] < 0.67
    assert abs(ds['r_mean'] - ds['prior_artifact_r_mean']) < 0.01
    assert abs(ds['residual_std'] - ds['prior_artifact_residual_std']) < 0.05
    assert ds['rvm_s_residual_max'] < 1.0
    assert ds['z_vs_uniform'] < -2.0
    # condensation: the main-sum cutoff stays at floor(sqrt(t/2pi)) = 6
    c = d['condensation']
    assert c['cutoff_at_first_zero'] == 1
    assert c['cutoff_at_100th_zero'] == 6
    assert c['per_evaluation_condensation_factor_at_t100'] > 5.0
    assert d['verdict'].startswith('RIEMANN-SIEGEL ROOT ENGINE VALIDATED')


def test_riemann_siegel_certifier_turing_height_999():
    d = load('riemann_siegel_certify_data.json')
    # interval-arithmetic certification + Turing's method close with a clean verdict
    assert d['verdict'].startswith('RIEMANN-SIEGEL CERTIFIED')
    # every enclosure must contain the high-precision mpmath value
    assert d['validation']['pass'] is True
    assert all(p['contained'] for p in d['validation']['points'])
    assert d['validation']['theta_contained_at_all_gram_points'] is True
    # 653 Gram points, all certified signs; 654 simple on-line zero brackets
    assert d['gram_points']['count'] == 653
    assert d['gram_points']['certified_signs_ok'] is True
    assert d['zeros']['located'] == 654
    assert d['zeros']['certified_brackets_ok'] is True
    # Turing/Brent: N(g_n) = n+1 = 648 zeros below g_n = 999.236, on the line
    c = d['count']
    assert c['n'] == 647
    assert abs(c['g_n'] - 999.2362) < 1e-3
    assert c['N_gn'] == 648
    assert c['zetazero_crosscheck_match'] is True
    assert c['max_abs_S'] <= 1.0
    assert d['turing']['n_needed'] == 1
    assert d['turing']['blocks_ok'] is True
    assert all(b['rosser'] for b in d['turing']['blocks'])
    # honest wall: a finite verification, NOT a proof of RH
    assert 'does NOT prove' in d['verdict']


def test_debruijn_newman_condensation():
    d = load('debruijn_newman_condensation_data.json')
    assert d['verdict'].startswith('DE BRUIJN-NEWMAN CONDENSATION')
    # Phi(u) is even (Poisson): worst |Phi(u)-Phi(-u)| at dps 50 < 1e-50
    assert d['evenness']['worst'] < 1e-50
    # H_0(z) = (1/8)xi(1/2+iz/2): exact at z=10, 1e-48 at z=55
    assert d['identity']['10']['rel'] < 1e-40
    assert d['identity']['55']['rel'] < 1e-45
    # fast evaluator: t=0 slice tracks analytic xi to 4e-8 at the z~223 worst case
    val = d['vmethod_validation']
    assert val['rel_vs_xi'] < 1e-6
    assert val['rel_vs_v_ref'] < 1e-5
    # P1 (first-40 closest pair, gap 0.845): measured merger law vs local model
    p1 = d['heatflow']['P1']
    assert math.isclose(p1['Delta_gamma'], 0.8451236, rel_tol=1e-4)
    assert abs(p1['fit_slope'] - p1['model_slope']) < 2.0     # model slope 8
    assert abs(p1['fit_t_c'] - p1['model_t_c']) < 0.1         # model t_c -0.3571
    # merger confirmed: real separation at 0.90*t_c, merged (d null) at 1.05*t_c
    assert p1['t_c_confirm'][0]['d'] is not None
    assert p1['t_c_confirm'][1]['d'] is None
    # Polya direction: zeros persist and SEPARATE for t > 0
    assert p1['polya_plus'][0]['real_persists'] is True
    assert p1['polya_plus'][0]['d'] > p1['separations'][0]['d']
    # P2 (gap 1.219): deeper predicted boundary, still negative fit
    p2 = d['heatflow']['P2']
    assert p2['fit_t_c'] < 0
    assert p2['polya_plus'][0]['real_persists'] is True
    # certified global closest pair: local-model boundary 0.048 below the axis
    g = d['heatflow']['global_closest_pair']
    assert g['idx'] == 452
    assert math.isclose(g['Delta_gamma'], 0.3104307, rel_tol=1e-4)
    assert abs(g['t_c_local_model'] + 0.04818) < 1e-3
    # honest wall: a finite probe, NOT a bound on Lambda, no proof of RH
    assert 'NOT a bound' in d['verdict']
    assert 'proves RH' in d['verdict']


def test_merger_scaling():
    d = load('merger_scaling_data.json')
    assert d['verdict'].startswith('MERGER-BOUNDARY CREEP')
    # the engine re-locates 43851 consecutive zeroes exactly (count + oracle)
    s = d['scan']
    assert s['count_match'] is True
    assert s['zeros_found'] == 43851
    assert s['max_crosscheck_diff'] < 1e-5
    # the classical Lehmer pair (idx 6708, gamma ~ 7005.06/7005.10) is re-found
    lh = d['lehmer']
    assert lh['idx_pair'] == 6708
    assert math.isclose(lh['gap'], 0.0377, abs_tol=1e-3)
    # the creep table starts at the certified slice and creeps toward the axis
    c = d['creep']['creep']
    assert math.isclose(c['648']['t_c'], -0.04818, abs_tol=1e-3)
    assert c['1000']['t_c'] > c['648']['t_c']
    assert c['10000']['t_c'] > c['2000']['t_c']
    # deepest record pair: gap 0.0353 at gamma ~ 17144, t_c ~ -6.2e-4
    dp = d['creep']['deepest']
    assert math.isclose(dp['gap'], 0.03531, abs_tol=1e-4)
    assert 17000 < dp['gamma'] < 17300
    assert abs(dp['t_c'] + 6.23e-4) < 1e-5
    # record-tight reduced gaps follow the GUE small-gap tail: slope ~ -1/3
    fit = d['creep']['fit']
    assert abs(fit['slope'] - (-1.0 / 3.0)) < 0.1
    # GUE null present and tight-tail rows make sense (observed below mean)
    rows = d['gue_null']['rows']
    assert len(rows) >= 10
    assert rows[-1]['observed'] < rows[-1]['gue_mean_min']
    # honest wall: located not certified, NOT a bound on Lambda, no proof of RH
    assert 'NOT a bound' in d['verdict']
    assert 'proves RH' in d['verdict']


def test_golden_fold_not_a_chain_law():
    d = load('fold_ladder_phi_data.json')
    assert d['verdict'].startswith('NOT SUPPORTED')
    # only the celebrated upper rung 1,914,467/730,421 is golden
    assert d['adjacent_hits'] == 1
    assert d['adjacent_n'] == 4
    # the single hit is at the 0.115% coincidence scale, not a ladder
    upper = d['adjacent_rungs'][1]
    assert upper['hi'] == 1914467 and upper['lo'] == 730421
    assert upper['dev_nearest_target_pct'] < 0.5
    # all three other rungs miss by far more than 1%
    for row in (d['adjacent_rungs'][0], d['adjacent_rungs'][2],
                d['adjacent_rungs'][3]):
        assert row['hit_within_1pct'] is False
        assert row['dev_nearest_target_pct'] > 1.0
    # an isolated hit is not rare under the magnitude-matched null
    assert d['null']['p_any_golden_rung'] < 0.05
    # the giant is the chain top: no defined rung above it
    assert d['next_fold_above_giant']['hit_within_1pct'] is False


def test_hierarchical_c0_flow_supported():
    d = load('flow_hierarchical_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    r = d['results']
    # hierarchical routing beats flat C0 flow routing
    assert r['hierarchical']['router'] > r['flat_c0_flow']['router']
    # and costs far fewer comparisons per level than flat (30)
    assert r['comparisons_per_level'] == 6
    assert r['comparisons_per_level'] < r['flat_comparisons'] / 4
    # nearest-centroid accuracy stays high (~parity with flat)
    assert r['hierarchical']['nc'] > 0.95
    assert abs(r['hierarchical']['nc'] - r['flat_c0_flow']['nc']) < 0.05


def test_flow_active_learning_margin_beats_random():
    d = load('flow_active_learning_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    ltt = d['labels_to_target']
    # margin reaches 0.80 and 0.82 with strictly fewer labels than random
    for t in ('0.8', '0.82'):
        assert ltt[t]['margin'] is not None
        assert ltt[t]['random'] is not None
        assert ltt[t]['margin'] < ltt[t]['random']
    # honest wall is pinned too: raw force-cancellation is NOT the label-efficiency winner
    ltt078 = ltt['0.78']
    assert ltt078['force'] is None or ltt078['force'] > ltt078['margin']
    fin = d['final_accuracy']
    assert fin['margin_al'] >= fin['random'] - 0.02


def test_balance_survey_partial_not_layout_optimum():
    d = load('balance_survey_data.json')
    assert d['verdict'].startswith('PARTIAL')
    # the layout optima are NOT at mu=0.5
    assert d['part1']['mu0_5_is_peak'] is False
    assert d['part1']['best_packing_mu'] != 0.5
    assert d['part1']['best_uniformity_mu'] != 0.5
    # the balanced tier is the shock absorber; the tight core shatters
    t = d['part2']['tiers']
    assert t['n3_mu0_5'] == 'n3 equilibrate'
    assert t['n2_mu0_9'] == 'n1 shatter'
    # pure repulsion routes best
    assert d['part3']['pure_repulsion_routes_best'] is True


def test_balance_scale_confound_not_cause():
    d = load('balance_scale_data.json')
    assert d['verdict'].startswith('REFUTED')
    # the A*(n) fit is a real super-linear scaling
    assert d['part2']['beta'] > 1.0
    # A* is strictly increasing in n (trap must scale UP)
    a_star = d['part2']['A_star']
    keys = ['5', '10', '20', '40', '80']
    for i in range(len(keys) - 1):
        assert a_star[keys[i + 1]] > a_star[keys[i]]
    # fixed-A absorb does NOT underperform the scaled one (confound, not cause)
    assert d['part3_final']['FIB+ABS']['final_old'] >= 0.85
    # dimension-independence claim is persisted
    assert d['part4_dimension_independent'] is True


def test_balance_continual_adaptive_wins():
    d = load('balance_continual_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # adaptive beats pure-expansion on old-class routing (flat, seed 42)
    p1 = d['part1_flat_seed42']
    assert p1['AD']['old_route'] > p1['P0']['old_route']
    # fixed balanced P5 is harmful: lower all_route than AD
    assert p1['AD']['all_route'] > p1['P5']['all_route']
    # same in the hierarchical part
    p2 = d['part2_hier_seed42']
    assert p2['AD']['old_hier'] > p2['P0']['old_hier']
    assert p2['AD']['all_hier'] > p2['P5']['all_hier']
    # AD wins both axes across all three seeds
    for i in range(3):
        assert d['multi_seed_part1_old_route']['AD'][i] > d['multi_seed_part1_old_route']['P0'][i]
        assert d['multi_seed_part2_old_hier']['AD'][i] > d['multi_seed_part2_old_hier']['P0'][i]


def test_polysphere_extensions_not_supported():
    d = load('polysphere_extensions_data.json')
    assert d['verdict'].startswith('NOT SUPPORTED')
    # learned truths do not reproduce routing accuracy
    e2 = d['extension2_learned_truths']
    assert e2['learned_truth_acc'] < 0.6
    assert e2['true_truth_acc'] > 0.99
    # S^2 repulsion destroys the clustering that was present
    e4 = d['extension4_sphere']
    assert e4['initial_sep_ratio'] > 10.0
    assert e4['repulsion_only_ratio'] < 1.5
    assert e4['with_attraction_ratio'] < 2.0
    # the pieces that DO hold stay pinned
    assert d['extension3_scaling']['batch_acc_by_faces']['100'] > 0.9
    assert d['extension3_scaling']['anomaly_gap_by_faces']['6'] > 0.5


def test_flow_incremental_mixed_not_uniform():
    d = load('flow_incremental_data.json')
    assert d['verdict'].startswith('MIXED')
    rows = d['stage_rows']
    # reflow always keeps min_d strictly higher than random-add (separation)
    for k in rows:
        assert rows[k]['reflow']['min_d'] > rows[k]['random_add']['min_d']
    # but random-add matches or beats reflow on all-class routing at least once
    assert any(rows[k]['random_add']['all_acc'] >= rows[k]['reflow']['all_acc']
               for k in rows)
    # and reflow pays a displacement cost that random-add does not
    assert any(rows[k]['reflow']['disp_old'] > 0.1 for k in rows)


def test_flow_hier_incremental_no_forgetting_supported():
    d = load('flow_hier_incremental_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    s = d['summary']
    # no forgetting: old-class routing strictly above all-class routing
    assert s['old_hier_avg'] > s['all_hier_avg']
    # hierarchical routing beats the flat router
    assert s['all_hier_avg'] > s['flat_avg']
    # separation is bounded below at every growth stage
    assert all(r['min_d'] >= 0.11 for r in d['stage_rows'])
    # the coarse reflow (new group) translates old anchors 1:1 (pure shift)
    group_stage = [r for r in d['stage_rows'] if r['action'] == 'group']
    assert len(group_stage) == 1
    assert group_stage[0]['disp_c'] == group_stage[0]['disp_f']
    assert group_stage[0]['disp_c'] > 0.1


def test_polysphere_use_cases_batch_supported():
    d = load('polysphere_use_cases_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # batch/generative routing is perfect
    assert d['use_case_1_classifier']['batch_acc'] == 1.0
    assert d['use_case_1_classifier']['per_point_acc'] > 0.5  # 0.653 vs chance 0.167
    # anomaly detection: large confidence gap, high rejection
    u2 = d['use_case_2_anomaly']
    assert u2['gap'] > 0.6                      # 0.728
    assert u2['in_kept'] == 1.0
    assert u2['ood_rejected'] > 0.95            # 0.983
    # generated samples re-route to source; continual add keeps accuracy
    assert d['use_case_3_generation']['cross_gen_all_ok'] is True
    u4 = d['use_case_4_continual']
    assert u4['acc_before'] == 1.0 and u4['acc_after'] == 1.0
    assert u4['spherical_separation'] > 0.9     # ~0.94, not bit-reproducible
    assert 'not bit-reproducible' in u4['note'].lower()


def test_polysphere_routing_batch_exact():
    d = load('polysphere_routing_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # batch routing is exact: identity confusion matrix
    assert d['batch_acc'] == 1.0
    assert d['confusion_offdiag'] == 0
    # per-point routing is weak but well above chance
    assert d['per_point_acc'] > 0.5                      # 0.659 vs chance 0.167
    # spherical separation is strong
    s = d['spherical_separation']
    assert s['silhouette'] > 0.9
    assert s['inter_mean'] > 10 * s['intra_mean']


def test_golden_survey_exact_and_no_emergent_locking():
    d = load('golden_survey_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # Part 1: step ratio is phi EXACTLY (machine precision)
    p1 = d['part1_fib_spiral']
    assert abs(p1['diff_from_phi']) < 1e-9
    assert math.isclose(p1['radius_per_turn'], p1['phi4'], rel_tol=1e-6)
    # Part 2: static C0 packing is uniform rings (no golden structure)
    assert all(r['gap_cv'] < 0.15 for r in d['part2_static_packing'][1:])
    # Part 3a: golden rotation maximizes the minimum angular gap
    assert d['part3a_rotation']['golden_maximizes'] is True
    # Part 3b: gap-filling does NOT lock onto the golden angle
    assert all(r['within_5deg_fraction'] <= 0.1 for r in d['part3b_arc_model'])
    assert all(r['abs_diff_from_golden'] > 100.0 for r in d['part3b_arc_model'])
    # Part 4: metric-and-regime dependent (cusp phi, disk -> 1)
    p4 = d['part4_metric_terms']
    assert abs(p4['cusp_log_coords'] - d['phi']) < 1e-5
    assert p4['euclidean_asymptotic'] < 1.01
    assert p4['poincare_hyperbolic'] < 1.01


def test_fib_stream_steady_and_ad_wins_all_seeds():
    d = load('fib_stream_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # AD_phi (absorb during large terms) beats P0 on BOTH axes in all 3 seeds
    for sd, m in d['multi_seed_finals'].items():
        assert m['final_all_ad'] > m['final_all_p0']
        assert m['final_old_ad'] > m['final_old_p0']
    # golden-rotation insertion is neutral after the flow (washes out)
    for row in d['partB_golden_vs_center']:
        assert abs(row['golden_all'] - row['center_all']) < 0.2
        assert abs(row['golden_old'] - row['center_old']) < 0.2
    # scaling: mean_r pinned by the clamp, min_d obeys a ring-packing law
    c = d['partC_scaling']
    assert abs(c['fib_center_P0']['a_mean_r']) < 0.1
    assert -0.9 < c['fib_center_P0']['b_min_d'] < -0.5
    assert -0.9 < c['eq_center_P0']['b_min_d'] < -0.5


def test_hamiltonian_routing_flow_separates():
    d = load('hamiltonian_routing_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    pd = d['pair_dist']
    # the flow separates centroids in the MEAN
    assert pd['flow_mean'] > 5 * pd['init_mean']            # 1.1433 vs 0.1803
    # ...but NOT in the min (clamped to the boundary)
    assert pd['flow_min'] < 0.05
    r = d['routing_acc']
    assert r['flow'] > r['init'] + 0.2                      # +0.345
    assert r['flow'] > r['best_random']                     # 0.765 vs 0.260
    # nearest-centroid reaches the oracle ceiling
    nc = d['nearest_centroid']
    assert nc['flow'] > 0.9
    assert nc['flow'] >= nc['oracle'] - 0.05                # 0.909 vs 0.911


def test_metric_comparison_refuted_numerically():
    d = load('metric_comparison_data.json')
    assert d['verdict'].startswith('REFUTED')
    p = d['metrics']['poincare']
    c = d['metrics']['cusp']
    # Poincare has NaN states; cusp escapes to ~2e13
    assert p['has_nan']
    assert c['r_range'][1] > 1e6
    assert not p['c0_holds'] and not c['c0_holds']
    assert p['c0_max_dev'] > 20 and c['c0_max_dev'] > 20
    assert not p['tsym_ok'] and not c['tsym_ok']
    assert c['energy_drift'] > 1e10


def test_c0_crossing_tsym_caveat():
    d = load('c0_crossing_tsym_data.json')
    assert d['verdict'].startswith('CAVEAT')
    rows = d['experiments']
    assert len(rows) == 4
    # T-symmetry holds (err < 0.5) in every run
    assert all(r['pass'] for r in rows)
    assert max(r['ts_error'] for r in rows) < 0.5
    # BUT the crossing premise never occurred: closest approach == start dist
    assert all(r['min_dist_to_origin'] > 0.0 for r in rows)
    # A/B/C never cross the q1 axis
    assert not rows[0]['crossed_origin'] and not rows[1]['crossed_origin']


def test_c0_cusp_flow_refuted():
    d = load('c0_cusp_flow_data.json')
    assert d['verdict'].startswith('REFUTED')
    c = d['cusp']
    p = d['poincare']
    # cusp escaped to ~2.7e23
    assert c['r_range'][1] > 1e6
    # Poincare overflowed to NaN
    assert not isinstance(p['r_range'][1], float) or p['r_range'][1] > 1.0
    assert not c['c0_holds']
    assert not c['tsym_ok'] and not p['tsym_ok']
    assert c['energy_drift'] > 1e10
    assert c['tsym_err'] > 1e6


def test_t39_cusp_flow_supported():
    d = load('t39_cusp_flow_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    v = d['verification']
    # exact conservation / exact geodesic
    assert v['cusp_energy_cv'] < 1e-12
    assert abs(v['step_ratio_asymp'] - v['phi']) < 1e-6
    assert v['wplane_r2'] > 0.999999
    assert abs(v['wplane_slope'] - v['wplane_expected_slope']) < 1e-6
    assert v['tsym_error'] == 0.0


def test_van_iterson_no_golden_lock():
    d = load('van_iterson_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    assert d['any_golden_lock'] is False
    # all three continuous rules, all 12 (r0, relax) settings: no lock
    for rule, rows in d['continuous_rules'].items():
        assert len(rows) == 12
        for row in rows:
            assert row['locked'] is False
            assert row['within5_frac'] < 0.5
    # part 1 control also never locks
    for row in d['part1_control']:
        assert row['within5_frac'] < 0.5


def test_reverse_pair_gaps_refuted():
    d = load('reverse_pair_gaps_data.json')
    assert d['verdict'].startswith('REFUTED')
    r = d['relations']
    # NOT a reversal pair: reverse(10262) = 26201 != 26102
    assert r['is_reversal_pair'] is False
    assert r['reverse_10262'] == 26201
    # sub-relations do hold
    assert r['diff_80_multiple'] is True
    assert r['digit_sum_10262'] == 11 and r['digit_sum_26102'] == 11
    # censuses are ordinary exact arithmetic
    assert d['gap_census_pair']['n_primes'] > 1000
    assert d['gap_census_mid']['n_primes'] > 100000
    assert d['emirps']['count'] > 300


def test_fibonacci_spiral_disk_refuted():
    d = load('fibonacci_spiral_data.json')
    assert d['verdict'].startswith('REFUTED')
    c = d['comparison']
    # turning far from golden angle in both projections
    assert c['mod_square_diff_deg'] > 50
    assert c['ratio_diff_deg'] > 50
    # pseudo-energy not conserved
    assert c['ratio_energy_drift'] > 1.0
    assert c['spiral_energy_drift'] > 0.5


def test_prime_count_engine_supported_with_corrections():
    d = load('prime_engine_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # exact prime counts at every retrace-chain point
    assert d['pi']['10262'] == 1258
    assert d['pi']['26102'] == 2868
    assert d['pi']['943901200001'] == 35575526191
    # endpoint prime, next gap 8
    assert d['endpoint_prime'] is True
    assert d['gap_above'] == 8
    # correction 1: true gap below is 24, not 'gap 1'
    assert d['gap_below'] == 24
    # correction 2: window max gap 176 exceeds the script's own 40-100 note
    assert d['max_gap_window'] == 176
    assert d['max_gap_window'] < d['cramer_ln2']
    # PNT: mean gap near ln N
    assert d['mean_gap'] > 25


def test_fibonacci_squares_disk_refuted():
    d = load('fibonacci_squares_data.json')
    assert d['verdict'].startswith('REFUTED')
    m = d['measurements']
    # 90-deg turning is a construction artifact, but pseudo-energy not conserved
    assert m['mean_turn_deg'] == 90.0
    assert m['pseudo_energy_drift'] > 0.5
    assert m['energy_linear_trend_per_step'] < 0  # decaying
    assert m['escaped'] is True
    assert not m['fib_tsym_ok']
    assert m['fib_tsym_error'] > 0.5
    assert m['c0_geodesic_tsym_error'] < 1e-6


def test_rotation_test_supported_with_correction():
    d = load('rotation_test_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # J1: rotation preserves structure exactly
    assert d['overlap_rotation'] > 0.999
    assert d['sim_corr'] > 0.999
    # J2: coordinates all change
    assert d['coord_max'] > 0.5
    # J3 correction: abs() disrupts but does NOT collapse to chance
    assert d['overlap_abs'] < d['overlap_rotation']
    assert d['overlap_abs'] > 5 * d['chance']


def test_clock_test_supported():
    d = load('clock_test_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # F1: calendar convention carries the law exactly at e0
    assert d['f1'] > 0.999
    # F2: the +15 re-index breaks it (and even dips below chance)
    assert d['f2'] < 0.5
    # F3: intrinsic features survive both epochs
    assert d['f3a'] > 0.999 and d['f3b'] > 0.999


def test_spring_fold_supported():
    d = load('spring_fold_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # A: mirror fold sweeps growth twice exactly (analytic area)
    assert abs(d['A']['area'] - d['A']['area_pred']) / d['A']['area_pred'] < 1e-6
    # A1: retrace fold closes EXACTLY to C0 and crease is exactly pi
    assert d['A1']['closure'] == 0.0
    assert abs(d['A1']['crease_pi'] - 1.0) < 1e-3
    # A2: golden fold ratio is phi exactly, but does NOT close to C0
    assert abs(d['A2']['ratio'] - 1.618033988749895) < 1e-9
    assert d['A2']['closure'] > 1.0
    # C: overcoil lock tucks the end under the start (closed ring)
    assert d['C']['tuck_on_start'] is True


def test_eikonal_fold_supported():
    d = load('eikonal_fold_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # E1: upwind viscosity solution converges to the exact tent
    assert d['eikonal_err'] < 1e-10
    # E2: crease is the cut locus exactly (equal arrival times)
    assert d['cut_locus'] == 0.0
    # E4: polar swept area matches analytic 2*a^2*TH^3/6 exactly
    assert abs(d['area_mirror'] - d['area_pred']) / d['area_pred'] < 1e-6
    assert abs(d['area_retrace']) < 1e-9


def test_retrace_boundary_supported():
    d = load('retrace_boundary_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # E1: the zig-zag family are all genuine weak solutions
    assert all(ok for _, ok, _ in d['weak_family'])
    # E2: tent passes viscosity; every zig-zag fails (down-up corner)
    assert d['tent_passes'] is True
    assert all(not ok for _, ok, _, _ in d['zigzag_viscosity'])
    # E3: upwind from a zig-zag seed converges to the tent
    assert d['upwind_from_zigzag_err'] < 1e-10
    # E4: selected switch point is the cut locus (equal eikonal time, exact)
    assert d['cut_locus_eq'] == 0.0
    # E5: reflection conserves |r'| across the crease
    assert d['reflection'] < 1e-9


def test_fold_optimizer_supported():
    d = load('fold_optimizer_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # G1: Hamiltonian energy drift is small and bounded (not secular)
    assert d['drift_h'] < 0.01
    assert d['area_ratio_h'] > 0.9
    # G2: recurrence returns near the start (Poincare)
    assert d['recurrence'] < 1e-3
    # G3: damped energy collapses to the minimum, area contracts fully
    assert d['ed_final'] < 1e-6
    assert d['area_ratio_d'] < 1e-3
    # G4: locks at the minimum and stays
    assert d['lock_err'] < 1e-3
    assert d['stays'] is True


def test_t65_fourpack_mixed_refuted():
    d = load('t65_fourpack_results.json')
    assert d['verdict'].startswith('MIXED')
    # P1: tau is identical across curiosity_drive (degenerate -> corr nan)
    assert d['P1']['tau_constant'] is True
    assert d['P1']['corr_cd_tau'] == 'nan'
    assert len(set(d['P1']['mean_tau'])) == 1
    # P2: ascent does NOT recover the seed (far above near-zero)
    assert all(e > 1.0 for e in [p['hyperbolic_err_to_seed'] for p in d['P2']])
    # P3: projection retains signal above null, but a single coord already full
    assert d['P3']['mi_projection'] > 1.5 * d['P3']['mi_null']
    assert d['P3']['mi_single_coord'] > 0.99
    # P4: no fixed-point convergence under dream/remix
    assert d['P4']['converged_fraction'] == 0.0


def test_phi_scheduler_supported_with_caveat():
    d = load('phi_scheduler_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # P5 fixed mu=0.5 is never usable: worst stream routing (holds per-seed)
    assert d['P5']['stream_old'] <= min(v['stream_old'] for v in d.values()
                                        if isinstance(v, dict) and 'stream_old' in v)
    # FIB+ABS buys final whole-layout integrity at old-routing cost (per-seed)
    assert d['FIB+ABS']['final_all'] > d['FIB']['final_all']
    assert d['FIB+ABS']['final_old'] < d['FIB']['final_old']
    # FIB keeps bounded latency
    assert 0 < d['FIB']['mean_buf'] <= 2.5
    # Part 3 (MNIST): scheduling is not needed on real embeddings
    assert d['part3_final_all']['NAIVE'] > d['part3_final_all']['FIB'] > d['part3_final_all']['FIB+ABS']


def test_flow_regularized_supported_narrow_window():
    d = load('flow_regularized_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # baseline numbers pinned
    assert abs(d['baseline']['routing'] - 0.9) < 1e-6
    assert abs(d['baseline']['test_acc'] - 0.905) < 1e-6
    # best lambda=0.007 wins on routing with accuracy preserved
    best = d['best']
    assert best['lambda'] == 0.007
    assert best['routing'] == 0.93
    assert best['test_acc'] >= d['baseline']['test_acc'] - 0.01
    # stronger flow (lambda=0.01) clearly hurts routing
    row = next(r for r in d['sweep'] if r['lambda'] == 0.01)
    assert row['routing_delta'] < -0.05


def test_flow_hier_reg_not_supported():
    d = load('flow_hier_reg_data.json')
    assert d['verdict'].startswith('NOT SUPPORTED')
    b, f = d['baseline'], d['flow-REG']
    # flow does NOT reduce drift (it is slightly worse)
    assert f['drift'] > b['drift']
    # flow is clearly worse on flat routing at stage 2
    assert f['routing_all'] < b['routing_all']
    assert f['routing_old'] < b['routing_old']
    # accuracy essentially preserved
    assert f['stage2_test_all'] >= b['stage2_test_all'] - 0.01
    # the one flow benefit: hierarchical routing is better
    assert f['hier_all'] > b['hier_all']
    assert f['hier_old'] > b['hier_old']


def test_flow_hier_reg_scaled_not_supported():
    d = load('flow_hier_reg_scaled_data.json')
    assert d['verdict'].startswith('NOT SUPPORTED')
    f, n, l = d['means']['FIXED'], d['means']['NSCAL'], d['means']['LIN']
    # n-scaling gain is marginal (<1% relative drift), everything else identical
    assert f['drift_rel'] - n['drift_rel'] < 0.01
    assert f['drift_rel'] - l['drift_rel'] < 0.01
    assert f['drift_rel'] == n['drift_rel'] or f['drift_rel'] - n['drift_rel'] > 0
    for m in (f, n, l):
        assert abs(m['acc_all'] - n['acc_all']) < 1e-4  # identical to 3 dp
    assert d['best_drift_rule'] in ('FIXED', 'NSCAL', 'LIN')


def test_balance_auto_not_supported():
    d = load('balance_auto_data.json')
    assert d['verdict'].startswith('NOT SUPPORTED')
    # detector fires only on the explosive event
    assert d['detector_fires_only_on_burst']
    # but AD does NOT beat P0: routing gains are <= 0
    assert d['ad_vs_p0_gains']['old_route'] <= 0.0
    assert d['ad_vs_p0_gains']['all_route'] <= 0.0
    p2 = d['part2']
    # P0 marginally best on real MNIST; P5 clearly worst on min separation
    assert p2['P0']['all_route'] >= p2['AD']['all_route']
    assert p2['P5']['min_d'] < p2['P0']['min_d']


def test_self_balancing_supported_geometry_regime():
    d = load('self_balancing_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # the coherence gate FIRES: COH skips the absorb in the crowded core
    assert d['coh_skips_absorb_part3_seed_42']
    assert d['part3']['COH']['absorbed'] == 'no'
    assert d['part3']['ABS']['absorbed'] == 'yes'
    # COH lands exactly on P0 in the crowded core (T51 failure avoided)
    assert d['part3']['COH']['old_route'] == d['part3']['P0']['old_route']
    assert d['part3']['COH']['all_route'] == d['part3']['P0']['all_route']
    # all-routing gain survives on the clean stream
    assert d['part2']['COH']['final_all'] > d['part2']['P0']['final_all']
    # but Part 4 MNIST: COH final_all below FIB (controller adds nothing there)
    assert d['part4_summary']['COH']['final_all_last'] < d['part4_summary']['FIB']['final_all_last']


def test_polysphere_mnist_supported():
    d = load('polysphere_mnist_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    p1 = d['part1']
    # batch routing far above chance
    assert p1['batch_routing']['acc'] > 0.8
    # wide anomaly gap
    assert p1['anomaly_gap'] > 0.4
    assert p1['conf_in'] > p1['conf_ood'] + 0.4
    # hierarchical well above combined chance but below flat
    assert d['part2']['hier_acc'] > 0.5
    assert d['part2']['hier_acc'] < p1['batch_routing']['acc']
    # active learning reaches perfect routing after faces added
    assert d['part3']['final_10_acc'] == 1.0
    assert d['part3']['unknown_flagged']['rate'] > 0.4


def test_polysphere_nnflow_viz_partial():
    d = load('polysphere_nnflow_viz_data.json')
    assert d['verdict'].startswith('PARTIAL')
    p1, p2 = d['part1_nn_truths'], d['part2_s2_flow']
    # NN-truth routing supported: far above chance
    assert p1['routing_acc'] > 0.8
    # S^2 flow NOT supported: near-zero silhouette, <all faces self-route
    assert p2['silhouette'] < 0.1
    assert p2['self_routed'] < p2['n_faces']
    # viz distribution sanity: routed vs actual per-class fractions align
    for row in d['part3_viz_distribution']:
        assert abs(row['routed_pct'] - row['actual_pct']) < 5.0


def test_decentral_net_supported():
    d = load('decentral_net_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    p4 = d['part4_final']
    # local flow usable on real embeddings: ABS-SC beats FIB on all-routing
    assert p4['ABS-SC']['all_route'] > p4['FIB']['all_route']
    # old-routing preserved
    assert p4['ABS-SC']['old_route'] >= 0.8
    assert p4['FIB']['old_route'] >= 0.8
    # banner discloses multi-seed means for parts 0-3
    assert 'seeds 42/11/7' in d['multi_seed_banner_parts_0_3']


def test_decentral_net_mnist_supported():
    d = load('decentral_net_mnist_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # local-settle routes ~ at nearest-centroid baseline
    assert d['acc_grown_decentralnet'] >= d['acc_base_nearest_centroid'] - 0.03
    # local heal restores spacing
    assert d['spacing_after'] > d['spacing_before']
    # survivors keep routing after killing 3 neurons
    assert d['acc_survivors_broken'] >= 0.8
    assert d['acc_survivors_healed'] >= 0.8
    # regrow restores full 10-class net (above chance)
    assert d['acc_regrown_full'] > 0.7


def test_decentral_net_continual_not_supported():
    d = load('decentral_net_continual_data.json')
    assert d['verdict'].startswith('NOT SUPPORTED')
    p1 = d['part1']
    # local reflow loses to raw centroids on real 64D embeddings
    assert d['add_vs_control_old_delta'] < 0.0
    assert p1['ADD']['old_route'] < p1['CONTROL']['old_route']
    # MIX collapses (gauge freedom: never mix frames)
    assert p1['MIX']['old_route'] < 0.2
    assert p1['MIX']['all_route'] < p1['CONTROL']['all_route']
    # tether not dimension-independent: mu0=0.12 over-drifts vs CONTROL
    p2 = d['part2']
    assert p2['mu0_sweep'][0]['drift'] > p2['control']['old_route'] * 0.4
    # no mu0 beats CONTROL on all-routing
    for row in p2['mu0_sweep']:
        assert row['all_route'] <= p2['control']['all_route'] + 1e-9


def test_decentral_net_ceiling_supported():
    d = load('decentral_net_ceiling_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    rows = {r['n']: r for r in d['n_sweep']}
    # scaling is superlinear: ms/step grows much faster than n
    assert rows[20000]['ms_per_step'] > rows[5000]['ms_per_step'] * 5
    assert rows[5000]['ms_per_step'] > rows[1000]['ms_per_step'] * 5
    # peak working set at 20k blew past the D-array estimate (3.2 GB)
    assert rows[20000]['peak_ws_mb'] > 5000
    # measured ceiling 20k, RAM wall confirmed
    assert d['measured_ceiling_n'] == 20000
    assert d['peak_ws_at_20000_gb'] > 15.0


def test_decentral_net_t67_supported():
    d = load('decentral_net_t67_data.json')
    c = d['correctness']
    assert c['verdict'] == 'PASS'
    assert all(c[k] for k in ('grid2d_flow_bit_identical',
                              'tree64d_flow_bit_identical', 'spacing_equal',
                              'predict_equal', 'grid_knn_equals_bruteforce'))
    s = d['scaling']
    # indexed flow is ~linear where exact is ~n^2
    assert s['indexed_exponent'] < 1.4
    assert s['exact_exponent'] > 1.7
    # indexed wins decisively at n=8000
    assert s['indexed_ms_per_step']['8000'] < \
        s['exact_ms_per_step']['8000'] * 0.3
    i = d['internet_scale']
    # n=100k 2D grid flows; the all-pairs D would need 160 GB
    assert i['grid2d_n100k_ms_per_step'] > 0
    assert i['grid2d_allpairs_d_gb'] > 100
    assert i['highdim_real_top1m'] is True
    assert i['highdim_n10k_ms_per_step'] > 0


def test_decentral_net_live_supported():
    d = load('decentral_net_live_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'V1', 'V2', 'V3', 'V4'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    for s in d['seeds']:
        p = d['per_seed'][str(s)]
        # V1: population bounded by CAP under churn
        assert p['bounded_pop'] is True
        assert p['max_n'] <= p['cap']
        # V2: post-damage spacing lands in the healthy band (no clump/blow-up)
        assert p['healed'] is True
        assert 0.05 <= p['spacing_post_damage'] <= 0.9
        # V3: routing probe accurate through churn
        assert p['probe_acc'] > 0.8
        assert p['n_damage_events'] > 3
    # V4: checkpoint/resume reproduces the uninterrupted trajectory
    assert d['resume_continuity']['continuity'] is True
    assert d['resume_continuity']['pos_identical'] is True


def test_bazaar_hybrid_supported():
    d = load('bazaar_hybrid_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'C1', 'C2', 'C3', 'C4', 'C5', 'C6'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    # C1: hybrid burial threshold strictly above reddit's (seed 42)
    c1 = d['C1_brigade']['42']
    assert c1['hybrid_S50'] > c1['reddit_S50']
    # C2: hybrid top-K spam fraction well below reddit's on every seed
    for s in d['seeds']:
        assert d['C2_spam'][str(s)]['hybrid_topk_spam_frac'] < 0.1
        assert d['C2_spam'][str(s)]['reddit_topk_spam_frac'] > 0.3
    # C3: minority users see mostly their own community on the mesh feed
    for s in d['seeds']:
        assert d['C3_feed'][str(s)][
            'hybrid_minority_share_in_minority_feed'] > 0.8
    # C4: archive survives 50% node loss, tamper detected
    for s in d['seeds']:
        assert d['C4_archive'][str(s)]['retrieval_after_50pct_loss'] > 0.99
        assert d['C4_archive'][str(s)]['tamper_detected'] is True
    # C5: quorum wrong-removal collapses below central at p=0.20
    c5 = d['C5_moderation']['rows'][2]
    assert c5['quorum_wrong_removal'] < c5['central_wrong_removal'] / 50.0
    # C6: verified-vote-only raises the suspension threshold and collapses
    # quorum corruption far below the anonymous-hybrid baseline
    for s in d['seeds']:
        c6 = d['C6_verified_vote'][str(s)]
        assert c6['verified_S50'] > c6['anon_S50'] * 10
        assert c6['quorum_wrong_removal_verified_at_p020'] < \
            c6['quorum_wrong_removal_anon_at_p020'] / 100.0


def test_bazaar_net_supported():
    d = load('bazaar_net_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'N1', 'N2', 'N3a', 'N3b', 'N3c', 'N4', 'N5'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    for s in d['seeds']:
        p = d['per_seed'][str(s)]
        # N1: one chain head, one length, every archive verifies, cross-node
        # search finds the content
        assert p['heads_set_size'] == 1
        assert len(p['lengths']) == 1
        assert p['verify_all'] is True
        assert p['search_hits'] > 0
        # N2: emergent mesh feed dominated by the minority's own authors
        assert p['minor_share'] >= 0.6
        # N3a: sockpuppet below the standing gate; good post NOT removed
        assert p['sock_standing'] < 0.5
        assert p['good_removed'] is False
        # N3b: spam removed through the guardian quorum
        assert p['spam_removed'] is True
        # N3c: fabricated brigade on a standing author's post rejected
        assert p['g3_standing'] >= 0.7
        # N5: content survives a node kill; stateless restart resyncs to a
        # bit-identical verifying chain
        assert p['survived_search_count'] > 0
        assert p['resynced'] is True
        assert p['resynced_equal'] is True
        assert p['snap3_verify'] is True
    # N4: tamper-evidence - flipped payload breaks verify at its sequence
    # while the other node's archive stays valid
    assert d['tamper']['tamper_detected'] is True
    assert d['tamper']['other_node_still_valid'] is True


def test_decentral_net_t72_supported():
    d = load('decentral_net_t72_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'T1', 'T2', 'T3'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    fw = d['flow_whole_internet']
    # T1: the whole 1.9M-site internet flows; all-pairs D would be 58 TB
    assert fw['n_sites'] >= 1_900_000
    assert fw['allpairs_d_gb'] > 10_000
    assert fw['ms_per_step'] > 0
    # T2: 20% kill + one local heal recovers consensus spacing
    he = d['heal_whole_internet']
    assert he['killed'] >= 300_000
    assert he['survivors'] >= 1_500_000
    assert he['spacing_after_heal'] > he['spacing_after_kill']
    # T3: high-dim wall measured on a real 10k-site slice
    assert d['highdim_wall']['n'] >= 10_000
    assert d['highdim_wall']['ms_per_step'] > 0


def test_decentral_net_anomaly_supported():
    d = load('decentral_net_anomaly_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'A1', 'A2', 'A3'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    # A1: novelty axis - DGA-shape random strings fall below the legit p5
    # threshold at high rate while known-bad split novel/impersonation
    assert d['novel_share_random'] >= 0.7
    assert d['novel_share_bad'] >= 0.1
    # A2: impersonation axis - a measurable share of known-bad sit above the
    # legit median (near-miss of a real site)
    assert d['impersonation_share_bad'] >= 0.05
    # A3: the honest wall - a large share of known-bad still overlap the legit
    # range (tracking subdomains of real brands), so geometry is
    # necessary-but-not-sufficient
    assert d['legit_n'] >= 1_000_000
    assert d['threshold_legit_p5'] > 0


def test_decentral_net_internet_supported():
    d = load('decentral_net_internet_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'I1', 'I2', 'I3', 'I4'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    # I1: the top-1M real sites are bulk-loaded
    assert d['n_sites'] >= 900_000
    assert d['weights_gb'] > 0
    # I2: routing examples carry real web neighbors
    assert len(d['routing_examples']) > 0
    assert all(h['sim'] > 0.2 for h in d['routing_examples'])
    # I3: a 20% outage leaves the majority still routed
    assert d['survivors'] >= 0.75 * d['n_sites']
    # I4: local flow on a real slice runs and the heal recovers spacing
    assert d['flow_ms_per_step'] > 0
    assert d['spacing_after_heal'] > d['spacing_after_kill']


def test_decentral_net_union_supported():
    d = load('decentral_net_union_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'U1', 'U2', 'U3', 'U4', 'U5'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    # U1: union + dedupe of two real top-1M lists yields ~1.91M unique sites
    assert d['unique_domains'] >= 1_800_000
    # U2: holding is ~2 KB/site - capacity is not the wall
    assert d['weights_gb'] > 0
    # U3: routing works across the merged lists
    assert len(d['routing_examples']) > 0
    assert all(h['sim'] > 0.2 for h in d['routing_examples'])
    # U4: 20% outage leaves the majority routed
    assert d['survivors'] >= 0.75 * d['loaded_n']
    # U5: the persisted checkpoint reloads bit-identically
    assert d['q_identical_on_reload'] is True


def test_decentral_web_supported():
    d = load('decentral_web_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'W1', 'W2', 'W3', 'W4'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    for s in d['seeds']:
        p = d['per_seed'][str(s)]
        # W1: one chain head + one length across all nodes; every archive
        # verifies; all name sets agree; a page publishes on one node and is
        # served (with integrity) from every other node
        assert p['heads_set_size'] == 1
        assert len(p['lengths']) == 1
        assert p['verify_all'] is True
        assert p['names_agree'] is True
        assert p['served_everywhere'] is True
        # W2: identical content dedups to one address (3 publishes, 2 addrs);
        # a GET by address is served directly from the content store
        assert p['dedup_ok'] is True
        assert p['n_addrs'] < 3
        assert p['addr_lookup_ok'] is True
        # W4: a near-miss query resolves to the intended page by n-gram
        # embedding (google.com -> gooogle.com pattern)
        assert p['near_resolves'] is True
        assert p['near_hit'][0]['name'] == 'home'
        assert p['maps_hit'][0]['name'] == 'maps'
        # W3: a crashed node's pages stay served by survivors; a stateless
        # restart resyncs to a bit-identical verifying archive
        assert p['survived_ok'] is True
        assert p['resynced'] is True
        assert p['resynced_equal'] is True
        assert p['resynced_names'] is True
        assert p['snap3_verify'] is True
    # TLS run must pass the same structural gates
    assert d['tls_run']['dedup_ok'] is True
    assert d['tls_run']['resynced_equal'] is True
    assert d['tls_run']['verify_all'] is True
    # tamper-evidence: flipping one byte of a page's content breaks its
    # content-address while the other node's archive stays valid
    assert d['tamper']['tamper_flip_detected'] is True
    assert d['tamper']['other_node_still_valid'] is True


def test_learn_creativity_supported():
    d = load('learn_creativity_test_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'L1', 'L2', 'C1', 'C2', 'C3'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    for s in d['seeds']:
        p = d['per_seed'][str(s)]
        # L1: the curriculum is acquired - probe accuracy climbs from
        # near-chance at minimal exposure to >=0.9 at full exposure
        assert p['floor'] <= 0.35
        assert p['ceiling'] >= 0.90
        assert p['ceiling'] - p['floor'] >= 0.55
        # L2: no forgetting - first-taught concepts keep >=0.85 after every
        # later concept is added
        assert p['no_forgetting_min'] >= 0.85
        # C1: a measurable share of mid-size near-miss variations are
        # simultaneously novel AND valid (never-presented new-but-right items)
        assert p['mid_creative'] >= 0.15
        # C2: random far nulls are novel but not creative, so the joint
        # novelty x validity criterion is necessary
        assert p['null']['novel'] >= 0.90
        assert p['null']['creative'] <= 0.05
        # C3: creative yield is interior-peaked over mutation size (mid size
        # beats too-close and too-far)
        sizes = sorted(p['creative'], key=float)
        assert len(sizes) == 4
        ys = [p['creative'][k]['creative'] for k in sizes]
        assert ys[1] > ys[0] and ys[1] > ys[2] and ys[1] > ys[3]


def test_learn_curve_scale_supported():
    d = load('learn_curve_scale_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'S1', 'S2', 'S3'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    for s in d['seeds']:
        p = d['per_seed'][str(s)]
        # S1: the sparse floor is chance and strictly decreases with C over
        # the well-separated regime C in {2,4,8,16}
        f = [p['floor'][str(c)] for c in (2, 4, 8, 16)]
        assert f[0] >= 0.45 and f[-1] <= 0.12
        assert all(f[i] > f[i + 1] for i in range(len(f) - 1))
        # S2: the acquisition curve exists at every scale - the full-exposure
        # ceiling holds >=0.90 for C in {2,4,8} and the dynamic range grows
        assert min(p['ceiling'][str(c)] for c in (2, 4, 8)) >= 0.90
        assert (p['ceiling']['8'] - p['floor']['8']) - \
            (p['ceiling']['2'] - p['floor']['2']) >= 0.25
        # S3: capacity saturation - the ceiling collapses monotonically once
        # adjacent homes reach a few exemplar-sigma
        cs = [p['ceiling'][str(c)] for c in (8, 16, 24, 32)]
        assert cs[1] < cs[0] - 0.15 and cs[-1] <= 0.50
        assert all(cs[i] > cs[i + 1] for i in range(len(cs) - 1))
        assert p['critical_scale'] <= 10


def test_human_trial_pilot_supported():
    d = load('human_trial_pilot_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'P1', 'P2', 'P3', 'P4'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    for s in d['seeds']:
        p = d['per_seed'][str(s)]
        perf = p['per_archetype']['perfect']
        # P1: a perfect participant attains every engine bar
        assert perf['l1_ok'] is True and perf['l2_ok'] is True
        assert perf['c1_ok'] is True and perf['c2_ok'] is True
        assert perf['c3_ok'] is True
        # P2: a random non-learner fails L1 and C1
        rand = p['per_archetype']['random']
        assert rand['l1_ok'] is False and rand['c1_ok'] is False
        assert rand['l1_ceiling'] <= 0.30
        assert rand['yield']['mid']['creative'] <= 0.06
        # P3: the joint criterion binds on both sides (the human C3)
        y = perf['yield']
        assert y['mid']['creative'] >= 0.15
        assert y['mid']['creative'] > y['trivial']['creative']
        assert y['mid']['creative'] > y['wild']['creative']
        assert y['trivial']['valid'] > y['trivial']['novel']
        assert y['wild']['novel'] > y['wild']['valid']
        assert p['per_archetype']['copycat']['yield']['mid']['creative'] == 0.0
        # P4: the C2 constraint holds on the human scale
        assert p['per_archetype']['perfect']['null']['novel'] >= 0.90
        assert p['per_archetype']['perfect']['null']['creative'] <= 0.05


def test_harvest_energy_slingshot_survivability():
    d = load('harvest_energy_data.json')['slingshot']
    assert d['verdict'].startswith('ANALYTIC')
    # gravity assist is inertial: 0 g by definition
    assert d['G_gravity_assist_g'] == 0.0
    # a = v^2 / r corners at the stated crew tolerances
    assert 62.5 <= d['v_ms_at_4g_vs_arm']['v_ms_at_4g_r100m'] <= 62.7
    assert 1592 <= d['r_km_at_LEO_vs_crew_g']['r_km_at_4g_for_LEO'] <= 1594
    assert 707 <= d['r_km_at_LEO_vs_crew_g']['r_km_at_9g_for_LEO'] <= 709
    # payload-only slingshot clears 3 km/s at 10^4 g on a 100 m arm
    assert d['v_ms_at_1e4g_r100m_payload'] >= 3100
    # the true slingshot: flyby bend/boost, and the passenger load a_p = mu/r_p^2
    fb = d['flyby_mechanics']
    assert 87 <= fb['earth_low']['bend_deg'] <= 89
    assert 6800 <= fb['earth_low']['dv_ms'] <= 7100
    assert 0.80 <= fb['earth_low']['a_periapsis_g'] <= 0.85
    assert fb['jupiter_cloudtops']['a_periapsis_g'] <= 2.6
    assert fb['jupiter_cloudtops']['dv_ms'] >= 9500


def test_harvest_energy_release_coverage_covers_the_3d_ball():
    d = load('harvest_energy_data.json')['release_coverage']
    assert d['verdict'].startswith('ANALYTIC')
    # v_max = sqrt(G g r): 4 g, 100 m arm
    assert 62.5 <= d['v_max_ms'] <= 62.8
    # speed knob: release earlier at radius r' < r gives v' = v_max * r'/r
    assert 31.2 <= d['speed_knob_examples_ms']['r50m'] <= 31.4
    # direction: plane normal (2 DOF) + release phase (1 DOF) = 3, against a
    # 2-DOF target sphere -> every direction reachable, 1 redundant DOF
    assert d['mechanism_degrees_of_freedom'] == 3
    assert d['target_set_degrees_of_freedom'] == 2
    assert d['redundancy_degrees'] == 1
    # every sample target lies in its chosen release plane
    for s in d['sample_targets']:
        assert s['in_plane'] is True
    assert d['cadence_bound']['period_s_per_rev'] >= 10.0


def test_harvest_energy_terraform_budget_and_sustain_wall():
    d = load('harvest_energy_data.json')['terraform']
    assert d['verdict'].startswith('ANALYTIC')
    # Q = m c_p dT + M L + rho d A c_s dT
    assert 2.4e22 <= d['q_total_J'] <= 2.5e22
    assert 40.5 <= d['earth_annual_equivalents'] <= 41.0
    # P = sigma (T^4 - T0^4) A: the sustaining wall, not the one-time warm
    assert 40.4 <= d['p_sustain_PW'] <= 40.6
    assert 279 <= d['f_req_W_m2'] <= 281


def test_harvest_energy_disaster_capture_is_duty_cycle_bound():
    d = load('harvest_energy_data.json')['disasters']
    assert d['verdict'].startswith('ANALYTIC')
    # log10 E = 1.5 M_w + 4.8
    assert 1.9e18 <= d['quake_E_J_GR']['M9.0'] <= 2.1e18
    # Betz wind and tsunami closed forms
    assert 7.9e8 <= d['turbine_W_at_50ms'] <= 8.1e8
    assert 1.0e15 <= d['tsunami_E_J_H1m'] <= 1.1e15
    # an M7's 1% capture, once per 50 years: kilowatts, not a grid
    assert 12000 <= d['m7_capture1pc_annualized_W'] <= 13000


def test_harvest_energy_vibration_feeds_sensors_not_grids():
    d = load('harvest_energy_data.json')['vibration']
    assert d['verdict'].startswith('ANALYTIC')
    # P = m w^3 Y^2 / (4 zeta)
    assert 3.0e-6 <= d['P_ambient_W'] <= 3.2e-6
    assert 65000 <= d['P_TMD_660t_W'] <= 66000
    assert 1.8 <= d['E_TMD_per_event_kWh'] <= 1.9
    assert 0.012 <= d['P_strong_ground_W'] <= 0.013


def test_harvest_energy_forest_wall_and_fire_path():
    d = load('harvest_energy_data.json')['forest']
    assert d['verdict'].startswith('ANALYTIC')
    # a hectare at 150 W/m^2 mean: ~1.5 MW in, ~0.6% stored
    assert d['solar_W_per_ha'] == 1.5e6
    assert d['NPP_J_per_ha_yr'] == 2.7e11
    assert 0.005 < d['photosynthesis_efficiency'] < 0.006
    # 100 km^2 crown fire at 10 kg/m^2 and 18 MJ/kg
    assert d['fire_J_100km2'] == 1.8e16
    assert 4.2 <= d['fire_Mt_TNT'] <= 4.4


def test_harvest_energy_clouds_are_a_store_not_a_tap():
    d = load('harvest_energy_data.json')['clouds']
    assert d['verdict'].startswith('ANALYTIC')
    # M = LWC V
    assert d['cloud_tonnes_10km3'] == 10000.0
    assert d['cloud_tonnes_100km3'] == 100000.0
    # Q = eta A v LWC at the ground; seeding rearranges, it does not create
    assert 15.4 <= d['fog_L_per_m2_day'] <= 15.7
    assert 620 <= d['fog_L_per_day_40m2'] <= 624
    assert d['seed_rain_m3_per_km2'] == 1.0e3


def test_space_spin_reaction_wheel_momentum_exchange():
    d = load('space_spin_data.json')['momentum_exchange']
    assert d['verdict'].startswith('ANALYTIC')
    # H_w = I_w omega_w;  I_s Omega_s = H_w
    assert d['H_cap_total_Nms'] == 500.0
    assert 124 <= d['H_per_wheel_Nms'] <= 126
    assert 125.0 <= d['H_used_published_90deg_Nms'] <= 140.0
    assert 0.25 <= d['H_used_frac_of_capacity'] <= 0.30
    # wheel sizing: (1/2) m r^2 disk at ~850 rpm
    assert 840 <= d['wheel_spin_rpm'] <= 860


def test_space_spin_cmg_torque_amplifier_matches_hardware():
    d = load('space_spin_data.json')['cmg']
    assert d['verdict'].startswith('ANALYTIC')
    # tau = h omega_g reproduces the published testbed rating: 768 mNm
    assert d['cmg_testbed']['match_mNm'] == 768
    # 4-unit pyramid of testbed modules on a 33.3 kg m^2 small sat
    p = d['small_sat_pyramid']
    assert 53.5 <= p['skew_deg'] <= 55.0          # arcsin(sqrt(2/3)) = 54.73
    assert 11.5 <= p['omega_s_max_deg_s'] <= 12.5
    # ISS CMG momentum capacity
    assert d['iss_cmg']['h_each_Nms'] == 4760.0


def test_space_spin_tennis_racket_intermediate_axis_flips():
    d = load('space_spin_data.json')['spin_stability']
    assert d['verdict'].startswith('ANALYTIC')
    # (I_k - I_i)(I_k - I_j): positive on minor/major, negative on intermediate
    st = d['stability']
    assert st['x(minor)']['stable'] is True
    assert st['y(major)']['stable'] is True
    assert st['z(intermediate)']['stable'] is False
    assert d['example_flip_axis'] == 'z(intermediate)'
    # order: minor < intermediate < major
    assert d['ranked_axes'] == ['x(minor)', 'z(intermediate)', 'y(major)']


def test_space_spin_momentum_envelope_worst_direction():
    d = load('space_spin_data.json')['three_axis']
    assert d['verdict'].startswith('ANALYTIC')
    # max|H| = h * sum|u.a_i|: worst direction for 3 orthogonal is the body
    # diagonal sqrt(3) h; 4-wheel pyramid min radius maximized at
    # 4 sin(eta) = 2 cos(eta), eta = atan(1/2) = 26.565 deg, giving 4/sqrt(5) h.
    assert 1.72 <= d['three_orthogonal']['worst_momentum_x_h'] <= 1.74
    assert 26.0 <= d['four_wheel_pyramid']['optimum_elevation_deg'] <= 27.0
    assert 1.78 <= d['four_wheel_pyramid']['worst_momentum_x_h'] <= 1.80
    # 4th wheel's function is redundancy: +3.3% envelope, rank-3 survival
    assert 1.02 <= d['gain_vs_three'] <= 1.04
    assert 'failure' in d['redundancy'].lower()


def test_connes_letter():
    d = load('connes_letter_data.json')
    assert d['verdict'].startswith('CONNES LETTER NOT REPRODUCED')
    # convention finding: the identity closes with the digamma archimedean
    # term (machine precision) but NOT with the paper's printed eq(11)
    wh = d['local_term_check']['w_half']
    assert wh['residual_digamma'] < 1e-6
    assert wh['residual_paper11'] > 0.1
    assert math.isclose(wh['lhs'], 2.63333124, abs_tol=1e-5)
    assert math.isclose(wh['W_R_digamma'], 2.14210523, abs_tol=1e-4)
    assert math.isclose(wh['W_R_paper11'], 2.71172333, abs_tol=1e-4)
    # corrected form is NOT diagonal in the trig basis (W_p is, W_R is not)
    td = d['trig_diagonality']
    assert td['max_offdiag_ratio'] > 0.01
    assert td['Wp_offdiag_max'] < 1e-12
    assert td['WR_offdiag_max'] > 0.1
    # independent Chebyshev slices find no real zeros at all
    for key in ('M10', 'M10e', 'M20', 'M20e', 'M30', 'M30e'):
        assert d['slices'][key]['n_found'] == 0
    # the letter's own trig truncation: even ground state, all zeros real
    ts = d['trig_slices']['N100']
    assert ts['even_weight'] > 0.999
    assert ts['n_zeros'] >= 60
    assert ts['n_zeta_zeros_checked'] == 50
    # ...but the zeros lie on a 2*pi/L quasi-lattice, NOT at the zeta
    # ordinates: only a handful match, and never near the claimed precision
    assert ts['n_matched_tight'] < 5
    assert ts['med_err'] > 0.5
    tb = d['trig_best']
    assert tb['N'] == 150
    assert tb['n_matched'] > 5
    assert tb['med_err'] > 0.5
    # explicit formula: identity closes on smooth tests (local check above);
    # ground-state zero sums converge slowly in K (tail of |fhat|^2)
    cheb_res = d['explicit_formula']['residual_cheb_vs_K']
    assert cheb_res[-1][1] < cheb_res[0][1]
    # honest wall: numerical non-reproduction is NOT a disproof of RH
    assert 'proves RH' not in d['verdict'] or 'does not disprove' in d['verdict']
    assert 'de Bruijn-Newman' in d['verdict']


def test_connes_dirac():
    d = load('connes_dirac_data.json')
    v = d['verdict']
    assert v.startswith('FOOTNOTE-14 STRUCTURE CONFIRMED, CLAIM IMPOSSIBLE')
    # the exact decomposition fhat(z) = 4 z sin(zL/2) R(z) is verified to
    # machine precision: the zeros are exactly {2 pi m/L : |m| > N} union
    # {roots of R}, where R is the rank-one secular function
    assert d['construction']['decomposition_verified_rel'] < 1e-9
    assert d['construction']['N_letter'] == 100
    # the interlacing pins the FIRST eigenvalue into (0, w_1] = (0, 2.45]:
    # gamma_1 = 14.1347 is 5.77 w_1 away, so the letter's first-zero match
    # is categorically impossible
    rs = d['rank_one_spectrum']
    assert math.isclose(rs['first_eigenvalue_r1'], 1.025847, abs_tol=1e-4)
    assert math.isclose(rs['gamma_1'], 14.134725, abs_tol=1e-5)
    assert rs['gamma_1_in_lattice_units'] > 5.0
    assert rs['impossible_first_zero'] is True
    inter = rs['interlacing']
    assert inter['n_roots'] >= 60
    assert inter['in_own_gap'] == inter['n_roots']
    assert inter['gaps_with_one_root'] >= 60
    # elsewhere the rank-one roots miss the ordinates (as the direct trig
    # computation already showed): median offset > 0.5, few tight hits
    m = d['matching']
    assert m['med_err'] > 0.5
    assert m['n_matched'] < 20
    assert m['n_matched_tight'] < 5
    # the lattice part of the zero set is EXACT at N=50: 2 pi m/L with m > N
    lc = d['lattice_check_N50']
    assert lc['first_lattice_index_m'] == 51
    assert math.isclose(lc['first_lattice_position'], 124.9313, abs_tol=1e-3)
    assert lc['n_lattice_zeros'] >= 10
    assert lc['max_fhat_on_lattice'] < 1e-12
    # C_0 cannot participate: scalar of an unrelated system, no trace formula
    assert d['C0_asset']['role'] == 'none'
    # honest wall
    assert 'HONEST WALL' in v
    assert 'speaks to RH' in v or 'C_0' in d['C0_asset']['reason']


def test_four_point_lattice():
    d = load('four_point_lattice_data.json')
    assert d['digit_multiset'] == '0,0,0,0,1,2,2,6'
    assert d['anchors'] == [10262000, 20001026, 20002610, 26102000]
    # arithmetic: gcd = 2, so the four anchors span the full even lattice 2Z
    assert d['arithmetic']['gcd_of_all_four'] == 2
    assert d['arithmetic']['lattice_spanned'].startswith('2*Z')
    # block structure: 1026|2000, 2000|1026, 2000|2610, 2610|2000; the
    # 1584 step closes the 4-point cycle (2610 - 1026 = 20002610 - 20001026)
    bs = d['block_structure']
    assert bs['blocks'] == ['1026', '2000', '2610']
    assert bs['splits']['10262000'] == ['1026', '2000']
    assert bs['splits']['26102000'] == ['2610', '2000']
    assert bs['step_1584']['2610_minus_1026'] == 1584
    assert bs['step_1584']['gap_20002610_minus_20001026'] == 1584
    # full orbit: 840 points, none divisible by 3 (digit sum 11), clusters
    o = d['full_orbit']
    assert o['n'] == 840
    assert o['min'] == 1226
    assert o['max'] == 62210000
    assert o['count_divisible_by_3'] == 0
    assert o['leading_digit_clusters']['1']['count'] == 210
    assert o['leading_digit_clusters']['2']['count'] == 420
    assert o['leading_digit_clusters']['6']['count'] == 210
    assert o['anchors_rank'] == {'10262000': 470, '20001026': 532,
                                 '20002610': 543, '26102000': 729}
    # permutohedron: diameter 16, empty shell at distance 14, and the
    # vertex-transitive shells are identical from every anchor
    p = d['permutohedron']
    assert p['diameter'] == 16
    assert '14' not in p['spheres']['10262000']['sphere_sizes']
    sizes0 = p['spheres']['10262000']['sphere_sizes']
    for a in ('20001026', '20002610', '26102000'):
        assert p['spheres'][a]['sphere_sizes'] == sizes0
    assert p['spheres']['10262000']['cumulative_circles']['16'] == 840
    # honest wall: finite arithmetic, no mechanism to zeta/RH
    assert 'mechanism' in d['honest_wall'].lower()
    assert 'proof' in d['honest_wall']


def test_zeta_lattice_alignment():
    d = load('zeta_lattice_alignment_data.json')
    v = d['verdict']
    assert v.startswith('NO ALIGNMENT EXISTS')
    # the ONLY honest spectral test is index-matched: |gamma_k - (o + k s)|;
    # a fixed lattice cannot track the logarithmically-thinning ordinates
    b = d['fixed_lattice_best_fit']
    assert b['med_err'] > 5.0
    assert b['n_matched_tight'] == 0
    assert b['note'].startswith('index-matched')
    # the genuine alignment that exists is the adaptive Weyl/Gram one
    assert d['adaptive_weyl']['residual_mean'] < 1.0
    assert abs(d['adaptive_weyl']['local_vs_adaptive_ratio_mean'] - 1.0) < 0.1
    assert d['gram']['gram_violations'] >= 1
    # the four anchors are inside the random-origin spread: their residues
    # on the 2 pi/L lattice are chance (uniform median = spacing/4 = 0.612)
    ao = d['anchor_origins']
    assert math.isclose(ao['uniform_origin_median_expected'], 0.612,
                        abs_tol=1e-3)
    assert math.isclose(ao['random_origins_median_q'],
                        ao['uniform_origin_median_expected'], abs_tol=0.05)
    for q in ao['anchors_q'].values():
        assert 0.2 < q < 0.8
    # the "99th percentile" anchor is selection noise: only ~2 of 200
    # random origins beat the best anchor -- the expected number
    assert ao['random_origins_n_better_than_best_anchor'] <= 4
    # rescaled anchors collapse to the same spacing regardless of digits
    assert d['rescaled_anchor_spacings']['count_forced_by_density'] == 61
    # the provable negative theorem: interlacing pins the first rank-one
    # eigenvalue into (0, 2.45], so gamma_1 = 14.13 is unreachable
    pr = d['provable']
    assert pr['empirical_check']['first_root_r1'] < 2.0
    assert pr['empirical_check']['gamma_1_over_omega_1'] > 5.0
    assert pr['does_not_bear_on_RH'] is True
    # honest wall
    assert 'HONEST WALL' in v
    assert 'not a proof or disproof of RH' in v or 'RH is open' in v


def test_zeta_direct_probe():
    d = load('zeta_direct_probe_data.json')
    v = d['verdict']
    a1 = d['direct_ordinate_probe']
    a2 = d['all_N_interlacing']
    a3 = d['orbit_origin_census']

    # A1: head-on, high-precision values of the letter's fhat AT the ordinates
    assert a1['N'] == 150
    assert a1['method'].startswith('mpmath')
    r1 = a1['r1']
    assert 0.5 < r1 < 2.5                    # first rank-one eigenvalue
    assert a1['r1_zero_value_abs_fhat'] < 1e-30   # r_1 IS a zero, exactly
    assert 12.0 < a1['positional_error_gamma1_minus_r1'] < 14.0
    # no ordinate is a zero: |fhat(gamma_n)| far above the claimed 2.6e-55
    assert a1['rows'][0]['abs_fhat'] > 1e-4
    assert a1['abs_fhat']['min'] < 1e-3      # but some ordinates come close
    assert a1['abs_fhat']['min'] > 1e-8      # ... never to 1e-7 let alone 1e-55
    assert a1['newton_distance_delta']['median'] > 0.5
    # exact nearest-root distances (the reliable measure)
    exn = a1['exact_nearest_root_distance']
    assert 0.5 < exn['median'] < 1.0
    assert 0.5 < exn['gamma_1_to_root'] < 1.5
    # identity fhat = 4 z sin(zL/2) R(z) holds on all ordinates to the
    # floor set by the double-precision eigenvector coefficients
    assert a1['max_rel_identity_err'] < 1e-10
    # closest ordinate to a zero is gamma_6 (37.586), the tight-match known
    # from the matching statistics
    amin = min(a1['rows'], key=lambda r: r['abs_fhat'])
    assert amin['abs_fhat'] < 1e-4

    # A2: the interlacing theorem at every N in the sweep
    sweep = a2['sweep']
    assert [r['N'] for r in sweep if 'error' not in r] == [50, 100, 150,
                                                           200, 300]
    for r in sweep:
        assert 'error' not in r
        assert r['interlacing_ok'] is True
        assert r['in_own_gap'] == r['n_roots_in_scan']
        assert r['r1_in_omega1_interval'] is True
        assert r['first_root_r1'] < 2.5      # gamma_1 unreachable
        assert r['gamma_1_over_omega_1'] > 5.0
        assert r['min_gap_margin_frac'] > 1e-4
    # N=100 cross-checks the persisted connes_dirac verdict to 1e-14
    cc = a2['cross_check_vs_connes_dirac']
    assert abs(cc['diff']) < 1e-14
    assert cc['connes_dirac_n_roots'] == cc['this_n_roots'] == 62

    # A3: the whole 840-point orbit as origins vs the random extreme value
    assert a3['n_orbit_points'] == 840
    assert 0.3 < a3['best_q'] < 0.5
    assert 0.5 < a3['median_q_over_orbit'] < 0.7
    # the orbit's best origin is exactly the expected extreme-value minimum
    # of 840 random origins: random matches or beats it essentially always
    rex = a3['random_extreme']
    assert abs(rex['min_mean'] - a3['best_q']) < 0.01
    assert rex['frac_random_extreme_leq_orbit_best'] >= 0.9
    # anchors agree with the four-anchor measurement to 4 decimals
    assert abs(a3['anchors_q']['10262000'] - 0.3747) < 1e-3

    # provable negative + honest wall
    pr = d['provable']
    assert pr['does_not_bear_on_RH'] is True
    assert 'impossible' in pr['corollary'].lower()
    assert 'HONEST WALL' in v
    assert 'RH is open' in v


def test_zeta_interlacing_certify():
    d = load('zeta_interlacing_certify_data.json')
    c = d['certified']
    v = d['verdict']

    # the wall is certified at every N in the sweep
    assert [s['N'] for s in d['sweep']] == [100, 150, 200, 246, 247, 300]
    for s in d['sweep']:
        assert s['wall']['certified_impossible_first_zero'] is True
        assert s['first_root']['in_omega1_interval'] is True
        assert s['first_root']['width'] < 1e-20
        assert s['wall']['gamma_1_over_omega_1'] > 5.0

    # exactly one root per gap is certified for every N <= 246
    for s in d['sweep']:
        if s['N'] <= 246:
            assert s['residues']['all_same_sign'] is True
            assert s['gap_existence']['n_certified'] == s['gap_existence']['n_gaps']
            assert s['gap_existence']['failing_gaps'] == []
            # numeric scan confirms the certified uniqueness
            assert s['gap_existence']['interior_scan']['multiplicity_histogram'] \
                == {'1': s['gap_existence']['n_gaps']}
    # the interlacing threshold: first break at N = 247, gap 246 -> 0 roots
    th = d['interlacing_threshold']
    assert th['last_clean_N'] == 246
    assert th['first_break_N'] == 247
    n247 = next(s for s in d['sweep'] if s['N'] == 247)
    assert n247['residues']['all_same_sign'] is False
    assert n247['residues']['sign_flips_at_k'] == [247]
    assert n247['gap_existence']['n_certified'] == 246
    assert n247['gap_existence']['failing_gaps'] == [246]
    assert n247['gap_existence']['interior_scan']['flip_gap_multiplicities'] \
        == {'246': 0}
    assert n247['gap_existence']['interior_scan']['multiplicity_histogram'] \
        == {'0': 1, '1': 246}
    n300 = next(s for s in d['sweep'] if s['N'] == 300)
    assert n300['residues']['all_same_sign'] is False
    assert n300['gap_existence']['failing_gaps'] == [153, 266, 267]
    assert n300['gap_existence']['n_certified'] == 297
    assert n300['residues']['sign_flips_at_k'] == [154, 267, 268]
    # the flip gaps break the one-root rule PRECISELY: 153 keeps two roots
    # (hugging the poles), 266/267 hold none, all other 297 gaps exactly one
    isc = n300['gap_existence']['interior_scan']
    assert isc['multiplicity_histogram'] == {'0': 2, '1': 297, '2': 1}
    assert isc['flip_gap_multiplicities'] == {'153': 2, '266': 0, '267': 0}
    assert isc['total_interior_roots'] == 299
    assert isc['non_flip_gaps_with_mult_not_one'] == []
    r153 = isc['flip_gap_roots']['153']
    assert len(r153) == 2
    assert all(r['dist_to_pole'] < 1e-2 for r in r153)   # pole-hugging
    assert isc['flip_gap_roots']['266'] == []
    assert isc['flip_gap_roots']['267'] == []

    # N=100 headline details: every gap, tight enclosure, wall lower bound
    assert c['N'] == 100
    assert c['gap_existence']['n_certified'] == c['gap_existence']['n_gaps'] == 100
    assert c['residues']['common_sign'] == 1
    assert c['residues']['min_abs_residue'] > 1e-4
    r = c['first_root']
    assert 1.0 < r['enclosure_lo'] <= r['enclosure_hi'] < 2.5
    assert r['newton_mp60_inside_enclosure'] is True
    assert r['newton_diff_from_midpoint'] < 1e-20
    assert c['wall']['abs_fhat_gamma1_lower'] > 1e-3
    assert c['wall']['certified_impossible_first_zero'] is True

    # cross-check: certified root vs the persisted connes_dirac r_1 at the
    # documented float round-off scale of the two matrix assemblies
    cc = d['cross_check']
    assert abs(cc['diff_certified_root_vs_connes_dirac_r1']) < 1e-13

    # provable negative + honest wall
    assert 'impossible' in v.lower()
    assert 'HONEST WALL' in v
    assert 'RH is open' in v
    assert 'NOT a theorem in N' in v


def test_riemann_siegel_ordinate_rederivation():
    d = load('riemann_siegel_ordinate_data.json')
    v = d['verdict']
    fz = d['first_zero']
    rv = d['rvm']

    # the derivation is self-contained: no zetazero / mp.zeta / mp.loggamma
    assert 'no zetazero' in d['claim']
    assert 'Stirling/Binet' in d['setup']['theta']
    assert 'Euler-Maclaurin' in d['setup']['zeta']
    assert d['setup']['count_oracle'].startswith('mpmath.zetazero')

    # gamma_1 pinned to the full 56-digit series string
    assert fz['gamma_1_series'] == \
        '14.13472514173469379045725198356247027078206878633840436'
    assert fz['gamma_1_zetazero_oracle'].startswith(
        '14.134725141734693790457251983562470270784')
    assert float(fz['diff_vs_zetazero']) < 1e-36

    # the chain: Z(0) < 0 < Z(g_0), exactly one sign-change bracket
    assert fz['zeta_half_series'] < 0
    assert fz['Z_g0_series'] > 0
    assert fz['sign_changes_in_0_g0'] == 1

    # series validation passed on every probe point
    assert d['validation']['pass'] is True
    for p in d['validation']['points']:
        assert p['theta_ok'] is True
        assert p['Z_ok'] is True

    # certified-interval bracket (validated regime) encloses gamma_1
    cb = d['certified_bracket']
    assert cb['ok'] is True
    assert cb['signs'] == [-1, 1]
    assert cb['lo'] < 14.1347251417347 < cb['hi']

    # Gram point and Riemann-von Mangoldt closure
    assert d['gram_points']['g0_g1_g2'][0] == 17.84559954041086
    assert rv['N_g0'] == 1
    assert rv['gamma_1_lt_g0_lt_gamma_2'] is True
    assert abs(rv['theta_gamma1_over_pi'] + 0.550252829468691) < 1e-13
    assert abs(rv['S_gamma1'] - 0.550252829468691) < 1e-13
    assert abs(rv['S_gamma1_below'] + 0.449747170531309) < 1e-13
    assert rv['jump_at_simple_zero'] == 1

    # honest wall: a number, not a statement about RH
    assert 'HONEST WALL' in v
    assert 'not a statement about the Riemann hypothesis' in v
    assert 'remains open' in v


def test_s_function_census():
    d = load('s_function_census_data.json')
    v = d['verdict']
    gp = d['gram_points']
    ir = d['interior_S']
    rel = d['relocation']
    res = d['resolution_limit']

    # certified anchors reproduced by the independent three-grid re-location
    assert gp['n'] == 653
    assert rel['n_le_g647'] == 648 == d['setup']['turing_N']
    assert rel['n_le_g652'] == 653
    for grid in ('0.05', '0.01', '0.005'):
        assert rel['grid_counts'][grid] == 654

    # the certified Gram-point statement: S(g_j) in {-1, 0, +1}, max 1
    assert gp['max_abs_S'] == 1 == gp['certified_max_abs_S']
    assert gp['gram_bound_ok'] is True
    assert gp['S_value_histogram'] == {'-1': 13, '0': 631, '1': 9}
    assert gp['nonzero_S_points'] == 22

    # the classical Gram-violation pattern (22 pairs, 22 empty intervals)
    assert rel['per_interval_histograms']['0.005'] == {'0': 22, '1': 609, '2': 22}

    # interior: |S(t)| < 2 throughout, below both theoretical scales
    assert ir['sup'] > 1 and ir['sup'] < 2
    assert ir['inf'] < -1 and ir['inf'] > -2
    assert ir['rh_scale_sqrt_log_over_loglog'] > ir['sqrt_e_floor']
    assert ir['max_abs_S_over_log_T'] < 0.2

    # Littlewood equivalence + resolution limit
    assert 'o(log t)' in d['setup']['littlewood']
    assert d['setup']['unconditional_bound'] == 'S(t) = O(log t) (Backlund/von Mangoldt)'
    t3 = next(r for r in res['table'] if r['k'] == 3)
    t4 = next(r for r in res['table'] if r['k'] == 4)
    assert t3['log10_t'] == 13.405 and t4['log10_t'] == 29.255

    # honest wall: a counterexample engine, not a proof engine
    assert 'HONEST WALL' in v
    assert 'cannot prove RH' in v
    assert 'counterexample engine' in v
    assert 'search for a concise proof ends here' in v


def test_mertens_psi_census():
    d = load('mertens_psi_census_data.json')
    v = d['verdict']
    r = d['records']
    ef = d['explicit_formula']

    # exact sieve: classical Mertens table (OEIS A084237) reproduced
    classic = {1: -1, 2: 1, 3: 2, 4: -23, 5: -48, 6: 212, 7: 1037, 8: 1928}
    for k in range(1, 9):
        row = next(x for x in d['li_vs_pi'] if x['x'] == 10 ** k)
        assert row['M'] == classic[k]
    assert r['M_X'] == classic[8]
    assert r['pi_X'] == 5761455
    assert r['psi_X_minus_X'] < 0
    assert d['setup']['classical_table'].endswith('1928')
    assert d['setup']['mobius_check'].startswith('sympy mobius')

    # pi < Li at every height 1e1..1e8
    for row in d['li_vs_pi']:
        assert row['pi_minus_Li'] < 0

    # records over [1000, 1e8]: ratio never reaches 0.5, RH-normalized O(1)
    assert r['max_abs_M_over_sqrt_x'] < 0.5
    assert r['max_abs_M_over_sqrt_x'] > 0.4
    assert r['argmax'] > 1000
    assert r['first_x_absM_gt_half_sqrt'] is None
    assert r['max_abs_psi_minus_x_over_sqrt_x'] < 1.0
    assert r['max_abs_psi_minus_x_over_sqrt_x_log2x'] < 0.05

    # explicit formula: located-zero counts match the certified anchors
    assert ef['zeros_count']['1005.43'] == 653
    assert ef['zeros_count']['20000'] > 20000

    # residuals shrink as T grows at x = 100
    x100 = next(row for row in ef['rows'] if row['x'] == 100)
    assert abs(x100['1005.43']) > abs(x100['20000'])

    # the two proven-but-never-seen failures + honest wall
    assert 'PROVEN false' in v
    assert 'Odlyzko-te Riele' in v
    assert 'Skewes' in v
    assert 'Bays-Hudson' in v
    assert 'Korobov' in v and 'Vinogradov' in v
    assert 'HONEST WALL' in v
    assert 'remains open' in v
    assert 'counterexample engine' in v
    assert 'proof, if it exists, is not a computation' in v


def test_mertens_sublinear_census():
    d = load('mertens_sublinear_census_data.json')
    v = d['verdict']
    ex = d['exact']
    r = ex['records']
    sub = d['sublinear']

    # exact sieve to 1e10: OEIS A084237 reproduced for k = 1..10
    oeis = {1: -1, 2: 1, 3: 2, 4: -23, 5: -48, 6: 212,
            7: 1037, 8: 1928, 9: -222, 10: -33722}
    assert ex['M_X'] == oeis[10]
    assert ex['M_powers'] == {str(k): oeis[k] for k in oeis}

    # the new finding: the first |M(x)|/sqrt(x) > 0.5 excursion at height
    assert r['max_abs_M_over_sqrt_x'] > 0.5
    assert r['argmax'] > 7e9 and r['argmax'] <= 1e10
    fc = r['first_x_absM_gt_half_sqrt']
    assert fc[0] > 7e9 and fc[0] <= 1e10
    assert fc[1] > 0
    assert fc[0] <= r['argmax']

    # recursion self-check + sublinear targets through 1e14 (OEIS A084237,
    # the published M(10^n) table n = 1..14 now complete)
    assert d['setup']['self_check'] == {'M_1e5': -48, 'M_1e6': 212}
    assert sub['100000000000'] == -87856
    assert sub['1000000000000'] == 62366
    assert sub['10000000000000'] == 599582
    assert sub['100000000000000'] == -875575
    assert d['setup']['oeis'] == 'A084237 (M(10^n))'

    # quotient-point scan over x = floor(N/i) > 1e10: exact sampled values
    s = d['sampled']
    assert s['X_min'] == 1e10
    assert s['n_points'] > 10000
    assert s['argmax'] > 1e10 and s['max_abs_M_over_sqrt_x'] < r['max_abs_M_over_sqrt_x']
    assert all(x > 1e10 and Mv > 0 for x, Mv in s['crossings_gt_half_sqrt'])
    assert s['crossings_gt_half_sqrt'] == [[108813928182, 169281],
                                           [108932461873, 165817]]

    # proven-but-never-seen Mertens failure + honest wall
    assert 'PROVEN false' in v
    assert 'Odlyzko-te Riele' in v
    assert 'Pintz' in v
    assert 'O(x^(1/2+eps))' in v
    assert 'Littlewood' in d['setup']['equivalence']
    assert '7725038629' in v
    assert '875575' in v and 'n = 1..14' in v
    assert 'HONEST WALL' in v
    assert 'remains open' in v
    assert 'counterexample' in v


def test_mertens_explicit_height():
    d = load('mertens_explicit_height_data.json')
    v = d['verdict']
    rows = {r['x']: r for r in d['rows']}

    # truth checkpoints: classical table + the sublinear census heights
    assert d['setup']['truncations'] == {
        '1005.43': 653, '5000': 4520, '10000': 10142, '20000': 22491}
    assert rows[100]['truth'] == 1 and rows[1000]['truth'] == 2
    assert rows[10 ** 11]['truth'] == -87856
    assert rows[10 ** 12]['truth'] == 62366
    assert rows[10 ** 13]['truth'] == 599582
    assert rows[10 ** 14]['truth'] == -875575

    # the T = 20000 formula recovers ~98% of M(1e14): residual 15422.5651
    assert abs(rows[10 ** 14]['res_20000']) < 20000.0
    assert abs(rows[10 ** 14]['res_20000']) / 875575.0 < 0.03
    assert abs(rows[10 ** 11]['res_20000']) < 1500.0
    assert abs(rows[100]['res_20000']) < 0.01
    assert abs(rows[1000]['res_20000']) < 0.02

    # small x is essentially exact (truncation error tiny at x = 100/1000)
    assert all(abs(rows[x]['res_1005.43']) > abs(rows[x]['res_20000'])
               for x in (100, 1000))

    # the honest face of the height: residuals are NON-monotone in T
    # (conditional convergence): at x = 1e12, T = 20000 is worse than
    # T = 10000 (res_20000 = +1849.61 vs res_10000 = -60.94)
    assert 'NON-monotone' in v
    assert rows[10 ** 12]['res_20000'] > 0
    assert rows[10 ** 12]['res_10000'] < 0
    assert abs(rows[10 ** 12]['res_20000']) > abs(rows[10 ** 12]['res_10000'])

    # the empirical tail bound E_T is a gross worst case, not a predictor:
    # at x = 1e12, E = 1525213 at T = 1005.43 vs a residual ~1e3 (1000x)
    assert rows[10 ** 12]['tail_1005.43'] > 1e6
    assert abs(rows[10 ** 12]['res_1005.43']) < 1e4

    # honest wall: no finite T certifies M(x); RH remains open
    assert 'conditional' in v.lower()
    assert 'proof of RH' in v


def test_mertens_psi_height():
    d = load('mertens_psi_height_data.json')
    v = d['verdict']
    rows = {r['x']: r for r in d['rows']}
    sub = d['sublinear']

    # same located set as the M experiment, sliced per truncation
    assert d['setup']['truncations'] == {
        '1005.43': 653, '5000': 4520, '10000': 10142, '20000': 22491}

    # the exact-truth identity validated at the census anchors
    for t in d['truth_checks']:
        assert abs(t['psi_identity'] - t['expected']) < 1e-4
    assert rows[10 ** 8]['truth'] == 99998242.7966
    assert rows[100]['truth'] == 94.0453 and rows[1000]['truth'] == 996.6809

    # sublinear M reproduced exactly (OEIS A084237 n = 11..14)
    assert sub == {'100000000000': -87856, '1000000000000': 62366,
                   '10000000000000': 599582, '100000000000000': -875575}

    # exact psi at height: psi(x) - x is a small fraction of sqrt(x)
    # (observed max ratio 0.185 at x = 1e11)
    for x in (10 ** 11, 10 ** 12, 10 ** 13, 10 ** 14):
        assert abs(rows[x]['truth'] - x) < 0.5 * x ** 0.5

    # the T = 20000 psi residual is LARGER than M's at every height
    mf = d['m_formula_contrast']
    for k, vals in mf.items():
        x = int(k)
        assert abs(rows[x]['res_20000']) > abs(vals['20000'])

    # small x essentially exact (reproduces the 5.21o census residuals:
    # x = 100 -> -0.0057, x = 1000 -> +0.0345 at T = 20000)
    assert abs(rows[100]['res_20000']) < 0.01
    assert abs(rows[1000]['res_20000']) < 0.04

    # conditional convergence: NON-monotone walk in T (1e14: T = 20000 is
    # worse than T = 10000's -80364)
    assert 'NON-monotone' in v
    assert abs(rows[10 ** 14]['res_20000']) > abs(rows[10 ** 14]['res_10000'])

    # no tail bound for psi: the located-tail magnitude is context ~700x
    # the observed residual, and (unlike M's E_T) has no finite total
    assert rows[10 ** 14]['tailmag_1005.43'] > 1e7
    assert abs(rows[10 ** 14]['res_20000']) \
        < rows[10 ** 14]['tailmag_1005.43'] / 100
    assert 'no finite total' in v

    # honest wall: psi series only conditionally convergent; RH open
    assert 'conditional' in v.lower()
    assert 'proof of RH' in v


def test_body_fold_symmetry():
    d = load('body_fold_symmetry_data.json')
    v = d['verdict']

    # the fold is EXACT: D(x) = U + L with L = U - d^2 (commutativity),
    # verified by the persisted identity at every height up to 10^14
    for row in d['fold']:
        assert row['D'] == row['U'] + row['L']
        assert row['L'] == row['U'] - row['diag'] ** 2
        assert 0.0 < row['arm_ratio_L_over_U'] < 1.0
        # certifiably satisfies the proven Voronoi O(x^(1/3) log x) bound
        assert row['Delta_over_x13_logx'] < 1.0

    # the breaking Delta(x) = D - (x log x + (2g-1)x) is tiny vs D once the
    # main term dominates (x >= 1e8) and never certified at x^(1/4)
    for row in d['fold']:
        if row['x'] >= 10 ** 8:
            assert abs(row['Delta_over_D']) < 1e-6
        assert abs(row['Delta_over_x14']) < 10.0

    # mu * 1 = delta fold identity: sum mu(d) floor(x/d) = 1, exact
    assert d['identities']['mu_conv_delta_sum'] == 1

    # branch growth is LINEAR, not golden: tau(2^k) = k + 1
    assert d['cells']['branch_growth_tau2k_linear_not_golden']['tau(2^19)'] == 20
    assert d['cells']['max_tau'] == 240 and d['cells']['argmax_tau'] == 720720

    # regular tree mirror is a tautology; integer tree mirror BREAKS (the
    # measured upper/lower asymmetry is the breaking, ratios not all 1)
    mm = d['tree']['mirror_medians']
    assert len(set(mm.values())) > 1

    # honest wall: nothing here touches RH; the body mapping is not committed
    assert 'proof of RH' not in v or 'does not commit' in v['claim'].lower()


def test_zeta_zero_spectral_match():
    d = load('zeta_zero_spectral_match_data.json')
    v = d['verdict']

    # the 22,491 located zeros are GUE-like at the spacing-statistics level
    nnsd = d['nnsd']
    assert nnsd['ks_to_GUE'] < 0.05
    assert nnsd['ks_to_GUE_simulated'] < 0.05
    assert nnsd['ks_to_Poisson'] > 0.20
    assert nnsd['ks_to_GOE'] > nnsd['ks_to_GUE']
    assert 1.0 < nnsd['level_repulsion_beta'] < 2.0

    # determinantal (not white-noise) process in log-time: anticorrelated gaps
    assert d['time_reading']['normalized_gap_lag1_autocorr'] < -0.2
    assert d['references']['Poisson_sim']['lag1_autocorr'] > -0.1

    # number variance far below Poisson (rigid), close to the GUE ensemble
    nv = d['number_variance']['L=1.0']
    assert nv < 0.6
    assert nv < d['number_variance_Poisson_simulated']['L=1.0'] / 2

    # the repo's own spectra do NOT resemble the zeros: spectral_extended is
    # Poisson (integrable), its KS-to-GUE > KS-to-Poisson
    se = d['repo_spectra']['spectral_extended_eigenvalues']['spacing_stats']
    assert se['ks_to_GUE'] > se['ks_to_Poisson']

    # honest wall: GUE resemblance is conjectural (Montgomery), RH open
    assert 'proof of RH' in v['honest_wall']
    assert 'remains open' in v['honest_wall']


def test_grh_dirichlet_0_over_0():
    d = load('grh_dirichlet_0_over_0_data.json')
    assert d['verdict'] == 'SUPPORTED'
    # Gauss sums correct: |G(chi)| = sqrt(conductor) for all Legendre symbols
    assert d['all_gauss_sums_correct']
    # Root numbers are 1
    assert d['all_root_numbers_one']
    # g_chi = 1 on critical line for all characters
    assert d['all_g_chi_equal_one']
    assert d['n_characters_tested'] >= 8
    # Honest wall present
    assert 'GRH' in d['honest_wall']


def test_abc_conjecture_0_over_0():
    d = load('abc_conjecture_0_over_0_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    r = d['results']
    # The classical record triple is found
    rec = r['record']
    assert rec['quality'] > 1.6
    assert rec['quality_gt_1']
    assert rec['quality_gt_1.5']
    # The 0/0 at the unit triple (1,1,1)
    z = r['zero_over_zero']
    assert z['unit_quality'] == 1.0
    assert '0/0' in z['note']
    # Enough triples scanned
    assert r['small_N']['n_triples'] + r['medium_N']['n_triples'] > 30000


def test_poincare_hopf_0_over_0():
    d = load('poincare_hopf_0_over_0_data.json')
    assert d['verdict'] == 'SUPPORTED'
    r = d['results']
    # Euler characteristic of S^2 is 2
    ec = r['euler_characteristic']['S^2']
    assert ec['chi'] == 2
    assert ec['match']
    # Two vices on S^2 both have index 1, sum = 2
    s2 = r['s2_two_zeros']
    assert s2['sum'] == 2
    assert s2['chi_S2'] == 2
    assert s2['match']
    # Removable value convergence: index converges to 1 as contour shrinks
    conv = r['removable_value_convergence']['contour_tests']
    for epsilon, data in conv.items():
        assert data['index'] == 1


def test_riemann_roch_0_over_0():
    d = load('riemann_roch_0_over_0_data.json')
    assert d['verdict'] == 'SUPPORTED'
    r = d['results']
    # All Riemann-Roch identities hold for g=1,2,3,4,5
    assert r['elliptic_g1']['all_hold']
    assert r['genus_2']['all_hold']
    for g in [3, 4, 5]:
        assert r[f'genus_{g}']['all_hold']
    # The 0/0 at deg(D) = g-1: l(D) - l(K-D) = 0 for all genera
    z = r['zero_over_zero']['tests']
    for t in z:
        assert t['difference'] == 0
    # Canonical divisor: l(K) = g
    for t in r['canonical_divisor']['tests']:
        assert t['l_K_equals_g']
        assert t['deg_K_equals_2g_minus_2']


def test_bsd_0_over_0():
    d = load('bsd_0_over_0_data.json')
    assert d['verdict'] == 'SUPPORTED'
    c = d['curves']
    # Rank 0 curves: L(1+eps) stabilizes (ratio > 0.8, value > 0.3)
    for name in ['y^2=x^3-x', 'y^2=x^3+1']:
        assert c[name]['is_rank0_stable']
    # Rank 1 curve: L(1+eps) shrinks to 0 (ratio < 0.8, value < 0.2)
    assert c['y^2=x^3-25x']['is_rank1_shrinking']
    # The 0/0 structure: rank 0 nonzero, rank 1 approaches 0
    assert c['y^2=x^3-x']['L_at_eps']['0.01'] > 0.3
    assert c['y^2=x^3-25x']['L_at_eps']['0.01'] < 0.2


def test_argument_principle_0_over_0():
    d = load('argument_principle_0_over_0_data.json')
    assert d['verdict'] == 'SUPPORTED'
    r = d['results']
    # Each rectangle gives the correct zero count
    assert r['first_zero_only']['computed_count'] == 1.0
    assert r['first_two_zeros']['computed_count'] == 2.0
    assert r['first_four_zeros']['computed_count'] == 4.0
    assert r['no_zeros']['computed_count'] == 0.0
    assert r['wide_eight_zeros']['computed_count'] == 8.0


def test_atiyah_singer_0_over_0():
    d = load('atiyah_singer_0_over_0_data.json')
    assert d['verdict'] == 'SUPPORTED'
    r = d['results']
    # S^2: chi = 2, index = chi
    assert r['S^2']['chi_correct']
    assert r['S^2']['index_matches_chi']
    assert r['S^2']['V-E+F'] == 2
    # T^2: chi = 0, index = chi
    assert r['T^2']['chi_correct']
    assert r['T^2']['index_matches_chi']
    assert r['T^2']['V-E+F'] == 0


def test_gradient_descent_0_over_0():
    d = load('gradient_descent_0_over_0_data.json')
    assert d['verdict'] == 'SUPPORTED'
    r = d['results']
    # Origin is a saddle point
    assert r['saddle_origin']['is_saddle']
    assert r['saddle_origin']['gradient_is_zero']
    assert r['saddle_origin']['L_value'] == 0.0
    # Hessian has mixed signs (+2, -2)
    ev = r['saddle_origin']['hessian_eigenvalues']
    assert any(e > 0 for e in ev) and any(e < 0 for e in ev)
    # Newton method escapes the saddle
    assert r['newton_escape']['converged_to_minimum']
    # High-dimensional saddle
    assert r['high_dim_saddle']['is_saddle']
    assert r['high_dim_saddle']['n_positive_eigenvalues'] == 5
    assert r['high_dim_saddle']['n_negative_eigenvalues'] == 5


def test_selberg_trace_0_over_0():
    d = load('selberg_trace_0_over_0_data.json')
    assert d['overall'] == 'SUPPORTED'
    # Analytical torus: zero mode = 1, Tr -> 1 at large t
    t = d['torus']['zero_mode_0_over_0']
    assert t['n_zero_modes_numerical'] == 1
    assert t['removable_value_is_one']
    # Analytical sphere: zero mode = 1, Tr -> 1 at large t
    s = d['sphere_analytical']['zero_mode_0_over_0']
    assert s['n_zero_modes_numerical'] == 1
    assert s['removable_value_is_one']


def test_lefschetz_fixed_point_0_over_0():
    d = load('lefschetz_fixed_point_0_over_0_data.json')
    assert d['overall'] == 'SUPPORTED'
    # S2: L(id) = chi = 2, has fixed point
    assert d['sphere']['chi_matches_Lefschetz_id']
    assert d['sphere']['identity_has_fixed_point']
    assert d['sphere']['Lefschetz_identity'] == 2
    # T2: L(id) = chi = 0
    assert d['torus']['chi_matches_Lefschetz_id']
    assert d['torus']['Lefschetz_identity'] == 0
    # Betti numbers correct
    assert d['sphere']['betti'] == [1, 0, 1]
    assert d['torus']['betti'] == [1, 2, 1]
    # 0/0 at rotation trace
    assert d['trace_analysis']['zero_0_over_0']['rotation_on_T2_H1']['zero_0_over_0']


def test_gauss_bonnet_0_over_0():
    d = load('gauss_bonnet_0_over_0_data.json')
    assert d['overall'] == 'SUPPORTED'
    # S2: chi = 2
    assert d['sphere']['gauss_bonnet_matches_euler']
    assert d['sphere']['chi_euler'] == 2
    assert abs(d['sphere']['chi_gauss_bonnet'] - 2.0) < 0.5
    # T2: chi = 0
    assert abs(d['torus']['chi_gauss_bonnet']) < 0.5
    assert d['torus']['chi_euler'] == 0
    # Torus revolution: chi = 0
    assert abs(d['torus_revolution']['chi_gauss_bonnet']) < 1.0
    assert d['torus_revolution']['chi_euler'] == 0
    # T2 flat: 0/0 at K=0
    assert d['torus_0_over_0']['is_0_over_0']


def test_weyl_law_0_over_0():
    d = load('weyl_law_0_over_0_data.json')
    assert d['overall'] == 'SUPPORTED'
    # T2: Weyl ratio converges
    assert d['torus']['converges']
    assert d['torus']['relative_error'] < 0.01
    # S2: Weyl ratio converges
    assert d['sphere']['converges']
    assert d['sphere']['relative_error'] < 0.02
    # 0/0 at lambda=0: ratio blows up
    assert d['torus_0_over_0']['blows_up_at_zero']
    assert d['sphere_0_over_0']['blows_up_at_zero']


def test_central_limit_theorem_0_over_0():
    d = load('central_limit_theorem_0_over_0_data.json')
    assert d['overall'] == 'SUPPORTED'
    for dist in ['uniform', 'exponential', 'bernoulli']:
        # Convergence at n=500
        conv = d[f'{dist}_convergence']
        assert conv[-1]['error'] < 0.01
        # 0/0 ratio -> -0.5
        z0 = d[f'{dist}_0_over_0']
        assert z0['converges']


def test_banach_fixed_point_0_over_0():
    d = load('banach_fixed_point_0_over_0_data.json')
    assert d['overall'] == 'SUPPORTED'
    # All three converge to fixed points
    assert d['cos']['converged']
    assert d['newton']['converged']
    assert d['linear']['converged']
    # Convergence rates match q
    assert d['cos']['rate_matches_q']
    assert d['linear']['rate_matches_q']
    # 0/0 removable values correct
    assert d['cos_0_over_0']['converges_to_removable']
    assert d['newton_0_over_0']['converges_to_removable']
    assert d['linear_0_over_0']['converges_to_removable']


def test_poisson_summation_0_over_0():
    d = load('poisson_summation_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['removable_value_near_0_error'] < 1e-3
    assert d['summary']['removable_value_near_1_error'] < 1e-3
    assert d['summary']['functional_equation_max_error'] < 1e-6
    assert d['summary']['theta_equation_max_error'] < 1e-6


def test_rayleigh_quotient_0_over_0():
    d = load('rayleigh_quotient_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['max_error_2d'] < 1e-6
    assert d['summary']['max_error_3d'] < 1e-6
    assert d['summary']['max_error_random'] < 1e-6
    assert d['summary']['bounds_hold']


def test_cauchy_integral_0_over_0():
    d = load('cauchy_integral_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['max_limit_error'] < 1e-4


def test_noether_landau_0_over_0():
    d = load('noether_landau_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['amplitude_error'] < 1e-2
    assert d['summary']['above_Tc_all_zero']
    assert d['summary']['below_Tc_all_nonzero']
    assert d['summary']['free_energy_minima']


def test_euler_maclaurin_0_over_0():
    d = load('euler_maclaurin_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['convergence_error'] < 1e-10
    assert d['summary']['euler_maclaurin_error'] < 1e-8


def test_laplace_method_0_over_0():
    d = load('laplace_method_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['gaussian_limit_error'] < 1e-8
    assert d['summary']['numerical_error'] < 1e-8


def test_wallis_product_0_over_0():
    d = load('wallis_product_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['convergence_error'] < 1e-4
    assert d['summary']['factor_limit_error'] < 1e-4


def test_cesaro_summation_0_over_0():
    d = load('cesaro_summation_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['grandi_cesaro_error'] < 1e-4


def test_fermat_little_0_over_0():
    d = load('fermat_little_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['all_removable_match']
    assert d['summary']['all_fermat_mod_p']
    assert d['summary']['all_geometric_identity']


def test_fta_0_over_0():
    d = load('fta_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['max_error'] < 1e-6


def test_pythagorean_0_over_0():
    d = load('pythagorean_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['max_triple_error'] < 1e-10
    assert d['summary']['max_continuous_error'] < 1e-10
    assert d['summary']['all_non_pythagorean_distinct']


def test_taylor_remainder_0_over_0():
    d = load('taylor_remainder_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['max_error'] < 1e-6


def test_fourier_uncertainty_0_over_0():
    d = load('fourier_uncertainty_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['all_gaussians_achieve_bound']
    assert d['summary']['all_boxcars_exceed_bound']
    assert d['summary']['all_scaling_ratios_constant']


def test_morse_theory_0_over_0():
    d = load('morse_theory_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['hessian_all_correct']
    assert d['summary']['euler_char_all_correct']
    assert d['summary']['min_max_removable_saddle_not']


def test_brouwer_fixed_point_0_over_0():
    d = load('brouwer_fixed_point_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['all_contraction_have_fixed_points']
    assert d['summary']['displacements_zero']
    assert d['summary']['displacement_ratios_converge']


def test_stokes_de_rham_0_over_0():
    d = load('stokes_de_rham_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['stokes_all_hold']
    assert d['summary']['d_squared_zero']
    assert d['summary']['cohomology_detected']


def test_sard_theorem_0_over_0():
    d = load('sard_theorem_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['all_1d_measure_zero']
    assert d['summary']['all_2d_measure_zero']
    assert d['summary']['measure_ratios_vanish']


def test_kkt_conditions_0_over_0():
    d = load('kkt_conditions_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['qp_inequality_kkt']
    assert d['summary']['equality_kkt']
    assert d['summary']['barrier_path_converges']


def test_euler_product_0_over_0():
    d = load('euler_product_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['euler_product_converges']
    assert d['summary']['ratio_converges_to_one']
    assert d['summary']['local_factor_ratios_converge']


def test_picard_little_0_over_0():
    d = load('picard_little_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['sin_removable_values_correct']
    assert d['summary']['exp_omits_zero']
    assert d['summary']['sinz_over_z_converges']


def test_weil_explicit_0_over_0():
    d = load('weil_explicit_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['log_deriv_identity_holds']
    assert d['summary']['explicit_formula_improves']
    assert d['summary']['prime_count_correction_helps']


def test_poincare_recurrence_0_over_0():
    d = load('poincare_recurrence_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['golden_ratio_recurs']
    assert d['summary']['periodic_rotations_exact']
    assert d['summary']['equidistribution_converges']


def test_prime_number_theorem_0_over_0():
    d = load('prime_number_theorem_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['pnt_converges']
    assert d['summary']['li_converges']
    assert d['summary']['pole_removable']
    assert d['summary']['chebyshev_bounds_hold']
    assert d['summary']['error_bounded']


def test_ising_model_0_over_0():
    d = load('ising_model_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['magnetization_correct']
    assert d['summary']['energy_at_Tc_correct']
    assert d['summary']['susceptibility_peaks_near_Tc']


def test_khintchine_0_over_0():
    d = load('khintchine_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['dirichlet_bound_holds']
    assert d['summary']['golden_ratio_optimal']
    assert d['summary']['farey_bound_holds']


def test_schanuel_0_over_0():
    d = load('schanuel_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['exp_identity_holds']
    assert d['summary']['lindemann_weierstrass_holds']
    assert d['summary']['exp_derivative_converges']
    assert d['summary']['transcendence_degrees_correct']


def test_shannon_entropy_0_over_0():
    d = load('shannon_entropy_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['zero_log_zero_removable']
    assert d['summary']['uniform_maximum']
    assert d['summary']['deterministic_zero']
    assert d['summary']['mi_0_over_0']
    assert d['summary']['kl_0_over_0']


def test_bayes_theorem_0_over_0():
    d = load('bayes_theorem_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['posterior_converges_to_prior']
    assert d['summary']['likelihood_ratio_removable']
    assert d['summary']['mixture_posterior_valid']
    assert d['summary']['map_matches_prior']


def test_lorenz_attractor_0_over_0():
    d = load('lorenz_attractor_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['lyapunov_positive']
    assert d['summary']['sum_of_exponents']
    assert d['summary']['hopf_bifurcation_detected']
    assert d['summary']['fixed_points_correct']


def test_boltzmann_entropy_0_over_0():
    d = load('boltzmann_entropy_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['boltzmann_ratio_one']
    assert d['summary']['zero_ln_zero_removable']
    assert d['summary']['mixing_max_at_half']
    assert d['summary']['gibbs_pure_zero']
    assert d['summary']['gibbs_uniform_correct']


def test_zeta_functional_eq_0_over_0():
    d = load('zeta_functional_eq_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['functional_equation_holds']
    assert d['summary']['zeta_zero_removable']
    assert d['summary']['trivial_zeros_correct']


def test_wigner_semicircle_0_over_0():
    d = load('wigner_semicircle_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['semicircle_fits']
    assert d['summary']['edge_0_over_0_removable']
    assert d['summary']['rigidity_converges']
    assert d['summary']['goe_fits']


def test_noether_theorem_0_over_0():
    d = load('noether_theorem_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['free_particle_conserved']
    assert d['summary']['harmonic_energy_conserved']
    assert d['summary']['pendulum_energy_conserved']
    assert d['summary']['symmetry_check_correct']


def test_spectral_gap_0_over_0():
    d = load('spectral_gap_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['critical_scaling_converges']
    assert d['summary']['away_from_criticality_grows']


def test_greens_function_0_over_0():
    d = load('greens_function_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['diagonal_correct']
    assert d['summary']['eigenfunction_converges']
    assert d['summary']['free_space_correct']
    assert d['summary']['disk_computed']


def test_mobius_function_0_over_0():
    d = load('mobius_function_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['mobius_values_correct']
    assert d['summary']['dirichlet_inverse_correct']
    assert d['summary']['mertens_correct']
    assert d['summary']['pnt_connection_holds']


def test_saddle_point_0_over_0():
    d = load('saddle_point_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['gaussian_saddle_converges']
    assert d['summary']['stirling_correct']
    assert d['summary']['saddle_0_over_0_removable']
    assert d['summary']['watson_lemma_correct']


def test_stirling_approx_0_over_0():
    d = load('stirling_approx_0_over_0_data.json')
    assert d['summary']['supported']
    assert d['summary']['ratio_converges']
    assert d['summary']['correction_0_over_0']
    assert d['summary']['gamma_stirling_correct']
    assert d['summary']['wallis_correct']


def test_log_limits_0_over_0():
    d = load('log_limits_0_over_0_data.json')
    for key in ['log_removable_singularity', 'log_product_limit',
                'log_stirling_ratio', 'log_harmonic_difference',
                'log_binet_formula', 'log_gamma_reflection']:
        assert d[key]['passed'], f"{key} failed"


def test_combinatorics_0_over_0():
    d = load('combinatorics_0_over_0_data.json')
    for key in ['stirling_number_ratio', 'catalan_asymptotic', 'binomial_limit',
                'motzkin_convergence', 'partition_function_hardy', 'derangement_limit']:
        assert d[key]['passed'], f"{key} failed"


def test_probability_0_over_0():
    d = load('probability_0_over_0_data.json')
    for key in ['lln_convergence', 'martingale_difference', 'birkhoff_ergodic',
                'conditional_expectation', 'shannon_mcmillan_breiman', 'kolmogorov_zero_one']:
        assert d[key]['passed'], f"{key} failed"


def test_nt_sums_0_over_0():
    d = load('nt_sums_0_over_0_data.json')
    for key in ['von_mangoldt_sum', 'euler_totient_sum', 'mertens_product',
                'chebyshev_bias', 'liouville_convergence', 'totient_sum_asymp']:
        assert d[key]['passed'], f"{key} failed"


def test_convex_variational_0_over_0():
    d = load('convex_variational_0_over_0_data.json')
    for key in ['legendre_transform', 'convex_conjugate_duality', 'friedrichs_sobolev',
                'brachistochrone_0_over_0', 'isoperimetric_inequality', 'calculus_of_variations_euler']:
        assert d[key]['passed'], f"{key} failed"


def test_random_matrix_0_over_0():
    d = load('random_matrix_0_over_0_data.json')
    for key in ['circular_law', 'tracy_widom_fluctuation', 'wigner_semicircle_0_over_0',
                'marchenko_pastur', 'sample_covariance_mean']:
        assert d[key]['passed'], f"{key} failed"


def test_ai_performable_professions():
    d = load('ai_performable_professions_data.json')
    assert d['class_counts']['A'] == 5
    assert d['class_counts']['D'] == 2
    assert len(d['professions']) == 14


def test_air_sizing():
    d = load('air_sizing_data.json')
    assert d['demand_scfm']['avg'] > 0
    assert d['sizing']['fad_scfm'] >= d['demand_scfm']['avg']


def test_calendar_universal():
    with open(os.path.join(ROOT, 'data', 'calendar_universal_data.json'), encoding='utf-8') as fp:
        d = json.load(fp)
    assert len(d['layers']) >= 13
    assert d['epoch_0d']['epoch_0d'] is not None
    assert d['calibration']['C0'] is not None


def test_complex_constant_test():
    d = load('complex_constant_test_data.json')
    assert len(d['part1_pi_census']) >= 5
    assert abs(d['part4_euler_identity']['residual_of_e_ipi_plus_1'][0]) < 1e-10
    assert d['part5_bridge_laws']['basel'] is not None


def test_decentral_bank():
    d = load('decentral_bank_data.json')
    results = d['results']
    pass_count = sum(1 for v in results.values() if v['verdict'] == 'PASS')
    assert pass_count >= 5


def test_decentral_bank_bridge():
    d = load('decentral_bank_bridge_data.json')
    results = d['results']
    for name, r in results.items():
        assert r['verdict'] == 'PASS', f"{name} failed: {r['verdict']}"
    assert len(results) == 3


def test_decentral_bank_net():
    d = load('decentral_bank_net_data.json')
    results = d['results']
    pass_or_measured = sum(1 for v in results.values() if v['verdict'] in ('PASS', 'MEASURED'))
    assert pass_or_measured >= 8


def test_euler_number_test():
    d = load('euler_number_test_data.json')
    assert len(d['part1_prefix_census']) >= 5
    assert d['part3_cf']['reading'] is not None
    assert d['part4_clock_test']['reading'] is not None


def test_golden_closure_constant():
    d = load('golden_closure_constant_data.json')
    assert abs(d['fit_tail']['a'] - 0.5) < 0.05
    assert abs(d['convergence_table'][-1]['ratio'] - 0.618033988742) < 1e-6


def test_mandate_report():
    d = load('mandate_report_data.json')
    assert d['class_counts']['A'] == 5
    assert d['class_counts']['D'] == 2
    assert len(d['professions']) == 14


def test_photon_rubber_ball():
    d = load('photon_rubber_ball_data.json')
    assert d['phaseA_absolute_zero']['verdict'] == 'PASS'
    assert d['phaseB_release_temperature']['verdict'] == 'MEASURED'


def test_rainwater_sizing():
    d = load('rainwater_data.json')
    assert d['harvest_over_demand'] > 1.0
    assert d['tank_sizing_m3']['uniform rainfall'] > 0


def test_servo_regen():
    d = load('servo_regen_data.json')
    assert d['per_cycle_axis']['recovered_fraction'] > 0
    assert isinstance(d['architecture'], str)


def test_standby_efficiency():
    d = load('standby_efficiency_data.json')
    assert d['kwh_per_day_without_sleep'] > d['kwh_per_day_with_sleep']
    assert d['payback_yr']['sleep_alone'] > 0


def test_refuted_claims_probe():
    d = load('refuted_claims_probe_data.json')
    # All six probes must PASS
    for key in ['probe_A_geodesic', 'probe_B_golden', 'probe_C_spectral',
                'probe_D_regularization', 'probe_E_bekenstein', 'probe_F_meta']:
        assert key in d, f"Missing probe: {key}"
        assert d[key]['verdict'] == 'PASS', f"{key} failed"

    # A: Integrator convergence
    assert d['probe_A_geodesic']['euler_converges']
    assert d['probe_A_geodesic']['midpoint_converges']

    # B: Golden 0/0 extracts sqrt(5) via L'Hopital; Binet 0/0 = -1
    assert d['probe_B_golden']['lhopital_is_sqrt5']
    assert d['probe_B_golden']['pade_is_sqrt5']
    assert d['probe_B_golden']['fib00_is_correct']

    # C: GOE level repulsion is removable (not pole)
    assert d['probe_C_spectral']['poisson_is_pole']
    assert d['probe_C_spectral']['goe_is_removable']

    # D: Regularization sensitivity exists
    assert d['probe_D_regularization']['old_class_sensitivity'] != 0

    # F: Meta-pattern recovers all 21 claims
    assert d['probe_F_meta']['recovery_rate'] == 1.0


def test_open_questions():
    d = load('open_questions_data.json')

    # Q1: Integrator constants converge (errors small relative to the constant)
    q1 = d['Q1_geodesic']
    # C values converge: C_euler ~ 0.184, C_mid ~ 0.061, C_rk4 ~ 0.59
    # Check they are positive and finite (converged)
    assert 0 < q1['C_euler'] < 1.0
    assert 0 < q1['C_midpoint'] < 1.0
    assert 0 < q1['C_rk4'] < 10.0

    # Q2: All polynomial 0/0 errors small
    assert d['Q2_algebraic']['max_error_all'] < 0.01
    assert d['Q2_algebraic']['aberth_converges']

    # Q3: Critical beta near 1.0
    assert d['Q3_spectral']['critical_beta_match']

    # Q4: 0/0 ratio converges as lambda->0
    assert d['Q4_sensitivity']['converges']

    # Q5: Fisher from quadratic 0/0
    assert d['Q5_geometry']['quadratic_00_correct']
    assert d['Q5_geometry']['d2KL_equals_Fisher']


def test_logic_0_over_0():
    d = load('logic_0_over_0_data.json')

    # Q1: Godel incompleteness
    g = d['Q1_godel']['godel']
    assert g['ratio_is_0_over_0']
    assert g['removable_value'] == 1.0
    assert g['verdict'] == 'PASS'

    # Consistency strength
    cs = d['Q1_godel']['consistency_strength']
    assert cs['each_level_Cannot_prove_own_consistency']
    assert cs['verdict'] == 'PASS'

    # Q2: Halting problem
    omega = d['Q2_halting']['omega_approximation']
    assert omega['convergence_to_1'] < 0.5
    assert omega['verdict'] == 'PASS'

    # Q3: Consistency strength
    ct = d['Q3_consistency']['ordinal_hierarchy']
    assert ct['verdict'] == 'PASS'
    assert d['Q3_consistency']['conservation']['ACA_0_same_as_PA']


def test_category_theory_0_over_0():
    d = load('category_theory_0_over_0_data.json')

    # Q1: Natural transformations
    nt = d['Q1_natural_transformations']['natural_transformations']
    assert nt['Nat_Id_Id_count'] > 0
    assert nt['zero_transformation_exists']
    assert nt['verdict'] == 'PASS'

    y = d['Q1_natural_transformations']['yoneda']
    assert y['bijection_holds']
    assert y['verdict'] == 'PASS'

    # Q2: Adjunctions
    adj = d['Q2_adjunctions']['adjunction']
    assert adj['removable_value'] == 1.0
    assert adj['currying_verification']['equal']
    assert adj['currying_verification']['verdict'] == 'PASS'

    # Q3: Limits/colimits
    eq = d['Q3_limits_colimits']['equalizer']
    assert 0 in eq['equalizer']
    assert eq['verdict'] == 'PASS'

    pb = d['Q3_limits_colimits']['pullback']
    assert [0, 0] in pb['pullback']
    assert pb['verdict'] == 'PASS'


def test_brody_navier_stokes():
    d = load('brody_navier_stokes_data.json')

    # Q1: Brody boundary
    b = d['Q1_brody_boundary']
    assert b['critical_beta_match']
    assert b['removable_values']['goe_exact_pi_over_2'] > 1.5
    assert b['removable_values']['goe_exact_pi_over_2'] < 1.6
    assert b['verdict'] == 'PASS'

    # Q2: Navier-Stokes
    ns = d['Q2_navier_stokes']
    assert ns['euler']['nonlinear_over_pressure_ratio'] == 1.0
    assert ns['euler']['always_removable']
    assert ns['blowup_classification']['brody_boundary_alpha'] == 1.0
    assert ns['burgers']['verdict'] == 'PASS'
    assert ns['euler']['verdict'] == 'PASS'


def test_entropy_condition():
    d = load('entropy_condition_data.json')

    # Q1: Burgers
    b = d['Q1_burgers']['burgers_shocks']
    assert b['verdict'] == 'PASS'
    # Verify Brody boundary: very weak shock has h near 0
    weak = [s for s in b['shocks'] if s['brody_boundary']][0]
    assert abs(weak['h']) < 0.001
    # Verify strong shock has h > 0
    strong = [s for s in b['shocks'] if s['u_L'] == 2.0 and s['u_R'] == 0.0][0]
    assert strong['h'] > 0

    # Q3: Riemann classification
    r = d['Q3_riemann']['riemann_classification']
    assert r['all_match']
    assert r['verdict'] == 'PASS'


def test_prime_geodesic():
    d = load('prime_geodesic_data.json')

    # Q1: PGT converges toward 1
    q1 = d['Q1_pgt']
    ratios = [r['ratio'] for r in q1['results']]
    # Ratios should be increasing toward 1
    assert ratios[-1] > ratios[0], "Ratios should increase toward 1"
    assert ratios[-1] > 0.8, f"Final ratio should be near 1, got {ratios[-1]}"

    # Q2: Selberg 1/4 and RH verified
    q2 = d['Q2_selberg']
    assert q2['selberg_1_4_holds']
    assert q2['all_on_critical_line']
    assert q2['verdict'] == 'PASS'

    # Q3: Both prime and prime-geodesic ratios converge toward 1
    q3 = d['Q3_comparison']
    prime_ratios = [c['ratio_prime'] for c in q3['comparison']]
    gamma_ratios = [c['ratio_gamma'] for c in q3['comparison']]
    assert prime_ratios[-1] > 0.9
    assert gamma_ratios[-1] > 0.8


def test_information_conservation():
    d = load('information_conservation_data.json')

    # Q1: I₀ = |lambda|² for all known forms
    q1 = d['Q1_conservation']
    assert q1['known_0_0s']['all_satisfy_I0_equals_lambda_squared']

    # Q2: Additivity
    q2 = d['Q2_additivity']
    assert q2['all_match']

    # Q3: Fisher information interpretation
    q3 = d['Q3_fisher']
    assert q3['all_match_linear']
    assert q3['match_gaussian']
    assert q3['verdict'] == 'PASS'


def test_qft():
    d = load('qft_0_over_0_data.json')

    # Q1: QED self-energy converges to physical mass
    qed = d['Q1_qed']['qed']
    assert qed['converge_to_physical_mass']
    last = qed['results'][-1]
    assert last['error'] < 1e-10

    # Q2: QCD asymptotic freedom
    qcd = d['Q2_qcd']['qcd']
    assert qcd['asymptotic_freedom']
    assert qcd['b_0'] == 7.0

    # Q3: Cosmological constant fine-tuning
    cc = d['Q3_cc']['cosmological_constant']
    assert cc['fine_tuning'] < 1e-100
    assert cc['removable_value'] == 1.0


def test_millennium():
    d = load('millennium_data.json')

    # Q1: P vs NP ratio -> 0
    pnp = d['Q1_p_vs_np']['p_vs_np']
    assert pnp['removable_value'] == 0
    last = pnp['results'][-1]
    assert last['ratio'] < 0.01

    # Q2: Riemann error -> 0
    rh = d['Q2_riemann']['riemann']
    assert rh['converge_to_0']
    assert rh['removable_value'] == 0

    # Q3: All six are 0/0s
    all6 = d['Q3_all_six']
    assert all6['all_are_zero_over_zero']
    assert all6['all_have_removable_value']
    assert len(all6['problems']) == 6


def test_poincare():
    d = load('poincare_data.json')

    # Q1: Hamilton 0/0 classifies singularities
    ham = d['Q1_hamilton']['hamilton_00']['classifications']
    neckpinch = [c for c in ham if 'Neckpinch' in c['name']][0]
    assert abs(neckpinch['removable_value'] - 1.0) < 0.01
    degenerate = [c for c in ham if 'Degenerate' in c['name']][0]
    assert degenerate['removable_value'] < 0.1

    # Q2: Ricci flow on S^2 x S^1 is neckpinch
    ricci = d['Q2_ricci']['ricci_flow']
    assert ricci['singularity_type'] == 'NECKPINCH'
    assert ricci['hamilton_removable'] == 1.0

    # Q3: No poles in 3D (Perelman)
    cls = d['Q3_classification']['classification']
    assert cls['no_poles_in_3d']
    assert cls['poincare_conjecture'] == 'TRUE (simply connected -> S^3)'


def test_chern_gauss_bonnet():
    d = load('chern_gauss_bonnet_data.json')

    # Q1: 2D ratio = 1
    q1 = d['Q1_dim2']['dimension_2']
    assert q1['all_ratio_1']

    # Q2: 4D ratio = 1
    q2 = d['Q2_dim4']['dimension_4']
    assert q2['all_ratio_1']

    # Q3: 6D ratio = 1, index = chi
    q3 = d['Q3_dim6']['dimension_6']
    assert q3['all_ratio_1']
    assert q3['all_index_match']


def test_riemann_roch():
    d = load('riemann_roch_data.json')

    # Q1: Curves - critical ratio = 1
    q1 = d['Q1_curves']['curves']['curve_results']
    for cr in q1:
        if cr['critical_ratio'] is not None:
            assert abs(cr['critical_ratio'] - 1.0) < 1e-10

    # Q2: Surfaces - Noether formula holds
    q2 = d['Q2_surfaces']['surfaces']['surface_results']
    for sr in q2:
        assert sr['chi_O_matches_noether']

    # Q3: CP^n - chi(O) = 1, chi(K) = (-1)^n
    q3 = d['Q3_cpn']['cpn']
    assert q3['all_chi_O_match']
    assert q3['all_chi_K_match']


def test_selberg_trace():
    d = load('selberg_trace_data.json')

    # Q1: Weyl law slopes match area/4pi
    q1 = d['Q1_weyl_law']['weyl_law']
    assert q1['all_slopes_correct']

    # Q2: Prime-geodesic ratio -> 1
    q2 = d['Q2_prime_geodesic']['prime_geodesic']
    assert q2['ratio_approaches_1']

    # Q3: GOE at beta=1, removable value pi/2
    q3 = d['Q3_brody_selberg']['brody_selberg']
    assert q3['goe_verified']


def test_selberg_zeta():
    d = load('selberg_zeta_data.json')

    # Q1: Selberg zeta zeros on critical line
    q1 = d['Q1_selberg_zeta']['selberg_zeta_torus']
    assert q1['all_zeros_verified']
    assert q1['nonzero_at_2']

    # Q2: Functional equation Z(s)/Z(1-s) ~ 1 on critical line
    q2 = d['Q2_functional_equation']['functional_equation']
    assert q2['critical_line_trivial']
    for sr in q2['symmetry_results']:
        assert sr['ratio_near_1']

    # Q3: Riemann zeta analogy
    q3 = d['Q3_riemann_analogy']['riemann_analogy']
    assert q3['all_zeta_match']
    assert q3['all_trivial_zero']


def test_h_theorem_navier_stokes():
    d = load('h_theorem_navier_stokes_data.json')

    # Q1: Energy monotonically decreasing, total dissipation <= H(0)
    q1 = d['Q1_energy_balance']['energy_balance']
    assert q1['H_decreasing']
    assert q1['energy_balance_ok']
    assert q1['total_dissipation_le_H0']

    # Q2: D/H starts at Poincare bound, increases (energy cascade)
    q2 = d['Q2_dissipation_ratio']['dissipation_ratio']
    assert q2['starts_at_poincare']
    assert q2['increases_over_time']

    # Q3: Total dissipation <= H(0) for all amplitudes, monotonic
    q3 = d['Q3_total_dissipation']['total_dissipation']
    assert q3['all_monotonic']
    assert q3['all_ratio_le_1']


def test_atiyah_singer():
    d = load('atiyah_singer_data.json')

    # Q1: de Rham index = Euler characteristic
    q1 = d['Q1_de_rham']['de_rham']
    assert q1['all_match']
    assert q1['all_integer']

    # Q2: Dolbeault index = chi(X,O) = integer
    q2 = d['Q2_dolbeault']['dolbeault']
    assert q2['all_match']
    assert q2['all_integer']

    # Q3: Dirac index = A-hat = integer
    q3 = d['Q3_dirac']['dirac']
    assert q3['all_integer']

    # Q4: All 17 indices are integers (lattice property)
    q4 = d['Q4_integer_constraint']['integer_constraint']
    assert q4['all_integer']


def test_de_rham():
    d = load('de_rham_data.json')

    # Q1: All Betti numbers are non-negative integers
    q1 = d['Q1_betti_numbers']['betti_numbers']
    assert q1['all_nonneg']
    assert q1['all_integer']

    # Q2: Euler characteristic from Betti = Gauss-Bonnet = formula
    q2 = d['Q2_euler_characteristic']['euler_characteristic']
    assert q2['all_match']

    # Q3: Integration map (Stokes) verified
    q3 = d['Q3_integration_map']['integration_map']
    assert q3['stokes_verified']


def test_knot_invariants():
    d = load('knot_invariants_data.json')

    # Q1: V_K(1) = 1 for all 7 knots, span = crossing number
    q1 = d['Q1_jones_values']['jones_values']
    assert q1['all_V1_equal_1']
    assert q1['all_span_match']

    # Q2: Split link delta formula
    q2 = d['Q2_skein_relation']['split_link']
    assert q2['matches']

    # Q3: Chern-Simons Z(1) = 1
    q3 = d['Q3_chern_simons']['chern_simons']
    assert q3['all_Z1_equal_1']


def test_modular_forms():
    d = load('modular_forms_data.json')

    # Q1: Hasse bound satisfied for all curves
    q1 = d['Q1_point_counts']['point_counts']
    assert q1['all_hasse_bounds']

    # Q2: L(E,1) nonzero (rank-0 curve)
    q2 = d['Q2_L_function']['L_function']
    assert q2['L_nonzero_at_1']

    # Q3: Modularity - arithmetic = analysis, all ratios = 1
    q3 = d['Q3_modularity']['modularity']
    assert q3['all_ratios_1']
    assert q3['sato_tate_bounded']


def test_random_matrix_theory():
    d = load('random_matrix_theory_data.json')

    # Q1: Level repulsion - eigenvalues repel (R_2(0) -> 0)
    q1 = d['Q1_level_repulsion']['level_repulsion']
    assert q1['level_repulsion']

    # Q2: GUE spacings match Wigner surmise (KS test)
    q2 = d['Q2_wigner_gue']['wigner_gue']
    assert q2['good_fit']
    assert abs(q2['mean_spacing'] - 1.0) < 0.01

    # Q3: GOE spacings match Wigner surmise (KS test)
    q3 = d['Q3_wigner_goe']['wigner_goe']
    assert q3['good_fit']
    assert abs(q3['mean_spacing'] - 1.0) < 0.01

    # Q4: Pair correlation matches Montgomery-Odlyzko formula
    q4 = d['Q4_pair_correlation']['pair_correlation']
    assert q4['good_fit']

    # Q5: Both GOE and GUE show level repulsion
    q5 = d['Q5_symmetry_classes']['symmetry_classes']
    assert q5['both_repel']


# -----------------------------------------------------------------------
# Langlands Program 0/0
# -----------------------------------------------------------------------

def test_langlands_program():
    d = load('langlands_program_data.json')

    # Q1: Hecke eigenvalues = Frobenius traces (Langlands GL(2)/Q)
    q1 = d['Q1_hecke_eigenvalues']['hecke_eigenvalues']
    assert q1['verdict'] == 'PASS'
    for curve in q1['curves']:
        assert curve['all_ratios_1']
        assert curve['all_ramanujan_holds']
        assert curve['all_hasse_bound']

    # Q2: Functional equation of L(E,s)
    q2 = d['Q2_functional_equation']['functional_equation']
    assert q2['verdict'] == 'PASS'
    assert q2['all_L_nonzero_at_1']

    # Q3: Functoriality (Sym^2, Rankin-Selberg)
    q3 = d['Q3_functoriality']['functoriality']
    assert q3['verdict'] == 'PASS'
    assert q3['all_sym2_converges']


# -----------------------------------------------------------------------
# TQFT 0/0
# -----------------------------------------------------------------------

def test_tqft():
    d = load('tqft_0_over_0_data.json')

    # Q1: Disjoint union axiom
    q1 = d['Q1_disjoint_union']['disjoint_union']
    assert q1['verdict'] == 'PASS'
    assert q1['all_ratios_1']

    # Q2: Functoriality
    q2 = d['Q2_functoriality']['functoriality']
    assert q2['verdict'] == 'PASS'
    assert q2['identity']['identity_holds']
    assert q2['poincare_duality']['duality_holds']

    # Q3: Topological invariance
    q3 = d['Q3_topological_invariance']['topological_invariance']
    assert q3['verdict'] == 'PASS'
    assert q3['torus_invariant']
    assert q3['sphere_invariant']


# -----------------------------------------------------------------------
# Gromov Non-Squeezing 0/0
# -----------------------------------------------------------------------

def test_gromov_non_squeezing():
    d = load('gromov_non_squeezing_data.json')

    # Q1: Symplectic capacity is dimension-independent
    q1 = d['Q1_capacity']['capacity']
    assert q1['verdict'] == 'PASS'
    assert q1['all_dimension_independent']

    # Q2: Non-squeezing verification
    q2 = d['Q2_non_squeezing']['non_squeezing']
    assert q2['verdict'] == 'PASS'
    assert q2['all_correct']
    assert q2['degenerate_0_over_0']['is_0_over_0']

    # Q3: Symplectic invariance
    q3 = d['Q3_symplectic_invariance']['symplectic_invariance']
    assert q3['verdict'] == 'PASS'
    assert q3['all_symp_maps_invariant']
    assert q3['non_symplectic_detected']


# -----------------------------------------------------------------------
# Non-commutative Geometry 0/0
# -----------------------------------------------------------------------

def test_non_commutative_geometry():
    d = load('non_commutative_geometry_data.json')

    # Q1: Spectral triple axioms
    q1 = d['Q1_spectral_triple_axioms']['spectral_triple_axioms']
    assert q1['verdict'] == 'PASS'
    assert q1['commutant_bounded']
    assert q1['skew_symmetric']
    assert q1['compact_resolvent']

    # Q2: Connes distance formula
    q2 = d['Q2_connes_distance']['connes_distance']
    assert q2['verdict'] == 'PASS'
    assert q2['commutative_test']['commutative_limit_holds']

    # Q3: Reconstruction theorem
    q3 = d['Q3_reconstruction']['reconstruction']
    assert q3['verdict'] == 'PASS'
    assert q3['S1_reconstruction']['is_skew_symmetric']
    assert q3['S1_reconstruction']['spectrum_match']
    assert q3['T2_reconstruction']['is_skew_symmetric']


# -----------------------------------------------------------------------
# Faltings' Theorem 0/0
# -----------------------------------------------------------------------

def test_faltings_theorem():
    d = load('faltings_theorem_data.json')

    # Q1: Finiteness
    q1 = d['Q1_finiteness']['finiteness']
    assert q1['verdict'] == 'PASS'

    # Q2: Height function
    q2 = d['Q2_height_function']['height_function']
    assert q2['verdict'] == 'PASS'
    assert q2['quadratic_test']['h_O_is_zero']
    assert q2['quadratic_test']['monotone']

    # Q3: Chabauty-Coleman
    q3 = d['Q3_chabauty_coleman']['chabauty_coleman']
    assert q3['verdict'] == 'PASS'
    assert q3['n_working'] == 2


# -----------------------------------------------------------------------
# ABC Conjecture 0/0
# -----------------------------------------------------------------------

def test_abc_conjecture():
    d = load('abc_conjecture_data.json')

    # Q1: Quality computation
    q1 = d['Q1_quality']['quality']
    assert q1['verdict'] == 'PASS'
    assert q1['supremum_at_least'] > 1.5
    assert q1['n_above_1'] > 0

    # Q2: Finiteness
    q2 = d['Q2_finiteness']['finiteness']
    assert q2['verdict'] == 'PASS'
    assert q2['all_finite_for_positive_eps']

    # Q3: Connections
    q3 = d['Q3_connections']['connections']
    assert q3['verdict'] == 'PASS'
    assert q3['all_effective']


# -----------------------------------------------------------------------
# Arakelov Theory 0/0
# -----------------------------------------------------------------------

def test_arakelov_theory():
    d = load('arakelov_theory_data.json')

    # Q1: Green function
    q1 = d['Q1_green_function']['green_function']
    assert q1['verdict'] == 'PASS'
    assert q1['all_sing_match']
    assert q1['symmetric']

    # Q2: Delta invariant
    q2 = d['Q2_delta_invariant']['delta_invariant']
    assert q2['verdict'] == 'PASS'
    assert q2['conformal_invariance_holds']

    # Q3: Arithmetic intersection
    q3 = d['Q3_arithmetic_intersection']['arithmetic_intersection']
    assert q3['verdict'] == 'PASS'
    assert q3['grothendieck_riemann_roch']


# -----------------------------------------------------------------------
# Schanuel's Conjecture 0/0
# -----------------------------------------------------------------------

def test_schanuels_conjecture():
    d = load('schanuels_conjecture_data.json')

    # Q1: Baker's theorem
    q1 = d['Q1_baker']['baker']
    assert q1['verdict'] == 'PASS'
    assert q1['decreasing']
    assert q1['avg_slope'] < 0

    # Q2: Lindemann-Weierstrass
    q2 = d['Q2_lindemann_weierstrass']['lindemann_weierstrass']
    assert q2['verdict'] == 'PASS'
    assert q2['all_transcendental']
    assert q2['n_verified'] == 4

    # Q3: Six Exponentials
    q3 = d['Q3_six_exponentials']['six_exponentials']
    assert q3['verdict'] == 'PASS'
    assert q3['all_transcendent']
    assert q3['condition_satisfied']
    assert q3['transcendence_ratio'] == 1.0


# -----------------------------------------------------------------------
# Iwasawa Main Conjecture 0/0
# -----------------------------------------------------------------------

def test_iwasawa_main_conjecture():
    d = load('iwasawa_main_conjecture_data.json')

    # Q1: Kubota-Leopoldt interpolation
    q1 = d['Q1_interpolation']['interpolation']
    assert q1['verdict'] == 'PASS'
    assert q1['all_match']
    assert q1['n_verified'] == 6

    # Q2: Bernoulli congruences
    q2 = d['Q2_bernoulli_congruences']['bernoulli_congruences']
    assert q2['verdict'] == 'PASS'
    assert q2['all_vs_integral']

    # Q3: BSD connection
    q3 = d['Q3_bsd_connection']['bsd_connection']
    assert q3['verdict'] == 'PASS'
    assert q3['rank_0_test']['bsd_holds']
    assert q3['iwasawa_connection']['characteristic_ideal_equals_L_function']


# -----------------------------------------------------------------------
# Arakelov GRR 0/0
# -----------------------------------------------------------------------

def test_arakelov_grr():
    d = load('arakelov_grr_data.json')

    # Q1: Self-intersection
    q1 = d['Q1_self_intersection']['self_intersection']
    assert q1['verdict'] == 'PASS'
    assert q1['removable_value_is_delta']
    assert q1['all_match_formula']

    # Q2: Structure sheaf
    q2 = d['Q2_structure_sheaf']['structure_sheaf']
    assert q2['verdict'] == 'PASS'

    # Q3: Pushforward
    q3 = d['Q3_pushforward']['pushforward']
    assert q3['verdict'] == 'PASS'
    assert q3['identity_test']['formula_holds']


# -----------------------------------------------------------------------
# Colmez Conjecture 0/0
# -----------------------------------------------------------------------

def test_colmez_conjecture():
    d = load('colmez_conjecture_data.json')

    # Q1: Faltings heights
    q1 = d['Q1_faltings_heights']['faltings_heights']
    assert q1['verdict'] == 'PASS'
    assert q1['all_finite']
    assert q1['n_curves'] == 5

    # Q2: L-values
    q2 = d['Q2_l_values']['l_values']
    assert q2['verdict'] == 'PASS'
    assert q2['all_L_nonzero']
    assert q2['all_bsd_reasonable']

    # Q3: Colmez formula
    q3 = d['Q3_colmez_formula']['colmez_formula']
    assert q3['verdict'] == 'PASS'
    assert q3['all_match_formula']
    assert q3['l_function_significant']


# -----------------------------------------------------------------------
# Vojta's Conjecture 0/0
# -----------------------------------------------------------------------

def test_vojta_conjecture():
    d = load('vojta_conjecture_data.json')

    # Q1: Height bounds
    q1 = d['Q1_height_bounds']['height_bounds']
    assert q1['verdict'] == 'PASS'
    assert q1['ratio_above_1']  # max ratio > 1

    # Q2: ABC quality
    q2 = d['Q2_abc_quality']['abc_quality']
    assert q2['verdict'] == 'PASS'
    assert q2['quality_above_1']

    # Q3: Mordell-Weil
    q3 = d['Q3_mordell_weil']['mordell_weil']
    assert q3['verdict'] == 'PASS'
    assert q3['identity_height_zero']
    assert q3['torsion_bounded']


# -----------------------------------------------------------------------
# Manin-Mumford Conjecture 0/0
# -----------------------------------------------------------------------

def test_manin_mumford():
    d = load('manin_mumford_data.json')

    # Q1: Torsion subgroups
    q1 = d['Q1_torsion_subgroups']['torsion_subgroups']
    assert q1['verdict'] == 'PASS'
    assert q1['all_finite']
    for r in q1['results']:
        assert r['all_on_curve']
        assert r['below_mazur_bound']

    # Q2: Height of torsion
    q2 = d['Q2_height_torsion']['height_torsion']
    assert q2['verdict'] == 'PASS'
    assert q2['all_bounded']
    assert q2['all_rank0']

    # Q3: Raynaud
    q3 = d['Q3_raynaud']['raynaud']
    assert q3['verdict'] == 'PASS'
    assert q3['horizontal_finite']
    assert q3['vertical_finite']


# -----------------------------------------------------------------------
# Uniform Boundedness Conjecture 0/0
# -----------------------------------------------------------------------

def test_uniform_boundedness():
    d = load('uniform_boundedness_data.json')

    # Q1: Mazur
    q1 = d['Q1_mazur']['mazur']
    assert q1['verdict'] == 'PASS'
    assert q1['all_below_bound']
    assert q1['all_in_mazur_list']
    assert q1['all_cm_consistent']

    # Q2: Quadratic torsion
    q2 = d['Q2_quadratic_torsion']['quadratic_torsion']
    assert q2['verdict'] == 'PASS'
    assert q2['all_bounded']
    assert q2['cm_growth']

    # Q3: Torsion towers
    q3 = d['Q3_torsion_towers']['torsion_towers']
    assert q3['verdict'] == 'PASS'
    assert q3['all_below_merel']
    assert q3['growth_bounded']


# -----------------------------------------------------------------------
# Zilber-Pink Conjecture 0/0
# -----------------------------------------------------------------------

def test_zilber_pink():
    d = load('zilber_pink_data.json')

    # Q1: Andre-Oort
    q1 = d['Q1_andre_oort']['andre_oort']
    assert q1['verdict'] == 'PASS'
    assert q1['all_finite']
    assert q1['cm_exist']

    # Q2: Unlikely intersections
    q2 = d['Q2_unlikely_intersections']['unlikely_intersections']
    assert q2['verdict'] == 'PASS'
    assert q2['all_finite']
    assert q2['zp_condition']

    # Q3: Dimension counting
    q3 = d['Q3_zp_dimension']['zp_dimension']
    assert q3['verdict'] == 'PASS'
    assert q3['all_match']


# -----------------------------------------------------------------------
# Shimura-Taniyama Correspondence 0/0
# -----------------------------------------------------------------------

def test_shimura_taniyama():
    d = load('shimura_taniyama_data.json')

    # Q1: Euler product
    q1 = d['Q1_euler_product']['euler_product']
    assert q1['verdict'] == 'PASS'
    assert q1['cm_primes_zero']
    assert q1['has_split']
    assert q1['hasse_ok']

    # Q2: CM correspondence
    q2 = d['Q2_cm_correspondence']['cm_correspondence']
    assert q2['verdict'] == 'PASS'
    assert q2['e1_all_match']
    assert q2['e2_all_match']
    assert q2['ramanujan']

    # Q3: Level = conductor
    q3 = d['Q3_level_conductor']['level_conductor']
    assert q3['verdict'] == 'PASS'
    assert q3['all_cm_condition']


# -----------------------------------------------------------------------
# Sato-Tate Conjecture 0/0
# -----------------------------------------------------------------------

def test_sato_tate():
    d = load('sato_tate_data.json')

    # Q1: Semicircle law
    q1 = d['Q1_semicircle']['semicircle']
    assert q1['verdict'] == 'PASS'
    assert q1['ks_ok']
    assert q1['hasse_ok']

    # Q2: CM degeneration
    q2 = d['Q2_cm_degeneration']['cm_degeneration']
    assert q2['verdict'] == 'PASS'
    assert q2['cm_primes_zero']
    assert q2['ks_rejects_semicircle']

    # Q3: Moments
    q3 = d['Q3_moments']['moments']
    assert q3['verdict'] == 'PASS'
    assert q3['all_close']


# -----------------------------------------------------------------------
# Explicit Formula 0/0
# -----------------------------------------------------------------------

def test_explicit_formula():
    d = load('explicit_formula_data.json')

    # Q1: Direct verification
    q1 = d['Q1_direct_verification']['direct_verification']
    assert q1['verdict'] == 'PASS'
    assert q1['errors_decreasing']
    assert q1['small_final_errors']

    # Q2: Zero contributions
    q2 = d['Q2_zero_contributions']['zero_contributions']
    assert q2['verdict'] == 'PASS'
    assert q2['oscillating']
    assert q2['error_decreases']

    # Q3: Tower stability
    q3 = d['Q3_tower_stability']['tower_stability']
    assert q3['verdict'] == 'PASS'
    assert q3['stable']
    assert q3['all_final_errors_small']


# -----------------------------------------------------------------------
# Montgomery-Odlyzko Law 0/0
# -----------------------------------------------------------------------

def test_montgomery_odlyzko():
    d = load('montgomery_odlyzko_data.json')

    # Q1: Repulsion
    q1 = d['Q1_repulsion']['repulsion']
    assert q1['verdict'] == 'PASS'
    assert q1['repulsion_detected']
    assert q1['mean_ok']

    # Q2: Variance
    q2 = d['Q2_variance']['variance']
    assert q2['verdict'] == 'PASS'
    assert q2['closer_to_gue']

    # Q3: Convergence
    q3 = d['Q3_convergence']['convergence']
    assert q3['verdict'] == 'PASS'
    assert q3['all_repulsion_low']
    assert q3['below_poisson']


# -----------------------------------------------------------------------
# Hardy Z-Function and Riemann Hypothesis 0/0
# -----------------------------------------------------------------------

def test_hardy_z_riemann_hypothesis():
    d = load('hardy_z_riemann_data.json')

    # Q1: Z(gamma_n) = 0
    q1 = d['Q1_hardy_z_zeros']['hardy_z_zeros']
    assert q1['verdict'] == 'PASS'
    assert q1['all_zero']

    # Q2: Sign changes at each zero
    q2 = d['Q2_no_missing_zeros']['no_missing_zeros']
    assert q2['verdict'] == 'PASS'
    assert q2['all_sign_change']
    assert q2['all_near_zero']

    # Q3: Functional equation Z(-t) = Z(t)
    q3 = d['Q3_functional_equation']['functional_equation']
    assert q3['verdict'] == 'PASS'
    assert q3['all_match']

