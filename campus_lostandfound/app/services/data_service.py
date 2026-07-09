import json
import os
import threading
from typing import List, Optional
from uuid import uuid4

from app.models.user import User
from app.models.item import LostItem
from app.models.comment import Comment
from app.models.message import Message
from app.models.report import Report

DATA_FILES = ['users.json', 'items.json', 'comments.json', 'messages.json', 'reports.json']


class JSONDataService:
    _lock = threading.Lock()
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            self.data_dir = os.path.join(basedir, 'data')
        else:
            self.data_dir = data_dir
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        os.makedirs(self.data_dir, exist_ok=True)
        
        for filename in DATA_FILES:
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
    
    def _read_file(self, filename: str) -> List[dict]:
        with self._lock:
            filepath = os.path.join(self.data_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
    
    def _write_file(self, filename: str, data: List[dict]):
        with self._lock:
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    
    def generate_id(self) -> str:
        return str(uuid4())[:8]
    
    def add_user(self, user: User):
        users = self._read_file('users.json')
        users.append(user.to_dict())
        self._write_file('users.json', users)
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        users = self._read_file('users.json')
        for u in users:
            if u['user_id'] == user_id:
                return User.from_dict(u)
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        users = self._read_file('users.json')
        for u in users:
            if u['username'] == username:
                return User.from_dict(u)
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        users = self._read_file('users.json')
        for u in users:
            if u['email'] == email:
                return User.from_dict(u)
        return None
    
    def update_user(self, user: User) -> bool:
        users = self._read_file('users.json')
        for i, u in enumerate(users):
            if u['user_id'] == user.user_id:
                users[i] = user.to_dict()
                self._write_file('users.json', users)
                return True
        return False
    
    def delete_user(self, user_id: str) -> bool:
        users = self._read_file('users.json')
        original_count = len(users)
        users = [u for u in users if u['user_id'] != user_id]
        if len(users) != original_count:
            self._write_file('users.json', users)
            return True
        return False
    
    def get_all_users(self) -> List[User]:
        users = self._read_file('users.json')
        return [User.from_dict(u) for u in users]
    
    def add_item(self, item: LostItem):
        items = self._read_file('items.json')
        items.append(item.to_dict())
        self._write_file('items.json', items)
    
    def get_item_by_id(self, item_id: str) -> Optional[LostItem]:
        items = self._read_file('items.json')
        for i in items:
            if i['item_id'] == item_id and not i.get('is_deleted', False):
                return LostItem.from_dict(i)
        return None
    
    def get_all_items(self) -> List[LostItem]:
        items = self._read_file('items.json')
        return [LostItem.from_dict(i) for i in items if not i.get('is_deleted', False)]
    
    def get_items_by_user(self, user_id: str) -> List[LostItem]:
        items = self._read_file('items.json')
        return [LostItem.from_dict(i) for i in items 
                if i['user_id'] == user_id and not i.get('is_deleted', False)]
    
    def update_item(self, item: LostItem) -> bool:
        items = self._read_file('items.json')
        for i, it in enumerate(items):
            if it['item_id'] == item.item_id:
                items[i] = item.to_dict()
                self._write_file('items.json', items)
                return True
        return False
    
    def delete_item(self, item_id: str) -> bool:
        items = self._read_file('items.json')
        original_count = len(items)
        items = [i for i in items if i['item_id'] != item_id]
        if len(items) != original_count:
            self._write_file('items.json', items)
            return True
        return False
    
    def search_items(self, keyword: str = '', item_type: str = '', 
                     status: str = '', location: str = '', sort_by: str = 'time') -> List[LostItem]:
        items = self.get_all_items()
        results = []
        
        for item in items:
            match = True
            if keyword and keyword.lower() not in item.item_name.lower() and \
               keyword.lower() not in item.description.lower():
                match = False
            if item_type and item.item_type != item_type:
                match = False
            if status and item.status != status:
                match = False
            if location and location.lower() not in item.location.lower():
                match = False
            if match:
                results.append(item)
        
        if sort_by == 'time':
            results.sort(key=lambda x: x.report_time, reverse=True)
        elif sort_by == 'name':
            results.sort(key=lambda x: x.item_name)
        
        return results
    
    def get_unverified_items(self) -> List[LostItem]:
        items = self._read_file('items.json')
        return [LostItem.from_dict(i) for i in items 
                if not i.get('is_verified', True) and not i.get('is_deleted', False)]
    
    def add_comment(self, comment: Comment):
        comments = self._read_file('comments.json')
        comments.append(comment.to_dict())
        self._write_file('comments.json', comments)
    
    def get_comments_by_item(self, item_id: str) -> List[Comment]:
        comments = self._read_file('comments.json')
        return [Comment.from_dict(c) for c in comments 
                if c['item_id'] == item_id and not c.get('is_deleted', False)]
    
    def delete_comment(self, comment_id: str) -> bool:
        comments = self._read_file('comments.json')
        original_count = len(comments)
        comments = [c for c in comments if c['comment_id'] != comment_id]
        if len(comments) != original_count:
            self._write_file('comments.json', comments)
            return True
        return False
    
    def add_message(self, message: Message):
        messages = self._read_file('messages.json')
        messages.append(message.to_dict())
        self._write_file('messages.json', messages)
    
    def get_messages_by_receiver(self, receiver_id: str) -> List[Message]:
        messages = self._read_file('messages.json')
        return [Message.from_dict(m) for m in messages if m['receiver_id'] == receiver_id]
    
    def get_unread_messages_count(self, user_id: str) -> int:
        messages = self._read_file('messages.json')
        return sum(1 for m in messages if m['receiver_id'] == user_id and not m.get('is_read', False))
    
    def mark_messages_read(self, user_id: str):
        messages = self._read_file('messages.json')
        for m in messages:
            if m['receiver_id'] == user_id:
                m['is_read'] = True
        self._write_file('messages.json', messages)
    
    def add_report(self, report: Report):
        reports = self._read_file('reports.json')
        reports.append(report.to_dict())
        self._write_file('reports.json', reports)
    
    def get_all_reports(self) -> List[Report]:
        reports = self._read_file('reports.json')
        return [Report.from_dict(r) for r in reports]
    
    def get_pending_reports(self) -> List[Report]:
        reports = self._read_file('reports.json')
        return [Report.from_dict(r) for r in reports if r['status'] == 'pending']
    
    def update_report(self, report: Report) -> bool:
        reports = self._read_file('reports.json')
        for i, r in enumerate(reports):
            if r['report_id'] == report.report_id:
                reports[i] = report.to_dict()
                self._write_file('reports.json', reports)
                return True
        return False
    
    def recommend_items(self, item_id: str, limit: int = 5) -> List[LostItem]:
        target_item = self.get_item_by_id(item_id)
        if not target_item:
            return []
        
        all_items = self.get_all_items()
        candidates = [i for i in all_items if i.item_id != item_id and i.status == 'lost']
        
        def score(item):
            score = 0
            if item.item_type == target_item.item_type:
                score += 5
            if item.location == target_item.location:
                score += 3
            if item.item_name[:2] == target_item.item_name[:2]:
                score += 2
            return score
        
        candidates.sort(key=score, reverse=True)
        return candidates[:limit]
