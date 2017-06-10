#!/bin/bash
set -e
#1.升级yum 
yum -y update 
yum  -y upgrade 

#2.安装基础开发包及安装python-dev
yum install -y  epel-release  
yum install -y  wget git psmisc gcc make vim nano
yum install -y  python-devel python-gevent
yum groupinstall -y "Development tools"

yum -y install python-pip 
pip install --upgrade pip  -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

#3.安装虚拟环境
#pip install virtualenv -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

#3.安装django flask sqlalchemy numpy 
pip install uwsgi   -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install -r /home/working/weekly/weekly/requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

#安装redis
yum install -y redis
systemctl enable redis
systemctl start redis

#安装postgresql
yum -y install postgresql postgresql-libs postgresql-server  
#初始化
postgresql-setup initdb
systemctl enable postgresql
systemctl start postgresql
#配置pg，修改默认密码，并且创建数据库
# su - postgres
# psql
# ALTER USER postgres WITH PASSWORD 'lanzhong';
# CREATE DATABASE test;
# \q
# exit

#手动修改pg认证方式 ，否则难以用密码连接上
#nano -w /var/lib/pgsql/data/pg_hba.conf
#  修改如下内容，信任指定服务器连接
#     # IPv4 local connections:
#     host    all            all      127.0.0.1/32      trust

#重启pg
systemctl restart postgresql
#配置uwsgi
mkdir /var/log/uwsgi
mkdir /etc/uwsgi
\cp -rf /home/working/weekly/deploy/uwsgi/uwsgi.ini /etc/uwsgi/

#uwsgi --http :8000 --chdir /home/working/weekly/weekly --module wsgi    --processes 2 --threads 2 &
#因为虚拟环境，需把wsgi复制到manage.py同路径，并在wsgi中加入 
# import sys
# sys.path.append('/py2/lib/python2.7/site-packages') 
#略过


#安装nginx
yum install -y nginx  
systemctl enable nginx
#配置nginx
mkdir  /etc/nginx/vhost.d
\cp -rf /home/working/weekly/deploy/nginx/nginx.conf /etc/nginx/nginx.conf
\cp -rf /home/working/weekly/deploy/nginx/vhost.d/  /etc/nginx/
systemctl stop nginx 
systemctl start nginx

#配置cupervisord
yum install -y  supervisor
mkdir /var/log/supervisor
echo_supervisord_conf > /etc/supervisord.conf
\cp -rf /home/working/weekly/deploy/supervisord/supervisord.d /etc/
\cp -rf /home/working/weekly/deploy/supervisord/supervisord.conf /etc/
#supervisord -c /etc/supervisord.conf

systemctl enable supervisord
# killall -9 supervisord
systemctl start supervisord 
supervisorctl reload



#4.安装nodejs 和cnpm
yum install -y nodejs
npm install cnpm -g --registry=https://registry.npm.taobao.org

# yum install -y httpd  
#清理yum
yum clean all
