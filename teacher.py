from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from db_func import fetch_basic_information, update_user_info, fetch_tea_course, \
    fetch_course_with_score, fetch_course_without_score, update_scores

bp = Blueprint('teacher', __name__, url_prefix='/teacher')


@bp.route('/<string:tid>', methods=['GET', 'POST'])
def teacher(tid):
    basic_info = fetch_basic_information(tid, 'teacher')
    if session.get('user_id') is not None:
        # 正常的话，应该进入展示教师基本信息的页面teacher_info.html
        return render_template('teacher_info.html', basic_info=basic_info)
    else:
        return redirect(url_for('log_manage.login'))


@bp.route('/edit/<string:tid>')
def teacher_edit(tid):
    # 通过主页中的修改按钮可以进入该函数
    basic_info = fetch_basic_information(tid, 'teacher')  # 传基本信息的原因是，可以在修改页面预填充原信息，然后可以仅修改某几项信息
    return render_template('tea_edit.html', basic_info=basic_info)


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
        return redirect(url_for('teacher.teacher', tid=_id))
    else:
        return 'Error while updating teacher information'


@bp.route('/course/<string:tid>')
def course_info(tid):
    # 点击查看开设课程按钮后进入该函数
    results_course = fetch_tea_course(tid)
    return render_template('tea_course.html', course=results_course)


@bp.route('/add_scores/<string:tid>', methods=['POST'])
def add_scores_view(tid):
    """
    点击录入成绩按钮后进入该函数（之前要输入课程号和对应学期），然后转入对应的html页面
    我的想法是，录入和修改成绩的修改在于，录入成绩时不显示SC表中的score（理论上也应该是null）
    修改成绩时预填充SC表中的score，然后可以有选择的进行修改
    """
    _cid = request.form['cid']
    _semester = request.form['semester']
    # 确认输入了课程号和学期
    if _cid and _semester:
        # 预查询相关信息，然后转入html页面
        results = fetch_course_without_score(_cid, tid, _semester)
        return render_template('add_scores.html', tid=tid, cid=_cid, sem=_semester, res=results)
    else:
        return redirect(url_for('teacher.teacher', tid=tid))


# 第一种路由来自教师主页点击修改课程分数信息按钮，第二种路由来自修改分数后
@bp.route('/modify_scores/<string:tid>', methods=['POST'])
@bp.route('/modify_scores/<string:tid>/<string:cid>/<string:semester>')
def modify_scores_view(tid, cid=None, semester=None):
    # 点击修改成绩按钮后进入该函数（之前要输入课程号和对应学期），然后转入对应的html页面
    if request.method == 'POST':
        _cid = request.form['cid']
        _semester = request.form['semester']
        # 确认输入了课程号和学期
        if _cid and _semester:
            # 预查询相关信息，然后转入html页面
            results = fetch_course_with_score(_cid, tid, _semester)
            return render_template('modify_scores.html', tid=tid, cid=_cid, sem=_semester, res=results)
        else:
            return redirect(url_for('teacher.teacher', tid=tid))
    else:
        if cid and semester:
            results = fetch_course_with_score(cid, tid, semester)
            return render_template('modify_scores.html', tid=tid, cid=cid, sem=semester, res=results)
        else:
            return redirect(url_for('teacher.teacher', tid=tid))


@bp.route('/add_scores_confirm/<string:tid>/<string:cid>', methods=['POST'])
def add_scores_confirm(tid, cid):
    # 点击录入成绩页面的提交按钮进入该函数，这里假设页面表单设置为list类型，即sids, scores都是list的格式
    sids = request.form.getlist('sids')
    scores = request.form.getlist('scores')
    update_scores(sids, scores, cid)
    flash("add successfully!")
    # 完全录入后回到教师主页
    return redirect(url_for('teacher.teacher', tid=tid))


@bp.route('/modify_scores_confirm/<string:tid>/<string:cid>/<string:semester>', methods=['POST'])
def modify_scores_confirm(tid, cid, semester):
    # 点击修改成绩页面的提交按钮进入该函数，每条记录应该都有一个提交按钮，所以是分条更新
    _sid = request.form['sid']
    _score = request.form['score']
    update_scores([_sid], [_score], cid)
    flash("modify successfully!")
    # 因为可能修改多条成绩，所以修改一条之后依然回到'modify_scores_view'
    return redirect(url_for('teacher.modify_scores_view', tid=tid, cid=cid, semester=semester))
