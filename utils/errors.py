class CustomError(Exception):
    """Base class for custom errors."""

    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f"{self.message} (status code: {self.status_code})"

class NotFoundError(CustomError):
    """Error for not found resources."""

    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)

class BadRequestError(CustomError):
    """Error for invalid requests."""

    def __init__(self, message="Bad request"):
        super().__init__(message, 400)

class UnauthorizedError(CustomError):
    """Error for unauthorized access."""

    def __init__(self, message="Unauthorized"):
        super().__init__(message, 401)

class ForbiddenError(CustomError):
    """Error for forbidden actions."""

    def __init__(self, message="Forbidden"):
        super().__init__(message, 403)

class InternalServerError(CustomError):
    """Error for internal server errors."""

    def __init__(self, message="Internal server error"):
        super().__init__(message, 500)