import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from datetime import datetime

from src.models.item import LostItem


def test_item_creation():
    item = LostItem(
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
    
    assert item.item_id == 'test1234'
    assert item.item_name == '手机'
    assert item.item_type == '电子产品'
    assert item.is_lost() is True


def test_item_to_dict():
    item = LostItem(
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
    
    item_dict = item.to_dict()
    
    assert isinstance(item_dict, dict)
    assert item_dict['item_id'] == 'test1234'
    assert item_dict['item_name'] == '手机'
    assert item_dict['status'] == 'lost'


def test_item_from_dict():
    item_dict = {
        'item_id': 'test1234',
        'item_name': '手机',
        'item_type': '电子产品',
        'description': '黑色iPhone 14',
        'location': '图书馆三楼',
        'contact_name': '张三',
        'contact_phone': '13800138000',
        'report_time': '2024-01-15 10:30:00',
        'status': 'lost'
    }
    
    item = LostItem.from_dict(item_dict)
    
    assert isinstance(item, LostItem)
    assert item.item_id == 'test1234'
    assert item.contact_name == '张三'


def test_mark_found():
    item = LostItem(
        item_id='test1234',
        item_name='手机',
        item_type='电子产品',
        description='',
        location='',
        contact_name='',
        contact_phone='',
        report_time='',
        status='lost'
    )
    
    assert item.is_lost() is True
    
    item.mark_found()
    
    assert item.status == 'found'
    assert item.is_lost() is False


def test_item_with_image_path():
    item = LostItem(
        item_id='test1234',
        item_name='手机',
        item_type='电子产品',
        description='',
        location='',
        contact_name='',
        contact_phone='',
        report_time='',
        status='lost',
        image_path='/images/phone.jpg'
    )
    
    assert item.image_path == '/images/phone.jpg'


def test_item_without_image_path():
    item = LostItem(
        item_id='test1234',
        item_name='手机',
        item_type='电子产品',
        description='',
        location='',
        contact_name='',
        contact_phone='',
        report_time='',
        status='lost'
    )
    
    assert item.image_path is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])