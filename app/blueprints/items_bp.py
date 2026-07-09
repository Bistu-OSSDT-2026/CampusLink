import os
import re
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, session

from app.models.item import LostItem
from app.models.comment import Comment
from app.services.data_service import JSONDataService
from app.config import Config

items_bp = Blueprint('items', __name__)
data_service = JSONDataService()

PHONE_REGEX = r'^1[3-9]\d{9}$'
FORBIDDEN_WORDS = ['色情', '暴力', '赌博', '毒品', '枪支', '诈骗', '广告']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def contains_forbidden_words(text):
    for word in FORBIDDEN_WORDS:
        if word in text:
            return True
    return False


@items_bp.route('/')
def index():
    items = data_service.get_all_items()
    items.sort(key=lambda x: x.report_time, reverse=True)
    
    current_user = None
    if 'user_id' in session:
        current_user = data_service.get_user_by_id(session['user_id'])
    
    unread_count = 0
    if current_user:
        unread_count = data_service.get_unread_messages_count(current_user.user_id)
    
    return render_template('items/index.html', items=items, current_user=current_user, unread_count=unread_count)


@items_bp.route('/post', methods=['GET', 'POST'])
def post():
    if 'user_id' not in session:
        flash('请先登录', 'danger')
        return redirect(url_for('auth.login'))
    
    user = data_service.get_user_by_id(session['user_id'])
    
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        item_type = request.form.get('item_type')
        description = request.form.get('description')
        location = request.form.get('location')
        contact_name = request.form.get('contact_name')
        contact_phone = request.form.get('contact_phone')
        
        if not item_name or not item_type or not location:
            flash('物品名称、类型和地点不能为空', 'danger')
            return render_template('items/post.html', user=user)
        
        if contact_phone and not re.match(PHONE_REGEX, contact_phone):
            flash('手机号格式不正确', 'danger')
            return render_template('items/post.html', user=user)
        
        if contains_forbidden_words(item_name) or contains_forbidden_words(description or ''):
            flash('内容包含违规信息，请修改后重试', 'danger')
            return render_template('items/post.html', user=user)
        
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = f"{data_service.generate_id()}_{file.filename}"
                filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
                file.save(filepath)
                image_path = f"uploads/{filename}"
        
        item = LostItem(
            item_id=data_service.generate_id(),
            user_id=user.user_id,
            item_name=item_name,
            item_type=item_type,
            description=description or '',
            location=location,
            contact_name=contact_name or user.nickname or user.username,
            contact_phone=contact_phone or user.phone or '',
            report_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            status='lost',
            image_path=image_path,
            is_verified=True
        )
        
        data_service.add_item(item)
        flash('发布成功！', 'success')
        return redirect(url_for('items.index'))
    
    return render_template('items/post.html', user=user)


@items_bp.route('/search', methods=['GET', 'POST'])
def search():
    keyword = request.args.get('keyword', '')
    item_type = request.args.get('item_type', '')
    status = request.args.get('status', '')
    sort_by = request.args.get('sort_by', 'time')
    
    items = data_service.search_items(keyword, item_type, status, sort_by=sort_by)
    
    current_user = None
    if 'user_id' in session:
        current_user = data_service.get_user_by_id(session['user_id'])
    
    return render_template('items/search.html', items=items, keyword=keyword, 
                           item_type=item_type, status=status, sort_by=sort_by,
                           current_user=current_user)


@items_bp.route('/detail/<item_id>')
def detail(item_id):
    item = data_service.get_item_by_id(item_id)
    if not item:
        flash('物品不存在', 'danger')
        return redirect(url_for('items.index'))
    
    comments = data_service.get_comments_by_item(item_id)
    comments.sort(key=lambda x: x.create_time, reverse=True)
    
    recommend_items = data_service.recommend_items(item_id)
    
    current_user = None
    if 'user_id' in session:
        current_user = data_service.get_user_by_id(session['user_id'])
    
    user = data_service.get_user_by_id(item.user_id)
    
    return render_template('items/detail.html', item=item, comments=comments,
                           recommend_items=recommend_items, current_user=current_user,
                           user=user)


@items_bp.route('/mark_found/<item_id>')
def mark_found(item_id):
    if 'user_id' not in session:
        flash('请先登录', 'danger')
        return redirect(url_for('auth.login'))
    
    item = data_service.get_item_by_id(item_id)
    
    if not item:
        flash('物品不存在', 'danger')
        return redirect(url_for('items.index'))
    
    if item.user_id != session['user_id'] and not data_service.get_user_by_id(session['user_id']).is_admin():
        flash('无权操作', 'danger')
        return redirect(url_for('items.detail', item_id=item_id))
    
    item.mark_found()
    data_service.update_item(item)
    flash('已标记为已找到', 'success')
    return redirect(url_for('items.detail', item_id=item_id))