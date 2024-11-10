package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"tender_warden/internal/handlers"
)

func main() {

	// Создаем директорию для хранения загруженных файлов (если её нет)
	err := os.MkdirAll("/Users/mivorobyeva/GolandProjects/tender_warden/internal/cs_files", os.ModePerm)
	if err != nil {
		log.Println(err)
	}

	handler := &handlers.Handler{}
	// Регистрируем маршрут
	http.HandleFunc("/check_sessions", handler.CheckSessions)
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Добро пожаловать на сервер!") // Отправляет сообщение на корневом маршруте
	})

	// Запускаем сервер
	port := "5003"
	fmt.Printf("Сервер запущен на http://localhost:%s", port)
	err = http.ListenAndServe(fmt.Sprintf(":%s", port), nil)
	if err != nil {
		log.Println(err)
	}
}
