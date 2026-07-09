import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_FILE = os.path.join(BASE_DIR, 'data', 'lost_items.json')

ITEM_TYPES = [
    '电子产品',
    '证件卡类',
    '衣物配饰',
    '学习用品',
    '生活用品',
    '其他'
]

STATUS_OPTIONS = [
    ('lost', '丢失'),
    ('found', '已找到')
]

APP_TITLE = '校园失物招领平台'

APP_WIDTH = 800
APP_HEIGHT = 600

CONTACT_PHONE_REGEX = r'^1[3-9]\d{9}$'