package handlers

import (
	postgresC "backend/client/postgres"
	"bytes"
	"database/sql"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"strconv"
	"strings"

	"github.com/labstack/echo/v4"
)

type Course struct {
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
	data := make([]Course, 0)

	query := fmt.Sprintf(`select id, name, university_name, description, rating, skills_covered from courses limit %d offset %d`, p.Limit, p.Offset)

	rows, err := db.Queryx(query)
	if err != nil && err != sql.ErrNoRows {
		return echo.NewHTTPError(http.StatusInternalServerError, fmt.Errorf("fail to get courses: %+v", err))
	}

	for rows.Next() {
		var c Course
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

type SearchReq struct {
	Value string `query:"value"`
	PaginationReq
}

func SearchCourses(c echo.Context) error {
	req := SearchReq{}
	if err := c.Bind(&req); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest)
	}

	p := req.Transform()

	req.Value = strings.TrimSpace(req.Value)
	if req.Value == "" {
		return echo.NewHTTPError(http.StatusBadRequest, "Value for search request is required")
	}

	if len(req.Value) > 200 {
		return echo.NewHTTPError(http.StatusBadRequest, "search length too big")
	}

	db := postgresC.DB
	data := make([]Course, 0)

	escapedValue := "%" + strings.ReplaceAll(req.Value, "\\", "\\\\") + "%"

	query := `
    SELECT id, name, university_name, description, rating, skills_covered
    FROM courses
    WHERE (name ILIKE $1 OR skills_covered ILIKE $1)
    LIMIT $2 OFFSET $3`

	rows, err := db.Queryx(query, escapedValue, p.Limit, p.Offset)
	if err != nil && err != sql.ErrNoRows {
		return echo.NewHTTPError(http.StatusInternalServerError, fmt.Errorf("fail to search courses: %+v", err))
	}

	for rows.Next() {
		var c Course
		if err := rows.StructScan(&c); err != nil {
			return echo.NewHTTPError(http.StatusInternalServerError, fmt.Errorf("fail to bind course: %+v", err))
		}
		c.Skills = strings.Split(c.SkillsStr, " ")
		data = append(data, c)
	}

	return c.JSON(http.StatusOK, map[string]any{
		"data": data,
	})
}

type SuggestCoursesReq struct {
	CourseIds []int `json:"course_ids"`
}

type SuggestCoursesRes struct {
	RecommendedCourseIDs []int `json:"recommended_courses"`
}

func SuggestCourses(c echo.Context) error {
	req := SuggestCoursesReq{}
	if err := c.Bind(&req); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest)
	}

	if len(req.CourseIds) == 0 {
		return echo.NewHTTPError(http.StatusBadRequest, "course ids can not be empty")
	}

	url := "http://course-recommendation:5000/recommendation-model/predict"

	requestBody, err := json.Marshal(req)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, fmt.Errorf("failed to marshal request: %v", err))
	}

	// Create a new HTTP request
	client := &http.Client{}
	httpReq, err := http.NewRequest(http.MethodPost, url, bytes.NewReader(requestBody))
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, fmt.Errorf("failed to create request: %v", err))
	}

	httpReq.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(httpReq)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, fmt.Errorf("failed to send request: %v", err))
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		bodyBytes, err := io.ReadAll(resp.Body)
		if err != nil {
			log.Fatal(err)
		}
		bodyString := string(bodyBytes)
		return echo.NewHTTPError(resp.StatusCode, fmt.Errorf("unexpected status code: %d: %s", resp.StatusCode, bodyString))
	}

	var response SuggestCoursesRes
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, fmt.Errorf("failed to parse response: %v", err))
	}

	if len(response.RecommendedCourseIDs) == 0 {
		return c.JSON(http.StatusOK, map[string]any{
			"data": []int{},
		})
	}

	db := postgresC.DB
	data := make([]Course, 0)

	// Format comma-separated list of course IDs directly
	var idList string
	for i, id := range response.RecommendedCourseIDs {
		if i > 0 {
			idList += ","
		}
		idList += strconv.Itoa(id)
	}

	query := fmt.Sprintf(`
        SELECT id, name, university_name, description, rating, skills_covered
        FROM courses
        WHERE id IN (%s)`, idList)

	rows, err := db.Queryx(query)
	if err != nil && err != sql.ErrNoRows {
		return echo.NewHTTPError(http.StatusInternalServerError, fmt.Errorf("fail to get suggested courses: %+v", err))
	}

	for rows.Next() {
		var c Course
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
