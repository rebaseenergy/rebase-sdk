
class RebaseError(Exception):
    pass


class InvalidUsageError(Exception):
    pass


class NotFoundError(RebaseError):
    """The resource was not found
    """
    pass

class TrainingNotReadyError(RebaseError):
    pass


class AuthenticationError(RebaseError):
    """If your API key was not accepted
    """
    pass


class ApiError(RebaseError):
    """If API returend unexpected error
    """
    pass


class InvalidInputError(RebaseError):
    """Raised when user input results in 400 bad request
    """
