"""Part 1: Core functions for the 5-panel phase portrait."""
import math
import numpy as np

def beta_Ib(G, lam):
    pi = math.pi
    w2 = (1.0 - 2.0*lam)**2
    denom = w2 - (29.0 - 9.0*lam)/(72.0*pi) * G
    if abs(denom) < 1e-30:
        return 0.0, 0.0
    num_lam = ((12.0 - 33.0*lam + 20.0*lam**2 - 200.0*lam**3)*G
               + (467.0 - 572.0*lam)/(12.0*pi) * G**2)
    num_G = (105.0 - 212.0*lam + 200.0*lam**2) * G**2
    bl = -2.0*lam + (1.0/(24.0*pi)) * num_lam / denom
    bG = 2.0*G - (1.0/(24.0*pi)) * num_G / denom
    return bG, bl

def find_fp():
    best = (1e30, 0, 0)
    for i in range(1, 300):
        for j in range(1, 49):
            G0, l0 = i/100.0, j/100.0
            for _ in range(200):
                bG, bl = beta_Ib(G0, l0)
                if abs(bG)+abs(bl) < 1e-14: break
                eps = 1e-8
                M00 = (beta_Ib(G0+eps,l0)[0]-bG)/eps
                M01 = (beta_Ib(G0,l0+eps)[0]-bG)/eps
                M10 = (beta_Ib(G0+eps,l0)[1]-bl)/eps
                M11 = (beta_Ib(G0,l0+eps)[1]-bl)/eps
                det = M00*M11-M01*M10
                if abs(det)<1e-30: break
                dG = -(M11*bG-M01*bl)/det
                dl = -(-M10*bG+M00*bl)/det
                G0 += dG; l0 += dl
                if l0>=0.5 or l0<=-0.01 or G0<=0: break
            if l0>0 and l0<0.5 and G0>0:
                bG2, bl2 = beta_Ib(G0, l0)
                res = bG2**2+bl2**2
                if res < best[0]:
                    best = (res, G0, l0)
    return best

def stability_matrix(G, lam):
    eps = 1e-7
    bG0, bl0 = beta_Ib(G, lam)
    return [[(beta_Ib(G+eps,lam)[0]-bG0)/eps, (beta_Ib(G,lam+eps)[0]-bG0)/eps],
            [(beta_Ib(G+eps,lam)[1]-bl0)/eps, (beta_Ib(G,lam+eps)[1]-bl0)/eps]]

def rk4_step(G, lam, dt):
    def f(g, l): return beta_Ib(g, l)
    k1 = f(G, lam)
    k2 = f(G+0.5*dt*k1[0], lam+0.5*dt*k1[1])
    k3 = f(G+0.5*dt*k2[0], lam+0.5*dt*k2[1])
    k4 = f(G+dt*k3[0], lam+dt*k3[1])
    return (G+(dt/6)*(k1[0]+2*k2[0]+2*k3[0]+k4[0]),
            lam+(dt/6)*(k1[1]+2*k2[1]+2*k3[1]+k4[1]))

def integrate(G0, l0, dt, nsteps):
    G, lam = G0, l0
    traj = [(G, lam)]
    for _ in range(nsteps):
        G, lam = rk4_step(G, lam, dt)
        if G <= 0 or lam >= 0.5 or lam < -0.1: break
        traj.append((G, lam))
    return traj
