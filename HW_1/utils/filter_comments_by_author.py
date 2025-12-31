from typing import List

from models.comment import Comment
from models.user import User


def filter_comments_by_author(comments: List[Comment], author: User) -> List[Comment]:
    filter_comments = [comment for comment in comments if comment.author_id == author.id]
    return filter_comments
