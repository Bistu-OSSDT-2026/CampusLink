from flask import Blueprint, render_template, redirect, url_for, flash, session

from app.services.data_service import JSONDataService

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
data_service = JSONDataService()


def admin_required():
    if 'user_id' not in session:
        flash('请先登录', 'danger')
        return False
    
    user = data_service.get_user_by_id(session['user_id'])
    if not user or not user.is_admin():
        flash('无权访问管理后台', 'danger')
        return False
    
    return True


@admin_bp.route('/')
def dashboard():
    if not admin_required():
        return redirect(url_for('auth.login'))
    
    user = data_service.get_user_by_id(session['user_id'])
    
    all_items = data_service.get_all_items()
    all_users = data_service.get_all_users()
    unverified_items = data_service.get_unverified_items()
    pending_reports = data_service.get_pending_reports()
    
    return render_template('admin/dashboard.html', user=user,
                           item_count=len(all_items),
                           user_count=len(all_users),
                           unverified_count=len(unverified_items),
                           report_count=len(pending_reports))


@admin_bp.route('/items')
def manage_items():
    if not admin_required():
        return redirect(url_for('auth.login'))
    
    user = data_service.get_user_by_id(session['user_id'])
    items = data_service.get_all_items()
    items.sort(key=lambda x: x.report_time, reverse=True)
    
    return render_template('admin/items.html', user=user, items=items)


@admin_bp.route('/items/delete/<item_id>', methods=['POST'])
def delete_item(item_id):
    if not admin_required():
        return redirect(url_for('auth.login'))
    
    data_service.delete_item(item_id)
    flash('物品已删除', 'success')
    return redirect(url_for('admin.manage_items'))


@admin_bp.route('/users')
def manage_users():
    if not admin_required():
        return redirect(url_for('auth.login'))
    
    user = data_service.get_user_by_id(session['user_id'])
    users = data_service.get_all_users()
    
    return render_template('admin/users.html', user=user, users=users)


@admin_bp.route('/users/delete/<user_id>', methods=['POST'])
def delete_user(user_id):
    if not admin_required():
        return redirect(url_for('auth.login'))
    
    data_service.delete_user(user_id)
    flash('用户已删除', 'success')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/reports')
def manage_reports():
    if not admin_required():
        return redirect(url_for('auth.login'))
    
    user = data_service.get_user_by_id(session['user_id'])
    reports = data_service.get_all_reports()
    reports.sort(key=lambda x: x.create_time, reverse=True)
    
    return render_template('admin/reports.html', user=user, reports=reports)


@admin_bp.route('/reports/handle/<report_id>', methods=['GET', 'POST'])
def handle_report(report_id):
    if not admin_required():
        return redirect(url_for('auth.login'))
    
    user = data_service.get_user_by_id(session['user_id'])
    report = data_service.get_all_reports()
    report = next((r for r in report if r.report_id == report_id), None)
    
    if not report:
        flash('举报不存在', 'danger')
        return redirect(url_for('admin.manage_reports'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action in ['approve', 'reject']:
            report.status = 'resolved' if action == 'approve' else 'rejected'
            data_service.update_report(report)
            
            if action == 'approve' and report.reported_item_id:
                item = data_service.get_item_by_id(report.reported_item_id)
                if item:
                    item.soft_delete()
                    data_service.update_item(item)
            
            flash('处理完成', 'success')
            return redirect(url_for('admin.manage_reports'))
    
    reported_item = None
    if report.reported_item_id:
        reported_item = data_service.get_item_by_id(report.reported_item_id)
    
    return render_template('admin/handle_report.html', user=user, 
                           report=report, reported_item=reported_item)


@admin_bp.route('/stats')
def stats():
    if not admin_required():
        return redirect(url_for('auth.login'))
    
    user = data_service.get_user_by_id(session['user_id'])
    
    all_items = data_service.get_all_items()
    total = len(all_items)
    lost = len([i for i in all_items if i.status == 'lost'])
    found = len([i for i in all_items if i.status == 'found'])
    
    type_stats = {}
    for item in all_items:
        type_stats[item.item_type] = type_stats.get(item.item_type, 0) + 1
    
    return render_template('admin/stats.html', user=user,
                           total=total, lost=lost, found=found,
                           type_stats=type_stats)
