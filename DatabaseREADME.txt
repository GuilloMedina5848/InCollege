incollegedb.backup is the backup database file created using 'pg_dump'
How to restore the database in your local machine:
    Enter the 'psql' interface
    1. Create a new Database: 
        (It's a good idea to restore the backup into a fresh database. 
        I recommend you create a new database called incollegedb)
            # createdb -U postgres incollegedb
    2. Restore the backup:
            # pg_restore -U postgres -h localhost -p 5432 -d incollegedb -F c "path_to_incollegedb.backup"
    
    -U postgres: Specifies the user (in this case, "postgres").
    -h localhost: Specifies the host (in this case, "localhost").
    -p 5432: Specifies the port (in this case, "5432").
    -d incollegedb: Specifies the database to which the backup should be restored, which is incollegedb.
    -F c: Indicates the format of the backup file (custom format in this case).
    "path_to_incollegedb.backup": Path to the backup file.
------------------------------------------------------------------------------------------------------
How to export and share a database dump:
    During development, you might change the database. Here is how you can share it to github.
    In the command prompt (for Windows), type:
        pg_dump -U postgres -h localhost -p 5432 -W -F c -b -v -f "path/to/store/incollegedb.backup" incollegedb
    In my machine, I use:
        pg_dump -U postgres -h localhost -p 5432 -W -F c -b -v -f "E:/SoftwareEngineeringCode/InCollege/incollegedb.backup" incollegedb
------------------------------------------------------------------------------------------------------
Database Schemas:
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
    salary DECIMAL
);

CREATE TABLE friendships (
    friendship_id SERIAL PRIMARY KEY,
    student1_id VARCHAR(255) REFERENCES users(user_id),
    student2_id VARCHAR(255) REFERENCES users(user_id),
    status TEXT CHECK (status IN ('pending', 'confirmed'))
);

------------------------------------------------------------------------------------------------------
Explanations:

1.	users Table:

user_id: A primary key of type VARCHAR(255) that will uniquely identify each user.
password: A TEXT field to store the password (In a real-world scenario, you'd want this to be securely hashed).
first_name & last_name: Both are VARCHAR(255) fields for storing the user's first and last names.
has_email, has_sms, has_ad: BOOLEAN fields with a default value of TRUE, indicating whether the user has opted for email, SMS, or ads.
university & major: VARCHAR(255) fields for storing the university name and major of the user, respectively.

2.	jobs Table:

job_id: An auto-incremented primary key of type SERIAL that will uniquely identify each job.
user_id: A foreign key that references the user_id in the users table. This establishes which user posted the job.
title: A VARCHAR(255) field for the job title.
description: A TEXT field for the job description.
employer, location: Both are VARCHAR(255) fields for storing the employer's name and the job's location.
salary: A DECIMAL field to store the salary (if provided).

3.	friendships Table:

friendship_id: An auto-incremented primary key of type SERIAL that will uniquely identify each friendship or friend request.
student1_id & student2_id: Both are foreign keys that reference the user_id in the users table. They indicate the two users involved in the friendship or friend request.
status: A TEXT field that checks whether the value is either 'pending' or 'confirmed'. This indicates the current status of the friend request.
------------------------------------------------------------------------------------------------------
