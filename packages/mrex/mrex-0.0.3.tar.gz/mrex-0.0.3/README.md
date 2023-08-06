# Magic Regex

Read and write regular expressions easily.

```python
import mrex
id_re = mrex.exactly('id: ').and_(mrex.DIGITS.group_as('id'))
print(id_re.find('id: 12345').group('id'))  # prints '12345'
```

# Installation

```bash
pip install mrex
```

# Thanks

Project influenced by [magic-regexp](https://github.com/danielroe/magic-regexp).
