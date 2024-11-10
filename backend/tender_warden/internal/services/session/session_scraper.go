package session

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"tender_warden/internal/services/models"
	"tender_warden/internal/services/utils"
)

type SessionScraper struct {
}

func (s *SessionScraper) ScrapeSession(url string) *models.CSRaw {
	cs := &models.CSRaw{}

	sessionJsonURL := utils.BuildSessionJsonURL(url)

	// Выполняем HTTP-запрос
	resp, err := http.Get(sessionJsonURL)
	if err != nil {
		log.Fatalf("Ошибка при выполнении запроса: %v", err)
	}
	defer resp.Body.Close()

	// Проверяем статус код ответа
	if resp.StatusCode != http.StatusOK {
		log.Fatalf("URL %s : Неудачный статус код: %d", sessionJsonURL, resp.StatusCode)
	}

	// Читаем тело ответа
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Ошибка при чтении тела ответа: %v", err)
	}

	// Декодируем JSON в структуру cs_model
	err = json.Unmarshal(body, cs)
	if err != nil {
		fmt.Printf("Ошибка при декодировании JSON: %v", err)
	}

	// Выводим результат для проверки
	return cs
}

func (s *SessionScraper) ScrapeItemProperties(itemId int) *models.PropertiesRaw {
	url := utils.BuildItemPropertiesURL(itemId)
	properties := &models.PropertiesRaw{}

	resp, err := http.Get(url)
	if err != nil {
		log.Fatalf("Ошибка при выполнении запроса: %v", err)
	}
	defer resp.Body.Close()

	// Проверяем статус код ответа
	if resp.StatusCode != http.StatusOK {
		log.Fatalf("URL %s : Неудачный статус код: %d", url, resp.StatusCode)
	}

	// Читаем тело ответа
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Ошибка при чтении тела ответа: %v", err)
	}

	// Декодируем JSON в структуру cs_model
	err = json.Unmarshal(body, properties)
	if err != nil {
		fmt.Printf("Ошибка при декодировании JSON: %v", err)
	}

	return properties
}
