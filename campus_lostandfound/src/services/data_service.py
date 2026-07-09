import json
import os
from typing import List, Optional
from uuid import uuid4

from src.models.item import LostItem


class DataService:
    def __init__(self, data_file: str = 'data/lost_items.json'):
        self.data_file = data_file
        self._ensure_data_file()

    def _ensure_data_file(self) -> None:
        dir_path = os.path.dirname(self.data_file)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _read_data(self) -> List[dict]:
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_data(self, items: List[dict]) -> None:
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

    def add_item(self, item: LostItem) -> None:
        items = self._read_data()
        items.append(item.to_dict())
        self._write_data(items)

    def get_all_items(self) -> List[LostItem]:
        items_data = self._read_data()
        return [LostItem.from_dict(data) for data in items_data]

    def get_item_by_id(self, item_id: str) -> Optional[LostItem]:
        items = self._read_data()
        for item_data in items:
            if item_data['item_id'] == item_id:
                return LostItem.from_dict(item_data)
        return None

    def update_item(self, updated_item: LostItem) -> bool:
        items = self._read_data()
        for i, item_data in enumerate(items):
            if item_data['item_id'] == updated_item.item_id:
                items[i] = updated_item.to_dict()
                self._write_data(items)
                return True
        return False

    def delete_item(self, item_id: str) -> bool:
        items = self._read_data()
        original_count = len(items)
        items = [item for item in items if item['item_id'] != item_id]
        if len(items) != original_count:
            self._write_data(items)
            return True
        return False

    def search_items(self, keyword: str = '', item_type: str = '', 
                     status: str = '', location: str = '') -> List[LostItem]:
        all_items = self.get_all_items()
        results = []
        
        for item in all_items:
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
        
        return results

    def get_lost_items(self) -> List[LostItem]:
        return [item for item in self.get_all_items() if item.is_lost()]

    def generate_id(self) -> str:
        return str(uuid4())[:8]