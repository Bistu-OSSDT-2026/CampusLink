from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Message:
    message_id: str
    sender_id: str
    receiver_id: str
    content: str
    create_time: str
    is_read: bool = False
    message_type: str = 'normal'
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Message':
        return cls(
            message_id=data.get('message_id', ''),
            sender_id=data.get('sender_id', ''),
            receiver_id=data.get('receiver_id', ''),
            content=data.get('content', ''),
            create_time=data.get('create_time', ''),
            is_read=data.get('is_read', False),
            message_type=data.get('message_type', 'normal')
        )
    
    def mark_read(self) -> None:
        self.is_read = True