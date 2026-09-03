"""
A tiny, from-scratch transformer built from the pieces verified in this
conversation:
  - FoldedReLU (CReLU-style paired unit): guarantees no simultaneous dead
    units, uses a mathematically valid subgradient (0.5, inside the proven
    [0,1] subdifferential of ReLU) at the kink instead of an arbitrary patch.
  - He initialization: derived variance-preserving scale, not guessed.
  - Residual connections: the mechanism shown earlier to prevent the
    information-collapse failure mode of a bare nonlinearity.
No autodiff library -- every gradient below is hand-derived and then
gradient-checked against finite differences before being trusted.
"""
import numpy as np

class FoldedReLU:
    """u = ReLU(x), v = ReLU(-x), combined as u - v (an identity-preserving
    'fold') but routed through TWO separate learned output weights, so the
    layer can express both x and |x| style behavior while guaranteeing at
    least one branch is always alive for any nonzero input."""
    def forward(self, x):
        self.x = x
        self.u = np.maximum(x, 0)
        self.v = np.maximum(-x, 0)
        return self.u, self.v

    def backward(self, du, dv):
        # subgradient at 0 set to 0.5 -- proven valid element of [0,1]
        gu = np.where(self.x > 0, 1.0, np.where(self.x < 0, 0.0, 0.5))
        gv = np.where(-self.x > 0, 1.0, np.where(-self.x < 0, 0.0, 0.5))
        dx = du*gu + dv*(-gv)
        return dx


def he_init(fan_in, fan_out):
    return np.random.randn(fan_in, fan_out) * np.sqrt(2.0/fan_in)


class Linear:
    def __init__(self, fan_in, fan_out):
        self.W = he_init(fan_in, fan_out)
        self.b = np.zeros(fan_out)
    def forward(self, x):
        self.x = x
        return x @ self.W + self.b
    def backward(self, dout):
        self.dW = self.x.T @ dout
        self.db = dout.sum(axis=0)
        return dout @ self.W.T


def softmax(z):
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e/e.sum(axis=-1, keepdims=True)


class SelfAttention:
    """Single-head self-attention, from scratch."""
    def __init__(self, d_model):
        self.Wq = he_init(d_model, d_model)
        self.Wk = he_init(d_model, d_model)
        self.Wv = he_init(d_model, d_model)
        self.d = d_model

    def forward(self, X):
        # X: (T, d_model)
        self.X = X
        self.Q = X @ self.Wq
        self.K = X @ self.Wk
        self.V = X @ self.Wv
        scores = self.Q @ self.K.T / np.sqrt(self.d)
        self.A = softmax(scores)     # (T,T)
        out = self.A @ self.V
        return out

    def backward(self, dout):
        T,d = self.X.shape
        dV = self.A.T @ dout
        dA = dout @ self.V.T
        # softmax backward (per row)
        dscores = np.zeros_like(dA)
        for i in range(T):
            a = self.A[i]
            da = dA[i]
            dscores[i] = a*(da - (a*da).sum())
        dscores /= np.sqrt(self.d)
        dQ = dscores @ self.K
        dK = dscores.T @ self.Q
        dX = dQ @ self.Wq.T + dK @ self.Wk.T + dV @ self.Wv.T
        self.dWq = self.X.T @ dQ
        self.dWk = self.X.T @ dK
        self.dWv = self.X.T @ dV
        return dX
