
# docker
sudo service docker start

http/web-stomp	::	15674
stomp	::	61613

sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15674:15674 -p 61613:61613 -p 15672:15672 rabbitmq:3-management

sudo docker container exec -it rabbitmq bash
rabbitmq-plugins enable rabbitmq_stomp
rabbitmq-plugins enable rabbitmq_web_stomp

# 会退出没起作用
sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15674:15674 -p 61613:61613 -p 15672:15672 rabbitmq:3-management sh -c "rabbitmq-plugins enable rabbitmq_stomp && rabbitmq-plugins enable rabbitmq_web_stomp"

# 通过构建 Dockerfile
FROM rabbitmq:3-management
RUN rabbitmq-plugins enable --offline rabbitmq_stomp rabbitmq_web_stomp

sudo docker build -t rabbitmq:fangyang .
构建了一个带插件的镜像
sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15674:15674 -p 61613:61613 -p 15672:15672 rabbitmq:fangyang