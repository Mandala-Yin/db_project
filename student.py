from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from db_func import fetch_basic_information, update_user_info, fetch_stu_course

bp = Blueprint('student', __name__, url_prefix='/student')


@bp.route('/<string:sid>', methods=['GET', 'POST'])
def student(sid):
    basic_info = fetch_basic_information(sid, 'student')
    if session.get('user_id') is not None:
        # 正常情况下，应该进入展示学生基本信息的页面student_info.html
        return render_template('student/student_info.html', basic_info=basic_info)
    else:
        return redirect(url_for('log_manage.login'))


@bp.route('/edit/<string:sid>')
def student_edit(sid):
    # 通过主页中的修改按钮可以进入该函数
    basic_info = fetch_basic_information(sid, 'student')  # 传基本信息的原因是，可以在修改页面预填充原信息，然后可以仅修改某几项信息
    return render_template('student/stu_edit.html', basic_info=basic_info)


@bp.route('/update', methods=['POST'])
def update_student():
    # 点击信息修改提交按钮后可以进入该函数
    _id = request.form['id']
    _telephone = request.form['telephone']
    _address = request.form['address']
    # validate the received values
    if _id and _telephone and _address and request.method == 'POST':
        # save edits, only consider telephone and address
        update_user_info(_id, _telephone, _address)
        flash(' Student information updated successfully!')
        # 修改完信息后，应该跳转回主页面
        return redirect(url_for('student.student_edit', sid=_id))
    else:
        return 'Error while updating student information'


@bp.route('/course/<string:sid>')
def course_check(sid):
    # 学生点击主页'课程审查'按钮后应该进入该函数
    basic_info = fetch_basic_information(sid, 'student') # 基本信息，方便回到学生主页
    results_major = fetch_stu_course(sid)  # 主学位课程信息
    results_non_major = fetch_stu_course(sid, False)  # 双学位课程信息，注意results可能为空
    return render_template('student/stu_course.html', major=results_major, minor=results_non_major, basic_info=basic_info)
