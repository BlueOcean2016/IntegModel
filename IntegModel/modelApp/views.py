# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render



from modelApp.models import DatabaseType,Database,Theme,FieldType,Table,Fields,TableLevel,TableDependency

from django.db.models import Q

from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


import datetime,sys,math,importlib
import os, sys, json, time,random,xlwt,io
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


def fields(request, tb_id):
    context = {}
    table = Table.objects.get(id=tb_id)
    context['table'] = table

    fields = Fields.objects.filter(tb_name_id=tb_id).order_by('fields_rank')
    db = Database.objects.get(id=table.db_name_id.id)
    fieldtypes = FieldType.objects.filter(db_type=db.db_type).order_by('id')
    context['fields'] = fields
    context['fieldtypes'] = fieldtypes
    context['db'] = db
    context['hdfsfile'] = str(table.db_name_id.warehouse_dir) + "/" + str(table.db_name_id.db_name) + "." + str(
        table.db_name_id.database_hdfs) + "/" + str(table.tb_name)
    return render(request, 'fields.html', context)



def saveFields(request):

    jsonString = str(request.GET['jsonString']);

    delete_flag = str(request.GET['delete_flag']);

    context = {}

    print(delete_flag)

    if delete_flag == "1":
        tb_name_id = int(jsonString)
        Fields.objects.filter(tb_name_id=tb_name_id).delete()
    else :
        index = 0

        fields = json.loads(jsonString)

        for field in fields:
            tb_name_id = str(field['tb_name_id'])
            fields_rank = str(field['fields_rank'])
            fields_name = str(field['fields_name'])
            fields_cn_name = str(field['fields_comment'])

            fields_type = str(field['fields_type'])


            partition_flag = str(field['partition_flag'])

            fields_detail = str(field['fields_detail'])


            myFields = Fields(tb_name_id=Table.objects.get(id=tb_name_id),fields_rank=fields_rank,fields_name=fields_name,fields_cn_name=fields_cn_name,fields_type=FieldType.objects.get(id=fields_type),partition_flag=partition_flag,fields_detail=fields_detail,)

            myFields.save()
            index = index + 1

        context['result'] = jsonString


    return HttpResponse(json.dumps(context), content_type='application/json')


# 字段详细信息
def fields_detail(request, field_id):

    context = {}

    field = Fields.objects.get(id=field_id)

    context['field'] = field

    return render(request, 'fields_detail.html', context)


#更新字段
def updateFields(request):
    context = {}
    field_id = str(request.GET['field_id']);
    fields_detail = str(request.GET['fields_detail']);

    vfield = Fields.objects.get(id=field_id)
    vfield.fields_detail = fields_detail

    vfield.save()

    context['fields_detail'] = fields_detail
    context['field_id'] = field_id

    return HttpResponse(json.dumps(context), content_type='application/json')


def searchtableresult(request):
    context = {}

    try:
        keyword = str(request.GET['keyword'])
    except:
        keyword = ''

    try:
        db_id = str(request.GET['db_id'])
    except:
        db_id = '-1'

    # 表状态
    try:
        # pass
        state_flag = str(request.GET['state_flag'])
    except:
        state_flag = '-1'
        pass

        # 主题域
    try:
        # pass
        table_theme_id = str(request.GET['table_theme_id'])
    except:
        table_theme_id = '-1'
        pass

        # 层次结构
    try:
        # pass
        table_level_id = str(request.GET['table_level_id'])
    except:
        table_level_id = '-1'
        pass

    # 是否有效
    try:
        eff_flag = str(request.GET['eff_flag'])
    except:
        eff_flag = '1'
        pass

    if keyword <> '':
        tables = Table.objects.filter(
            Q(tb_cn_name__icontains=keyword) | Q(tb_name__icontains=keyword) | Q(tb_job__icontains=keyword))
    else:
        tables = Table.objects.all()

    # 判断数据库
    if db_id == '-1':
        pass
    else:
        tables = tables.filter(db_name_id=db_id)
        pass

        # 判断表状态
    if state_flag == '-1':
        pass
    else:
        tables = tables.filter(state_flag=state_flag)

    # 判断表主题
    if table_theme_id == '-1':
        pass
    else:
        tables = tables.filter(table_theme=table_theme_id)

    # 判断表层级
    if table_level_id == '-1':
        pass
    else:
        tables = tables.filter(table_level=table_level_id)

    if eff_flag == '-1':
        pass
    else:
        tables = tables.filter(eff_flag=eff_flag)

    tablelevels = TableLevel.objects.all()
    themes = Theme.objects.all()
    databases = Database.objects.all()

    # 表分页
    paginator = Paginator(tables, 10)
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
    context['contacts'] = contacts

    context['table_cnt'] = tables.count()
    context['tables'] = tables
    context['page'] = int(page)
    context['tablelevels'] = tablelevels
    context['themes'] = themes
    context['databases'] = databases

    context['keyword'] = keyword
    context['db_id'] = int(db_id)
    context['state_flag'] = state_flag
    context['table_theme_id'] = int(table_theme_id)
    context['table_level_id'] = int(table_level_id)
    context['eff_flag'] = int(eff_flag)

    return render(request, 'searchtableresult.html', context)


