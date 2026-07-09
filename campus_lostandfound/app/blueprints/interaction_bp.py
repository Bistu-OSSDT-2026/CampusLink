from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, session

from app.models.comment import Comment
from app.models.message import Message
from app.models.report import Report
from app.services.data_service import JSONDataService

interaction_bp = Blueprint('interaction', __name__)
data_service = JSONDataService()


@interaction_bp.route('/add_comment/<item_id>', methods=['POST'])
def add_comment(item_id):
    if 'user_id' not in session:
        flash('请先登录', 'danger')
        return redirect(url_for('auth.login'))
    
    content = request.form.get('content')
    
    if not content or len(content.strip()) == 0:
        flash('评论内容不能为空', 'danger')
        return redirect(url_for('items.detail', item_id=item_id))
    
    if len(content) > 500:
        flash('评论内容不能超过500字', 'danger')
        return redirect(url_for('items.detail', item_id=item_id))
    
    comment = Comment(
        comment_id=data_service.generate_id(),
        item_id=item_id,
        user_id=session['user_id'],
        content=content.strip(),
        create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    data_service.add_comment(comment)
    flash('评论成功', 'success')
    
    item = data_service.get_item_by_id(item_id)
    if item and item.user_id != session['user_id']:
        message = Message(
            message_id=data_service.generate_id(),
            sender_id=session['user_id'],
            receiver_id=item.user_id,
            content=f'有人在您发布的「{item.item_name}」下发表了评论：{content[:50]}...',
            create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            message_type='comment'
        )
        data_service.add_message(message)
    
    return redirect(url_for('items.detail', item_id=item_id))


@interaction_bp.route('/send_message/<user_id>', methods=['GET', 'POST'])
def send_message(user_id):
    if 'user_id' not in session:
        flash('请先登录', 'danger')
        return redirect(url_for('auth.login'))
    
    if session['user_id'] == user_id:
        flash('不能给自己发送消息', 'danger')
        return redirect(url_for('auth.profile'))
    
    receiver = data_service.get_user_by_id(user_id)
    current_user = data_service.get_user_by_id(session['user_id'])
    
    if not receiver:
        flash('用户不存在', 'danger')
        return redirect(url_for('auth.profile'))
    
    if request.method == 'POST':
        content = request.form.get('content')
        
        if not content or len(content.strip()) == 0:
            flash('消息内容不能为空', 'danger')
            return render_template('interaction/send_message.html', receiver=receiver)
        
        if len(content) > 1000:
            flash('消息内容不能超过1000字', 'danger')
            return render_template('interaction/send_message.html', receiver=receiver)
        
        message = Message(
            message_id=data_service.generate_id(),
            sender_id=session['user_id'],
            receiver_id=user_id,
            content=content.strip(),
            create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            message_type='normal'
        )
        
        data_service.add_message(message)
        flash('消息发送成功', 'success')
        return redirect(url_for('interaction.inbox'))
    
    return render_template('interaction/send_message.html', receiver=receiver)


@interaction_bp.route('/inbox')
def inbox():
    if 'user_id' not in session:
        flash('请先登录', 'danger')
        return redirect(url_for('auth.login'))
    
    messages = data_service.get_messages_by_receiver(session['user_id'])
    messages.sort(key=lambda x: x.create_time, reverse=True)
    
    data_service.mark_messages_read(session['user_id'])
    
    senders = {}
    for msg in messages:
        if msg.sender_id not in senders:
            senders[msg.sender_id] = data_service.get_user_by_id(msg.sender_id)
    
    return render_template('interaction/inbox.html', messages=messages, senders=senders)


@interaction_bp.route('/report/<item_id>', methods=['GET', 'POST'])
def report(item_id):
    if 'user_id' not in session:
        flash('请先登录', 'danger')
        return redirect(url_for('auth.login'))
    
    item = data_service.get_item_by_id(item_id)
    
    if not item:
        flash('物品不存在', 'danger')
        return redirect(url_for('items.index'))
    
    if request.method == 'POST':
        reason = request.form.get('reason')
        detail = request.form.get('detail')
        
        if not reason:
            flash('请选择举报原因', 'danger')
            return render_template('interaction/report.html', item=item)
        
        report = Report(
            report_id=data_service.generate_id(),
            reporter_id=session['user_id'],
            item_id=item_id,
            reason=reason,
            detail=detail or '',
            create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        data_service.add_report(report)
        flash('举报提交成功，管理员将尽快处理', 'success')
        return redirect(url_for('items.detail', item_id=item_id))
    
    return render_template('interaction/report.html', item=item)
