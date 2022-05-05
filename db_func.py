import psycopg2

default_map = ['id', 'name', 'sex', 'faculty', 'telephone', 'address']
login_map = ['id', 'password', 'role']
adm_extra = ['working_year', 'is_cadre']
tea_extra = ['working_year', 'title']
stu_extra = ['grade', 'is_foreign_stu']
SC_info = ['cid', 'score', 'is_major', 'is_w', 'semester', 'cname', 'category', 'credit']
category_info = ['category', 'credit', 'avg_score']


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
    trans_res = []
    for row in raw_res:
        row, trans_row = list(row), {}
        for col, val in zip(mapping, row):
            trans_row[col] = val
        trans_res.append(trans_row)

    return trans_res


# 将fetchone的结果从tuple转换为dict
def format_trans_one(raw_res, mapping=default_map):
    row, trans_row = list(raw_res), {}
    for col, val in zip(mapping, row):
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
    if u_role == 'admin':
        cur.execute(f'SELECT id, name, sex, fname, telephone, address, working_year, is_cadre '
                    f'FROM "admin_information" '
                    f'WHERE "admin_information".id=\'{u_id}\'')
        raw_res = cur.fetchone()
        close_db_connection(cur, db)
        return format_trans_one(raw_res, default_map+adm_extra)
    elif u_role == 'teacher':
        cur.execute(f'SELECT id, name, sex, fname, telephone, address, working_year, title '
                    f'FROM "teacher_information" '
                    f'WHERE "teacher_information".id=\'{u_id}\'')
        raw_res = cur.fetchone()
        close_db_connection(cur, db)
        return format_trans_one(raw_res, default_map + tea_extra)
    else:
        cur.execute(f'SELECT id, name, sex, fname, telephone, address, grade, is_foreign_stu '
                    f'FROM "student_information" '
                    f'WHERE "student_information".id=\'{u_id}\'')
        raw_res = cur.fetchone()
        close_db_connection(cur, db)
        return format_trans_one(raw_res, default_map + stu_extra)


def update_user_info(_id, _telephone, _address):
    sql = f'UPDATE "Users" SET telephone=\'{_telephone}\', address=\'{_address}\' WHERE id=\'{_id}\''
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(sql)
    db.commit()
    close_db_connection(cur, db)


def fetch_stu_course(sid, is_major=True):
    # 为了便于操作，建立了学生-选课视图，每次查询会重建视图
    sql = f'CREATE OR REPLACE VIEW student_course AS ' \
          f'SELECT "SC".cid, "SC".score, "SC".is_w, "SC".semester, "Course".cname, "Course".category, "Course".credit ' \
          f'FROM "SC", "Course" ' \
          f'WHERE "SC".sid = \'{sid}\' and "SC".is_major={is_major} ' \
          f'and "SC".cid = "Course".cid and "SC".tid = "Course".tid'
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(sql)
    db.commit()
    sql = f'SELECT * FROM student_course'
    cur.execute(sql)
    # results用于展示学生选课的所有信息(is_major的限制下，包括了退课的课)
    results_full = format_trans(cur.fetchall(), SC_info)
    # 按类别统计学分, 平均成绩
    sql = f'SELECT category, SUM(credit), AVG(score)::float FROM student_course GROUP BY category'
    cur.execute(sql)
    results_category = format_trans(cur.fetchall(), category_info)
    close_db_connection()

    return results_full, results_category


'''
if __name__ == '__main__':
    conn = get_db_connection()
    print(fetch_basic_information(conn, '200215', 'student'))
    close_db_connection(conn)
'''
