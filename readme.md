
# Docker
启动docker服务:
> sudo service docker start

插件端口占用情况:
* http/web-stomp	::	15674
* stomp	::	61613

官方给出的容器启动命令:
> sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15674:15674 -p 61613:61613 -p 15672:15672 rabbitmq:3-management

插件启动命令:
> sudo docker container exec -it rabbitmq bash

> rabbitmq-plugins enable rabbitmq_stomp

> rabbitmq-plugins enable rabbitmq_web_stomp

考虑使用docker命令在container启动之后, 在命令行启动插件, 以下命令失败, 容器会退出, 没起作用

> sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15674:15674 -p 61613:61613 -p 15672:15672 rabbitmq:3-management sh -c "rabbitmq-plugins enable rabbitmq_stomp && rabbitmq-plugins enable rabbitmq_web_stomp"

# Dockerfile使用
根据Dockerfile构建新的镜像(增加插件支持)
> sudo docker build -t rabbitmq:fangyang .

启动容器:
> sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15674:15674 -p 61613:61613 -p 15672:15672 rabbitmq:fangyang