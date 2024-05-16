package handlers

import (
	postgresC "backend/client/postgres"
	"database/sql"
	"fmt"
	"net/http"
	"strings"

	"github.com/labstack/echo/v4"
)

type Coures struct {
	ID             int      `json:"id" db:"id"`
	Name           string   `json:"name" db:"name"`
	Description    string   `json:"description" db:"description"`
	UniversityName string   `json:"university_name" db:"university_name"`
	Rating         float32  `json:"rating" db:"rating"`
	SkillsStr      string   `json:"-" db:"skills_covered"`
	Skills         []string `json:"skills_covered"`
}

func GetCourses(c echo.Context) error {
	pReq := PaginationReq{}
	if err := c.Bind(&pReq); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest)
	}
	p := pReq.Transform()

	db := postgresC.DB
	data := make([]Coures, 0)

	query := fmt.Sprintf(`select id, name, university_name, description, rating, skills_covered from courses limit %d offset %d`, p.Limit, p.Offset)

	rows, err := db.Queryx(query)
	if err != nil && err != sql.ErrNoRows {
		return echo.NewHTTPError(http.StatusInternalServerError, fmt.Errorf("fail to get courses: %+v", err))
	}

	for rows.Next() {
		var c Coures
		if err := rows.StructScan(&c); err != nil {
			return echo.NewHTTPError(http.StatusInternalServerError, fmt.Errorf("fail to bind course: %+v", err))
		}
		c.Skills = strings.Split(c.SkillsStr, "  ")
		data = append(data, c)
	}

	return c.JSON(http.StatusOK, map[string]any{
		"data": data,
	})
}
