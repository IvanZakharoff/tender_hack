package dto

type CSListDTO struct {
	CSList    []CSBlock              `json:"cs_list"`
	FilePools map[string][]FileBlock // key - url
}

type CSBlock struct {
	Url   string `json:"url"`
	Rules []int  `json:"rules"`
}

type FileBlock struct {
	FileName    string
	FileContent []byte
}