def searchfieldresult(request):
    context = {}

    try:
        keyword = str(request.GET['keyword'])
    except:
        keyword = ''

    try:
        # pass
        state_flag = str(request.GET['state_flag'])
    except:
        state_flag = '-1'
        pass

    tablelevels = TableLevel.objects.all()
    themes = Theme.objects.all()

    context['tablelevels'] = tablelevels
    context['themes'] = themes

    if keyword <> '':
        fields = Fields.objects.filter(Q(fields_name__icontains=keyword) | Q(fields_cn_name__icontains=keyword) | Q(
            fields_detail__icontains=keyword))
    # tables = Table.objects.filter(Q(tb_cn_name__icontains=keyword)|Q(tb_name__icontains=keyword)|Q(tb_job__icontains=keyword))
    else:
        fields = Fields.objects.all()

    # 字段分页
    paginator = Paginator(fields, 10)
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
    context['contacts'] = contacts

    context['keyword'] = keyword
    context['fields'] = fields
    context['fields_cnt'] = fields.count()
    return render(request, 'searchfieldresult.html', context)


#一键生成建表语句
def createTableSql(request):
    context = {}

    tb_id = str(request.GET['tb_id'])

    # db 数据库
    db = Table.objects.get(id=tb_id).db_name_id
    db_type = db.db_type
    db_name = db.db_name
    db_cn_name = db.db_cn_name

    remark = db.remark
    # table 表
    table = Table.objects.get(id=tb_id)
    tb_name = table.tb_name
    tb_cn_name = table.tb_cn_name

    commentline = ")comment '%s'" % (tb_cn_name)

    table_level = table.table_level.table_level_cn_name
    table_theme = table.table_theme.table_theme_cn_name
    manage_external_flag = table.manage_external_flag
    partition_flag = table.partition_flag
    sd_flag = table.sd_flag
    static_flag = table.static_flag

    # hdfsfile = table.hdfsfile
    if table.hdfsfile == '':
        hdfsfile = str(table.db_name_id.warehouse_dir) + "/" + str(table.db_name_id.db_name) + "." + str(
        table.db_name_id.database_hdfs) + "/" + table.tb_name
    else:
        hdfsfile = table.hdfsfile

    table_author = table.table_author
    table_detail = table.table_detail

    # 字段
    # 非分区字段
    vfields = Fields.objects.filter(tb_name_id=tb_id, partition_flag='0').order_by('fields_rank')

    filedsline = ''
    i = 0
    for field in vfields:
        # print field.fields_name,field.fields_cn_name
        if i == 0 :
            line = "`%s`    %s      comment     '%s' \n" % (
                str(field.fields_name), str(field.fields_type.fields_type), str(field.fields_cn_name))
        else :
            line = ",`%s`    %s      comment     '%s' \n" % (
        str(field.fields_name), str(field.fields_type.fields_type), str(field.fields_cn_name))

        filedsline = filedsline + line
        i = i + 1

    # 分区字段
    partitionfiledsline = ''
    alterpartitionfiledsline = ''
    alterline = ''
    vfields = Fields.objects.filter(tb_name_id=tb_id, partition_flag='1').order_by('fields_rank')

    if vfields.count() == 0:
        pass
    else:
        partitionfiledsline = '\npartitioned by ('
        line2 = '/'
        for field in vfields:
            tmpline = "%s='2018-01-01'," % (str(field.fields_name))

            line = "%s  %s," % (str(field.fields_name), str(field.fields_type))

            partitionfiledsline = partitionfiledsline + line
            alterpartitionfiledsline = alterpartitionfiledsline + tmpline
            line2 = line2 + "%s/" % (str(field.fields_name))

        partitionfiledsline = partitionfiledsline[:-1] + ")"

        alterline = '''

        -- insert overwrite table %s.%s  partition(ds='{{yesterday}}')


       alter table %s.%s drop if exists partition(%s); \n
       alter table  %s.%s add if not exists partition(%s) \n location '%s%s';

    ''' % (db_name, tb_name, db_name, tb_name, alterpartitionfiledsline[:-1], db_name, tb_name,
           alterpartitionfiledsline[:-1], hdfsfile, line2)

    formatline = '''\n row format delimited
       fields terminated by '^' '''

    formatline = '''\nrow format delimited \nnull defined as "" \nstored as textfile '''

    #locationline = ''
    createline = ''
    # print table_type_cn_name
    if str(manage_external_flag) == '1':
        manage_external = 'external'
    else:
        manage_external = ''

    locationline = "\nlocation '%s';" % (hdfsfile)
    createline = '''--建表语句-- \n create %s table if not exists %s.%s ( \n ''' % (str(manage_external),db_name, tb_name)

    line0 = "drop table if exists %s.%s ;" % (db_name, tb_name) + "\n"

    insersql = "\n" + "--  insert overwrite table %s.%s  partition(ds='{{yesterday}}') " % (db_name, tb_name)
    context['dropsql'] = line0
    context['result'] = createline + filedsline[
                                     :-2] + "\n" + commentline + partitionfiledsline + formatline + locationline + "\n" + insersql

    context['altersql'] = alterline
    context['db_name'] = db_name
    context['tb_name'] = tb_name

    return HttpResponse(json.dumps(context), content_type='application/json')


