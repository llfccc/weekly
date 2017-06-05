# 新建容器
docker run  -v F:/Docker:/home/working/ -p 192.168.19.12:80:80   --privileged   --name week -d -it  centos /usr/sbin/init 

#进入容器
docker exec -it week bash

#执行shell
bash /home/working/weekly/deploy/init.sh