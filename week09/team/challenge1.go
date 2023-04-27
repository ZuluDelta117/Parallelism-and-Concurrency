package main

import (
	"fmt"
	"time"
)

func main() {

	// TODO use 'make' to make a channel that takes an integer

	// TODO use 'go' to create a goroutine and pass in the channel to send an integer
	fmt.Println("Sending value to channel")

	// TODO use 'go' to create a goroutine and pass in the channel to receive an integer
	fmt.Println("Receiving from channel")

	// leave this
	time.Sleep(time.Second * 5)
	fmt.Println("DONE")
}

func send(ch chan int) {
	// TODO pass an integer to the channel.
}

func receive(ch chan int) {
	// TODO receive the integer from the channel (call the int 'val')
	fmt.Printf("Value Received=%d in receive function\n", val)
}
