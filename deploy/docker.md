# 新建容器
docker run  -v F:/Docker:/home/working/ -p 80:80 -p 5431:5432 -p 8081:8080 -p 8001:8000 -p 6379:6379 --privileged   --name weekly -d -it  centos /usr/sbin/init

#进入容器
docker exec -it weekly bash

#执行shell
bash /home/working/weekly/deploy/init.sh

#备份还原pg sql数据
cd "c:\Program Files\PostgreSQL\9.6\bin\"
pg_dump   -U postgres test > f:\docker\weekly\test.bak

psql test -f /home/working/weekly/test.bak

#备份还原django数据
备份一个APP的数据
python manage.py dumpdata accounts --format=json > accounts.json
备份整个db
python manage.py dumpdata --format=json > bak.json
2.恢复
python manage.py loaddata app.json


# 为运行的container增加多个端口
#先关掉容器
docker ps -a
docker stop weekly
#2. commit the container,NOTE: The above, test02 is a new image that I'm constructing from the test01 container.test02 是新的image name
docker commit weekly publish
docker rm weekly
3. re-run from the commited image
docker run -v F:/Docker:/home/working/ -p 80:80 -p 5431:5432 -p 8081:8080 -p 8001:8000 -p 6379:6379 -p 9001:9001  --name weekly --privileged  publish /usr/sbin/init


#vue-cli不会热刷新
echo fs.inotify.max_user_watches=524288 |  tee -a /etc/sysctl.conf &&  sysctl -p