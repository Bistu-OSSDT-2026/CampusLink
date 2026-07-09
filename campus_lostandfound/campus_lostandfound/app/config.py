import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'campus_lostandfound_secret_key_2026'
    
    DATA_DIR = os.path.join(basedir, 'data')
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    ITEM_TYPES = [
        '电子产品', '证件卡类', '衣物配饰', 
        '学习用品', '生活用品', '其他'
    ]
    
    USER_ROLES = ['loser', 'finder', 'admin']
    
    SESSION_TYPE = 'filesystem'