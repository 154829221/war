# -*- coding: UTF-8 -*-

import sys,os
from flask import render_template
from flask import Markup,flash
from flask import Flask, request, redirect, url_for,abort,session,escape
from werkzeug import secure_filename
from dbtools import *
from xmltools import statexml as sx
from werkzeug import SharedDataMiddleware

#cookie
from flask import make_response

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__,template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#只需设置一个名为 FLASKR_SETTINGS 的环境变量，指向要加载的配置文件。启用静默模式告诉 Flask 在没有设置该环境变量的情况下噤声。
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/stat')
def stat():
    return 'OK'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath

#结尾带上斜杠的访问时候如果不带斜杠，斜杠将补全
@app.route('/projects/')
def projects():
    return 'The project page'

##结尾不带斜杠的，访问带斜杠的将返回404
@app.route('/about')
def about():
    return 'The about page'

#变量规则
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

#方法
# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     error = None
#     searchword = request.args.get('q', '')
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#                        request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#     # the code below is executed if the request method
#     # was GET or the credentials were invalid
#     return render_template('login.html', error=error)


#session
@app.route('/')
def show_entries():
    return redirect(url_for('stat_status'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'dengyunfei':
            error = 'Invalid username'
        elif request.form['password'] != '123456':
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))
# set the secret key.  keep this really secret:
#app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.secret_key = os.urandom(24)

#消息闪现 http://docs.jinkan.org/docs/flask/patterns/flashing.html#message-flashing-pattern


#文件上传
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #url_for使用示例
            return redirect(url_for('upload_result',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
    <p><input type=file name=file>
    <input type=submit value=Upload>
    </form>
    '''

@app.route('/upload_result', methods=['GET'])
def upload_result():
    return  '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>%s Upload Success</h1>
    '''

#实现文件的下载（也可以借助nginx服务发布）
app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=False)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})

#构造 URL,显示访问链接
with app.test_request_context():
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    # assert request.path == '/about'
    assert request.method == 'GET'

    print url_for('stat')
    print url_for('projects')
    print url_for('about')
    print url_for('about',next='/')
    #根据函数名找到装饰器配置形成的url路径
    print url_for('show_user_profile',username='dengyunfei')
    #打印静态文件url路径
    print url_for('static', filename='style.css')
    #对数据的转义。<strong>Hello &lt;blink&gt;hacker&lt;/blink&gt;!</strong>
    print Markup('<strong>Hello %s!</strong>') % '<blink>hacker</blink>'

#cookie 示例。
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    resp = make_response(render_template('hello.html', name=name))
    has_cookie = request.cookies.get('has_cookie')
    if has_cookie=='true':
        print has_cookie
        return render_template('hello.html', name=name,cookie=has_cookie)
    else:
        resp.set_cookie('has_cookie', 'true')
        return resp

#401 跳转
@app.route('/redirect')
def redirect1func():
    #url_for('redirect2func') == '/redirect2'
    return redirect(url_for('redirect2func'))

@app.route('/redirect2')
def redirect2func():
    abort(401)
    # this_is_never_executed()

@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('page_not_found.html'),404)
    #设定头信息
    resp.headers['X-Something'] = 'A value'
    return resp

#http://192.168.33.101:5000/state_status
@app.route('/state_status')
def stat_status():
    #获取了数据库的操作句柄
    dconn = get_mysql_handle()
    statStatus = dconn.getStatStatus()
    # if statStatus[1]!=None:
    #     print "Can not get state status."
    #     return "Can not get state status."
    # else:
    #     print "stat_status_to_xml= sx.state_status(statStatus[0])"
    stat_status_to_xml= sx.state_status(statStatus)
    return stat_status_to_xml

app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')