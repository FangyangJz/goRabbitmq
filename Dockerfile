FROM rabbitmq:3-management
RUN rabbitmq-plugins enable --offline rabbitmq_stomp rabbitmq_web_stomp