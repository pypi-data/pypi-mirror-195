from typing import Generic, Optional, TypeVar, Set, Type

T = TypeVar('T')
E = TypeVar('E')


class Result(Generic[T, E]):
    """
    Allows to hand exceptions across thread boundaries conveniently by wrapping them into a result object. Use the
    classmethod factories to produce expressive code i.e.:

    >>> def everything_went_fine():
    ...     return Result.ok(42)

    >>> def something_went_wrong():
    ...     return Result.error(RuntimeError("Something bad has happened"))

    >>> everything_went_fine().unwrap()
    42
    >>> something_went_wrong().is_error()
    True
    >>> something_went_wrong().unwrap()
    Traceback (most recent call last):
      ...
    RuntimeError: Something bad has happened
    """

    def __init__(self, value: Optional[T] = None, error: Optional[E] = None, ignored: Optional[E] = None):
        """
        @param value: value of a valid result
        @param error: error of an invalid result
        @param ignored: ignored error
        """
        self._value = value
        self._error = error
        self._ignored = ignored

    @classmethod
    def ok(cls, value: T) -> "Result":
        """
        Factory method creating a valid Result object
        @param value: value of the valid result
        @return: Result object containing the value

        >>> Result.ok(42)
        Result(value=42)
        """
        return cls(value=value)

    @classmethod
    def error(cls, error: E) -> "Result":
        """
        Factory method creating an invalid Result object
        @param error: error which caused the result to be invalid
        @return: Result object containing an error

        >>> Result.error(RuntimeError("Something bad has happened"))
        Result(error=RuntimeError('Something bad has happened'))
        """
        return cls(error=error)

    @classmethod
    def ignored(cls, error: E) -> "Result":
        """
        Factory method creating an error Result object where the error has been ignored
        @param error: error which has been ignored
        @return: Result object containing an ignored error

        >>> Result.ignored(RuntimeError("Something bad has happened"))
        Result(ignored=RuntimeError('Something bad has happened'))
        """
        return cls(ignored=error)

    def unwrap(self) -> T:
        """
        Extract the value of a valid Result object, and throws the set error if it is invalid i.e.:
        @return: value of valid object

        >>> Result.ok(42).unwrap()
        42
        >>> Result.error(RuntimeError("Something bad has happened")).unwrap()
        Traceback (most recent call last):
          ...
        RuntimeError: Something bad has happened
        """
        if self.is_error():
            raise self._error
        return self._value

    def ignore(self, exceptions: Set[Type[E]]) -> "Result":
        """
        Ignore specified exception errors and return new Result object with ignored errors if they match.
        @param exceptions: set of exception types to be ignored
        @return: new result object with exceptions ignored if they match

        >>> Result.error(RuntimeError("An error to be ignored")).ignored({RuntimeError}).unwrap()

        """
        if self.is_error() and type(self._error) in exceptions:
            return Result.ignored(self._error)
        return self

    def is_error(self) -> bool:
        """
        Returns true if an error has been set, and the Result object is invalid
        @return: boolean
        """
        return self._error is not None

    def is_ignored(self) -> bool:
        """
        Returns true if an error has been ignored, and the Result object is invalid
        @return: boolean
        """
        return self._ignored is not None

    def report_error(self) -> str:
        """
        Report the error's string representation.
        @return: string representing the error

        >>> Result.error(RuntimeError("Error report")).report_error()
        'Error report'
        """
        return str(self._error)

    def __repr__(self):
        if self.is_error():
            return f"Result(error={self._error!r})"
        elif self.is_ignored():
            return f"Result(ignored={self._ignored!r})"
        else:
            return f"Result(value={self._value!r})"
