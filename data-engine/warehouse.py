import psycopg2
import pandas as pd
import numpy as np
from decouple import config
import time


def process_data_from_db():
    """
    Connects to the database, extracts data, and saves it to the shared volume.
    """

    print("ETL: extracting data from sources", flush=True)
    # Connect to database
    conn = psycopg2.connect(
        host=config("DB_HOST"),
        port=config("DB_PORT"),
        database=config("DB_NAME"),
        user=config("DB_USER"),
        password=config("DB_PASS"),
    )

    # Extract data from database
    sql_query = "SELECT * FROM Courses;"

    print("ETL: transforming data", flush=True)
    data = pd.read_sql(sql_query, conn)

    data["tags"] = data["name"].str.cat(
        [data["description"], data["skills_covered"]], sep=" "
    )

    data["tags"] = data["tags"].str.lower()

    # data["tags"] = data["skills_covered"]
    data = data.copy()[["id", "rating", "tags"]]

    # Fill missing or 0 values in rating with the average (excluding NaN)
    def clean_zero_value(data):
        data["rating"] = data["rating"].where(
            ~data["rating"].isin([0, np.nan]), data["rating"].mean(skipna=True)
        )

        # Fill remaining NaN with the mean excluding 0.0
        data["rating"] = data["rating"].fillna(data["rating"].mean(skipna=True))
        return data

    data = clean_zero_value(data.copy())

    # Save data to shared volume
    print("ETL: loading data to data lake", flush=True)
    data.to_csv("/data/processed_data.csv", index=False)

    # Close database connection
    conn.close()

    time.sleep(5)

    print("Data processing complete!", flush=True)
