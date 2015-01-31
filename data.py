#coding=utf-8
# this is mybolg app data


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#coding=utf-8
from sqlalchemy import and_, or_,func
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


#--Model For Blog--

class Category(db.Model):
    def __init__(self,name):
        self.name = name
        
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),unique=True)
    num=db.Column(db.Integer)
    
    def __unicode__(self):
        return self.name


class Tag(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),unique=True)

    def __unicode__(self):
        return self.name


class Article( db.Model ):
    id = db.Column( db.Integer, primary_key=True)
    title = db.Column( db.String(100))
    content = db.Column( db.Text)
    status = db.Column( db.Integer, default=1) #0, 草稿、1, 完成、-1,  失效
    created_time = db.Column( db.DateTime, default=datetime.now)
    modified_time = db.Column( db.DateTime, default=datetime.now)
    is_always_above = db.Column( db.Integer, default=0) #置顶 0,1
    share = db.Column(  db.Integer, default=0) #分享到社交网络
    click_count = db.Column( db.Integer, default=0)
    category_id = db.Column( db.Integer, db.ForeignKey('category.id'))
    category = db.relationship( 'Category', backref=db.backref('articles',lazy='dynamic'))
    
    author_id = db.Column( db.Integer, db.ForeignKey('user.id'), default=1)
    author = db.relationship( 'User', backref='articles', lazy='select')
    tags = db.Column(db.String)
    #tags = db.relationship( 'Tag', secondary=article_tags, backref=db.backref('articles',lazy='dynamic'))
    
    def __init__(self, title,rawbody, tags, category):
        self.title = title
        self.content = rawbody  # TODO: markdown support
        self.created = datetime.utcnow()
        self.tags = tags
        self.category = category  # added category to the Post object
        
    def __unicode__(self):
        return self.title

class Comment( db.Model ):
    id = db.Column( db.Integer, primary_key=True)
    username = db.Column( db.String(50))
    email_address = db.Column( db.String(80))
    site = db.Column( db.String(100))
    avatar = db.Column( db.String(100)) #头像
    content = db.Column( db.Text)
    post_date = db.Column( db.DateTime, default=datetime.now)
    visible = db.Column( db.Integer, default=1) #是否展示
    reply_to_comment_id = db.Column( db.Integer, db.ForeignKey('comment.id'))
    reply_to_comment = db.relationship( 'Comment', backref='comments', remote_side=[id])
    article_id = db.Column( db.Integer, db.ForeignKey('article.id'))
    article = db.relationship( 'Article', backref=db.backref('comments',lazy='dynamic') )
    
    
class User( db.Model ):
    id = db.Column( db.Integer, primary_key=True)
    #social account
    uid = db.Column( db.BigInteger)
    name = db.Column( db.String(50))
    avatar = db.Column( db.String(100))
    token = db.Column( db.String(80))
    login_type = db.Column( db.Integer) #1:weibo;

    def __unicode__(self):
        return self.name


class Link( db.Model ):
    id = db.Column( db.Integer, primary_key=True)
    name = db.Column( db.String(50))
    site = db.Column( db.String(100)) #url

    def __unicode__(self):
        return self.name


class BlackList( db.Model ):
    id = db.Column( db.Integer, primary_key=True)
    ip_address = db.Column( db.String(15))

    def __unicode__(self):
        return self.ip_address


class Subscriber( db.Model ):
    id = db.Column( db.Integer, primary_key=True)
    username = db.Column( db.String(50))
    email_address = db.Column( db.String(80))
    subscrible_time = db.Column( db.DateTime, default = datetime.now)
    enabled = db.Column( db.Integer, default=True)

    def __unicode__(self):
        return self.username
class Image(db.Model):
    def __init__(self,name):
        self.name = name
        
    key = db.Column(db.Integer,primary_key = True)
    #photo =db.Column(camelot.types.Image(app.config.IMG_DIR))
    
# -- Data Operation --
class Data( object ):
    def create_all(self):
        db.create_all()

class DataWrapper(object):
    def get_all_category(self):
        return Category.query.all()

    def get_all_tag(self):
        return Tag.query.all()

    def create_article(self, title, content, tags, category):
        a = Article(title=title, content=content, category_id=category)
        tag_list = tags.split()
        for name in tag_list:
            #不需要lower限制，默认就是忽略大小写的
            #t = db.session.query(Tag).filter( func.lower(Tag.name)==name.lower() ).first()
            t = db.session.query(Tag).filter( Tag.name==name ).first()
            if not t:
                t = Tag(name=name)
            a.tags.append(t)
        db.session.add(a)
        db.session.commit()
        return a
    def del_article(self, title, content, tags, category):
        a = Article(title=title, content=content, category_id=category)
        article = Article.query.get(id)
        if a:
           db.session.delete(a)
           db.session.commit()
           #flash("Post deleted.")
        else:
            pass#flash("Couldn't delete.")
        return  article
        
    def get_article_by_id(self, id):
        article = Article.query.get(id)
        return article

    def get_article_by_page(self, pid, per_page):
        p = Article.query.order_by(Article.created_time.desc()).paginate(pid, per_page,error_out=True)
        #p = Article.query.paginate(pid, per_page,error_out=True)
        return p

    def search_article(self, keywords, page=1, per_page=10):
        filter_clause = []
        for k in keywords.split():
            filter_clause.append( or_(*[ Article.title.contains(k),
                                        Article.content.contains(k)]) )
        articles = Article.query.filter( and_(*filter_clause) ).all()
        return articles

    def get_category_by_id(self, id):
        return Category.query.get(id)

    def get_tag_by_id(self, id):
        return Tag.query.get(id)

    def create_comment(self, username, email_address, site, avatar, content, ip, \
                        reply_to_comment_id, article_id):
        c = Comment(username=username, email_address=email_address, site=site, \
            avatar=avatar, content=content, article_id=article_id)
        if reply_to_comment_id:
            c.reply_to_comment_id = int(reply_to_comment_id)
        db.session.add(c)
        db.session.commit()
        return c

    def get_comment_by_id(self, id):
        comment = Comment.query.get(id)
        return comment

    def get_user_by_id(self, id):
        user = User.query.get(id)
        return user

    def get_all_link(self):
        links = Link.query.all()
        return links
    
    #获取文章总数
    def get_all_Artcile_Num(self):
        tatol_num=len(Article.query.all())
        return tatol_num
    
    def get_imgs(self,offset=None, limit=6):
        '''返回所有的图片'''
        images = Image.query.all()
        '''
        if offset is not None:
            offset = images % offset
        prefix = settings.K_IMG.replace('%s', '')
        l = len(prefix)
        ret = []
        for k in Image.query.all() #(prefix, limit=limit, marker=offset):
            ret.append(k[l:])
        '''
        return images

    

