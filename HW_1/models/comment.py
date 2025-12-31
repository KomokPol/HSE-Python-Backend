from datetime import datetime
from uuid import UUID


class Comment:
    author_id: UUID
    text: str
    create_data: datetime
    update_data: datetime
    like_count: int

    def __init__(self, author_id: UUID, text: str) -> None:
        self.author_id = author_id
        self.text = text
        self.create_data = datetime.now()
        self.update_data = self.create_data
        self.like_count = 0

    def edit_comment(self, new_text: str) -> None:
        self.text = new_text
        self.update_data = datetime.now()

    def like(self) -> None:
        self.like_count += 1
        self.update_data = datetime.now()

    def dislike(self) -> None:
        self.like_count -= 1
        self.update_data = datetime.now()

    def __repr__(self) -> str:
        return f"Присвоен пользователю с ID {self.author_id},\nСодержимое: {self.text},\nДата публикации: {self.create_data},\nКол-во лайков: {self.like_count}\n"
