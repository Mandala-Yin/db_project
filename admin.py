from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from db_func import fetch_basic_information, update_user_info, faculty_id, \
    faculty2stu, faculty2tea, faculty2course, get_tid, update_course

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/<string:aid>', methods=['GET', 'POST'])
def admin(aid):
    basic_info = fetch_basic_information(aid, 'admin')
    if session.get('user_id') is not None:
        # 正常的话，应该进入展示教务基本信息的页面admin_info.html
        return render_template('admin_info.html', basic_info=basic_info)
    else:
        return redirect(url_for('log_manage.login'))


@bp.route('/edit/<string:aid>')
def admin_edit(aid):
    # 通过主页中的修改按钮可以进入该函数
    basic_info = fetch_basic_information(aid, 'admin')  # 传基本信息的原因是，可以在修改页面预填充原信息，然后可以仅修改某几项信息
    return render_template('admin_edit.html', basic_info=basic_info)


@bp.route('/update', methods=['POST'])
def update_admin():
    # 点击信息修改提交按钮后可以进入该函数
    _id = request.form['id']
    _telephone = request.form['telephone']
    _address = request.form['address']
    # validate the received values
    if _id and _telephone and _address and request.method == 'POST':
        # save edits, only consider telephone and address
        update_user_info(_id, _telephone, _address)
        flash('admin information updated successfully!')
        return redirect(url_for('admin.admin', aid=_id))
    else:
        return 'Error while updating admin information'


@bp.route('/faculty_info/<string:aid>')
def faculty_info(aid):
    # 查询学生、教师、课程相关信息，然后传入对应的html页面
    fid = faculty_id(aid)['fid']
    res_stu = faculty2stu(fid)
    res_tea = faculty2tea(fid)
    res_course = faculty2course(fid)
    return render_template('admin_get_faculty_info.html', stu_info=res_stu, tea_info=res_tea, course_info=res_course)


@bp.route('/add_course/<string:aid>')
def add_course_view(aid):
    # 新加本院系开设的课程，点击添加课程按钮应该进入该函数
    fid = faculty_id(aid)['fid']
    # 预查询本院系教师信息，提供选择（html中tid一栏可以设为下拉单）
    candidate_tid = get_tid(fid)
    return render_template('admin_add_course.html', fid=fid, tea_info=candidate_tid)


@bp.route('/add_course_confirm/<string:aid>', methods=['POST'])
def add_course_confirm(aid):
    # 在添加课程页面点击提交按钮应该进入该函数，对数据库进行更新后返回教务主页
    _cid = request.form['cid']
    _tid = request.form['tid']
    _cname = request.form['cname']
    _category = request.form['category']
    _credit = request.form['credit']
    update_course(_cid, _tid, _cname, _category, _credit)
    flash("new course added successfully!")
    return redirect(url_for('admin.admin', aid=aid))