# 导出全平台或者指定数据库
def exportTable(request, db_id, tb_id):
    context = {}
    style_heading = xlwt.easyxf("""
        font:
            name Arial,
            colour_index white,
            bold on,
            height 200;
        align:
            wrap off,
            vert center,
            horiz center;
        pattern:
            pattern solid,
            fore-colour 0x19;
        borders:
            left THIN,
            right THIN,
            top THIN,
            bottom THIN;
        """
                                )

    style_heading1 = xlwt.easyxf("""
        font:
            name Arial,
            colour_index white,
            bold on,
            height 200;
        align:
            wrap off,
            vert center,
            horiz center;
        pattern:
            pattern solid,
            fore-colour aqua;
        borders:
            left THIN,
            right THIN,
            top THIN,
            bottom THIN;
        """
                                 )

    style_body = xlwt.easyxf("""
        font:
            name 微软雅黑,
            bold off,
            height 200;
        borders:
            left THIN,
            right THIN,
            top THIN,
            bottom THIN;
        """
                             )
    style_body2 = xlwt.easyxf("""
        font:
            name 微软雅黑,
            bold off,
            height 200;
        borders:
            left THIN,
            right THIN,
            top THIN,
            bottom THIN;
        """
                              )

    style_body3 = xlwt.easyxf("""
        font:
            name 微软雅黑,
            bold on,
            colour_index blue,
            height 200;
        borders:
            left THIN,
            right THIN,
            top THIN,
            bottom THIN;

        """
                              )

    style_body4 = xlwt.easyxf("""
        font:
            name 微软雅黑,
            bold on,
            colour_index black,
            height 200;
        borders:
            left THIN,
            right THIN,
            top THIN,
            bottom THIN;

        """
                              )

    # 维护一些样式， style_heading, style_body, style_red, style_green
    style_green = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x11;")

    style_red = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x0A;")

    style_blue = xlwt.easyxf(
        " pattern: pattern solid,fore-colour 0x01;align: wrap on, vert centre, horiz center;border: left 1,right 1,top 1,bottom 1 ;font: colour_index blue,bold on")

    style_black = xlwt.easyxf(
        " pattern: pattern solid,fore-colour 0x01;align: wrap on, vert centre, horiz center;border: left 1,right 1,top 1,bottom 1 ;font: colour_index black,bold on")

    fmts = [
        'M/D/YY',
        'D-MMM-YY',
        'D-MMM',
        'MMM-YY',
        'h:mm AM/PM',
        'h:mm:ss AM/PM',
        'h:mm',
        'h:mm:ss',
        'M/D/YY h:mm',
        'mm:ss',
        '[h]:mm:ss',
        'mm:ss.0',
    ]
    style_body.num_format_str = fmts[0]

    # 创建一个文件
    wb = xlwt.Workbook(encoding='utf-8')

    # 设置HttpResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # 判断是否为全平台还是指定数据库
    # 如果是全部数据库,取全表
    if str(db_id) == '-1':

        # alltables = Table.objects.all()
        # 指定有效的表
        alltables = Table.objects.filter(eff_flag=1)
        response['Content-Disposition'] = 'attachment;filename=db_%s.xls' % (
            datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    # 否则取指定的数据库
    else:
        pass
        db_name = Database.objects.get(id=db_id).db_name
        alltables = Table.objects.filter(db_name_id=db_id, eff_flag=1)
        response['Content-Disposition'] = 'attachment;filename=%s.xls' % (db_name)
    sheet = wb.add_sheet("目录")
    sheet.write_merge(0, 5, 0, 14, "大数据平台字典--%s \r\n" % (datetime.datetime.now().strftime('%Y%m%d')), style_heading1)
    # table.write_merge(x, x + m, y, y + n, string, style)
    # x表示行，y表示列，m表示跨行个数，n表示跨列个数，string表示要写入的单元格内容，style表示单元格样式。
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # sheet.write_merge(6,6+3,0,13,'generated by %s' % (request.user.username+"  "+nowtime),style_heading1)
    sheet.write(6, 0, '序号', style_heading)
    sheet.write(6, 1, '类型', style_heading)
    sheet.write(6, 2, '主题域', style_heading)
    sheet.write(6, 3, '层次结构', style_heading)
    sheet.write(6, 4, '数据库名称', style_heading)
    sheet.write(6, 5, '表名称', style_heading)
    sheet.write(6, 6, '表解释', style_heading)
    sheet.write(6, 7, '管理/外部表', style_heading)
    sheet.write(6, 8, '全/增量', style_heading)
    sheet.write(6, 9, '是否分区', style_heading)
    sheet.write(6, 10, '是否静态', style_heading)
    sheet.write(6, 11, '作业名称', style_heading)
    sheet.write(6, 12, 'hdfs路径', style_heading)
    sheet.write(6, 13, '状态', style_heading)
    sheet.write(6, 14, '负责人', style_heading)

    # 所有表的集合

    if str(db_id) == '-1' or str(db_id) == '':
        # tablelist = Table.objects.all()
        tablelist = Table.objects.filter(eff_flag=1)
    elif str(tb_id) == '-1' or str(tb_id) == '':
        tablelist = Table.objects.filter(db_name_id=db_id, eff_flag=1)
    else:
        tablelist = Table.objects.filter(db_name_id=db_id, id=tb_id, eff_flag=1)

    index = 7
    for indextable in tablelist:

        # 数据库名称
        db_name = str(indextable.db_name_id.db_name)
        # 数据库类型名称
        db_type = str(indextable.db_name_id.db_type.db_type_name)
        # 数据库中文名称
        db_cn_name = str(indextable.db_name_id.db_cn_name)
        # 表名称
        tb_name = str(indextable.tb_name)
        # 表解释
        tb_cn_name = str(indextable.tb_cn_name)
        # hdfs路径
        # hdfsfile = str(indextable.hdfsfile)

        # location路径
        if indextable.hdfsfile == '':
            hdfsfile = str(indextable.db_name_id.warehouse_dir) + "/" + str(indextable.db_name_id.db_name) + "." + str(
            indextable.db_name_id.database_hdfs) + "/" + str(indextable.tb_name)
        else :
            hdfsfile = str(indextable.hdfsfile)

        # 管理表外部表
        manage_external = ''
        # 全量/增量
        sd_name = ''
        # 是否分区
        partition_name = ''
        # 作业名称
        tb_job = str(indextable.tb_job)
        # 是否静态
        static_name = ''
        # 状态
        state_flag = str(indextable.state_flag)
        # 更新时间
        update_date = str(indextable.update_date)
        # 负责人
        table_author = str(indextable.table_author)
        # 表层级
        table_level = str(indextable.table_level.table_level_name)
        # 主题域
        table_theme = str(indextable.table_theme.table_theme_cn_name)

        sheet.write(index, 0, str(index - 6), style_body2)
        sheet.write(index, 1, str(indextable.db_name_id.db_type.db_type_name), style_body2)
        sheet.write(index, 2, str(indextable.table_theme.table_theme_cn_name), style_body2)
        sheet.write(index, 3, str(indextable.table_level.table_level_name), style_body2)
        sheet.write(index, 4, str(indextable.db_name_id.db_name), style_body2)
        sheet.write(index, 5, str(indextable.tb_name), style_body2)

        link = 'HYPERLINK("#%s";"%s")' % (
        str(str(indextable.id) + '_' + indextable.tb_cn_name) + '!A1', str(indextable.tb_cn_name))
        sheet.write(index, 6, xlwt.Formula('%s' % link), style_body3)
        # sheet.write(index,6, str(indextable.tb_cn_name), style_body2)

        # 管理/外部

        if str(indextable.manage_external_flag) == '1':
            manage_external = '外部'
        elif str(indextable.manage_external_flag) == '0':
            manage_external = '管理'
        else:
            manage_external = '其他'
        # sheet.write(index,6, str(indextable.manage_external_flag), style_body2)
        sheet.write(index, 7, manage_external, style_body2)

        # 全量/增量

        if str(indextable.sd_flag) == '1':
            sd_name = '全量'
        else:
            sd_name = '增量'
        # sheet.write(index,7, str(indextable.sd_flag), style_body2)
        sheet.write(index, 8, sd_name, style_body2)

        # 是否分区

        if str(indextable.partition_flag) == '1':
            partition_name = '是'
        else:
            partition_name = '否'

        # sheet.write(index,8, str(indextable.partition_flag), style_body2)
        sheet.write(index, 9, partition_name, style_body2)

        # 是否静态

        if str(indextable.static_flag) == '1':
            static_name = '是'
        else:
            static_name = '否'

        # sheet.write(index,9, str(indextable.static_flag), style_body2)
        sheet.write(index, 10, static_name, style_body2)

        sheet.write(index, 11, str(indextable.tb_job), style_body2)
        sheet.write(index, 12, str(indextable.hdfsfile), style_body2)
        sheet.write(index, 13, str(indextable.state_flag), style_body2)
        sheet.write(index, 14, str(indextable.table_author), style_body2)

        # 每一张表创建一个sheet,名称为: ods.test(测试)
        sheet_name = str(indextable.id) + '_' + tb_cn_name

        tablesheet = wb.add_sheet(sheet_name)

        # tablesheet.write_merge(0,0,1,4,db_name,style_black)

        baserow = 2

        tablesheet.write_merge(0, baserow - 1, 0, 9, db_name + '.' + tb_name + '(' + tb_cn_name + ')', style_black)

        # 第一行
        tablesheet.write(baserow + 0, 0, '数据库名称:', style_heading1)
        tablesheet.write_merge(baserow + 0, baserow + 0, 1, 3, db_name, style_black)  # 合并第1行到第1行 第2列到第4列

        tablesheet.write(baserow + 0, 4, '数据库类型:', style_heading1)
        tablesheet.write_merge(baserow + 0, baserow + 0, 5, 7, db_type, style_black)
        # link = 'HYPERLINK("#%s";"%s")' % ('目录!A10','返回')
        # tablesheet.write_merge(0,0,5,8,xlwt.Formula('%s'%link),style_blue)  #合并第1行到第1行 第6列到第9列

        # 第二行 数据库类型  数据库名称
        tablesheet.write(baserow + 1, 0, '表名称:', style_heading1)
        tablesheet.write_merge(baserow + 1, baserow + 1, 1, 3, tb_name, style_black)

        tablesheet.write(baserow + 1, 4, '层级:', style_heading1)
        tablesheet.write_merge(baserow + 1, baserow + 1, 5, 7, table_level, style_black)

        # 第三行
        tablesheet.write(baserow + 2, 0, '表解释:', style_heading1)
        tablesheet.write_merge(baserow + 2, baserow + 2, 1, 3, tb_cn_name, style_black)

        tablesheet.write(baserow + 2, 4, '主题域:', style_heading1)
        tablesheet.write_merge(baserow + 2, baserow + 2, 5, 7, table_theme, style_black)

        # 第四行
        tablesheet.write(baserow + 3, 0, '管理/外部表:', style_heading1)
        tablesheet.write_merge(baserow + 3, baserow + 3, 1, 3, manage_external, style_black)

        tablesheet.write(baserow + 3, 4, '全/增量:', style_heading1)
        tablesheet.write_merge(baserow + 3, baserow + 3, 5, 7, sd_name, style_black)

        # 第五行
        tablesheet.write(baserow + 4, 0, '是否分区:', style_heading1)
        tablesheet.write_merge(baserow + 4, baserow + 4, 1, 3, partition_name, style_black)

        tablesheet.write(baserow + 4, 4, '作业名称:', style_heading1)
        tablesheet.write_merge(baserow + 4, baserow + 4, 5, 7, tb_job, style_black)

        # 第六行
        #tablesheet.write(baserow + 5, 0, '是否静态:', style_heading1)
        #tablesheet.write_merge(baserow + 5, baserow + 5, 1, 3, static_name, style_black)

        #tablesheet.write(baserow + 5, 4, '表状态:', style_heading1)
        #tablesheet.write_merge(baserow + 5, baserow + 5, 5, 7, state_flag, style_black)

        # 第六行
        tablesheet.write(baserow + 5, 0, '更新时间:', style_heading1)
        tablesheet.write_merge(baserow + 5, baserow + 5, 1, 3, update_date, style_black)

        tablesheet.write(baserow + 5, 4, '负责人:', style_heading1)
        tablesheet.write_merge(baserow + 5, baserow + 5, 5, 7, table_author, style_black)

        # 第七行
        tablesheet.write(baserow + 6, 0, 'HDFS:', style_heading1)
        tablesheet.write_merge(baserow + 6, baserow + 6, 1, 7, hdfsfile, style_black)

        #第8行
        tablesheet.write(baserow + 7, 0, '使用备注:', style_heading1)
        tablesheet.write_merge(baserow + 7, baserow + 7, 1, 7, '', style_black)

        # 返回按钮
        link = 'HYPERLINK("#%s";"%s")' % ('目录!A10', '返回')
        tablesheet.write_merge(baserow + 0, baserow + 7, 8, 9, xlwt.Formula('%s' % link), style_blue)

        # 合并第2行到第3行的第0列到第3列。
        # worksheet.write_merge(1, 2, 0, 3, 'Second Merge', style)

        index = index + 1

        # 写字段
        # 写标题栏
        tablesheet.write(baserow + 8, 0, '序号', style_heading)
        tablesheet.write(baserow + 8, 1, '字段英文名', style_heading)
        tablesheet.write(baserow + 8, 2, '字段解释', style_heading)
        tablesheet.write(baserow + 8, 3, '字段类型', style_heading)
        tablesheet.write(baserow + 8, 4, '是否分区', style_heading)
        # tablesheet.write(baserow+8,5, '备注', style_heading)
        tablesheet.write(baserow + 8, 5, '标签1', style_heading)
        tablesheet.write(baserow + 8, 6, '标签2', style_heading)
        tablesheet.write_merge(baserow + 8, baserow + 8, 7, 9, '备注', style_heading)
        # sheet.write(2,6, '建表辅助', style_red)
        row = baserow + 9
        for field in Fields.objects.filter(tb_name_id=indextable.id).order_by('fields_rank'):
            tablesheet.write(row, 0, str(field.fields_rank), style_body4)
            tablesheet.write(row, 1, str(field.fields_name), style_body)
            tablesheet.write(row, 2, str(field.fields_cn_name), style_body)
            tablesheet.write(row, 3, str(field.fields_type.fields_type), style_body)

            tablesheet.write(row, 4, '是' if str(field.partition_flag) == '1' else '否', style_body)
            tablesheet.write(row, 5, '', style_body)
            tablesheet.write(row, 6, '', style_body)
            # tablesheet.write(row,5, field.fields_detail,style_body2)
            tablesheet.write_merge(row, row, 7, 9, field.fields_detail, style_body2)
            row = row + 1

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response


def tabledependency(request, tb_id):
    context = {}

    table = Table.objects.get(id=tb_id)
    context['table'] = table

    db_id = int(table.db_name_id.id)

    context['db_id'] = db_id

    context['db_name'] = Database.objects.get(id=db_id).db_name

    context['db_cn_name'] = Database.objects.get(id=db_id).db_cn_name

    context['db_type'] = Database.objects.get(id=db_id).db_type

    AfterTableDependencys = TableDependency.objects.filter(before_table_id=tb_id)
    AfterTable = []

    for index in AfterTableDependencys:
        id = index.after_table_id.id
        vtable = Table.objects.get(id=id)
        AfterTable.append(vtable)

    BeforeTableDependencys = TableDependency.objects.filter(after_table_id=tb_id)
    BeforeTable = []

    for index in BeforeTableDependencys:
        id = index.before_table_id.id
        vtable = Table.objects.get(id=id)
        BeforeTable.append(vtable)

    context['AfterTableDependencys'] = AfterTableDependencys
    context['AfterTable'] = AfterTable

    context['BeforeTableDependencys'] = BeforeTableDependencys
    context['BeforeTable'] = BeforeTable

    return render(request, 'tabledependency.html', context)


# 添加前置依赖表
def addbeforejobdependency(request, tb_id):
    context = {}

    table = Table.objects.get(id=tb_id)
    context['table'] = table

    # 获取所有前置依赖

    BeforeTableDependencys = TableDependency.objects.filter(after_table_id=tb_id)
    BeforeTable = []

    for index in BeforeTableDependencys:
        id = index.before_table_id.id
        vtable = Table.objects.get(id=id)
        BeforeTable.append(vtable)

    context['BeforeTable'] = BeforeTable

    AllTable = Table.objects.all()

    context['AllTable'] = AllTable

    cur_id = tb_id

    try:
        before_table_id = str(request.GET['before_table_id'])
        add_delete_type = str(request.GET['add_delete_type'])
        # 保存依赖关系表
        after_table_id = tb_id

        if add_delete_type == "add":
            vTableDependency = TableDependency(before_table_id=Table.objects.get(id=before_table_id),
                                               after_table_id=Table.objects.get(id=after_table_id), remark='')

            vTableDependency.save()
        elif add_delete_type == "delete":
            # Fields.objects.filter(tb_name_id=tb_name_id).delete()
            TableDependency.objects.filter(before_table_id=before_table_id, after_table_id=after_table_id).delete()
            return redirect('/tabledependency/tb_id=' + tb_id)
    except:
        pass

    add_delete_type = ''
    try:
        add_delete_type = str(request.GET['add_delete_type'])
    except:
        pass

    if add_delete_type == "delete":
        return redirect('tabledependency/tb_id=' + tb_id)

    return render(request, 'addbeforejobdependency.html', context)


def execRelation(request):
    keywords = str(request.GET['keywords'])
    context = {}

    if keywords <> '':
        table = Table.objects.get(id=keywords)
        # tableDependency1 = TableDependency.objects.filter(before_table_id=table.id)
        # tableDependency2 = TableDependency.objects.filter(after_table_id=table.id)
        tableDependency = TableDependency.objects.filter(Q(before_table_id=table.id) | Q(after_table_id=table.id));
    else:
        table = Table.objects.all()
        tableDependency = TableDependency.objects.all()

    tablelist = []
    for index in tableDependency:
        tablelist.append(index.before_table_id)
        tablelist.append(index.after_table_id)

    try:
        tablelist.append(Table.objects.get(id=keywords))
    except:
        pass
    # 顶点
    nodes = []

    v_dict1 = {"shape": "rect",
               "label": "A",
               "keep": 20,
               "runoff": 80,
               "id": "A"
               }
    v_dict2 = {"shape": "rect",
               "label": "B",
               "keep": 20,
               "runoff": 80,
               "id": "B"
               }

    # nodes.append(v_dict1)
    # nodes.append(v_dict2)

    # for index in table:
    for index in list(set(tablelist)):
        v_dict1 = {"shape": "rect",
                   "label": index.db_name_id.db_name + "." + index.tb_name,
                   "keep": 20,
                   "runoff": 80,
                   "id": str(index.id),
                   }
        nodes.append(v_dict1)

    # 边
    edges = []
    v_dict1 = {"source": "A",
               "target": "B",
               "val": 30,
               "id": "A_B"
               }
    # edges.append(v_dict1)

    for index in tableDependency:
        # for index in list(set(tableDependency)):
        v_dict1 = {"source": str(index.before_table_id.id),
                   "target": str(index.after_table_id.id),
                   "val": 30,
                   "id": str(index.before_table_id.id) + "_" + str(index.after_table_id.id)
                   }
        edges.append(v_dict1)

    context['data'] = "data"
    context['nodes'] = nodes
    context['edges'] = edges

    return HttpResponse(json.dumps(context), content_type='application/json')


def searchjobdependency(request):
    context = {}

    tableDependency = TableDependency.objects.all()

    context['tableDependency'] = tableDependency

    return render(request, 'searchjobdependency.html', context)