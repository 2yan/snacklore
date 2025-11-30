"""Error handling utilities."""


class ValidationError(Exception):
    """Custom validation error."""
    pass


class NotFoundError(Exception):
    """Custom not found error."""
    pass


class PermissionError(Exception):
    """Custom permission error."""
    pass


def format_error_response(error, message, details=None):
    """Format error response."""
    response = {
        'error': error,
        'message': message
    }
    if details:
        response['details'] = details
    return response


