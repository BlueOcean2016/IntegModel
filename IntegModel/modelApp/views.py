# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render



import datetime,sys,math,importlib
reload(sys)
sys.setdefaultencoding( "utf-8" )

# Create your views here


def home(request):
    request.encoding='utf-8'

    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #now_time = 10

    return render(request, 'home.html',{'now_time': now_time})


