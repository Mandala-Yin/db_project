import psycopg2

default_map = ['id', 'name', 'sex', 'faculty', 'telephone', 'address']
sex_dict = {True: 'Male', False: 'Female'}
login_map = ['id', 'password', 'role']
adm_extra = ['working_year', 'is_cadre']
tea_extra = ['working_year', 'title']
stu_extra = ['grade', 'is_foreign_stu']
SC_info = ['cid', 'score', 'gpa', 'is_w',
           'semester', 'cname', 'category', 'credit']
category_info = ['category', 'credit', 'avg_score', 'avg_gpa']
TC_info = ['cid', 'cname', 'category', 'credit',
           'semester', 'avg_score', 'max_score']


# 建立数据库连接
def get_db_connection():
    db = psycopg2.connect(host='127.0.0.1',
                          database='Information_Management_System',
                          user='postgres',
                          password='')
    return db


# 关闭数据库连接
def close_db_connection(cursor, db_connection):
    cursor.close()
    db_connection.close()


# 将fetchall的结果从list(tuple)转换为list(dict)
def format_trans(raw_res, mapping=default_map):
    if not raw_res:
        return []
    trans_res = []
    for row in raw_res:
        row, trans_row = list(row), {}
        for col, val in zip(mapping, row):
            if col == 'sex':
                val = sex_dict[val]
            trans_row[col] = val
        trans_res.append(trans_row)

    return trans_res


# 将fetchone的结果从tuple转换为dict
def format_trans_one(raw_res, mapping=default_map):
    if not raw_res:
        return {}
    row, trans_row = list(raw_res), {}
    for col, val in zip(mapping, row):
        if col == 'sex':
            val = sex_dict[val]
        trans_row[col] = val

    return trans_row


# 用户登录检查
def login_check(u_id, u_password, u_role):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute('SELECT id, password, role FROM public."Users"')
    users = cur.fetchall()
    close_db_connection(cur, db)
    users = format_trans(users, login_map)
    for user in users:
        if user['id'] == u_id and user['password'] == u_password \
                and user['role'] == u_role[:3]:
            return True

    return False


# 获取用户基本信息，从视图中提取信息
def fetch_basic_information(u_id, u_role):
    db = get_db_connection()
    cur = db.cursor()
    paras = [u_id]
    if u_role == 'admin':
        cur.execute(f'SELECT id, name, sex, fname, telephone, address, working_year, is_cadre '
                    f'FROM "admin_information" '
                    f'WHERE "admin_information".id=%s', paras)
        raw_res = cur.fetchone()
        close_db_connection(cur, db)
        return format_trans_one(raw_res, default_map+adm_extra)
    elif u_role == 'teacher':
        cur.execute(f'SELECT id, name, sex, fname, telephone, address, working_year, title '
                    f'FROM "teacher_information" '
                    f'WHERE "teacher_information".id=%s', paras)
        raw_res = cur.fetchone()
        close_db_connection(cur, db)
        return format_trans_one(raw_res, default_map + tea_extra)
    else:
        cur.execute(f'SELECT id, name, sex, fname, telephone, address, grade, is_foreign_stu '
                    f'FROM "student_information" '
                    f'WHERE "student_information".id=%s', paras)
        raw_res = cur.fetchone()
        close_db_connection(cur, db)
        return format_trans_one(raw_res, default_map + stu_extra)


# 更改用户信息
def update_user_info(_id, _telephone, _address):
    # 调用存储过程: 'modify_users'
    sql = f'CALL modify_users(%s, %s, %s);'
    paras = [_telephone, _address, _id]
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(sql, paras)
    db.commit()
    close_db_connection(cur, db)


