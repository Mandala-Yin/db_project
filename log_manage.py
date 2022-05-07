from flask import Blueprint, request, redirect, render_template, session, url_for, flash
from db_func import login_check

bp = Blueprint('log_manage', __name__)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        return render_template('login.html')
    user_id = request.form['ID']
    pwd = request.form['pwd']
    role = request.form['role']
    # 检查用户名，账号，身份是否配对，然后跳转到对应的页面
    if login_check(user_id, pwd, role):
        session['user_id'] = user_id
        if role == 'admin':
            return redirect(url_for('admin.admin', aid=user_id))
        elif role == 'teacher':
            return redirect(url_for('teacher.teacher', tid=user_id))
        else:
            return redirect(url_for('student.student', sid=user_id))
    else:
        flash("Please input correct ID and password!")
        return render_template('login.html')


@bp.route('/logout')
def logout():
    # 用户点击退出按钮后应该进入该函数
    del session['user_id']
    return redirect('login')
