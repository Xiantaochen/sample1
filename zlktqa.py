#encoding: utf-8
from flask import Flask,render_template,make_response,url_for,request,redirect,session
from flask_bootstrap import Bootstrap
from flask_script import Manager
from decorators import login_required
import config
from models import User,Question
from exts import db
from functools import wraps
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

#登录限制的APP
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
             return  func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper

@app.route("/")
@login_required
def index():
    return render_template('index.html')

@app.route('/login/',methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        telephone = request.form.get("telephone")
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone,User.password == password).first()
        if user:
            session["user_id"] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u"手机号码或者密码错误，请确认后登录"

@app.route('/regist/',methods = ['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template("regist.html")
    else:
        telephone = request.form.get("telephone")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        #手机号码验证
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u"该手机已经被注册，请更换号码"
        else:
            #password1 要和password2想等
            if password1 != password2:
                return u"两次号码不相等，请核对后在填写!"
            else:
                user = User(telephone = telephone,username = username,password = password1)
                db.session.add(user)
                db.session.commit()
                #如果注册成功 ，跳转到登录页面
                return redirect(url_for('login'))
@app.route("/logout/")
def logout():
    session.pop("user_id")
    return redirect(url_for('login'))
@app.route("/question/",methods=["GET","POST"])
@login_required
def question():
    if request.method == "GET":
        return  render_template('question.html')
    else:
        title = request.form.get("title")
        content = request.form.get('content')
        question =Question(title = title,content = content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id ==user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("index"))

@app.context_processor
def my_context_processor():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id ==user_id).first()
        if user:
            return {"user" : user}
    return {}


if __name__ == '__main__':
    app.run()
