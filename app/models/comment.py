from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Comment:
    comment_id: str
    item_id: str
    user_id: str
    content: str
    create_time: str
    is_deleted: bool = False
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Comment':
        return cls(
            comment_id=data.get('comment_id', ''),
            item_id=data.get('item_id', ''),
            user_id=data.get('user_id', ''),
            content=data.get('content', ''),
            create_time=data.get('create_time', ''),
            is_deleted=data.get('is_deleted', False)
        )
    
    def soft_delete(self) -> None:
        self.is_deleted = True