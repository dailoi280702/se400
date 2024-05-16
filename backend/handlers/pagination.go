package handlers

const (
	paginationDefaultLimit = 100
	paginationMaxLimit     = 1000
)

type PaginationReq struct {
	Limit int `query:"limit"`
	Page  int `query:"page" validate:"min=0"`
}

func (p PaginationReq) Transform() Pagination {
	if p.Limit < 1 {
		p.Limit = paginationDefaultLimit
	}

	if p.Limit > paginationMaxLimit {
		p.Limit = paginationMaxLimit
	}

	if p.Page == 0 {
		p.Page = 1
	}

	return Pagination{Limit: p.Limit, Offset: (p.Page - 1) * p.Limit}
}

type Pagination struct {
	Limit  int `json:"limit,omitempty"`
	Offset int `json:"offset,omitempty"`
}
