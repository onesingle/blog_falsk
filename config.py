#coding=utf-8
import os
import os.path as osp
import inspect
from data import app
import jinja2 

from g import _site_info,DEBUG
from template import PaboBlogRender



if DEBUG:
    import logging
    logging.getLogger().setLevel(logging.DEBUG)


PABO_PATH = osp.dirname(osp.abspath(__file__))
#BLOG_PATH=osp.abspath(path)

TEMPLATE_DIR = osp.join(PABO_PATH, 'templates')
IMG_DIR = (PABO_PATH, "database/uploads/")
def IMG_DET_SAVE(filename):
    return osp.join(PABO_PATH, "database/uploads/",filename)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])   #允许上传的文件格式
#######################################################################
# site_info  ?
#######################################################################

_extra = dict(
    site_info=_site_info,
    
)


#env = Environment(loader=FileSystemLoader(['/myblog/templates/admin/', 'templates']))
#app.jinja_loader = env
#app.jinja_env = Environment(extensions=['jinja2.ext.do'])

#env.loader.FileSystemLoader(['/myblog/templates/admin/', \
#                                 '/myblog/templates'])

my_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(['/myblog/templates/admin/', \
                                 '/myblog/templates']),
        
    ],)


app.jinja_loader = my_loader

app.jinja_env.add_extension("jinja2.ext.do") #加载 do 
'''
render = PaboBlogRender(                           #PaboBlogRender?
    template_path=[
        osp.join(TEMPLATE_DIR, 'normal', _theme),      # 普通模板
        osp.join(TEMPLATE_DIR, 'admin', _admin)     # admin后台管理模板,如果有admin_theme，就加载，否则加载default
    ],
    trim_blocks=True,
    auto_reload=settings.DEBUG,
    extra=_extra,
    extensions=['jinja2.ext.do'],
)
'''

# SQL config
# MYSQL_HOST='localhost'
# MYSQL_PORT='8090'
MYSQL_USR=''
MYSQL_PASS=''
MYSQL_DB=''
SQLALCHEMY_DATABASE_URI='sqlite:////home/single/workspace/myblog/database/test1.db'
ad_pass='single'
ad_user='admin'


#####################################################################

######################################################################