# 获取学生课程信息
def fetch_stu_course(sid, is_major=True):
    # 通过score计算gpa, 并保留两位小数
    sql = f'CREATE OR REPLACE VIEW student_course AS ' \
          f'SELECT "SC".cid, "SC".score, CAST((4-3*(100-"SC".score)^2/1600) as DECIMAL(3,2)) AS gpa, "SC".is_w, ' \
          f'"SC".semester, "Course".cname, "Course".category, "Course".credit ' \
          f'FROM "SC", "Course" ' \
          f'WHERE "SC".sid = %s and "SC".is_major= %s ' \
          f'and "SC".cid = "Course".cid and "SC".tid = "Course".tid'
    paras = [sid, is_major]
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(sql, paras)
    db.commit()
    sql = f'SELECT * FROM student_course'
    cur.execute(sql)
    # results用于展示学生选课的所有信息(is_major的限制下，包括了退课的课)
    results_full = format_trans(cur.fetchall(), SC_info)
    # 按类别统计学分, 平均成绩, 平均gpa, 保留两位小数
    sql = f'SELECT category, SUM(credit) AS total_credits, CAST(AVG(score) as DECIMAL(5,2)) AS avg_scores, ' \
          f'CAST((SUM(credit*gpa)/SUM(credit)) as DECIMAL(3,2)) AS avg_gpa ' \
          f'FROM student_course GROUP BY category'
    cur.execute(sql)
    results_category = format_trans(cur.fetchall(), category_info)
    close_db_connection(cur, db)

    return results_full, results_category


# 获取去重的课程号
def fetch_cid(tid):
    sql = f'SELECT "Course".cid UNIQUE FROM "Course" WHERE "Course".tid=%s'
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(sql, [tid])
    results = format_trans(cur.fetchall(), ['cid'])
    close_db_connection(cur, db)

    return results


# 获取教师授课信息
def fetch_tea_course(tid):
    # 按课程、学期统计平均分、最高分 建立了临时视图
    sql = f'WITH "S_ANY"(cid, semester, avg_score, max_score) AS ( ' \
          f'SELECT cid, semester, CAST(AVG("SC".score) as DECIMAL(5,2)), MAX("SC".score) ' \
          f'FROM "SC" WHERE "SC".tid=%s GROUP BY "SC".cid, "SC".semester) ' \
          f'SELECT "Course".cid, "Course".cname, "Course".category, "Course".credit, ' \
          f'"S_ANY".semester, "S_ANY".avg_score, "S_ANY".max_score ' \
          f'FROM "Course", "S_ANY" WHERE "Course".cid="S_ANY".cid and "Course".tid=%s ' \
          f'UNION ' \
          f'SELECT "Course".cid, "Course".cname, "Course".category, "Course".credit, null, null, null ' \
          f'FROM "Course" WHERE "Course".cid not in (SELECT cid FROM "SC") AND "Course".tid=%s'
    paras = [tid] * 3
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(sql, paras)
    results = format_trans(cur.fetchall(), TC_info)
    close_db_connection(cur, db)

    return results


# 获取不带score的信息（给定tid, cid, semester，返回sid, s_name），用于提供给add_scores页面
def fetch_course_without_score(cid, tid, semester):
    # 已经中期退课的学生成绩不由老师负责
    sql = f'SELECT "SC".sid, "student_information".name ' \
          f'FROM "SC", "student_information" ' \
          f'WHERE "SC".cid=%s and "SC".tid=%s and "SC".semester=%s and ' \
          f'"SC".sid="student_information".id and "SC".is_w=False'
    paras = [cid, tid, semester]
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(sql, paras)
    results = format_trans(cur.fetchall(), ['sid', 's_name'])
    close_db_connection(cur, db)

    return results


# 获取带score的信息（给定tid, cid, semester，返回sid, s_name, score），用于提供给modify_scores页面
def fetch_course_with_score(cid, tid, semester):
    # 已经中期退课的学生成绩不由老师负责
    sql = f'SELECT "SC".sid, "student_information".name, "SC".score ' \
          f'FROM "SC", "student_information" ' \
          f'WHERE "SC".cid=%s and "SC".tid=%s and "SC".semester=%s and ' \
          f'"SC".sid="student_information".id and "SC".is_w=False'
    paras = [cid, tid, semester]
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(sql, paras)
    results = format_trans(cur.fetchall(), ['sid', 's_name', 'score'])
    close_db_connection(cur, db)

    return results


# 更新学生成绩（包括增加和修改）
def update_scores(sids, scores, cid):
    db = get_db_connection()
    cur = db.cursor()
    for sid, score in zip(sids, scores):
        sql = f'UPDATE "SC" SET score=%s WHERE sid=%s and cid=%s'
        paras = [score, sid, cid]
        cur.execute(sql, paras)
    db.commit()
    close_db_connection(cur, db)


