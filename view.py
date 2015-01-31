#coding=utf-8

from data import *
from g import USER,_site_info,admin_url,static_url,admin_static
import json
from flask import Flask,render_template,session,request,session,\
        url_for, redirect,Response,jsonify,g,Blueprint,flash,get_template_attribute,abort
from functools import wraps
from flask.ext.misaka import Misaka
from config import IMG_DET_SAVE
from werkzeug import secure_filename
from os import  path
from admin import *
import itertools
dw = DataWrapper()

Misaka(app)

@app.before_request
def before_request():
    g.user = USER
    g.info = _site_info
    g.admin_url = admin_url
    g.static_url = static_url
    g.admin_static = admin_static


@app.route('/')
@app.route('/page/<int:pid>')
def index(pid=1):
    per_page = 2
    p = dw.get_article_by_page(pid, per_page)
    articles = p.items
    if not p.total:
        pagination = [0]
    elif p.total % per_page:
        pagination = range(1, p.total / per_page + 2)
    else:
        pagination = range(1, p.total / per_page + 1)

    return render_template('index.html',
        articles=articles,
        pid=pid,
        pagination=pagination[:2],
        last_page=pagination[-1],
        nav_current="index",

        )


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != "admin":
            error = 'Invalid username'
        elif request.form['password'] != "single":
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('admin_base'))
        flash(error)
    return render_template('login.html', error=error)



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('index'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logged = session.get('logged_in', None)
        if not logged:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

'''
@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():

    if request.method == 'POST':

        try:
            title = request.form['title']
            content = request.form['content']
            tags = request.form['tags']
            category = Category.query.filter_by(name=request.form['category']).first()
            #category="test"
            flash('nothing !!')
            # Added first() so that only one category is added
        except Exception as e:
            flash('There was an error with your input: %s' % e)

            return redirect(url_for('new_post'))
        for thing in request.form.keys():  # verification
            if not request.form[thing]:
                flash('Error: %s incorrect.' % thing)
                return redirect(url_for('new_post'))

        p = Article(title, content, tags, category)

        tag_list = tags.split()
        for name in tag_list:

            #t = db.session.query(Tag).filter( func.lower(Tag.name)==name.lower() ).first()
            t = db.session.query(Tag).filter( Tag.name==name ).first()
            if not t:
                t = Tag(name=name)
            p.tags.append(t)

        db.session.add(p)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        categories = Category.query.all()
        return render_template('admin_add_article.html', categories=categories)
'''

@app.route("/admin/del/<int:id>")
def del_Article():
    del_Article()
    #return redirect(url_for("/admin/"))

@app.route("/admin/")
@login_required
def admin_base():
    app.jinja_env.add_extension("jinja2.ext.do")
    return render_template("/admin/admin_base.html")


#添加文章
@app.route("/admin/article/add",methods=['GET', 'POST'])
@login_required
def admin_article_add():
    car = dw.get_all_category()
    if request.method == "POST":
        try:
            title = request.form['title']
            content = request.form['md']
            #tags = request.form['tags']
            tags="tags"
            category = Category.query.filter_by(name=request.form['cls']).first()
            #category="test"
            flash('nothing !!')
            # Added first() so that only one category is added
        except Exception as e:
            flash('There was an error with your input: %s' % e)

            return redirect(url_for('new_post'))
        for thing in request.form.keys():  # verification
            if not request.form[thing]:
                flash('Error: %s incorrect.' % thing)
                return redirect(url_for('new_post'))

        p = Article(title, content, tags, category)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('index'))
    else:

        return render_template("/admin/admin_add_article.html",categories=car)

@app.route("/admin/articles/manage")
@login_required
def admin_articles_manage():
    articles = Article.query.order_by(Article.created_time.desc())
    total_num=dw.get_all_Artcile_Num()
    cur_num = 1
    return render_template("admin/admin_manage_articles.html",articles = articles,
                           total_num=total_num,cur_num = cur_num )


#分页
@app.route('/admin.get.articles.page.')
def admin_article_page():
    articles = Article.query.order_by(Article.created_time.desc())
    total_num=dw.get_all_Artcile_Num()
    cur_num = 1
    page=total_num/cur_num
    return jsonify(page)


@app.route("/admin/classes")
@login_required
def admin_add_classes():
    if request.path.endswith('.json'):
        car = get_template_attribute('/admin/admin_widgets.html', 'calsses_table')      #get macro in a template
        categories = car(categories=dw.get_all_category(), ajax=True)
        return jsonify(categories)              #flask.json.jsonify(*args, **kwargs)
    else:
        car = dw.get_all_category()
        return render_template("admin/admin_classes.html",categories=car)

@app.route("/_add_widgets")
def admin_widgets():
    car = get_template_attribute('/admin/admin_widgets.html', 'classes_table')
    categories = dw.get_all_category()
    return jsonify(categories,ajax=True)                   #有bug json 转换

@app.route("/_add_class",methods=['GET', 'POST'])
def add_class():
    if request.method == 'POST':

        name = json.dumps(request.form['cls']) # get cls

        p =Category(name)
        db.session.add(p)
        db.session.commit()
        return jsonify()
    else:
        return render_template("admin/admin_classes.html")

@app.route("/admin/attachments")
def admin_attachment():

    return render_template("admin/admin_attachments.html")

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
#IMG_DIR = osp.join(PABO_PATH, "/database/uploads")
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/admin.upload.img.json", methods=['GET', 'POST'])
def admin_add_img():
    '''
    file = request.files['pic']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(IMG_DIR, filename)
        '''
    if request.method == 'POST':
        file = request.files['pic']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(IMG_DET_SAVE(filename))
            #return redirect(url_for('uploaded_file',
            #                       filename=filename))
            #img = Image(file)
            #db.session.add(img)
            #db.session.commit()
    #i = Image.key
    return jsonify(file)
@app.route("/admin.get.imgs.marker.",methods=['GET','POST'])
def admin_get_imgs():
    images = Image.query.all()
    if request.method == 'GET':
        pass
    else:

        return render_template("admin/admin_attachments.html",imgs=images)
@app.route("/admin/settings")
def admin_settings():

    return render_template("admin/admin_settings.html")

@app.route("/admin/friends")
def admin_friends():

    return render_template("admin/admin_friends.html")

@app.route("/admin/stats")
def admin_stats():

    return render_template("admin/admin_stats.html")

###########################################################
@app.route('/article/<int:id>')
def article(id):
    article = dw.get_article_by_id(id)
    if not article:
        abort(404)
        #return '404'
    comments = article.comments.order_by(Comment.post_date).all() #升序排序
    return render_template('blog.html',
        article=article,
        comments=comments,

        )

@app.route("/comments/add",methods =['POST'])
def comment_add():
    avatar="/static/images/gravatar.jpg"
    ip = '192.168.12.123'
    '''
    article_id = request.form.get["article",None]
    name=request.form["name"]
    email=request.form["email"]
    site=request.form["site"]
    message=request.form["message"]
    reply_to_comment_id = request.form.get('reply_to_comment', None)
    '''
    if request.method == 'POST':
        try:
            article_id = request.form.get("article",None)
            name=request.form["name"]
            email=request.form["email"]
            site=request.form["website"]
            message=request.form["message"]
            reply_to_comment_id = request.form.get('reply_to_comment', None)
        except Exception as e:
            flash("nothing")
    p=dw.create_comment(name, email, site, avatar, message,ip,reply_to_comment_id, article_id)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for("index"))

