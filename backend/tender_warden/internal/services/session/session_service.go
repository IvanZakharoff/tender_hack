package session

import (
	"bytes"
	"fmt"
	"github.com/ledongthuc/pdf"
	"io/ioutil"
	"regexp"
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

func (s *SessionService) ProcessSessions(csListDTO *dto.CSListDTO) {
	csList := s.SessionModelConstructor(csListDTO)
	fmt.Println(csList.CSList)
	for k, v := range csList.CSList {
		s.ProcessSession(&v, k)
	}
}

func (s *SessionService) ProcessSession(cs *models.CSBlock, cs_url string) {
	csRaw := s.SessionScraper.ScrapeSession(cs_url)
	propertiesRawMap := make(map[int]*models.PropertiesRaw, len(csRaw.Items))
	for _, item := range csRaw.Items {
		propertiesRaw := s.SessionScraper.ScrapeItemProperties(item.Id)
		propertiesRawMap[item.Id] = propertiesRaw
		rules := s.BuildSessionRules(cs, csRaw, propertiesRawMap)
		fmt.Println(rules.RulesList)
	}

}

func (s *SessionService) BuildSessionRules(
	cs *models.CSBlock,
	csRaw *models.CSRaw,
	propertiesRaw map[int]*models.PropertiesRaw,
) *models.Rules {
	contractStr, tzStr := s.ParseDocs(cs)

	rules := &models.Rules{
		Text:      contractStr + "\n" + tzStr,
		RulesList: make([]models.RuleBlock, 0, len(cs.Rules)),
	}

	for _, rule := range cs.Rules {
		switch rule.Id {
		case models.NAME_EQUALITY:
			rules.RulesList = append(rules.RulesList, models.RuleBlock{
				Rule: rule.Id,
				Args: struct {
					ContractName string
				}{
					ContractName: csRaw.Name,
				},
			})
		case models.CONTRACT_ENFORSEMENT:
			rules.RulesList = append(rules.RulesList, models.RuleBlock{
				Rule: rule.Id,
				Args: struct {
					IsContractGuaranteeRequired bool
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
					LicenseFiles []string
				}{
					LicenseFiles: licenseFiles,
				},
			})
		case models.SUPPLY_SCHEDULE_AND_STAGE:
			lastDelivery := csRaw.Deliveries[len(csRaw.Deliveries)-1]
			rules.RulesList = append(rules.RulesList, models.RuleBlock{
				Rule: rule.Id,
				Args: struct {
					PeriodDaysFrom string
					PeriodDaysTo   string
					DeliveryStage  string
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
					StartCost       string
					MaxContractCost string
				}{
					StartCost:       fmt.Sprintf("%f", csRaw.StartCost),
					MaxContractCost: fmt.Sprintf("%f", csRaw.ContractCost),
				},
			})
		case models.TECHNICAL_SPECIFICATION:
			type Property struct {
				Name  string
				Value string
			}

			type Item struct {
				Name        string
				Properties  []Property
				Quantity    string
				CostPerUnit string
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
					Text  string
					Items []Item
				}{
					Text:  tzStr,
					Items: itemsProperties,
				},
			})
		}
	}

	return rules
}

func (s *SessionService) CleanString(inputString *string) string {
	// Удаляем все символы, которые не являются буквами
	re := regexp.MustCompile(`[^a-zA-Zа-яА-ЯёЁ\s]`)
	cleanedString := re.ReplaceAllString(*inputString, "")

	// Удаляем лишние пробелы
	cleanedString = strings.TrimSpace(cleanedString)
	re = regexp.MustCompile(`\s+`)
	cleanedString = re.ReplaceAllString(cleanedString, " ")

	// Приводим строку к нижнему регистру
	cleanedString = strings.ToLower(cleanedString)

	return cleanedString
}

func convertPDFToText(pdfData *[]byte) string {
	r, err := pdf.NewReader(bytes.NewReader(*pdfData), 0)
	if err != nil {
		return ""
	}

	var text strings.Builder
	totalPage := r.NumPage()

	for pageIndex := 1; pageIndex <= totalPage; pageIndex++ {
		p := r.Page(pageIndex)
		if p.V.IsNull() {
			continue
		}

		content, err := p.GetPlainText(nil)
		if err != nil {
			return ""
		}

		text.WriteString(content)
	}

	return text.String()
}

func ConvertDocxToText(docxBytes []byte) (string, error) {
	// Сохраняем байтовый массив во временный файл, поскольку библиотека требует путь к файлу
	tempFile := "temp.docx"
	err := ioutil.WriteFile(tempFile, docxBytes, 0644)
	if err != nil {
		return "", fmt.Errorf("не удалось записать временный файл: %v", err)
	}

	// Открываем DOCX файл
	doc, err := docx.Open(tempFile)
	if err != nil {
		return "", fmt.Errorf("не удалось прочитать DOCX: %v", err)
	}
	defer doc.Close()

	// Извлекаем текст
	var textContent bytes.Buffer
	paragraphs, err := doc.Paragraphs()
	if err != nil {
		return "", fmt.Errorf("ошибка при извлечении параграфов: %v", err)
	}
	for _, para := range paragraphs {
		textContent.WriteString(para)
		textContent.WriteString("\n") // добавляем перенос строки между абзацами
	}

	return textContent.String(), nil
}

func (s *SessionService) ConvertFileToText(fileData *[]byte, fileName string) string {
	if strings.HasSuffix(fileName, ".pdf") {
		return convertPDFToText(fileData)
	}
	if strings.HasSuffix(fileName, ".docx") {
		return convertDOCXToText(fileData)
	}

	return ""
}

func (s *SessionService) ParseDocs(cs *models.CSBlock) (contractStr, tzStr string) {
	for fileName, file := range cs.Files {
		if strings.HasPrefix(fileName, "tz") {
			tzStr = s.ConvertFileToText(&file, fileName)
		}
		if strings.HasPrefix(fileName, "contract") {
			contractStr = s.ConvertFileToText(&file, fileName)
		}
	}
	return contractStr, tzStr
}
