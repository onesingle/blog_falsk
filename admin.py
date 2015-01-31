# coding: utf-8
from data import DataWrapper as dw
from data import *
###########################################################################
#                                   分类管理                              #
###########################################################################

def add_cls(name):
    '''添加分类'''
    import string
    


def get_all_category(self):
    '''查询所有分类'''         
    categories=Category.query.all()
    return categories