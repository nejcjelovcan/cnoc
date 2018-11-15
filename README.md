# Contains No Contains

This is a `ply` lexer and compiler for a very basic language that describes what should and what shouldnt be present in a string.

```sql
"python" and ("compiler" or "lexer") and not "snake"
```

```python
In [1]: from cnoc import match

In [2]: match('"python" and ("compiler" or "lexer") and not "snake"', 'test')
Out[2]: False

In [3]: match('"python" and ("compiler" or "lexer") and not "snake"', 'python compiler')
Out[3]: True

In [4]: match('"python" and ("compiler" or "lexer") and not "snake"', 'python snake')
Out[4]: False
```


# Usage

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 tests.py
```
