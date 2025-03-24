// src-samples/go/main.go
package main

import (
	"fmt"
	"log"
	"net/http"
	"sample-go-2/internal/monitor"
)

func indexHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprint(w, `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Go Web App</title>
</head>
<body>
    <h1>Hello from Go net app-2</h1>
    <p>This is a simple Go web application.</p>
</body>
</html>`)
}

func main() {
	monitor.Start() // Starts background metric server and collectors

	http.HandleFunc("/", indexHandler)
	addr := "0.0.0.0:8080"
	log.Printf("app-2 -> Server running at http://%s/", addr)
	if err := http.ListenAndServe(addr, nil); err != nil {
		log.Fatalf("could not start server: %v", err)
	}
}
