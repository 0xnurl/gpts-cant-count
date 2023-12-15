# GPTs can't count

### Demo for even the most advanced LLMs' inability to handle basic arithmetic.

For a theory about what might be the source of this and how it could be fixed, see [Minimum Description Length Recurrent Neural Networks](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00489/112499/Minimum-Description-Length-Recurrent-Neural).

The script runs a binary search of all number combinations in a range, using the prompt `a+b=`, e.g.:
```
17+950=
```

Until a first pair of numbers `a`, `b` is given a wrong answer. 

The script currently uses OpenAI's latest model, `gpt-3.5-turbo-instruct`.

### Example:

```bash
python cant_count.py --min 100000000 --max 100001000 --max_attempts 250
```

Output:
```
>> Running binary search from 100,000,000 to 100,001,000...
100,000,000 + 100,000,000 correct
100,000,500 + 100,000,500 correct
...
100,001,000 + 100,000,877 correct
100,001,000 + 100,000,938 correct
100,001,000 + 100,000,969 INCORRECT !!!
Model answered: '200002969'.
Correct answer was: 200,001,969.
```

## Usage

1. Install the OpenAI API package:

```bash
pip install openai==1.4.0
```

2. Add your OpenAI API Key as environment variable or add directly to script:
```bash
export OPENAI_API_KEY=...
```

3. Run:
```bash
python cant_count.py --min 100000000 --max 100001000 --max_attempts 250
```

* Note that OpenAI model responses are nondeterministic, results may vary.  