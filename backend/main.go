package main

import (
	"backend/handlers"
	"context"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"time"

	"github.com/getsentry/sentry-go"
	"github.com/joho/godotenv"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {
	// Load env
	err := godotenv.Load()
	if err != nil {
		fmt.Printf("Error loading .env file: %s\n", err.Error())
	}

	port := os.Getenv("SERVER_PORT")
	sentryDsn := os.Getenv("SENTRY_DSN")

	// Set up Sentry
	err = sentry.Init(sentry.ClientOptions{
		Dsn:   sentryDsn,
		Debug: true,
	})
	if err != nil {
		fmt.Printf("error initializing sentry %s", err.Error())
	}
	defer sentry.Flush(2 * time.Second)

	// Set up server
	e := echo.New()
	e.Use(middleware.Logger())
	e.Pre(middleware.RemoveTrailingSlash())
	e.Use(middleware.CORS())

	api := e.Group("/api")

	registerRouter(api)

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()
	go func() {
		fmt.Printf("Starting server on port %s\n", port)
		if err := e.Start(":" + port); err != nil && err != http.ErrServerClosed {
			e.Logger.Fatalf("shutting down the server: %s", err.Error())
		}
	}()

	// Wait for interrupt signal to gracefully shutdown the server with a timeout of 10 seconds.
	<-ctx.Done()
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := e.Shutdown(ctx); err != nil {
		e.Logger.Fatal(err)
	}
}

func registerRouter(e *echo.Group) {
	coursesGr := e.Group("/courses")
	coursesGr.GET("", handlers.GetCourses)
	coursesGr.GET("/:id", handlers.GetCourseByID)

	e.GET("/search", handlers.SearchCourses)

	e.POST("/suggest", handlers.SuggestCourses)
	e.POST("/webhook/clear-course-suggestions", handlers.ClearSuggestedCoursesCache)
}
