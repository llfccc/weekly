# 新建容器
docker run  -v F:/Docker:/home/working/ -p 192.168.19.12:80:80   --privileged   --name week -d -it  centos /usr/sbin/init 

#进入容器
docker exec -it week bash

#执行shell
bash /home/working/weekly/deploy/init.sh

#备份还原pg sql数据
pg_dump   -U postgres test > C:\test.bak
psql  -U postgres -d test < /home/working/test.bak

#备份还原django数据
备份莫一个APP
python manage.py dumpdata accounts --format=json > accounts.json
备份整个db
python manage.py dumpdata --format=json > bak.json
2.恢复
python manage.py loaddata app.json