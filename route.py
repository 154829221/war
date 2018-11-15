# -*- coding: UTF-8 -*-

import sys
from flask import Flask
from dbtools import *
from xmltools import statexml as sx
from flask import Blueprint, render_template
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

app = Flask(__name__,template_folder='template')

@app.route('/stat')
def stat():
    return 'OK'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

#http://192.168.33.101:5000/state_status
@app.route('/state_status')
def stat_status():
    #获取了数据库的操作句柄
    dconn = get_mysql_handle()
    statStatus = dconn.getStatStatus()
    if statStatus[1]!=None:
        return "Can not get state status."
    else:
        stat_status_to_xml= sx.state_status(statStatus[0])
        return stat_status_to_xml
