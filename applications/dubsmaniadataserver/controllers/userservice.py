# -*- coding: utf-8 -*-
# try something like
import gluon.contenttype
import datetime
import json

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

def register():
    username = request.vars.username
    password = request.vars.password
    email = request.vars.email
    dob = datetime.datetime.strptime(request.vars.dob, "%Y%m%d").date()

    row = db.auth_user(username = username)
    if not row:
        user = db.auth_user.validate_and_insert(username = username, password = password, email = email, dob = dob)
	if not user.id == None:
            return gluon.contrib.simplejson.dumps({'result': True})
	else:
	    return gluon.contrib.simplejson.dumps({'result': False})
    else:
        raise HTTP(409, 'username exists')

def login():
    username = request.vars.username
    password = request.vars.password

    user = auth.login_bare(username,password)
    if not user:
        return gluon.contrib.simplejson.dumps({'result': user})
    return gluon.contrib.simplejson.dumps({'result': True})

def loginfailed(*args):
    raise HTTP(409, 'autorization failed')

auth.settings.on_failed_authentication = loginfailed

def verifyUser():
    username = request.vars['username']
    user = db(db.auth_user.username == username).select()
    import gluon.contrib.simplejson
    try:
        user[0]
        return gluon.contrib.simplejson.dumps({'result': True})
    except:
        return gluon.contrib.simplejson.dumps({'result': False})

def verifyUserEmail():
    useremail = request.vars['useremail']
    user = db(db.auth_user.email == useremail).select()
    import gluon.contrib.simplejson
    try:
        user[0]
        return gluon.contrib.simplejson.dumps({'result': True})
    except:
        return gluon.contrib.simplejson.dumps({'result': False})

@auth.requires_login()
def addvedioboard():
    user = auth.user
    board_name = request.vars.name
    icon = int(request.vars.icon)
    try:
        db.video_board.insert(board_name = board_name, user_d = user, icon_id = icon)
        return gluon.contrib.simplejson.dumps({'result': True})
    except:
        return gluon.contrib.simplejson.dumps({'result': False})

@auth.requires_login()
def addvideo():
    user = auth.user
    name = request.vars.name
    fileid = request.vars.fileid
    thumbnail = request.vars.thumbnail
    tags = json.loads(request.vars.tags)

    try:
        db.video.insert(name = name, thumbnail = thumbnail, user_d = user, fileid = fileid)
        return gluon.contrib.simplejson.dumps({'user': auth.user.username, 'result': True, 'name':name, 'fileid':fileid, 'thumbnail':thumbnail})
    except:
        return gluon.contrib.simplejson.dumps({'user': auth.user.username, 'result': False, 'name':name, 'fileid':fileid, 'thumbnail':thumbnail})

@service.jsonrpc
def markfavorite():
    user = auth.user
    video = request.vars.videoid
    try:
        db.favrioute.insert(vedio, user = user)
        return {'user': auth.user, 'result': True}
    except:
        return {'result': False}

@auth.requires_login()
def addvideotoboard():
    user = auth.user
    board = request.vars.boardid
    video = request.vars.videoid
    try:
        board = db((db.video_board.user_d == user) & (db.video_board.board_name == board)).select()[0]
        video = db((db.video.user_d == user) & (db.video.id == video)).select()[0]
        db.video_board_item.insert(video_board = board, video = video)
        return gluon.contrib.simplejson.dumps({'result': True})
    except:
        return gluon.contrib.simplejson.dumps({'result': False})

@auth.requires_login()
def getboards():
    user = auth.user
    try:
        row = db(db.video_board.user_d == user).select()
        return gluon.contrib.simplejson.dumps({'boardlist':[{'id': r.id, 'name': r.board_name, 'iconid': r.icon_id} for r in row]})
    except:
        return gluon.contrib.simplejson.dumps({'result': False})

@service.jsonrpc
def addtag(tag, vedio):
    try:
        tag = db(db.tag.tag == tag).select()
        vedio = db(db.vedio.id == vedio).select()
        db.tag_item.insert(tag = tag, vedio = vedio)
        return {'result': True}
    except:
        return {'result': False}
