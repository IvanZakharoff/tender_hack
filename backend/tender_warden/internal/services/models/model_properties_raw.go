package models

type PropertiesRaw struct {
	Characteristics []struct {
		Name  string `json:"name"`
		Value string `json:"value"`
	} `json:"characteristics"`
	AuctionItemDelivery []struct {
		Quantity float64 `json:"quantity"`
	} `json:"auctionItemDelivery"`
}
