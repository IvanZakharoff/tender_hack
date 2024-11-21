package models

const (
	NAME_EQUALITY             = 1
	CONTRACT_ENFORSEMENT      = 2
	CERTIFICATION             = 3
	SUPPLY_SCHEDULE_AND_STAGE = 4
	CONTRACT_COST             = 5
	TECHNICAL_SPECIFICATION   = 6
)

type Rules struct {
	Text      string      `json:"text"`
	RulesList []RuleBlock `json:"rules"`
}

type RuleBlock struct {
	Rule int         `json:"rule"`
	Args interface{} `json:"args"`
}
