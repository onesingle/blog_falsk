#coding=utf-8
import os
import os.path as osp

DEBUG = 'SERVER_SOFTWARE' not in os.environ            #?
DEBUG = True

USER = {
    'name' : u'单 行 道',
    'email': u'xishimy'
        }

Mons = {
    '1':u'一',
    '2':u'二',
    '3':u'三',
    '4':u'四',
    '5':u'五',
    '6':u'六',
    '7':u'七',
    '8':u'八',
    '9':u'九',
    '10':u'十',
    '11':u'十一',
    '12':u'十二'
}

def static_url(url):
    url = url
    return "/static/" + url

def admin_url(url):
    url = url
    return "/static/admin/" + url

def admin_static(url):
    url=url
    return "/static/admin/" + url

_site_info = {
        # 用于登录的网址，起一个别人不容易知道的网址
        'login_url': '/login' if DEBUG else '/must_not_be_guessed',
        'title': u'Pabo Blog',
        'subtitle': u'知识就是力量',
        'keywords': u'博客 python tornado sae pabo 开源',  # 网站关键字
        'description': u'Pabo是一个利用python tornado web server搭建于sae上面的博客程序. 采用KVDB存储全站数据.',  # 给搜索引擎用的
        'theme': 'default',  # 网站主题样式
        'admin_theme': 'admin',  # 后台管理主题样式
        # 友链
        'links': {
            'http://pabo.sinaapp.com': 'Pabo Blog',
            'http://www.baidu.com': u'百度一下，你就知道',
        },
        'author': {
            'name': u'书记',
            'intro': u'书记，专注Web前端技术的凡夫俗子。',
        },
        # 注: 请不要修改链接link值
        'navs': [
            {'link': '/', 'label': u'首页', 'title': u'Pabo Blog首页'},
            {'link': '/archives', 'label': u'归档', 'title': u'文章归档'},
            {'link': '/message', 'label': u'留言', 'title': u'访客留言'},
            {'link': '/rss', 'label': u'订阅', 'title': u'RSS订阅'},
            #{'link': '/about', 'label': u'关于', 'title': u'关于'},
        ],
        'app': 5,  # article per page
        # 是否预览友链(如果友链多了，可能会比较卡)
        # XXX 如果友链那边设置了'X-Frame-Options'(如设为'SAMEORIGIN'),
        # 那么iframe将不能显示.
        'links_preview': False,
        # 是否显示登录链接[安全起见，最好设置为False]
        'show_login':DEBUG,
        'rss_full': False,  # rss是否全文输出
        # url显示类型，将按照顺序加载，如果加载失败，将自动尝试后面一种显示类型
        # XXX 目前暂时用short
        # 可以根据情况变换4种类型的顺序
        # short是短网址，一般为5个小写字母;(推荐使用)
        # digit则是文章的id, 速度最快;
        # english: Google翻译标题作为网址(可能不能正常访问Google导致翻译失败);
        # pinyin: 将文章标题转换为拼音.(产生的url可能会很长)
        'url_show_order': ['short', 'digit', 'english', 'pinyin'],

        'admin': {
            'url': '/admin',
            'title': u'后台管理',
            'navs': [
                # 不要修改link的值
                {'link': '/admin/stats', 'label': u'概览', 'icon': 'home'},
                {'icon': 'book', 'label': u'文章', 'sub':[
                    {'link': '/admin/article/add', 'label': u'发表文章'},
                    {'link': '/admin/articles/manage', 'label': u'管理文章'},
                ]},
                {'link': '/admin/classes', 'label': u'分类', 'icon': 'th-list'},
                {'link': '/admin/attachments', 'label': u'附件', 'icon': 'paper-clip'},
                {'link': '/admin/friends', 'label': u'友链', 'icon': 'link'},
                {'link': '/admin/settings', 'label': u'设置', 'icon': 'cog'},
                {'link': '/admin/kv', 'label': u'KVDB', 'icon': 'hdd'},
            ],
            'default': '/admin/stats',  # 登录后台后默认显示的页面
        },
        'baidu_statistics': '''
<script>
var _bdhmProtocol = (("https:" == document.location.protocol) ? " https://" : " http://");
document.write(unescape("%3Cscript src='" + _bdhmProtocol + "hm.baidu.com/h.js%3Fb665710f3241366f461da2dfe6af1dda' type='text/javascript'%3E%3C/script%3E"));
</script>''',
    }
