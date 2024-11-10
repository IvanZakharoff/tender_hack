package models

type CSList struct {
	CSList map[string]CSBlock // key - url
}

type CSBlock struct {
	Files map[string][]byte // key - filename
	Rules []Rule
}

type Rule struct {
	Id   int
	Args []byte // json нужных полей спаршенных с сайта
}
