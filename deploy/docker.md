# 新建容器
docker run  -v F:/Docker:/home/working/ -p 192.168.19.12:80:80   --privileged   --name week -d -it  centos /usr/sbin/init 
docker run  -v F:/Docker:/home/working/ -p 192.168.19.12:80:80 -p 8080:8080 -p 8000:8000   --privileged   --name weekly -d -it  week02 /usr/sbin/init 

#进入容器
docker exec -it week bash

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
stop running container
docker ps -a
docker stop test01
2. commit the container
docker commit test01 test02
NOTE: The above, test02 is a new image that I'm constructing from the test01 container.test02 是新的image name

3. re-run from the commited image
docker run -p 8080:8080 -p 80:80-td test02


#vue-cli不会热刷新
echo fs.inotify.max_user_watches=524288 |  tee -a /etc/sysctl.conf &&  sysctl -p