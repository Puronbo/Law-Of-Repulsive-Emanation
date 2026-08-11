"""Example plug-and-play functions: drop a decorated function in this
directory and it appears in the web UI, the CLI, and the tests.

Two styles are shown:
  - ``add``      declares its params explicitly (Param objects)
  - ``greet``    declares nothing - the signature's type hints + defaults
                 become the form fields automatically

Run them programmatically:
    from puno_flow.plugin import run
    run("add", {"a": 2.5, "b": 3.5})        -> {"sum": 6.0, "text": "2.5 + 3.5 = 6.0"}
    run("greet", {"name": "world"})         -> "hello, world!"

Any return value works: the registry normalizes numpy arrays, sets, tuples,
dataclasses, and nested dicts to JSON-safe values before the UI renders it.
"""

from puno_flow.plugin import param, plugin


@plugin(title="Add two numbers",
        description="Adds a and b and shows the sum and the equation.",
        params=[param("a", float, 0.0, "first operand"),
                param("b", float, 0.0, "second operand")])
def add(a=0.0, b=0.0):
    return {"sum": a + b, "text": "%s + %s = %s" % (a, b, a + b)}


@plugin(title="Greet a name",
        description="Returns a friendly greeting. Params auto-derived.")
def greet(name="world", excited=True, times=1):
    msg = "hello, %s!" % name
    if excited:
        msg = msg.upper()
    return {"greeting": (msg + " ") * times, "excited": excited}


@plugin(title="Collatz steps",
        description="Number of steps to reach 1 from n (Collatz conjecture).")
def collatz(n=27):
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return {"steps": steps}


@plugin(title="Word frequency",
        description="Token frequencies in a text (returns a dict, sets, "
                    "and tuples to show JSON normalization).")
def word_freq(text="the quick brown fox jumps over the lazy dog"):
    import re
    words = re.findall(r"[a-z']+", text.lower())
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    uniq = set(words)
    return {"frequencies": freq, "unique_count": len(uniq),
            "first_three": tuple(words[:3])}
