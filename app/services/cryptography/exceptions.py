class CryptoError(Exception):
    """Base exception for crypto errors."""
    pass


class InvalidTokenError(CryptoError):
    """Raised when token cannot be decoded or verified."""
    pass


class InvalidKeyError(CryptoError):
    """Raised when AES key is invalid."""
    pass