# 根据教务，查找对应的院系号
def faculty_id(aid):
    db = get_db_connection()
    cur = db.cursor()
    sql = f'SELECT fid FROM "Users" WHERE id=%s'
    cur.execute(sql, [aid])
    result = format_trans_one(cur.fetchone(), ['fid'])
    close_db_connection(cur, db)

    return result


# 根据院系号，统计学生信息
def faculty2stu(fid):
    db = get_db_connection()
    cur = db.cursor()
    # 按性别统计人数
    sql = f'SELECT sex, COUNT(*) FROM student_information WHERE fid=%s ' \
          f'GROUP BY sex'
    paras = [fid]
    cur.execute(sql, paras)
    res_sex = format_trans(cur.fetchall(), ['sex', 'stu nums'])
    # 按年级统计人数
    sql = f'SELECT grade, COUNT(*) FROM student_information WHERE fid=%s ' \
          f'GROUP BY grade'
    cur.execute(sql, paras)
    res_grade = format_trans(cur.fetchall(), ['grade', 'stu nums'])
    close_db_connection(cur, db)

    return res_sex, res_grade


# 根据院系号，统计教师信息
def faculty2tea(fid):
    db = get_db_connection()
    cur = db.cursor()
    # 按性别统计人数
    sql = f'SELECT sex, COUNT(*) FROM teacher_information WHERE fid=%s ' \
          f'GROUP BY sex'
    paras = [fid]
    cur.execute(sql, paras)
    res_sex = format_trans(cur.fetchall(), ['sex', 'tea nums'])
    # 按职称统计人数
    sql = f'SELECT title, COUNT(*) FROM teacher_information WHERE fid=%s ' \
          f'GROUP BY title'
    cur.execute(sql, paras)
    res_title = format_trans(cur.fetchall(), ['title', 'tea nums'])
    close_db_connection(cur, db)

    return res_sex, res_title


# 根据院系号，统计课程信息
def faculty2course(fid):
    db = get_db_connection()
    cur = db.cursor()
    # 按类别统计课程数，这里在用COUNT聚集函数的时候加了distinct关键字，因为Course表中同一课程可能有多名教师授课，但是只算一次
    sql = f'SELECT category, COUNT(distinct cid) FROM "Course" WHERE tid in ' \
          f'(SELECT id FROM teacher_information WHERE fid=%s) ' \
          f'GROUP BY category'
    cur.execute(sql, [fid])
    res_cate = format_trans(cur.fetchall(), ['category', 'course nums'])
    close_db_connection(cur, db)

    return res_cate


# 根据院系号，查询教师
def get_tid(fid):
    db = get_db_connection()
    cur = db.cursor()
    sql = f'SELECT id FROM teacher_information WHERE fid=%s'
    cur.execute(sql, [fid])
    res_tid = format_trans(cur.fetchall(), ['tid'])
    close_db_connection(cur, db)

    return res_tid


# 根据院系号，查询教师
def get_teachers_by_fid(fid):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(f'SELECT id, name, sex, fname, telephone, address, working_year, title '
                f'FROM "teacher_information" '
                f'WHERE "teacher_information".fid=%s', [fid])
    res = format_trans(cur.fetchall(), default_map + tea_extra)
    close_db_connection(cur, db)
    return res


# 根据院系号，查询学生
def get_students_by_fid(fid):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(f'SELECT id, name, sex, fname, telephone, address, grade, is_foreign_stu '
                f'FROM "student_information" '
                f'WHERE "student_information".fid=%s', [fid])
    res = format_trans(cur.fetchall(), default_map + stu_extra)
    close_db_connection(cur, db)
    return res


# 添加新课程
def update_course(cid, tid, cname, category, credit):
    db = get_db_connection()
    cur = db.cursor()
    sql = f'INSERT INTO "Course" VALUES (%s, %s, %s, %s, %s)'
    paras = [cid, tid, cname, category, credit]
    cur.execute(sql, paras)
    db.commit()
    close_db_connection(cur, db)
