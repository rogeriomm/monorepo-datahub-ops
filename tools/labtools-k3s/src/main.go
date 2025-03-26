package main

import (
	"fmt"
	"github.com/google/uuid"
)

func main() {
	// Generate a new UUID (version 4)
	id := uuid.New()
	fmt.Println("Generated UUID:", id)
}
