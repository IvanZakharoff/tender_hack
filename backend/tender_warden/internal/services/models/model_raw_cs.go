package models

type CSRaw struct {
	Name                        string   `json:"name"`
	IsContractGuaranteeRequired bool     `json:"isContractGuaranteeRequired"`
	LicenseFiles                []string `json:"licenseFiles"`
	Deliveries                  []struct {
		PeriodDaysFrom int `json:"periodDaysFrom"`
		PeriodDaysTo   int `json:"periodDaysTo"`
	} `json:"deliveries"`
	StartCost    float64  `json:"startCost"`
	ContractCost *float64 `json:"contractCost"` // maxContractCost
	Items        []struct {
		Id          int     `json:"id"`
		CostPerUnit float64 `json:"costPerUnit"`
		Name        string  `json:"name"`
	} `json:"items"`
	UploadLicenseDocumentsComment string `json:"uploadLicenseDocumentsComment"`
}
