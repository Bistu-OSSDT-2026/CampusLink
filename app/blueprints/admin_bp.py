from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, session

from app.models.item import LostItem
from app.models.report import Report
from app.services.data_service import JSONDataService

admin_bp = Blueprint('admin', __name__)
data_service = JSONDataService()


def is_admin():
    if 'user_id' not in session:
        return False
    user = data_service.get_user_by_id(session['user_id'])
    return user and user.is_admin()


@admin_bp.route('/dashboard')
def dashboard():
    if not is_admin():
        flash('无权限访问', 'danger')
        return redirect(url_for('items.index'))
    
    users = data_service.get_all_users()
    items = data_service.get_all_items()
    reports = data_service.get_all_reports()
    
    stats = {
        'total_users': len(users),
        'total_items': len(items),
        'pending_reports': len([r for r in reports if r.status == 'pending']),
        'lost_items': len([i for i in items if i.status == 'lost'])
    }
    
    return render_template('admin/dashboard.html', stats=stats, users=users[:5], items=items[:5], reports=reports[:5])


@admin_bp.route('/users')
def users():
    if not is_admin():
        flash('无权限访问', 'danger')
        return redirect(url_for('items.index'))
    
    users = data_service.get_all_users()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/items')
def items():
    if not is_admin():
        flash('无权限访问', 'danger')
        return redirect(url_for('items.index'))
    
    items = data_service.get_all_items()
    unverified_items = data_service.get_unverified_items()
    
    return render_template('admin/items.html', items=items, unverified_items=unverified_items)


@admin_bp.route('/verify_item/<item_id>')
def verify_item(item_id):
    if not is_admin():
        flash('无权限访问', 'danger')
        return redirect(url_for('items.index'))
    
    item = data_service.get_item_by_id(item_id)
    
    if not item:
        flash('物品不存在', 'danger')
        return redirect(url_for('admin.items'))
    
    item.verify()
    data_service.update_item(item)
    flash('审核通过', 'success')
    return redirect(url_for('admin.items'))


@admin_bp.route('/delete_item/<item_id>')
def delete_item(item_id):
    if not is_admin():
        flash('无权限访问', 'danger')
        return redirect(url_for('items.index'))
    
    item = data_service.get_item_by_id(item_id)
    
    if not item:
        flash('物品不存在', 'danger')
        return redirect(url_for('admin.items'))
    
    item.soft_delete()
    data_service.update_item(item)
    flash('已下架该物品', 'success')
    return redirect(url_for('admin.items'))


@admin_bp.route('/reports')
def reports():
    if not is_admin():
        flash('无权限访问', 'danger')
        return redirect(url_for('items.index'))
    
    reports = data_service.get_all_reports()
    reports.sort(key=lambda x: x.status, reverse=True)
    
    return render_template('admin/reports.html', reports=reports)


@admin_bp.route('/handle_report/<report_id>', methods=['GET', 'POST'])
def handle_report(report_id):
    if not is_admin():
        flash('无权限访问', 'danger')
        return redirect(url_for('items.index'))
    
    report = None
    for r in data_service.get_all_reports():
        if r.report_id == report_id:
            report = r
            break
    
    if not report:
        flash('举报不存在', 'danger')
        return redirect(url_for('admin.reports'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        result = request.form.get('result')
        
        if action == 'approve':
            report.approve(result)
            
            item = data_service.get_item_by_id(report.item_id)
            if item:
                item.soft_delete()
                data_service.update_item(item)
        elif action == 'reject':
            report.reject(result)
        
        report.handle_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_service.update_report(report)
        
        flash('处理完成', 'success')
        return redirect(url_for('admin.reports'))
    
    item = data_service.get_item_by_id(report.item_id)
    reporter = data_service.get_user_by_id(report.reporter_id)
    
    return render_template('admin/handle_report.html', report=report, item=item, reporter=reporter)


@admin_bp.route('/stats')
def stats():
    if not is_admin():
        flash('无权限访问', 'danger')
        return redirect(url_for('items.index'))
    
    items = data_service.get_all_items()
    users = data_service.get_all_users()
    
    type_stats = {}
    for item in items:
        type_stats[item.item_type] = type_stats.get(item.item_type, 0) + 1
    
    status_stats = {
        'lost': len([i for i in items if i.status == 'lost']),
        'found': len([i for i in items if i.status == 'found'])
    }
    
    role_stats = {
        'loser': len([u for u in users if u.is_loser()]),
        'finder': len([u for u in users if u.is_finder()]),
        'admin': len([u for u in users if u.is_admin()])
    }
    
    return render_template('admin/stats.html', 
                           type_stats=type_stats, 
                           status_stats=status_stats,
                           role_stats=role_stats,
                           total_items=len(items),
                           total_users=len(users))