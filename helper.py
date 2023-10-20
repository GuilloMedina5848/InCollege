import psycopg

DATABASE_QUERY_STRING = """
                        CREATE TABLE users (
                            user_id VARCHAR(255) PRIMARY KEY,
                            password TEXT NOT NULL,
                            first_name VARCHAR(255) NOT NULL,
                            last_name VARCHAR(255) NOT NULL,
                            has_email BOOLEAN DEFAULT TRUE,
                            has_sms BOOLEAN DEFAULT TRUE,
                            has_ad BOOLEAN DEFAULT TRUE,
                            language VARCHAR(255) DEFAULT 'English',
                            university VARCHAR(255),
                            major VARCHAR(255)
                        );

                        CREATE TABLE jobs (
                            job_id SERIAL PRIMARY KEY,
                            user_id VARCHAR(255) REFERENCES users(user_id),
                            title VARCHAR(255) NOT NULL,
                            description TEXT,
                            employer VARCHAR(255) NOT NULL,
                            location VARCHAR(255) NOT NULL,
                            salary DECIMAL,
                            first_name VARCHAR(255),
                            last_name VARCHAR(255)
                        );

                        CREATE TABLE friendships (
                            friendship_id SERIAL PRIMARY KEY,
                            student1_id VARCHAR(255) REFERENCES users(user_id),
                            student2_id VARCHAR(255) REFERENCES users(user_id),
                            status TEXT CHECK (status IN ('pending', 'confirmed'))
                        );
                        
                        CREATE TABLE profiles (
                            profile_id SERIAL PRIMARY KEY,
                            user_id VARCHAR(255) REFERENCES users(user_id),
                            title TEXT,
                            about TEXT
                        );

                        CREATE TABLE experiences (
                            experience_id SERIAL PRIMARY KEY,
                            user_id VARCHAR(255) REFERENCES users(user_id),
                            title VARCHAR(255),
                            employer VARCHAR(255),
                            date_started DATE,
                            date_ended DATE,
                            location VARCHAR(255),
                            description TEXT
                        );

                        CREATE TABLE educations (
                            education_id SERIAL PRIMARY KEY,
                            user_id VARCHAR(255) REFERENCES users(user_id),
                            school_name VARCHAR(255),
                            degree VARCHAR(255),
                            year_started INT,
                            year_ended INT
                        );"""

MAX_USERS = 10
MAX_JOBS = 5

def createDatabase(databaseUser, databasePassword, databaseName, databaseHost, databasePort, databaseQueryString = DATABASE_QUERY_STRING):
    with psycopg.connect(user=databaseUser, password=databasePassword) as connection:
       connection._set_autocommit(True)
       with connection.cursor() as cursor:
          cursor.execute(f"""CREATE DATABASE {databaseName};""")
    with psycopg.connect(dbname=databaseName, user=databaseUser, password=databasePassword, host=databaseHost, port=databasePort) as connection:
        with connection.cursor() as cursor:
          cursor.execute(databaseQueryString)