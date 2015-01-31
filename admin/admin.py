#coding=utf-8
from werkzeug.serving import run_simple

from index import app
from flask import Flask
from flask_admin import Admin,BaseView,expose
from flask_admin.contrib.sqla import ModelView
from data import (db, Category, Tag, Article, Comment, User,\
                    Link, BlackList, Subscriber)


class MyView(ModelView):
   def is_accessible(self):
       return True
        
class FirstView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')



#app_admin = Flask(__name__)
#admin=Admin(app_admin)

admin=Admin(app,url="/admin")


admin.add_view(MyView(Category,db.session))
admin.add_view(MyView(Tag,db.session))
admin.add_view(MyView(Article,db.session))
admin.add_view(MyView(Comment,db.session))
admin.add_view(MyView(User,db.session))
admin.add_view(MyView(Link,db.session))
admin.add_view(MyView(BlackList,db.session))
admin.add_view(MyView(Subscriber,db.session))


if __name__ == '__main__':
    run_simple('localhost', 5000, app,
               use_reloader=True, use_debugger=True, use_evalex=True)