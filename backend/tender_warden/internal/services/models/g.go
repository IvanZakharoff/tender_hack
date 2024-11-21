package models

type T struct {
	Text  string `json:"text"`
	Rules []struct {
		Rule       string `json:"rule"`
		ParsedArgs struct {
			ContractName string `json:"contractName"`
		} `json:"parsed_args,omitempty"`
		Args struct {
			IsContractGuaranteeRequired bool     `json:"isContractGuaranteeRequired,omitempty"`
			LicenseFiles                []string `json:"licenseFiles,omitempty"`
			PeriodDaysFrom              string   `json:"periodDaysFrom,omitempty"`
			PeriodDaysTo                string   `json:"periodDaysTo,omitempty"`
			DeliveryStage               string   `json:"deliveryStage,omitempty"`
			StartCost                   string   `json:"startCost,omitempty"`
			MaxContractCost             string   `json:"maxContractCost,omitempty"`
			Items                       []struct {
				Name       string `json:"name"`
				Properties []struct {
					Name  string `json:"name"`
					Value string `json:"value"`
				} `json:"properties"`
				Quantity    string `json:"quantity"`
				CostPerUnit string `json:"costPerUnit"`
			} `json:"items,omitempty"`
		} `json:"args,omitempty"`
		Text string `json:"text,omitempty"`
	} `json:"rules"`
}
