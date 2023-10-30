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
                        );
                        
                        CREATE TABLE job_applications (
                            application_id SERIAL PRIMARY KEY,
                            user_id VARCHAR(255) REFERENCES users(user_id),
                            job_id INT REFERENCES jobs(job_id) ON DELETE CASCADE,
                            graduation_date DATE,
                            start_date DATE,
                            paragraph_text TEXT,
                            UNIQUE (user_id, job_id)
                        );

                        CREATE TABLE saved_jobs (
                            user_id VARCHAR(255) REFERENCES users(user_id),
                            job_id INT REFERENCES jobs(job_id) ON DELETE CASCADE,
                            PRIMARY KEY (user_id, job_id)
                        );
                        """

def createDatabase(databaseUser, databasePassword, databaseName, databaseHost, databasePort, databaseQueryString = DATABASE_QUERY_STRING):
    with psycopg.connect(user=databaseUser, password=databasePassword) as connection:
       connection._set_autocommit(True)
       with connection.cursor() as cursor:
          cursor.execute(f"""CREATE DATABASE {databaseName};""")
    with psycopg.connect(dbname=databaseName, user=databaseUser, password=databasePassword, host=databaseHost, port=databasePort) as connection:
        with connection.cursor() as cursor:
          cursor.execute(databaseQueryString)

def getDate():
    while True:
        year = input('Enter year: ')
        if year.isnumeric():
            year = int(year)
            if year <= 9999 and year >= 1:
                break
        print('Invalid input. Please input a valid year.')

    while True:
        month = input('Enter month: ')
        if month.isnumeric():
            month = int(month)
            if month <= 12 and month >= 1:
                break
        print('Invalid input. Please input a valid month.')
    
    if month == 2:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            max = 29
        else:
            max = 28
    elif month in (1, 3, 5, 7, 8, 10, 12):
        max = 31
    else: max = 30

    while True:
        day = input('Enter day: ')
        if day.isnumeric():
            day = int(day)
            if day <= max and day >= 1:
                break
        print('Invalid input. Please input a valid day.')
    
    return f"{year}-{month}-{day}"