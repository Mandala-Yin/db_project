from datetime import timedelta
from flask import Flask, redirect
import log_manage
import admin
import teacher
import student

app = Flask(__name__)
app.secret_key = 'my_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.register_blueprint(log_manage.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(teacher.bp)
app.register_blueprint(student.bp)


@app.route('/')
def homepage():  # 主页展示
    return redirect('/login')


if __name__ == '__main__':
    app.run()
