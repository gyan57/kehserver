# -*- coding: utf-8 -*-
# try something like
import gluon.contenttype

def searchapi():
	return service()

def gettrendingvideos():
    region = request.vars.region
    start = int(request.vars.start)
    end = int(request.vars.end)
    #return gluon.contrib.simplejson.dumps({'result': True})

    #try:
    region = db(db.d_region.f_region == region).select()[0]
    videos = [v.video for v in db(db.trending_vedio.f_region == region).select(db.trending_vedio.video)] #limitby=(start,end))]
    row = db(db.video.id.belongs(videos)).select(db.video.id, db.video.name, db.video.desc)
    #return db(db.video.id.belongs(videos)).select(db.video.id, db.video.name, db.video.desc)
    return gluon.contrib.simplejson.dumps({'video_list':[{'id': r.id, 'name': r.name, 'user': r.user_d, 'desc': r.desc} for r in row]})

def getfav():
    user = request.vars.user
    user = db(db.auth_user.username == user).select()[0]
    videos = [v.video for v in db(db.favriouts.user_d == user).select(db.favriouts.video)]
    row = db(db.video.id.belongs(videos)).select(db.video.id)
    return gluon.contrib.simplejson.dumps({'video_fav_list':[{'id': r.id } for r in row]})

def geticon():
    id = request.vars.id
    import gluon.contenttype
    #try:
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.jpg')
    row = db(db.video.id == id).select(db.video.thumbnail).first()
    #return gluon.contrib.simplejson.dumps({'result': row.thumbnail})
    filename, file = db.video.thumbnail.retrieve(row.thumbnail)
    return file.read()
    #except:
    return gluon.contrib.simplejson.dumps({'result': 'error'})

def getvideo():
    id = request.vars.id
    import gluon.contenttype
    #try:
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.mp4')
    row = db(db.video.id == id).select(db.video.video).first()
    #return gluon.contrib.simplejson.dumps({'result': row.thumbnail})
    filename, file = db.video.video.retrieve(row.video)
    return file.read()
    #except:
    return gluon.contrib.simplejson.dumps({'result': 'error'})


'''
@service.jsonrpc
def gettrendingvedioboard(start, end):
    return db(db.trending_board).select(limitby=(start,end))

@service.jsonrpc
def getboardvideos(board):
    board = db(db.video_board.board_name == board).select()[0]
    videos = [v.video for v in db(db.video_board_item.video_board == board).select(db.video_board_item.video)]
    return db(db.video.id.belongs(videos)).select()

@service.jsonrpc
def seachbytag(tag):
    tag = db(db.tag.tag == tag).select()
    return db(db.vedio.id == tag.id).select()
'''
