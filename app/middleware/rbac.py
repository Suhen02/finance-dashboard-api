from fastapi import Request
from app.exceptions.app_exception import AppException
from app.models.user import UserRole

ROLE_HIERARCHY = {UserRole.viewer: 1, UserRole.analyst: 2, UserRole.admin: 3}

def require_role(min_role: UserRole):
    """Dependency that enforces minimum role level via X-User-Id and X-User-Role headers.
    
    NOTE: In production, replace header-based RBAC with JWT token validation.
    Headers can be spoofed — this is for demonstration purposes only.
    """
    def dependency(request: Request):
        user_id = request.headers.get("X-User-Id")
        user_role = request.headers.get("X-User-Role")
        if not user_id or not user_role:
            raise AppException("Missing RBAC headers (X-User-Id, X-User-Role)", 401)
        try:
            user_id_int = int(user_id)
        except ValueError:
            raise AppException("X-User-Id must be an integer", 400)
        try:
            role_enum = UserRole(user_role)
        except ValueError:
            raise AppException(f"Invalid role: {user_role}. Must be one of: viewer, analyst, admin", 400)
        if ROLE_HIERARCHY.get(role_enum, 0) < ROLE_HIERARCHY.get(min_role, 0):
            raise AppException(f"Insufficient permissions. Required: {min_role.value}, got: {user_role}", 403)
        request.state.user_id = user_id_int
        request.state.user_role = user_role
    return dependency
