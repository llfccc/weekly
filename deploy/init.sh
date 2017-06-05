#!/bin/bash
#1.升级yum 
yum -y update 
yum  -y upgrade 

#2.安装基础开发包及安装python-dev
yum install -y  python-devel python-gevent
yum install -y  git   psmisc   gcc make vim

yum groupinstall -y "Development tools"

yum -y install epel-release wget 
yum -y install python-pip
pip install --upgrade pip

#安装nginx
yum install -y redis emacs  nginx   supervisor 
systemctl enable nginx.service
systemctl start nginx.service
systemctl enable redis
systemctl start redis
systemctl enable supervisor 
systemctl start supervisor 


#4.安装nodejs 和cnpm
yum install -y nodejs

npm install cnpm -g

#3.安装
pip install virtualenv

#3.安装django flask sqlalchemy numpy 

pip install numpy pandas uwsgi gunicorn  
pip install jupyter notebook
#安装redis 和postgresql
yum install -y redis
#安装pg
yum -y install postgresql postgresql-libs postgresql-server  
#初始化
postgresql-setup initdb
systemctl enable postgresql
systemctl start postgresql

#配置pg

#配置uwsgi
#因为虚拟环境，需把wsgi复制到manage.py同路径，并在wsgi中加入 
# import sys
# sys.path.append('/py2/lib/python2.7/site-packages') 
#略过

#
#清理yum
yum clean all