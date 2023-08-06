# pyminmax
``minmax(x)`` is equivalent to ``(min(x), max(x))``, except that it requires
only one pass through the argument(s), as opposed to two. It is written in C,
adapted straight from CPython's implementation of ``min()`` and ``max()``.
## Installation
```
pip install pyminmax
```
## Usage
```python3
>>> from pyminmax import minmax
>>> minmax([5, 2, 0, 100, -100, 10])
(-100, 100)
```
## Test
Once installed, run the test suite via
```
python -m unittest pyminmax.tests --verbose
```
