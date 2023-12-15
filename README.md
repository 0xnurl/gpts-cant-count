# GPTs can't count 🎲 

### Demo of even the most advanced LLMs' inability to handle basic arithmetic.

For a theory about what might be the source of this and how it could be fixed, see [Minimum Description Length Recurrent Neural Networks](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00489/112499/Minimum-Description-Length-Recurrent-Neural).

The script runs a binary search of all number combinations in a range, using the template `a{op}b=`, e.g.:
```
17+950=
```

until a first pair of numbers `a`, `b` yields a wrong answer. 

Currently uses OpenAI's latest model, `gpt-3.5-turbo-instruct`.

### Example: addition

```bash
python cant_count.py --min 1000 --max 1100 --max_attempts 20 --op "+"
```

Output:
```
Running binary search from 1,000 to 1,100, operator '+'... 
1,000 + 1,000 correct.                                     
1,050 + 1,050 correct.                                     
...
1,100 + 1,060 correct.                                     
1,100 + 1,080 correct.                                     
1,100 + 1,090 INCORRECT!!!                                 
Model answered: '2180'.                                    
Correct answer was: 2,190.
```

### Example: multiplication

```bash
python cant_count.py --min 1000 --max 1100 --max_attempts 20 --op "*"
```

Output:
```
Running binary search from 1,000 to 1,100...                  
1,000 * 1,000 correct.                                        
1,050 * 1,050 correct.                                        
1,075 * 1,075 correct.                                        
1,088 * 1,037 INCORRECT!!!                                    
Model answered: 'The product of 1088 and 1037 is 1,127,456.'.  
Correct answer was: 1,128,256.                                
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
python cant_count.py --min 1000 --max 1100 --max_attempts 20 --op "+"
```

Available operators: `+`, `-`, `*`.

* Note that OpenAI model responses are nondeterministic, results may vary.