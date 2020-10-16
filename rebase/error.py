
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
