import pytest
import json
import os
from datetime import datetime

from app import create_app
from app.models.user import User
from app.models.item import LostItem
from app.models.comment import Comment
from app.models.message import Message
from app.models.report import Report
from app.services.data_service import JSONDataService

app = create_app()
app.config['TESTING'] = True
client = app.test_client()

TEST_DATA_DIR = 'tests/test_data'


@pytest.fixture(autouse=True)
def setup_and_teardown():
    os.makedirs(TEST_DATA_DIR, exist_ok=True)
    
    files = ['users.json', 'items.json', 'comments.json', 'messages.json', 'reports.json']
    for f in files:
        with open(os.path.join(TEST_DATA_DIR, f), 'w', encoding='utf-8') as fp:
            json.dump([], fp)
    
    yield
    
    for f in files:
        path = os.path.join(TEST_DATA_DIR, f)
        if os.path.exists(path):
            os.remove(path)
    if os.path.exists(TEST_DATA_DIR):
        os.rmdir(TEST_DATA_DIR)


def test_register():
    response = client.post('/register', data={
        'username': 'testuser',
        'password': '123456',
        'confirm_password': '123456',
        'email': 'test@example.com',
        'nickname': '测试用户'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert '登录' in response.get_data(as_text=True)


def test_login():
    client.post('/register', data={
        'username': 'testlogin',
        'password': '123456',
        'confirm_password': '123456',
        'email': 'login@example.com',
        'nickname': '登录测试'
    })
    
    response = client.post('/login', data={
        'username': 'testlogin',
        'password': '123456'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert '发布失物' in response.get_data(as_text=True)


def test_index():
    response = client.get('/')
    assert response.status_code == 200
    assert '校园失物招领' in response.get_data(as_text=True)


def test_post_item():
    client.post('/register', data={
        'username': 'postuser',
        'password': '123456',
        'confirm_password': '123456',
        'email': 'post@example.com'
    })
    client.post('/login', data={
        'username': 'postuser',
        'password': '123456'
    })
    
    response = client.post('/post', data={
        'item_name': '测试物品',
        'item_type': '电子产品',
        'description': '这是一个测试物品',
        'location': '教学楼A座',
        'contact_name': '测试用户',
        'contact_phone': '13800138000'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert '测试物品' in response.get_data(as_text=True)


def test_search():
    response = client.get('/search?keyword=测试')
    assert response.status_code == 200
    assert '搜索' in response.get_data(as_text=True)


def test_inbox():
    client.post('/register', data={
        'username': 'inboxuser',
        'password': '123456',
        'confirm_password': '123456',
        'email': 'inbox@example.com'
    })
    client.post('/login', data={
        'username': 'inboxuser',
        'password': '123456'
    })
    
    response = client.get('/inbox')
    assert response.status_code == 200
    assert '收件箱' in response.get_data(as_text=True)


def test_user_model():
    user = User(
        user_id='test001',
        username='testuser',
        password_hash='hash123',
        email='test@example.com',
        phone='13800138000',
        role='loser',
        nickname='测试用户',
        created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    assert user.user_id == 'test001'
    assert user.is_loser() is True
    assert user.is_admin() is False
    
    user.toggle_role()
    assert user.is_finder() is True
    
    user_dict = user.to_dict()
    assert user_dict['username'] == 'testuser'
    
    user2 = User.from_dict(user_dict)
    assert user2.username == 'testuser'


def test_item_model():
    item = LostItem(
        item_id='item001',
        user_id='user001',
        item_name='手机',
        item_type='电子产品',
        description='黑色iPhone',
        location='图书馆',
        contact_name='张三',
        contact_phone='13800138000',
        report_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        status='lost'
    )
    
    assert item.item_id == 'item001'
    assert item.is_lost() is True
    
    item.mark_found()
    assert item.status == 'found'
    
    item_dict = item.to_dict()
    assert item_dict['item_name'] == '手机'
    
    item2 = LostItem.from_dict(item_dict)
    assert item2.item_name == '手机'


def test_data_service():
    service = JSONDataService(TEST_DATA_DIR)
    
    user = User(
        user_id=service.generate_id(),
        username='serviceuser',
        password_hash='hash123',
        email='service@example.com',
        phone='',
        role='loser',
        created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    service.add_user(user)
    
    retrieved = service.get_user_by_username('serviceuser')
    assert retrieved is not None
    assert retrieved.username == 'serviceuser'
    
    all_users = service.get_all_users()
    assert len(all_users) == 1
    
    item = LostItem(
        item_id=service.generate_id(),
        user_id=user.user_id,
        item_name='测试物品',
        item_type='学习用品',
        description='测试描述',
        location='测试地点',
        contact_name='测试',
        contact_phone='',
        report_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        status='lost'
    )
    
    service.add_item(item)
    
    retrieved_item = service.get_item_by_id(item.item_id)
    assert retrieved_item is not None
    assert retrieved_item.item_name == '测试物品'
    
    all_items = service.get_all_items()
    assert len(all_items) == 1
    
    search_results = service.search_items(keyword='测试')
    assert len(search_results) == 1
    
    search_results = service.search_items(item_type='电子产品')
    assert len(search_results) == 0


def test_logout():
    client.post('/register', data={
        'username': 'logoutuser',
        'password': '123456',
        'confirm_password': '123456',
        'email': 'logout@example.com'
    })
    client.post('/login', data={
        'username': 'logoutuser',
        'password': '123456'
    })
    
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert '登录' in response.get_data(as_text=True)


def test_profile():
    client.post('/register', data={
        'username': 'profileuser',
        'password': '123456',
        'confirm_password': '123456',
        'email': 'profile@example.com'
    })
    client.post('/login', data={
        'username': 'profileuser',
        'password': '123456'
    })
    
    response = client.get('/profile')
    assert response.status_code == 200
    assert '个人中心' in response.get_data(as_text=True)


def test_role_switch():
    service = JSONDataService(TEST_DATA_DIR)
    
    user = User(
        user_id='roleuser001',
        username='roleuser',
        password_hash='hash123',
        email='role@example.com',
        phone='',
        role='loser',
        nickname='测试用户',
        created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    service.add_user(user)
    
    assert user.is_loser() is True
    user.toggle_role()
    assert user.is_finder() is True
    service.update_user(user)
    
    retrieved = service.get_user_by_username('roleuser')
    assert retrieved.is_finder() is True


def test_comment_model():
    comment = Comment(
        comment_id='c001',
        item_id='item001',
        user_id='user001',
        content='这是一条评论',
        create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    assert comment.comment_id == 'c001'
    assert comment.content == '这是一条评论'
    
    comment_dict = comment.to_dict()
    assert comment_dict['content'] == '这是一条评论'
    
    comment2 = Comment.from_dict(comment_dict)
    assert comment2.content == '这是一条评论'
    
    comment.soft_delete()
    assert comment.is_deleted is True


def test_message_model():
    message = Message(
        message_id='m001',
        sender_id='user001',
        receiver_id='user002',
        content='这是一条私信',
        create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        is_read=False
    )
    
    assert message.message_id == 'm001'
    assert message.is_read is False
    
    message.mark_read()
    assert message.is_read is True
    
    message_dict = message.to_dict()
    assert message_dict['content'] == '这是一条私信'


def test_report_model():
    report = Report(
        report_id='r001',
        reporter_id='user001',
        item_id='item001',
        reason='虚假信息',
        detail='这条信息是假的',
        create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        status='pending'
    )
    
    assert report.report_id == 'r001'
    assert report.status == 'pending'
    
    report.approve('已下架')
    assert report.status == 'approved'
    
    report_dict = report.to_dict()
    assert report_dict['reason'] == '虚假信息'


def test_add_comment():
    client.post('/register', data={
        'username': 'commentuser',
        'password': '123456',
        'confirm_password': '123456',
        'email': 'comment@example.com'
    })
    client.post('/login', data={
        'username': 'commentuser',
        'password': '123456'
    })
    
    client.post('/post', data={
        'item_name': '评论测试物品',
        'item_type': '电子产品',
        'description': '测试',
        'location': '测试地点',
        'contact_name': '测试',
        'contact_phone': ''
    })
    
    response = client.post('/add_comment/item001', data={
        'content': '测试评论内容'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_send_message():
    client.post('/register', data={
        'username': 'sender',
        'password': '123456',
        'confirm_password': '123456',
        'email': 'sender@example.com'
    })
    client.post('/register', data={
        'username': 'receiver',
        'password': '123456',
        'confirm_password': '123456',
        'email': 'receiver@example.com'
    })
    
    client.post('/login', data={
        'username': 'sender',
        'password': '123456'
    })
    
    response = client.post('/send_message/receiver', data={
        'content': '测试私信内容'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_admin_user_model():
    admin_user = User(
        user_id='admin001',
        username='admin',
        password_hash='hash123',
        email='admin@example.com',
        phone='',
        role='admin',
        nickname='管理员',
        created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    assert admin_user.is_admin() is True
    assert admin_user.is_loser() is False
    assert admin_user.is_finder() is False


def test_recommend_items():
    service = JSONDataService(TEST_DATA_DIR)
    
    user1 = User(
        user_id='user001',
        username='user1',
        password_hash='hash123',
        email='u1@example.com',
        phone='',
        role='loser',
        created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    user2 = User(
        user_id='user002',
        username='user2',
        password_hash='hash123',
        email='u2@example.com',
        phone='',
        role='finder',
        created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    service.add_user(user1)
    service.add_user(user2)
    
    lost_item = LostItem(
        item_id='lost001',
        user_id='user001',
        item_name='手机',
        item_type='电子产品',
        description='黑色iPhone手机',
        location='图书馆',
        contact_name='用户1',
        contact_phone='',
        report_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        status='lost'
    )
    
    found_item = LostItem(
        item_id='found001',
        user_id='user002',
        item_name='iPhone手机',
        item_type='电子产品',
        description='捡到一部黑色手机',
        location='图书馆',
        contact_name='用户2',
        contact_phone='',
        report_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        status='lost'
    )
    
    service.add_item(lost_item)
    service.add_item(found_item)
    
    recommendations = service.recommend_items('lost001')
    assert isinstance(recommendations, list)


def test_delete_account():
    client.post('/register', data={
        'username': 'deleteuser',
        'password': '123456',
        'confirm_password': '123456',
        'email': 'delete@example.com'
    })
    client.post('/login', data={
        'username': 'deleteuser',
        'password': '123456'
    })
    
    response = client.post('/delete_account', follow_redirects=True)
    assert response.status_code == 200
    assert '登录' in response.get_data(as_text=True)


def test_edit_profile():
    client.post('/register', data={
        'username': 'edituser',
        'password': '123456',
        'confirm_password': '123456',
        'email': 'edit@example.com'
    })
    client.post('/login', data={
        'username': 'edituser',
        'password': '123456'
    })
    
    response = client.get('/edit_profile')
    assert response.status_code == 200
    assert '修改信息' in response.get_data(as_text=True)


def test_report_item():
    client.post('/register', data={
        'username': 'reportuser',
        'password': '123456',
        'confirm_password': '123456',
        'email': 'report@example.com'
    })
    client.post('/login', data={
        'username': 'reportuser',
        'password': '123456'
    })
    
    client.post('/post', data={
        'item_name': '举报测试物品',
        'item_type': '电子产品',
        'description': '测试',
        'location': '测试地点',
        'contact_name': '测试',
        'contact_phone': ''
    })
    
    response = client.get('/report/item001')
    assert response.status_code == 200 or response.status_code == 302