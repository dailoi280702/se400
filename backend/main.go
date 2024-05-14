package main

import (
	"log"
	"net/http"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /api/*", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("fuck you"))
	})

	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Println("server stop!")
	}
}
