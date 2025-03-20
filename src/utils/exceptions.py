class BaseAppException(Exception):
    """Base exception for all application exceptions"""
    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message)


class TaskNotFoundException(BaseAppException):
    """Exception raised when a task is not found"""
    def __init__(self, message="Task not found"):
        super().__init__(message)


class AuthenticationException(BaseAppException):
    """Exception raised when there's an authentication error"""
    def __init__(self, message="Authentication failed"):
        super().__init__(message)


class UnauthorizedAccessException(BaseAppException):
    """Exception raised when a user tries to access a resource without authorization"""
    def __init__(self, message="Unauthorized access"):
        super().__init__(message)


class ValidationException(BaseAppException):
    """Exception raised when there's a data validation error"""
    def __init__(self, message="Validation error", errors=None):
        self.errors = errors or {}
        super().__init__(message)


class DatabaseException(BaseAppException):
    """Exception raised when there's a database-related error"""
    def __init__(self, message="Database error"):
        super().__init__(message)


class ServiceException(BaseAppException):
    """Exception raised when there's an error in the service layer"""
    def __init__(self, message="Service error"):
        super().__init__(message)