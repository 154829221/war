# -*- coding: UTF-8 -*-

import sys,os
from flask import render_template
from flask import Markup
from flask import Flask, request, redirect, url_for
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

#http://192.168.33.101:5000/state_status
@app.route('/state_status')
def stat_status():
    #获取了数据库的操作句柄
    dconn = get_mysql_handle()
    statStatus = dconn.getStatStatus()
    if statStatus[1]!=None:
        print "Can not get state status."
        return "Can not get state status."
    else:
        print "stat_status_to_xml= sx.state_status(statStatus[0])"
        stat_status_to_xml= sx.state_status(statStatus[0])
        return stat_status_to_xml

