# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


# 1.数据库类型
from modelApp.models import DatabaseType

# 2.主题域
from modelApp.models import Theme

#3.字段类型
from modelApp.models import FieldType

#4.表层次结构
from modelApp.models import TableLevel

#5.数据库
from modelApp.models import Database

#6.表
from modelApp.models import Table

#7.字段
from modelApp.models import Fields

# Register your models here.


admin.site.register(DatabaseType)
admin.site.register(Theme)
admin.site.register(FieldType)
admin.site.register(TableLevel)
admin.site.register(Database)
admin.site.register(Table)
admin.site.register(Fields)
#admin.site.register(BusinessLine)
#admin.site.register(TableDependency)
#admin.site.register(Fields)