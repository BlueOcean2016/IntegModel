"""IntegModel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from modelApp import views as modelAppViews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', modelAppViews.home, name='home'),
    url(r'^home/$', modelAppViews.home, name='home'),
    url(r'^model/$', modelAppViews.model, name='model'),
    url(r'^table/db=(.*)/$',modelAppViews.table,name='table'),
    url(r'^fields/tb_id=(.*)/$',modelAppViews.fields,name='fields'),
    url(r'^saveFields/$',modelAppViews.saveFields,name='saveFields'),
    url(r'^fields_detail/field_id=(.*)/$',modelAppViews.fields_detail,name='fields_detail'),
    url(r'^updateFields/$',modelAppViews.updateFields,name='updateFields'),
    url(r'^searchtableresult/$',modelAppViews.searchtableresult,name='searchtableresult'),
    url(r'^searchfieldresult/$',modelAppViews.searchfieldresult,name='searchfieldresult'),
    url(r'^createTableSql/$',modelAppViews.createTableSql,name='createTableSql'),
    url(r'^exportTable/db_id=(.*)/tb_id=(.*)/$',modelAppViews.exportTable,name='exportTable'),
    url(r'^tabledependency/tb_id=(.*)/$',modelAppViews.tabledependency,name='tabledependency'),
    url(r'^addbeforejobdependency/tb_id=(.*)/$',modelAppViews.addbeforejobdependency,name='addbeforejobdependency'),
    url(r'^searchjobdependency/$',modelAppViews.searchjobdependency,name='searchjobdependency'),
    url(r'^execRelation/$',modelAppViews.execRelation,name='execRelation'),
]
