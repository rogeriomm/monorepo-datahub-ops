package main

import (
	"fmt"
	"github.com/google/uuid"
)

func main() {
	fmt.Println("labtools-k3s")

	id := uuid.New()
	fmt.Println("Generated UUID:", id)
}
