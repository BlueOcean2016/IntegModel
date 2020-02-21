# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render



from modelApp.models import DatabaseType,Database,Theme,FieldType,Table,Fields

from django.db.models import Q

from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


import datetime,sys,math,importlib
reload(sys)
sys.setdefaultencoding( "utf-8" )

# Create your views here


def home(request):
    request.encoding='utf-8'

    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #now_time = 10

    return render(request, 'home.html',{'now_time': now_time})



def model(request):
    context = {}
    request.encoding = 'utf-8'
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        db_type = str(request.GET['db_type'])
    except:
        pass

    try:
        eff_flag = str(request.GET['eff_flag'])
    except:
        pass

    databaseTypes = DatabaseType.objects.all().order_by("id")

    themes = Theme.objects.all().order_by("id")

    databases = Database.objects.all().order_by("id")

    if db_type:
        databases = databases.filter(db_type=db_type)

    if eff_flag:
        databases = databases.filter(eff_flag=eff_flag)

    db_list = {}

    for db in databases:
        pass
        # db['table_cnt'] = 100
        # db_list[] = 100

    paginator = Paginator(databases, 10)
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    if paginator.num_pages > 11:
        if page - 5 < 1:
            pageRange = range(1, 11)  # 按钮数
        elif page + 5 > paginator.num_pages:  # 按钮数加5大于分页数
            pageRange = range(page - 5, page + 1)  # 显示的按钮数
        else:
            pageRange = range(page - 5, page + 6)  # range求的是按钮数   如果你的按钮数小于分页数 那么就按照正常的分页数目来显示
    else:
        pageRange = range(1, paginator.num_pages + 1)

    context['pageRange'] = pageRange

    context['now_time'] = now_time

    context['databaseTypes'] = databaseTypes
    context['themes'] = themes
    #context['businesslines'] = businesslines

    context['databases'] = databases
    context['contacts'] = contacts

    context['db_type'] = db_type
    context['eff_flag'] = eff_flag

    return render(request, 'model.html', context)


def table(request, db_id):
    context = {}

    # 数据库ID

    context['db_id'] = int(db_id)
    # 数据库名称

    context['db_name'] = Database.objects.get(id=db_id).db_name

    # 数据库类型

    context['db_type'] = Database.objects.get(id=db_id).db_type

    # 表列表

    tables = Table.objects.filter(db_name_id=db_id).order_by("tb_name")
    context['tables'] = tables

    tables_num = Table.objects.filter(db_name_id=db_id).count()
    context['tables_num'] = tables_num
    # context['db_name'] = str(dbname)
    # tables = Table.objects.all()
    # tables = Table.objects.filter(db_name=dbname)
    # context['tables'] = tables
    return render(request, 'table.html', context)