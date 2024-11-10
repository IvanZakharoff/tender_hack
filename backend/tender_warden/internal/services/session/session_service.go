package session

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"mime/multipart"
	"net/http"
	"strconv"
	"strings"
	"tender_warden/internal/handlers/dto"
	"tender_warden/internal/services/models"
)

type SessionService struct {
	SessionScraper SessionScraper
}

func (s *SessionService) SessionModelConstructor(csListDTO *dto.CSListDTO) *models.CSList {
	csList := &models.CSList{}
	csList.CSList = make(map[string]models.CSBlock)

	for _, csBlock := range csListDTO.CSList {
		rules := make([]models.Rule, 0, len(csBlock.Rules))
		for _, ruleID := range csBlock.Rules {
			rulesBlock := &models.Rule{}
			rulesBlock.Id = ruleID
			rules = append(rules, *rulesBlock)
		}

		csList.CSList[csBlock.Url] = models.CSBlock{
			Rules: rules,
			Files: make(map[string][]byte),
		}
	}

	for url, files := range csListDTO.FilePools {
		for _, file := range files {
			csList.CSList[url].Files[file.FileName] = file.FileContent
		}
	}

	return csList

}

func (s *SessionService) ProcessSessions(csListDTO *dto.CSListDTO) []*models.ResultList {
	resultList := make([]*models.ResultList, 0, len(csListDTO.CSList))
	csList := s.SessionModelConstructor(csListDTO)
	fmt.Println(csList.CSList)
	for k, v := range csList.CSList {
		result, err := s.ProcessSession(&v, k)
		if err == nil {
			resultList = append(resultList, result)
		}
	}

	return resultList
}

//func (s *SessionService) SendResult(result *models.ResultList) {
//	// Преобразуем структуру result в JSON
//	resultJSON, err := json.Marshal(result)
//	if err != nil {
//		return
//	}
//
//	// Создаем POST-запрос
//	url := "http://localhost:8000/session_result"
//	req, err := http.NewRequest("POST", url, bytes.NewBuffer(resultJSON))
//	if err != nil {
//		return
//	}
//	req.Header.Set("Content-Type", "application/json")
//
//	// Выполняем запрос
//	client := &http.Client{}
//	resp, err := client.Do(req)
//	if err != nil {
//		return
//	}
//	defer resp.Body.Close()
//	return
//}

//func (s *SessionService) SendError() {
//	// Создаем POST-запрос
//	url := "http://localhost:8000/session_result"
//	message := "Упс! Что-то пошло не так."
//	req, err := http.NewRequest("POST", url, strings.NewReader(message))
//	if err != nil {
//		return
//	}
//	req.Header.Set("Content-Type", "text/plain")
//
//	// Выполняем запрос
//	client := &http.Client{}
//	resp, err := client.Do(req)
//	if err != nil {
//		return
//	}
//	defer resp.Body.Close()
//}

func (s *SessionService) ProcessSession(cs *models.CSBlock, cs_url string) (*models.ResultList, error) {
	csRaw := s.SessionScraper.ScrapeSession(cs_url)
	var rules *models.Rules
	propertiesRawMap := make(map[int]*models.PropertiesRaw, len(csRaw.Items))
	for _, item := range csRaw.Items {
		propertiesRaw := s.SessionScraper.ScrapeItemProperties(item.Id)
		propertiesRawMap[item.Id] = propertiesRaw
		rules = s.BuildSessionRules(cs, csRaw, propertiesRawMap)
	}

	result := &models.ResultList{}
	err := s.CheckSession(rules, cs, result)
	if err != nil {
		return nil, err
	}
	result.Url = cs_url
	result.Name = csRaw.Name

	return result, nil
}

func (s *SessionService) CheckSession(rules *models.Rules, cs *models.CSBlock, result *models.ResultList) error {
	// Создаем новый буфер для записи multipart/form-data
	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)

	// Преобразуем структуру rules в JSON и добавляем в форму
	rulesJSON, err := json.Marshal(rules)
	if err != nil {
		return err
	}
	part, err := writer.CreateFormField("rules")
	if err != nil {
		return err
	}
	_, err = part.Write(rulesJSON)
	if err != nil {
		return err
	}

	// Добавляем файлы в форму
	for filename, file := range cs.Files {
		fileType := strings.Split(filename, ".")[0]
		part, err := writer.CreateFormFile(fileType, filename)
		if err != nil {
			return err
		}
		_, err = part.Write(file)
		if err != nil {
			return err
		}
	}

	// Закрываем форму
	err = writer.Close()
	if err != nil {
		return err
	}

	// Создаем POST-запрос
	url := "http://localhost:8000/check_session"
	req, err := http.NewRequest("POST", url, body)
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", writer.FormDataContentType())

	// Выполняем запрос
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	// Читаем тело ответа
	respBody, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	// Декодируем JSON-ответ в структуру result
	err = json.Unmarshal(respBody, result)
	if err != nil {
		return err
	}

	return nil
}

