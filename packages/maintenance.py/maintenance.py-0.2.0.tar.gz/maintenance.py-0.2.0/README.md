# maintenance.py: Utilities for Maintenance

## Usage

```python
todo(fn: Optional[Callable[P, R]] = None) -> Callable[P, NoReturn] | NoReturn
```

```python
deprecated(
    message: Optional[str] = None,
    *,
    since: Optional[str] = None,
    new: Any = None,
    add_sphinx_directive: bool = False
) -> Callable[[Callable[P, R]], Callable[P, R]]
```

### Parameters

message
> Overrides the default warn message.

since
> The version since when the object is deprecated.

new
> The new object that replaces the deprecated one. This may be
> the object itself or its name as a string.

add_sphinx_directive
> Adds the
> [deprecated directive](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directiveshtml#directive-deprecated)
> to the beginning of the docstring of the object.

### Examples
```python
def new():
    return 1

@deprecated(since="1.2.3.post4", new=new)
def old():
    return None
```

```python
unstable(
    message: Optional[str] = None,
    *,
    until: Optional[str] = None
) -> Callable[[Callable[P, R]], Callable[P, R]]
```


## Links

* [Source Code](https://github.com/phoenixr-codes/maintenance.py)
* [PyPI](https://pypi.org/project/maintenance.py)
