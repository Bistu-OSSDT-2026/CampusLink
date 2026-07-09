import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from src.services.data_service import DataService
from src.models.item import LostItem


class TestDataService:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_file = os.path.join(self.temp_dir, 'test_data.json')
        self.service = DataService(self.test_data_file)
        
        self.test_item = LostItem(
            item_id='test1234',
            item_name='手机',
            item_type='电子产品',
            description='黑色iPhone 14',
            location='图书馆三楼',
            contact_name='张三',
            contact_phone='13800138000',
            report_time='2024-01-15 10:30:00',
            status='lost'
        )

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_add_item(self):
        self.service.add_item(self.test_item)
        items = self.service.get_all_items()
        
        assert len(items) == 1
        assert items[0].item_id == 'test1234'
        assert items[0].item_name == '手机'

    def test_get_all_items_empty(self):
        items = self.service.get_all_items()
        assert len(items) == 0

    def test_get_item_by_id(self):
        self.service.add_item(self.test_item)
        
        item = self.service.get_item_by_id('test1234')
        assert item is not None
        assert item.item_name == '手机'
        
        not_found = self.service.get_item_by_id('nonexistent')
        assert not_found is None

    def test_update_item(self):
        self.service.add_item(self.test_item)
        
        self.test_item.item_name = '更新后的手机'
        result = self.service.update_item(self.test_item)
        
        assert result is True
        
        updated_item = self.service.get_item_by_id('test1234')
        assert updated_item.item_name == '更新后的手机'

    def test_update_item_not_found(self):
        result = self.service.update_item(self.test_item)
        assert result is False

    def test_delete_item(self):
        self.service.add_item(self.test_item)
        
        result = self.service.delete_item('test1234')
        assert result is True
        
        items = self.service.get_all_items()
        assert len(items) == 0

    def test_delete_item_not_found(self):
        result = self.service.delete_item('nonexistent')
        assert result is False

    def test_search_by_keyword(self):
        self.service.add_item(self.test_item)
        
        item2 = LostItem(
            item_id='test5678',
            item_name='笔记本电脑',
            item_type='电子产品',
            description='银色MacBook Pro',
            location='教学楼A栋',
            contact_name='李四',
            contact_phone='13900139000',
            report_time='2024-01-15 11:00:00',
            status='lost'
        )
        self.service.add_item(item2)
        
        results = self.service.search_items(keyword='手机')
        assert len(results) == 1
        assert results[0].item_name == '手机'

    def test_search_by_type(self):
        self.service.add_item(self.test_item)
        
        item2 = LostItem(
            item_id='test5678',
            item_name='学生证',
            item_type='证件卡类',
            description='计算机学院学生证',
            location='食堂',
            contact_name='王五',
            contact_phone='13700137000',
            report_time='2024-01-15 12:00:00',
            status='lost'
        )
        self.service.add_item(item2)
        
        results = self.service.search_items(item_type='电子产品')
        assert len(results) == 1
        assert results[0].item_name == '手机'

    def test_search_by_status(self):
        self.service.add_item(self.test_item)
        
        found_item = LostItem(
            item_id='test5678',
            item_name='书包',
            item_type='生活用品',
            description='蓝色双肩包',
            location='操场',
            contact_name='赵六',
            contact_phone='13600136000',
            report_time='2024-01-15 09:00:00',
            status='found'
        )
        self.service.add_item(found_item)
        
        lost_items = self.service.search_items(status='lost')
        assert len(lost_items) == 1
        assert lost_items[0].item_name == '手机'
        
        found_items = self.service.search_items(status='found')
        assert len(found_items) == 1
        assert found_items[0].item_name == '书包'

    def test_get_lost_items(self):
        self.service.add_item(self.test_item)
        
        found_item = LostItem(
            item_id='test5678',
            item_name='书包',
            item_type='生活用品',
            description='',
            location='',
            contact_name='',
            contact_phone='',
            report_time='',
            status='found'
        )
        self.service.add_item(found_item)
        
        lost_items = self.service.get_lost_items()
        assert len(lost_items) == 1
        assert lost_items[0].item_name == '手机'

    def test_generate_id(self):
        id1 = self.service.generate_id()
        id2 = self.service.generate_id()
        
        assert len(id1) == 8
        assert len(id2) == 8
        assert id1 != id2

    def test_search_combined_filters(self):
        self.service.add_item(self.test_item)
        
        item2 = LostItem(
            item_id='test5678',
            item_name='耳机',
            item_type='电子产品',
            description='白色AirPods',
            location='图书馆',
            contact_name='李四',
            contact_phone='13900139000',
            report_time='2024-01-15 11:00:00',
            status='lost'
        )
        self.service.add_item(item2)
        
        results = self.service.search_items(location='图书馆', item_type='电子产品')
        assert len(results) == 2
        
        results = self.service.search_items(location='三楼', item_type='电子产品')
        assert len(results) == 1
        assert results[0].item_name == '手机'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])