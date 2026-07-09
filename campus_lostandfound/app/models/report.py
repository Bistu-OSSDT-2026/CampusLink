from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Report:
    report_id: str
    reporter_id: str
    item_id: str
    reason: str
    detail: str
    create_time: str
    status: str = 'pending'
    handle_time: Optional[str] = None
    handle_result: Optional[str] = None
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Report':
        return cls(
            report_id=data.get('report_id', ''),
            reporter_id=data.get('reporter_id', ''),
            item_id=data.get('item_id', ''),
            reason=data.get('reason', ''),
            detail=data.get('detail', ''),
            create_time=data.get('create_time', ''),
            status=data.get('status', 'pending'),
            handle_time=data.get('handle_time'),
            handle_result=data.get('handle_result')
        )
    
    def approve(self, result: str) -> None:
        self.status = 'approved'
        self.handle_result = result
    
    def reject(self, result: str) -> None:
        self.status = 'rejected'
        self.handle_result = result