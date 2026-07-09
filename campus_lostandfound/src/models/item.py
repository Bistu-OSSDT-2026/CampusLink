from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class LostItem:
    item_id: str
    item_name: str
    item_type: str
    description: str
    location: str
    contact_name: str
    contact_phone: str
    report_time: str
    status: str
    image_path: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'LostItem':
        return cls(
            item_id=data.get('item_id', ''),
            item_name=data.get('item_name', ''),
            item_type=data.get('item_type', ''),
            description=data.get('description', ''),
            location=data.get('location', ''),
            contact_name=data.get('contact_name', ''),
            contact_phone=data.get('contact_phone', ''),
            report_time=data.get('report_time', ''),
            status=data.get('status', 'lost'),
            image_path=data.get('image_path')
        )

    def mark_found(self) -> None:
        self.status = 'found'

    def is_lost(self) -> bool:
        return self.status == 'lost'