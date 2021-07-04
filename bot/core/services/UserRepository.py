from bot.core.services.EntityRepository import EntityRepository
from bot.core.models.sqlalchemy.User import User


class UserRepository(EntityRepository[User]):
    def __init__(self):
        super(UserRepository, self).__init__()
        self._user = self.session.query(User)

    def add(self, user: User):
        pass

    def update(self, user: User):
        pass

    def delete(self, user: User):
        pass

    def get(self, user: User):
        pass

    def exists(self, user: User) -> bool:
        pass
