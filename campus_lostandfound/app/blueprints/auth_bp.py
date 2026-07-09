import re
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.user import User
from app.services.data_service import JSONDataService

auth_bp = Blueprint('auth', __name__)
data_service = JSONDataService()

PHONE_REGEX = r'^1[3-9]\d{9}$'
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('items.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')
        phone = request.form.get('phone')
        nickname = request.form.get('nickname')
        role = request.form.get('role', 'loser')
        
        if not username or not password or not email:
            flash('用户名、密码和邮箱不能为空', 'danger')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('两次输入的密码不一致', 'danger')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('密码长度至少为6位', 'danger')
            return render_template('auth/register.html')
        
        if not re.match(EMAIL_REGEX, email):
            flash('邮箱格式不正确', 'danger')
            return render_template('auth/register.html')
        
        if phone and not re.match(PHONE_REGEX, phone):
            flash('手机号格式不正确', 'danger')
            return render_template('auth/register.html')
        
        if data_service.get_user_by_username(username):
            flash('用户名已存在', 'danger')
            return render_template('auth/register.html')
        
        if data_service.get_user_by_email(email):
            flash('邮箱已被注册', 'danger')
            return render_template('auth/register.html')
        
        user = User(
            user_id=data_service.generate_id(),
            username=username,
            password_hash=generate_password_hash(password),
            email=email,
            phone=phone,
            role=role,
            nickname=nickname or username,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        data_service.add_user(user)
        flash('注册成功，请登录', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('items.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('请输入用户名和密码', 'danger')
            return render_template('auth/login.html')
        
        user = data_service.get_user_by_username(username)
        
        if not user or not check_password_hash(user.password_hash, password):
            flash('用户名或密码错误', 'danger')
            return render_template('auth/login.html')
        
        session['user_id'] = user.user_id
        flash('登录成功', 'success')
        return redirect(url_for('items.index'))
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('已退出登录', 'success')
    return redirect(url_for('items.index'))


@auth_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = data_service.get_user_by_id(session['user_id'])
    items = data_service.get_items_by_user(session['user_id'])
    
    return render_template('auth/profile.html', user=user, items=items)


@auth_bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = data_service.get_user_by_id(session['user_id'])
    
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        bio = request.form.get('bio')
        
        if email and not re.match(EMAIL_REGEX, email):
            flash('邮箱格式不正确', 'danger')
            return render_template('auth/edit_profile.html', user=user)
        
        if phone and not re.match(PHONE_REGEX, phone):
            flash('手机号格式不正确', 'danger')
            return render_template('auth/edit_profile.html', user=user)
        
        existing_user = data_service.get_user_by_email(email)
        if existing_user and existing_user.user_id != user.user_id:
            flash('邮箱已被使用', 'danger')
            return render_template('auth/edit_profile.html', user=user)
        
        user.nickname = nickname or user.nickname
        user.email = email or user.email
        user.phone = phone or user.phone
        user.bio = bio
        
        data_service.update_user(user)
        flash('信息修改成功', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/edit_profile.html', user=user)


@auth_bp.route('/toggle_role')
def toggle_role():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = data_service.get_user_by_id(session['user_id'])
    
    if user.is_admin():
        flash('管理员身份不能切换', 'warning')
        return redirect(url_for('auth.profile'))
    
    user.toggle_role()
    data_service.update_user(user)
    
    role_text = '捡拾者' if user.is_finder() else '丢失者'
    flash(f'身份已切换为：{role_text}', 'success')
    return redirect(url_for('auth.profile'))


@auth_bp.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    if data_service.delete_user(user_id):
        session.pop('user_id', None)
        flash('账号已注销', 'success')
        return redirect(url_for('items.index'))
    
    flash('注销失败', 'danger')
    return redirect(url_for('auth.profile'))