package main

import (
	"log"
	"os"

	"github.com/streadway/amqp"
)

func failOnError(err error, msg string){
	if err!=nil{
		log.Fatalf("%s, %s",msg, err)
	}
}

func main() {
	conn, err := amqp.Dial("amqp://guest:guest@localhost:5672/")
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channed")
	defer ch.Close()

	err = ch.ExchangeDeclare(
		"direct_logs",
		"direct",
		true,  // durable
		false, // auto-deleted
		false,  // internal
		false,  // no-wait
		nil,   // arguments
	)
	failOnError(err, "Failed to declare an exchange")

	q, err := ch.QueueDeclare(
		"",  // name
		false,  // durable
		false,  // delete when unused
		true,  // exclusive
		false,  // no-wait
		nil,  // arguments
	)
	failOnError(err, "Failed to declare a queue")

	if len(os.Args) < 2{
		log.Printf("Usage: %s [info] [warning] [error]", os.Args[0])
		os.Exit(0)
	} 
	for _, s := range os.Args[1:]{
		log.Printf("Binding queue %s to exchange %s with routing key %s",
				q.Name, "direct_logs", s)
		err = ch.QueueBind(
			q.Name,
			s,
			"direct_logs",
			false,
			nil,
		)
		failOnError(err, "Failed to bind a queue")
	}

	msgs, err := ch.Consume(
		q.Name,
		"",  // consumer
		true, // auto-ack 
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	failOnError(err, "Failed to register a consumer")
	
	forever := make(chan bool)

	go func(){
		for d:= range msgs{
			log.Printf("Received a message : %s", d.Body)
		}
	}()

	log.Printf("[*] Waiting for message. To exit press CTRL+C")
	<-forever
}