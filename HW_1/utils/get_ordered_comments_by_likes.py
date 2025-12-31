from typing import List

from models.comment import Comment


def get_ordered_comments_by_likes(comments: List[Comment]) -> List[Comment]:
    ordered_comments = sorted(comments, key=lambda com: com.like_count, reverse=True)
    return ordered_comments
