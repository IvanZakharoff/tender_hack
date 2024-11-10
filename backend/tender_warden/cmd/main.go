package main

import (
	"fmt"
	"log"
	"net/http"
	"tender_warden/internal/handlers"
)

func main() {
	handler := &handlers.Handler{}
	// Регистрируем маршрут
	http.HandleFunc("/check_sessions", handler.CheckSessions)
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Добро пожаловать на сервер!") // Отправляет сообщение на корневом маршруте
	})

	// Запускаем сервер
	port := "5003"
	fmt.Printf("Сервер запущен на http://localhost:%s", port)
	err := http.ListenAndServe(fmt.Sprintf(":%s", port), nil)
	if err != nil {
		log.Println(err)
	}
}
