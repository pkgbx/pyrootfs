"""
This module contains all related error
classes and utilities used within the project.
"""
class PyRootFSError(Exception):
    """
    Base error class, all specialized error classes
    should inherit from this one.
    """
    def __init__(self, message: str, code: int = 1) -> None:
        """
        Create a new error instance with a message string and an optional error code.

        The error code defaults to 1.
        """
        super(PyRootFSError, self).__init__(message)

        self.message = message
        self.code = code

    def __str__(self) -> str:
        """
        Return a user friendly representation of the error.
        """
        return f'[ERR] {self.message}'

    def __repr__(self) -> str:
        """
        Return a "not so much" user friendly representation of the error.
        """
        c = self.__class__.__name__
        return f'{c}("{self.message}", code={self.code})'
