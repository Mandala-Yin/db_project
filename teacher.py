from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from db_func import fetch_basic_information, update_user_info

bp = Blueprint('teacher', __name__, url_prefix='/teacher')


@bp.route('/?<string:tid>', methods=('GET', 'POST'))
def teacher(tid):
    basic_info = fetch_basic_information(tid, 'teacher')
    if session.get('user_id') is not None:
        # 正常的话，应该进入展示教师基本信息的页面student.html
        return render_template('teacher.html', basic_info)
    else:
        return redirect(url_for('log_manage.login'))


@bp.route('/edit/<string:tid>')
def teacher_edit(tid):
    # 通过主页中的修改按钮可以进入该函数
    basic_info = fetch_basic_information(tid, 'teacher')  # 传基本信息的原因是，可以在修改页面预填充原信息，然后可以仅修改某几项信息
    return render_template('edit_tea.html', basic_info)


@bp.route('/update', methods=['POST'])
def update_teacher():
    # 点击信息修改提交按钮后可以进入该函数
    _id = request.form['id']
    _telephone = request.form['telephone']
    _address = request.form['address']
    # validate the received values
    if _id and _telephone and _address and request.method == 'POST':
        # save edits, only consider telephone and address
        update_user_info(_id, _telephone, _address)
        flash('teacher information updated successfully!')
        return redirect('/')
    else:
        return 'Error while updating teacher information'

