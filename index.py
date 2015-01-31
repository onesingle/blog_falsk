#coding=utf-8
from werkzeug.serving import run_simple
from datetime import datetime
import g
from data import db,app

import view

app.config.from_object('config')




#app.register_blueprint(admin,url_prefix = '/admin')





def _timestr0(dt):
    mon = g.Mons[str(dt.month)]
    return u'%s月<span>%d</span>' % (mon, dt.day)
app.jinja_env.filters['timestr0'] = _timestr0

def _timestr1(dt):
    return '%d:%d' % ( dt.hour, dt.minute )
app.jinja_env.filters['timestr1'] = _timestr1

def _timestr2(dt):
    return u'%d年%d月%d日 %d:%d:%d' % ( dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second )
app.jinja_env.filters['timestr2'] = _timestr2

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))


if __name__ == '__main__':
    
    db.create_all()
    run_simple('localhost', 5000, app,
               use_reloader=True, use_debugger=True, use_evalex=True)