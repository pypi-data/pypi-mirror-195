# flake8-assert-finder

A simple flake8 Plugin that checks if assert is used

The `assert` Keyword is very useful in Python, but has one big problem: Python has a [optimized mode](https://docs.python.org/3/using/cmdline.html?highlight=pythonoptimize#cmdoption-O). When using this, The `assert` Keyword will no longer work, so if you use `assert` in a Library, this can lead to Problems.

You should replace assert with this little function:
```python
def assert_func(expression: bool) -> None:
    """
    The assert keyword is not available when running Python in optimized mode.
    This function is a drop-in replacement.
    See https://docs.python.org/3/using/cmdline.html?highlight=pythonoptimize#cmdoption-O
    """
    if not expression:
        raise AssertionError()
```
This makes sure, your will be working.

If you just write your own Program, which you don't use with the optimized mode or if you use something like [pytest](https://docs.pytest.org), you can use `assert` of course.

This Plugin just checks for the use of the `assert` Keyword. Nothing more.

### List of warnings:

| ID    | Description  |
| ----- | ------------ |
| AF100 | Found assert |
