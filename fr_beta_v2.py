"""
f(R) beta functions from Codello 2009 eq.(117)+(119).
Evaluate PDE RHS at n+1 well-spaced R values, solve for Taylor coefficients.
Iterate for self-consistent fp_dot/fpp_dot.
"""
import math

def flow_rhs(R, g, fp_dot_val=0.0, fpp_dot_val=0.0):
    pi = math.pi
    R2=R*R; R3=R2*R; R4=R3*R
    f = sum(g[i]*R**i for i in range(len(g)))
    fp = sum(i*g[i]*R**(i-1) for i in range(1,len(g)))
    fpp = sum(i*(i-1)*g[i]*R**(i-2) for i in range(2,len(g)))
    fppp = sum(i*(i-1)*(i-2)*g[i]*R**(i-3) for i in range(3,len(g)))
    pf = 384.0*pi**2/30240.0
    def sd(num,den): return num/den if abs(den)>1e-40 else 0.0
    denT = 3*f-(R-3)*fp
    numT = (20*(311*R3-126*R2-22680*R+45360)*(fp_dot_val+2*fp-2*R*fpp)
            -252*(R2+360*R-1080)*fp)
    Rm3sq = (R-3)**2
    denS = fpp*Rm3sq+2*f+(3-2*R)*fp
    numS = (1008*(29*R2+360*R+1080)*fp
            +4*(185*R3+3654*R2+22680*R+45360)*(fp_dot_val+2*fp-2*R*fpp)
            -2016*(29*R3+273*R2-3240)*fpp
            -9*(181*R4+3248*R3+15288*R2-90720)*(fpp_dot_val-2*R*fppp))
    Tpoles = -1008*(511*R2-360*R-1080)/(R-3) - 2016*(607*R2-360*R-2160)/(R-4)
    Sig = sd(-10*(R2-20*R+54)*R2, R2-7*R+12)
    return pf*(Tpoles + sd(numT,denT) + sd(numS,denS) + Sig)

def solve_lu(A, b):
    n = len(b)
    M = [row[:]+[b[i]] for i,row in enumerate(A)]
    for c in range(n):
        br = max(range(c,n), key=lambda r: abs(M[r][c]))
        M[c],M[br] = M[br],M[c]
        p = M[c][c]
        if abs(p)<1e-40: continue
        for r in range(c+1,n):
            fac = M[r][c]/p
            for j in range(c,n+1): M[r][j] -= fac*M[c][j]
    x = [0.0]*n
    for i in range(n-1,-1,-1):
        s = M[i][n]
        for j in range(i+1,n): s -= M[i][j]*x[j]
        x[i] = s/M[i][i] if abs(M[i][i])>1e-40 else 0.0
    return x

def extract_betas(g, nmax, R_eval=None):
    n = nmax+1
    if R_eval is None:
        R_eval = [i*0.4 for i in range(n)]
    A = [[Rj**k for k in range(n)] for Rj in R_eval]
    Ainv_rows = []
    for i in range(n):
        ei = [0.0]*n; ei[i]=1.0
        Ainv_rows.append(solve_lu(A, ei))
    betas = [0.0]*n
    for iteration in range(30):
        fp_dots = []
        fpp_dots = []
        for Rj in R_eval:
            fpd = sum(i*betas[i]*Rj**(i-1) for i in range(1,n))
            fppd = sum(i*(i-1)*betas[i]*Rj**(i-2) for i in range(2,n))
            fp_dots.append(fpd)
            fpp_dots.append(fppd)
        rhs = [flow_rhs(R_eval[j], g, fp_dots[j], fpp_dots[j]) for j in range(n)]
        new_betas = [sum(Ainv_rows[i][j]*rhs[j] for j in range(n)) for i in range(n)]
        mx = max(abs(new_betas[i]-betas[i]) for i in range(n))
        betas = new_betas
        if mx < 1e-25: break
    return betas

def get_eval_points(n):
    pts = []
    for i in range(n):
        x = i * 2.5 / max(n-1, 1)
        if x > 2.8: x += 0.5
        if x > 3.8: x += 0.5
        pts.append(x)
    return pts

def stability_matrix(g, nmax, eps=1e-7):
    n = nmax+1
    M = [[0.0]*n for _ in range(n)]
    for j in range(n):
        gp = list(g); gp[j]+=eps
        gm = list(g); gm[j]-=eps
        bp = extract_betas(gp, nmax)
        bm = extract_betas(gm, nmax)
        for i in range(n):
            M[i][j] = (bp[i]-bm[i])/(2*eps)
    return M

def eigenvalues_2x2(M):
    tr = M[0][0]+M[1][1]
    det = M[0][0]*M[1][1]-M[0][1]*M[1][0]
    disc = tr*tr-4*det
    if disc >= 0:
        sq = math.sqrt(disc)
        return [-(tr+sq)/2, -(tr-sq)/2]
    else:
        sq = math.sqrt(-disc)
        return [complex(-tr/2, sq/2), complex(-tr/2, -sq/2)]

if __name__ == '__main__':
    print('='*70)
    print('f(R) BETA FUNCTIONS - SELF-CONSISTENT EXTRACTION')
    print('='*70)

    fp_data = {
        1: [5.226e-3, -20.140e-3],
        2: [3.292e-3, -12.726e-3, 1.514e-3],
        3: [5.184e-3, -19.596e-3, 0.702e-3, -9.682e-3],
        4: [5.059e-3, -20.585e-3, 0.270e-3, -10.967e-3, -8.646e-3],
    }

    for nmax in [1, 2, 3, 4]:
        g_fp = fp_data[nmax]
        n = nmax+1
        Rpts = get_eval_points(n)
        b = extract_betas(g_fp, nmax, Rpts)
        res = math.sqrt(sum(x**2 for x in b))
        strs = ', '.join('%.4e'%x for x in b)
        print(f'n={nmax}: betas=[{strs}], residual={res:.4e}')

    print()
    print('='*70)
    print('STABILITY MATRIX (n=4)')
    print('='*70)
    g4 = fp_data[4]
    M = stability_matrix(g4, 4, eps=1e-7)
    for i in range(5):
        row = ', '.join('%.4e'%M[i][j] for j in range(5))
        print(f'  [{row}]')

    ev = eigenvalues_2x2(M[:2][:2])
    print(f'First 2 eigenvalues: {ev}')
