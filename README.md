# IntegModel

#  安装数据库

# 创建数据库 
drop database if exists integmodel; 
create database if not exists integmodel; 
alter database integmodel default character set utf8 collate utf8_general_ci;

# 创建项目
django-admin startproject IntegModel

# 创建模块
python manage.py startapp modelApp

# 创建更改的文件 
python manage.py makemigrations

# 将生成的py文件应用到数据库 
python manage.py migrate

# 创建用户
python manage.py createsuperuser

admin
admin@123
