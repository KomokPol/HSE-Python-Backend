import uuid
from uuid import UUID


class User:
    id: UUID
    name: str
    comments_count: int
    rate: int
    is_banned: bool

    def __init__(self, name: str) -> None:
        self.id = uuid.uuid4()
        self.name = name
        self.comments_count = 0
        self.rate = 0
        self.is_banned = False

    def edit_name(self, new_name: str) -> None:
        self.name = new_name

    def increment_rate(self) -> None:
        self.rate += 1

    def ban_user(self) -> None:
        self.is_banned = True

    def unban_user(self) -> None:
        self.is_banned = False

    def __repr__(self) -> str:
        return f"Пользователь: {self.name} с ID {self.id},\nРейтинг: {self.rate},\nКол-во комментов: {self.comments_count},\nЗабанен: {self.is_banned}\n"
