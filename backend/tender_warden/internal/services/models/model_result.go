package models

type ResultList struct {
	Url     string        `json:"url"`
	Name    string        `json:"name"`
	Results []ResultBlock `json:"results"`
}

type ResultBlock struct {
	RuleId string `json:"rule_id"`
	Status bool   `json:"status"`
	Reason string `json:"reason"`
}
