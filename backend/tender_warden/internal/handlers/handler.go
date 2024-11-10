package handlers

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"tender_warden/internal/handlers/dto"
	"tender_warden/internal/services/session"
)

type Handler struct {
	SessionService session.SessionService
}

func (h *Handler) CheckSessions(w http.ResponseWriter, r *http.Request) {
	// Ограничиваем размер загружаемых данных (например, до 50 МБ)
	r.ParseMultipartForm(50 << 20) // TODO что-то тут надо подумать

	// собираем данные о КС
	buf := &dto.CSListDTO{}
	dataField := r.FormValue("data")
	if dataField == "" {
		http.Error(w, "Поле data не найдено", http.StatusBadRequest)
		return
	}

	err := json.Unmarshal([]byte(dataField), &buf)
	if err != nil {
		http.Error(w, "Ошибка при декодировании JSON", http.StatusBadRequest)
		return
	}

	filePoolsBlock := make(map[string][]dto.FileBlock)

	// Собираем файлы КС
	filePoolListHTTP := r.MultipartForm.File
	for filePoolKey, filePool := range filePoolListHTTP {
		filePoolsBlock[filePoolKey] = make([]dto.FileBlock, 0, len(filePool))

		for _, fileData := range filePool {

			file, err := fileData.Open()
			if err != nil {
				http.Error(w, "Не удалось получить файл из запроса", http.StatusBadRequest)
				return
			}
			defer file.Close()

			fileBlock := &dto.FileBlock{}
			fileBlock.FileName = fileData.Filename
			fileBlock.FileContent, err = io.ReadAll(file)
			if err != nil {
				http.Error(w, fmt.Sprintf("Не удалось прочитать файл %s", fileData.Filename), http.StatusBadRequest)
				return
			}

			filePoolsBlock[filePoolKey] = append(filePoolsBlock[filePoolKey], *fileBlock)
		}
	}

	buf.FilePools = filePoolsBlock

	results := h.SessionService.ProcessSessions(buf)
	resultsJSON, err := json.Marshal(results)

	// Отправляем успешный ответ
	w.Write(resultsJSON)
}
