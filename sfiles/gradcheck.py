import numpy as np
from block import TransformerBlock

np.random.seed(0)
d_model, d_hidden, T = 6, 10, 5
block = TransformerBlock(d_model, d_hidden)
X = np.random.randn(T, d_model)*0.5

def loss_fn(X):
    out = block.forward(X)
    return np.sum(out**2)

# Analytic gradient
out = block.forward(X)
dout = 2*out
dX_analytic = block.backward(dout)

# Numeric gradient check on INPUT X
eps=1e-5
dX_numeric = np.zeros_like(X)
for i in range(T):
    for j in range(d_model):
        Xp = X.copy(); Xp[i,j]+=eps
        Xm = X.copy(); Xm[i,j]-=eps
        dX_numeric[i,j] = (loss_fn(Xp)-loss_fn(Xm))/(2*eps)

print("Gradient check on INPUT X:")
print("  max abs diff:", np.max(np.abs(dX_analytic-dX_numeric)))
print("  relative error:", np.max(np.abs(dX_analytic-dX_numeric))/np.max(np.abs(dX_numeric)))

# Numeric gradient check on a WEIGHT matrix (attn.Wq)
def loss_with_Wq(Wq_new):
    old = block.attn.Wq.copy()
    block.attn.Wq = Wq_new
    L = loss_fn(X)
    block.attn.Wq = old
    return L

out = block.forward(X)
dout = 2*out
block.backward(dout)
dWq_analytic = block.attn.dWq

dWq_numeric = np.zeros_like(block.attn.Wq)
Wq = block.attn.Wq
for i in range(Wq.shape[0]):
    for j in range(Wq.shape[1]):
        Wp = Wq.copy(); Wp[i,j]+=eps
        Wm = Wq.copy(); Wm[i,j]-=eps
        dWq_numeric[i,j] = (loss_with_Wq(Wp)-loss_with_Wq(Wm))/(2*eps)

print()
print("Gradient check on attention Wq:")
print("  max abs diff:", np.max(np.abs(dWq_analytic-dWq_numeric)))
print("  relative error:", np.max(np.abs(dWq_analytic-dWq_numeric))/np.max(np.abs(dWq_numeric)))
