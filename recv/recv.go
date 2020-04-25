package main

import (
	"fmt"
	"log"

	"github.com/streadway/amqp"
)

func failOnError(err error, msg string){
	if err!=nil{
		log.Fatalf("%s, %s", msg, err)
		panic(fmt.Sprintf("%s, %s", msg, err))
	}
}

func main() {
	conn, err := amqp.Dial("amqp://guest:guest@192.168.0.104:5672")
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()
	q, err:= ch.QueueDeclare(
		"hello",
		false,
		false,
		false,
		false,
		nil,
	)
	failOnError(err, "Failed to declare a queue")

	// body := "hellooo body"
	// err = ch.Publish(
	// 	"",
	// 	q.Name,
	// 	false,
	// 	false,
	// 	amqp.Publishing{
	// 		ContentType: "text/plain",
	// 		Body: []byte(body),
	// 	},
	// )
	// log.Printf("[x] Send %s", body)
	// failOnError(err, "Failed to publish a message")

	msgs, err := ch.Consume(
		q.Name,
		"",
		true,
		false,
		false,
		false,
		nil,
	)
	failOnError(err, "Failed to register a consumer")
	forever := make(chan bool)
	go func(){
		for d:= range msgs{
			log.Printf("Received a message : %s", d.Body)
		}
	}()
	log.Printf("[*] Waiting for messages. To exit press CTRL+C")
	<-forever
}