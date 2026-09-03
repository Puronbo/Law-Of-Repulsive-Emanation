import numpy as np
from model import Linear, SelfAttention, FoldedReLU

class FoldedMLP:
    """MLP using the folded-pair activation instead of plain ReLU."""
    def __init__(self, d_model, d_hidden):
        self.lin1 = Linear(d_model, d_hidden)
        self.act = FoldedReLU()
        self.lin_u = Linear(d_hidden, d_model)  # separate output weights for u,v branches
        self.lin_v = Linear(d_hidden, d_model)

    def forward(self, x):
        h = self.lin1.forward(x)
        u,v = self.act.forward(h)
        out_u = self.lin_u.forward(u)
        out_v = self.lin_v.forward(v)
        return out_u + out_v

    def backward(self, dout):
        du = self.lin_u.backward(dout)
        dv = self.lin_v.backward(dout)
        dh = self.act.backward(du, dv)
        dx = self.lin1.backward(dh)
        return dx

    def params(self):
        return [(self.lin1,'W'),(self.lin1,'b'),(self.lin_u,'W'),(self.lin_u,'b'),
                (self.lin_v,'W'),(self.lin_v,'b')]

class TransformerBlock:
    def __init__(self, d_model, d_hidden):
        self.attn = SelfAttention(d_model)
        self.mlp = FoldedMLP(d_model, d_hidden)

    def forward(self, X):
        self.X0 = X
        a = self.attn.forward(X)
        self.X1 = X + a               # residual 1
        m = self.mlp.forward(self.X1)
        self.X2 = self.X1 + m         # residual 2
        return self.X2

    def backward(self, dX2):
        dX1_b = dX2                          # through residual 2 identity path
        dm = dX2                             # into mlp
        dX1_a = self.mlp.backward(dm)
        dX1 = dX1_b + dX1_a
        dX0_b = dX1                          # through residual 1 identity path
        da = dX1
        dX0_a = self.attn.backward(da)
        dX0 = dX0_b + dX0_a
        return dX0
