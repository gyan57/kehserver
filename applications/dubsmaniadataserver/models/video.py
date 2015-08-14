# -*- coding: utf-8 -*-
from gluon.tools import Auth
auth = Auth(db)

db.define_table('video_board', Field('board_name', 'string', required=True),
                Field('user_d', db.auth_user, required=True),
                Field('icon_id', 'integer'),
                format='%(board_name)s')

db.define_table('video',
                Field('name', 'string', required=True),
                Field('user_d', db.auth_user, required=True),
		Field('desc', 'string'),
                Field('thumbnail', 'upload', required=True),
		Field('video', 'upload', required=True),
                format='%(name)s')

db.define_table('video_board_item', Field('video_board', db.video_board, required=True),
                Field('video', db.video, required=True))

db.define_table('tag', Field('tag', 'string', required=True, unique=True))

db.define_table('tag_item', Field('tag', db.tag, required=True),
                Field('vedio', db.video))

db.define_table('favriouts', Field('user_d', db.auth_user, required=True),
                Field('video', db.video, required=True))


# db for region
db.define_table('d_region', Field('f_region', 'string', required=True), format='%(f_region)s')

db.define_table('trending_vedio',
                Field('f_region', db.d_region, required=True),
                Field('index_i', 'integer', required=True),
                Field('video', db.video, required=True))

db.define_table('trending_board', Field('region', 'string', required=True),
                Field('index_i', 'integer', required=True),
                Field('vedio_board', db.video_board, required=True))

db.define_table('discover', Field('region', 'string', required=True),
                Field('index_i', 'integer', required=True),
                Field('vedio', db.video, required=True))
