import csv
import psycopg2

# Database connection details (replace with your own)
dbname = "postgres"
dbuser = "postgres"
dbpassword = "postgres"
dbhost = "localhost"
dbport = "5433"

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname=dbname, user=dbuser, password=dbpassword, host=dbhost, port=dbport
    )
    cur = conn.cursor()
except Exception as e:
    print("Error connecting to database:", e)
    exit()

# Define the SQL statement to insert data
sql = """
INSERT INTO Courses (name, university_name, difficulty_level, rating, description, skills_covered)
VALUES (%s, %s, %s, %s, %s, %s)
"""

# Open the CSV file
try:
    with open("data.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        # Skip the header row (assuming the first line is header)
        next(reader)
        for row in reader:
            # Basic cleaning (replace with more sophisticated cleaning as needed)
            name = row[0].strip()
            university_name = row[1].strip()
            difficulty_level = row[2].strip()
            try:
                rating = float(
                    row[3].strip()
                )  # Convert rating to float if possible (handle errors)
            except ValueError:
                rating = 0  # Set rating to None if conversion fails
            description = row[5].strip()
            skills_covered = row[6].strip()

            # Execute the insert statement with the cleaned data
            cur.execute(
                sql,
                (
                    name,
                    university_name,
                    difficulty_level,
                    rating,
                    description,
                    skills_covered,
                ),
            )

    # Commit the changes to the database
    conn.commit()
    print("Data imported successfully!")
except Exception as e:
    print("Error importing data:", e)
finally:
    # Close the connection
    if conn:
        conn.close()
