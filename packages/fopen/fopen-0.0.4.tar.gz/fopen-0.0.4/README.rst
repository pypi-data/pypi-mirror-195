.. code-block:: console

    pip install fopen

.. code-block:: python

    from fopen import Fopen

    f = Fopen("file.json")
    parsed = f.load()

    f = Fopen("file.toml")
    parsed = f.load()

    f = Fopen("file.csv")
    for line in f.load_lines():
        parsed = line

    f = Fopen("file.jsonl")
    for line in f.load_lines():
        parsed = line

The above is roughly equivalent to this:

.. code-block:: python

    import json
    import toml
    import csv

    with open("file.json", "r", encoding="utf-8") as f:
        parsed = json.load(f)

    with open("file.toml", "r", encoding="utf-8") as f:
        parsed = toml.load(f)

    with open("file.csv", "r", encoding="utf-8") as f:
        for line in csv.reader(f):
            parsed = line

    with open("file.jsonl", "r", encoding="utf-8") as f:
        for line in f.readlines():
            parsed = json.loads(line)
