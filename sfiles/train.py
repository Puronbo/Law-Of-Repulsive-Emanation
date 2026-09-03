import numpy as np
from model import Linear, he_init, softmax
from block import TransformerBlock

np.random.seed(0)
VOCAB = 4
T = 4          # sequence length
D = 16         # model dimension
H = 32         # mlp hidden dim

# task: REVERSE a length-4 sequence of symbols from a small vocab.
# (chosen because it genuinely requires attention -- a copy task wouldn't.)
def sample_example():
    seq = np.random.randint(0, VOCAB, size=T)
    target = seq[::-1].copy()
    return seq, target

embed = he_init(VOCAB, D)                  # token embedding table
pos = he_init(T, D)*0.1                    # positional embedding
block = TransformerBlock(D, H)
out_proj = Linear(D, VOCAB)

params = [embed, pos]
def all_linear_layers():
    return [block.attn, block.mlp.lin1, block.mlp.lin_u, block.mlp.lin_v, out_proj]

def forward(seq):
    X = embed[seq] + pos                   # (T,D)
    Z = block.forward(X)
    logits = out_proj.forward(Z)           # (T,VOCAB)
    return logits, X

def loss_and_grad(seq, target):
    logits, X = forward(seq)
    probs = softmax(logits)
    onehot = np.zeros_like(probs)
    onehot[np.arange(T), target] = 1
    loss = -np.mean(np.sum(onehot*np.log(probs+1e-9), axis=1))
    dlogits = (probs - onehot)/T

    dZ = out_proj.backward(dlogits)
    dX = block.backward(dZ)

    d_embed = np.zeros_like(embed)
    for t in range(T):
        d_embed[seq[t]] += dX[t]
    d_pos = dX.copy()
    return loss, d_embed, d_pos

lr = 0.05
losses=[]
for step in range(4001):
    seq, target = sample_example()
    loss, d_embed, d_pos = loss_and_grad(seq, target)
    losses.append(loss)

    embed -= lr*d_embed
    pos   -= lr*d_pos
    block.attn.Wq -= lr*block.attn.dWq
    block.attn.Wk -= lr*block.attn.dWk
    block.attn.Wv -= lr*block.attn.dWv
    for layer in [block.mlp.lin1, block.mlp.lin_u, block.mlp.lin_v, out_proj]:
        layer.W -= lr*layer.dW
        layer.b -= lr*layer.db

    if step%500==0:
        recent = np.mean(losses[-100:])
        print(f"step {step:5d}: loss={recent:.4f}")

print()
print("Test on 10 fresh random sequences:")
correct=0
for _ in range(200):
    seq, target = sample_example()
    logits,_ = forward(seq)
    pred = np.argmax(logits, axis=1)
    correct += np.all(pred==target)
print(f"exact-sequence accuracy on 200 fresh test examples: {correct}/200")
