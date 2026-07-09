from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class User:
    user_id: str
    username: str
    password_hash: str
    email: str
    phone: str
    role: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    created_at: str = ''
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(
            user_id=data.get('user_id', ''),
            username=data.get('username', ''),
            password_hash=data.get('password_hash', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            role=data.get('role', 'loser'),
            nickname=data.get('nickname'),
            avatar=data.get('avatar'),
            bio=data.get('bio'),
            created_at=data.get('created_at', '')
        )
    
    def is_admin(self) -> bool:
        return self.role == 'admin'
    
    def is_loser(self) -> bool:
        return self.role == 'loser'
    
    def is_finder(self) -> bool:
        return self.role == 'finder'
    
    def toggle_role(self) -> None:
        if self.role == 'loser':
            self.role = 'finder'
        elif self.role == 'finder':
            self.role = 'loser'