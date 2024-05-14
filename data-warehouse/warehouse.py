import psycopg2
import pandas as pd


def process_data_from_db():
    """
    Connects to the database, extracts data, and saves it to the shared volume.
    """

    print("ETL: extracting data from sources", flush=True)
    # Connect to database
    conn = psycopg2.connect(
        host="postgres",
        port="5432",
        database="postgres",
        user="postgres",
        password="postgres",
    )

    # Extract data from database (replace with your specific query)
    sql_query = "SELECT * FROM Courses;"

    print("ETL: transforming data", flush=True)
    data = pd.read_sql(sql_query, conn)

    # Save data to shared volume
    print("ETL: loading data to data lake", flush=True)
    data.to_csv("/data/processed_data.csv", index=False)

    # Close database connection
    conn.close()

    print("Data processing complete!", flush=True)
