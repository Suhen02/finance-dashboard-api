from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.exceptions.app_exception import AppException
from app.utils.logger import get_logger

logger = get_logger(__name__)

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def is_bootstrap(self) -> bool:
        return self.repo.count() == 0

    def create_user(self, data: UserCreate, caller_role: str | None = None) -> User:
        if not self.is_bootstrap():
            if caller_role != UserRole.admin.value:
                raise AppException("Only admin can create users", 403)
        if self.repo.get_by_email(data.email):
            raise AppException("Email already registered", 409)
        user = User(name=data.name, email=data.email, role=data.role, status=data.status)
        logger.info(f"Creating user: {data.email}")
        return self.repo.create(user)

    def get_users(self) -> list[User]:
        return self.repo.get_all()

    def update_user(self, user_id: int, data: UserUpdate) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise AppException("User not found", 404)
        update_data = data.model_dump(exclude_unset=True)
        if "email" in update_data and update_data["email"]:
            existing = self.repo.get_by_email(update_data["email"])
            if existing and existing.id != user_id:
                raise AppException("Email already taken", 409)
        return self.repo.update(user, update_data)