func (s *SessionService) BuildSessionRules(
	cs *models.CSBlock,
	csRaw *models.CSRaw,
	propertiesRaw map[int]*models.PropertiesRaw,
) *models.Rules {
	rules := &models.Rules{
		Text:      "",
		RulesList: make([]models.RuleBlock, 0, len(cs.Rules)),
	}

	for _, rule := range cs.Rules {
		switch rule.Id {
		case models.NAME_EQUALITY:
			rules.RulesList = append(rules.RulesList, models.RuleBlock{
				Rule: rule.Id,
				Args: struct {
					ContractName string `json:"contractName"`
				}{
					ContractName: csRaw.Name,
				},
			})
		case models.CONTRACT_ENFORSEMENT:
			rules.RulesList = append(rules.RulesList, models.RuleBlock{
				Rule: rule.Id,
				Args: struct {
					IsContractGuaranteeRequired bool `json:"isContractGuaranteeRequired"`
				}{
					IsContractGuaranteeRequired: csRaw.IsContractGuaranteeRequired,
				},
			})
		case models.CERTIFICATION:
			licenseFiles := make([]string, 0, len(csRaw.LicenseFiles))
			for _, licenseFile := range csRaw.LicenseFiles {
				licenseFiles = append(licenseFiles, licenseFile)
			}

			if csRaw.UploadLicenseDocumentsComment != "" {
				licenseFiles = append(licenseFiles, csRaw.UploadLicenseDocumentsComment)
			}

			rules.RulesList = append(rules.RulesList, models.RuleBlock{
				Rule: rule.Id,
				Args: struct {
					LicenseFiles []string `json:"licenseFiles"`
				}{
					LicenseFiles: licenseFiles,
				},
			})
		case models.SUPPLY_SCHEDULE_AND_STAGE:
			lastDelivery := csRaw.Deliveries[len(csRaw.Deliveries)-1]
			rules.RulesList = append(rules.RulesList, models.RuleBlock{
				Rule: rule.Id,
				Args: struct {
					PeriodDaysFrom string `json:"periodDaysFrom"`
					PeriodDaysTo   string `json:"periodDaysTo"`
					DeliveryStage  string `json:"deliveryStage"`
				}{
					PeriodDaysFrom: strconv.Itoa(lastDelivery.PeriodDaysFrom),
					PeriodDaysTo:   strconv.Itoa(lastDelivery.PeriodDaysTo),
					DeliveryStage:  strconv.Itoa(len(csRaw.Deliveries)),
				},
			})
		case models.CONTRACT_COST:
			rules.RulesList = append(rules.RulesList, models.RuleBlock{
				Rule: rule.Id,
				Args: struct {
					StartCost       string `json:"startCost"`
					MaxContractCost string `json:"maxContractCost"`
				}{
					StartCost:       fmt.Sprintf("%f", csRaw.StartCost),
					MaxContractCost: fmt.Sprintf("%f", csRaw.ContractCost),
				},
			})
		case models.TECHNICAL_SPECIFICATION:
			type Property struct {
				Name  string `json:"name"`
				Value string `json:"value"`
			}

			type Item struct {
				Name        string     `json:"name"`
				Properties  []Property `json:"properties"`
				Quantity    string     `json:"quantity"`
				CostPerUnit string     `json:"costPerUnit"`
			}

			itemsProperties := make([]Item, 0, len(csRaw.Items))
			for _, itemRaw := range csRaw.Items {
				n := len(propertiesRaw[itemRaw.Id].AuctionItemDelivery)
				item := Item{
					Name:        itemRaw.Name,
					Properties:  make([]Property, 0, len(propertiesRaw[itemRaw.Id].Characteristics)),
					Quantity:    fmt.Sprintf("%f", propertiesRaw[itemRaw.Id].AuctionItemDelivery[n-1].Quantity),
					CostPerUnit: fmt.Sprintf("%f", itemRaw.CostPerUnit),
				}

				for _, propertyRaw := range propertiesRaw[itemRaw.Id].Characteristics {
					item.Properties = append(item.Properties, Property{
						Name:  propertyRaw.Name,
						Value: fmt.Sprintf("%f", propertyRaw.Value),
					})
				}

				itemsProperties = append(itemsProperties, item)
			}

			rules.RulesList = append(rules.RulesList, models.RuleBlock{
				Rule: rule.Id,
				Args: struct {
					Text  string `json:"text"`
					Items []Item `json:"items"`
				}{
					Text:  "",
					Items: itemsProperties,
				},
			})
		}
	}

	return rules
}
