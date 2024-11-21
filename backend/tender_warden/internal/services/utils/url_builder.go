package utils

import (
	"fmt"
	"strings"
)

const (
	SessionJsonURLTemplate    = "https://zakupki.mos.ru/newapi/api/Auction/Get?auctionId=%s"
	ItemPropertiesURLTemplate = "https://zakupki.mos.ru/newapi/api/Auction/GetAuctionItemAdditionalInfo?itemId=%d"
)

func BuildSessionJsonURL(url string) string {
	urlParts := strings.Split(url, "/")
	id := urlParts[len(urlParts)-1]
	return fmt.Sprintf(SessionJsonURLTemplate, id)
}

func BuildItemPropertiesURL(itemId int) string {
	return fmt.Sprintf(ItemPropertiesURLTemplate, itemId)
}
