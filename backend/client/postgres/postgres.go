package postgresC

import (
	"log"

	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
)

var DB *sqlx.DB

func init() {
	var err error

	if DB, err = sqlx.Connect("postgres", "host=postgres user=postgres dbname=postgres password=postgres port=5432 sslmode=disable"); err != nil {
		log.Fatalln(err)
	}

	if err = DB.Ping(); err != nil {
		log.Println(err)
	}

	log.Println("DB Connected")
}
