from fastapi import HTTPException, status


class AppError:
    INVALID_CREDENTIALS_ERROR = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    USERNAME_ALREADY_EXISTS_ERROR = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Username already exists",
        headers={"WWW-Authenticate": "Bearer"},
    )

    PASSWORD_MISMATCH_ERROR = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Password does not match",
        headers={"WWW-Authenticate": "Bearer"},
    )
