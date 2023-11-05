import re, helper, psycopg
from InquirerPy import prompt 
from psycopg.rows import dict_row

# Connect to your PostgreSQL server
DATABASE_NAME_ = "incollegedb"
DATABASE_USER_ = "postgres"
DATABASE_PASSWORD_ = "postgres"
DATABASE_HOST_ = "localhost" 
DATABASE_PORT_ = "5432"  # default PostgreSQL port

class InCollegeServer():
    DATABASE_NAME = ""
    DATABASE_USER = ""
    DATABASE_PASSWORD = ""
    DATABASE_HOST = ""
    DATABASE_PORT = ""

    loggedIn = False
    userID = ""
    first_name = ""
    last_name = ""

    has_email = True
    has_sms = True
    has_ad = True
    language = "English"

    maxJobs = 5
    maxUsers = 10

    def validUser(self, UserID, password):
        """
        Checks if the provided UserID is unique
        Check if the provided password meets certain requirements
        """
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                search_query = f"""
                SELECT user_id
                FROM users
                WHERE user_id = %s;
                """
                cursor.execute(search_query, (UserID,))
                users = cursor.fetchall()

                if users:
                    return False

        if not (8 <= len(password) <= 12):
            return False
        # Check if the password contains at least one capital letter
        if not re.search(r'[A-Z]', password):
            return False
        # Check if the password contains at least one digit
        if not re.search(r'\d', password):
            return False
        # Check if the password contains at least one special character (non-alphanumeric)
        if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]', password):
            return False
        return True

    def addJob(self):
        """
        Allows a logged-in user to post a job.
        """
        # Connect to the database
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                # Get the number of jobs in the database
                cursor.execute("SELECT COUNT(*) FROM jobs;")
                jobs_count = cursor.fetchone()[0]

        if jobs_count >= self.maxJobs:
            print("You have reached the maximum number of job postings.")
            return

        print("\n============================\n")
        title = input("Please enter the job title: ")
        description = input("Please enter the job description: ")
        employer = input("Please enter the employer: ")
        location = input("Please enter the location: ")
        while True:
            try:
                salary_input = float(input('Please enter the salary: '))
                salary = round(salary_input, 2)  # Ensure it's rounded to 2 decimal places if needed
                break
            except ValueError:
                print("\nPlease enter a valid number for salary.\n")

        # jobsList.append((self.first_name, self.last_name, title, description, employer, location, salary))
        # saveJobs(jobsList)

        # Connect to the database
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                # Insert job details into the jobs table
                insert_query = """
                INSERT INTO jobs (title, description, employer, location, salary, user_id, first_name, last_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(insert_query, (title, description, employer, location, salary, self.userID, self.first_name, self.last_name))

        print("\nJob posted successfully!")

    def signIn(self):
        """
        allow existing user to log in
        """
        while True:
            existingUserID = input("Please enter UserID: ")
            existingPassword = input("Please enter password: ")
            # Connect to the database
            with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
                with connection.cursor(row_factory=dict_row) as cursor:
                    # Fetch user details from the database
                    cursor.execute("SELECT * FROM users WHERE user_id = %s AND password = %s", (existingUserID, existingPassword))
                    user = cursor.fetchone()

            # Check if the user exists in the database
            if user:
                self.userID = user['user_id']
                self.first_name = user['first_name']
                self.last_name = user['last_name']
                self.has_email = user['has_email']
                self.has_sms = user['has_sms']
                self.has_ad = user['has_ad']
                self.language = user['language']
                self.tier = user['tier']
                self.loggedIn = True

                print(f"\nWelcome, {existingUserID}. You have successfully logged in.")
                return
            
            else:
                print("\nIncorrect username / password, please try again\n")

    def signUp(self):
        try:
        # Connect to the database
            with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
                with connection.cursor() as cursor:
                    # Get the number of users in the database
                    cursor.execute("SELECT COUNT(*) FROM users;")
                    user_count = cursor.fetchone()[0]

            if user_count >= self.maxUsers:
                print("\nAll permitted accounts have been created, please come back later\n")
            else:
                """
                Registers a new user, provided the UserID is unique and the 
                password meets the requirements.
                """
                print("\n============================\n")
                # variable to store user ID
                while True:
                    userID = input("Please enter UserID: ")
                    print("===============================\n1) Password must be 8 - 12 characters\n2) Must contain at least one capital letter\n3) Must contain a number\n4) Must contain a special character\n =================================")
                    password = input("Please enter password: ")
                    first = input("Please enter your first name: ")
                    last = input("Please enter your last name: ")
                    university = input("Please enter your university: ")
                    major = input("Please enter your major: ")
                    try:
                        # Ask for user input
                        choice = prompt({ "type": "list",
                                            "message" : "Select a membership tier",
                                            "choices": ["Standard (free)",
                                                        "Plus ($10/month)"]
                            })
                        
                        match choice[0]:
                            case "Standard (free)":
                                tier = "Standard"

                            case "Plus ($10/month)":
                                tier = "Plus"
                            
                            case __:  # <--- Else
                                raise ValueError
                    
                    except ValueError:
                        print("Choice not found, please try again.\n") 
                    
                    has_email = True
                    has_sms = True
                    has_ad = True

                    if self.validUser(userID, password):
                        print("\nYour username is unique and the password meets all the requirements.\n")

                        # Connect to the database
                        with psycopg.connect(dbname= self.DATABASE_NAME, user= self.DATABASE_USER, password= self.DATABASE_PASSWORD, host= self.DATABASE_HOST, port= self.DATABASE_PORT) as connection:
                            with connection.cursor() as cursor:
                                # Insert Data into users table
                                insert_query = """
                                INSERT INTO users (user_id, password, first_name, last_name, has_email, has_sms, has_ad, university, major, tier)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                                """
                                cursor.execute(insert_query, (userID, password, first, last, has_email, has_sms, has_ad, university, major, tier))

                        print("\n============================\n")
                        print("Thank you for creating an account.")

                        self.userID = userID
                        self.first = first
                        self.last = last
                        self.loggedIn = True
                        self.has_email = True
                        self.has_sms = True
                        self.has_ad = True
                        self.language = "English"
                        self.tier = tier
                        
                        print(f"\nWelcome, {self.userID}. You have successfully logged in.\n")
                        break
                    else:
                        print("\nYour username is already taken or the password doesn't meet requirements. Please start over\n")
        
        except Exception as e:
            print(f"An error occurred: {e}")

    def signInOrUp(self):
        """
        "Sign Up" Option under "General" under "Useful Link"
        This gives not logged-in user 3 choices to either sign in, sign up, or back
        """           
        run = True
        while run:
            try:
                # Ask for user input
                choice = prompt({
                    "type": "list",
                    "message": "General",
                    "choices": [
                        "For Existing User",
                        "To Create an Account",
                        "Back to General"
                    ]
                })

                match choice[0]:
                    case "For Existing User":
                        self.signIn()
                        if self.loggedIn:
                            self.mainMenu()
                    case "To Create an Account":
                        self.signUp()
                        if self.loggedIn:
                            self.mainMenu()

                    case "Back to General":
                        run = False
                        break
                        
                    case __:  # <--- Else
                        raise ValueError

            except ValueError:
                print("Choice not found, please try again.\n") 

    def searchExistingUsers(self):
        # Search for existing users by last name, university, or major
        # When results of these searches are displayed, the student will have the option of sending that student a
        # request to connect
        column_map = {
            "Last Name": "last_name",
            "University": "university",
            "Major": "major"
        }
        
        while True:
            try:
                choice_response = prompt({
                    "type": "list",
                    "message": "Search by:",
                    "choices": [
                        "Last Name",
                        "University",
                        "Major",
                        "Exit"
                    ]
                })

                choice = choice_response[0]

                if choice == "Exit":
                    return

                prompt_message = None
                if choice == "Last Name":
                    prompt_message = "Enter the user's last name: "
                elif choice == "University":
                    prompt_message = "Enter the university: "
                elif choice == "Major":
                    prompt_message = "Enter the major: "

                search_criteria = input(prompt_message)

                # Connect to the database
                with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
                    with connection.cursor() as cursor:
                        # Construct the query based on the chosen option
                        search_query = f"""
                        SELECT user_id, first_name, last_name, university, major 
                        FROM users 
                        WHERE lower({column_map[choice]}) = %s AND user_id != %s;
                        """
                        cursor.execute(search_query, (search_criteria.lower(), self.userID))

                        users = cursor.fetchall()

                        if users:
                            print("\nUser found in the InCollege system.\n")
                            # If logged in, show the option to connect
                            if self.loggedIn:
                                prompts = []
                                ids = []
                                for user in users:
                                    ids.append(user[0])
                                    prompts.append(f"User ID: {user[0]}, Name: {user[1]} {user[2]}, University: {user[3]}, Major: {user[4]}")
                                prompts.append("Go back.")
                                try:
                                    choice_response = prompt({
                                        "type": "list",
                                        "message": "Users:",
                                        "choices": prompts
                                    })
                                    if choice_response[0] == "Go back.":
                                        break
                                    elif choice_response[0] in prompts:
                                        connect_choice = input("Do you want to send this user a request to connect? (yes/no): ").lower()
                                        if connect_choice == "yes":
                                            # Handle sending a request
                                            self.sendConnectRequest(from_user_id = self.userID, to_user_id = ids[prompts.index(choice_response[0])])
                                        else:
                                            print("Request not sent.")
                                    else:
                                        raise ValueError
                                except ValueError:
                                    print("Invalid choice, please try again.\n")
                                
                            else:
                                for user in users:
                                    print(f"User ID: {user[0]}, Name: {user[1]} {user[2]}, University: {user[3]}, Major: {user[4]}")
                                
                        else:
                            print(f"\nNo user found with {choice}: {search_criteria}.\n")

            except ValueError:
                print("Invalid choice, please try again.\n")

    def getDate(self):
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

    def completeRow(self, table, crit = []):
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
            
                query = f"""SELECT *
                            FROM {table}
                            WHERE user_id = '{self.userID}'
                            """
                
                if crit:
                    i = 0
                    while i < len(crit)-1:
                        query = query + f""" AND {crit[i]} = {crit[i+1]}"""
                        i = i+2

                query = query + ';'
                cursor.execute(query)
                vals = cursor.fetchall()

                if not vals:
                    return False
                
                vals = vals[0]

                if None in vals:
                    return False
                
                return True
                
    # change crit/crit2 method to accept a list of lists with critical rows and critical entries?
    def changeEntry(self, table, column, entry, crit = "", crit2 = ""):

        # Update class attributes
        if column in ["has_email", "has_sms", "has_ad", "language"]:
            setattr(self, column, entry)

        # Connect to the database and execute the UPDATE statement
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                # Update the user's preference in the database
                update_query = f"""
                UPDATE {table} SET {column} = %s WHERE user_id = %s
                """
                if crit and crit2:
                    update_query = update_query + f""" AND {crit} = {str(crit2)}"""
                update_query = update_query + ';'
                cursor.execute(update_query, (entry, self.userID))

    def changeLanguage(self):
        print("\nCurrent Language: " + self.language + "\n")

        while True:
            try:
                # Ask for user input
                choice = prompt({
                    "type": "list",
                    "message" : "Languages",
                    "choices": ["English",
                                "Spanish",
                                "Back to Important Links"]
                })

                match choice[0]:
                    case "English":
                        if self.language == "English":
                            print("\nCurrent Language is already in English\n")
                        else:
                            self.changeEntry("users", "language", "English")
                            print("\nLanguage changed to English\n")
                        
                    case "Spanish":
                        if self.language == "Spanish":
                            print("\nCurrent Language is already in Spanish\n")
                        else:
                            self.changeEntry("users", "language", "Spanish")
                            print("\nLanguage changed to Spanish\n")

                    case "Back to Important Links":
                        break

                    case __:  # <--- Else
                        raise ValueError

            except ValueError:
                print("Choice not found, please try again.\n")

    def guestControls(self):
        while True:
            if self.has_email == True:
                emailPreference = "ON"
            elif self.has_email == False:
                emailPreference = "OFF"

            if self.has_sms == True:
                smsPreference = "ON"
            elif self.has_sms == False:
                smsPreference = "OFF"
            
            if self.has_ad == True:
                adsPreference = "ON"
            elif self.has_ad == False:
                adsPreference = "OFF"
            
            print("\nCurrent preferences (Emails: " + emailPreference + ", SMS: " + smsPreference + ", Advertising: " + adsPreference + ")\n")
            
            try:
                # Ask for user input
                choice = prompt({ "type": "list",
                                    "message" : "Guest Controls",
                                    "choices": ["Email",
                                                "SMS",
                                                "Advertising",
                                                "Back to Important Links"]
                    })

                match choice[0]:
                    case "Email":
                        emailChoice = input("\nDo you want to receive InCollege emails? Type yes or no.\n").lower()

                        if emailChoice == "yes":
                            self.changeEntry("users", "has_email", True)
                            print("\nYou will keep receiving InCollege emails\n")
                        elif emailChoice == "no":
                            self.changeEntry("users", "has_email", False)
                            print("\nYou will stop receiving InCollege emails\n")
                        else: 
                            print("\nPlease type yes or no\n")

                    case "SMS":
                        SMSChoice = input("\nDo you want to receive InCollege SMS's? Type yes or no.\n").lower()

                        if SMSChoice == "yes":
                            self.changeEntry("users", "has_sms", True)
                            print("\nYou will keep receiving InCollege SMS's\n")
                        elif SMSChoice == "no":
                            self.changeEntry("users", "has_sms", False)
                            print("\nYou will stop receiving InCollege SMS's\n")
                        else: 
                            print("\nPlease type yes or no\n")

                    case "Advertising":
                        adsChoice = input("\nDo you want to receive InCollege advertising? Type yes or no.\n").lower()

                        if adsChoice == "yes":
                            self.changeEntry("users", "has_ad", True)
                            print("\nYou will keep receiving InCollege advertising\n")    
                        elif adsChoice == "no":
                            self.changeEntry("users", "has_ad", False)
                            print("\nYou will stop receiving InCollege advertising\n")
                        else: 
                            print("\nPlease type yes or no\n")

                    case "Back to Important Links":
                        break

                    case __:  # <--- Else
                        raise ValueError

            except ValueError:
                print("Choice not found, please try again.\n")

    def generalLinks(self):
        """
        "General" option under "Useful Links"
        """
        run = True
        while run:
            try:
                # Ask for user input
                choice = prompt({
                    "type": "list",
                    "message": "General",
                    "choices": [
                        "Sign Up",
                        "Help Center",
                        "About",
                        "Press",
                        "Blog",
                        "Careers",
                        "Developers",
                        "Back to Useful Links"
                    ]
                })

                match choice[0]:
                    case "Sign Up":
                        if self.loggedIn:
                            print("\nYou are already logged in!\n")
                        else:
                            self.signInOrUp()
                    case "Help Center":
                        print("\nWe're here to help.\n")
                    case "About":
                        print("\nIn College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide.\n")
                    case "Press":
                        print("\nIn College Pressroom: Stay on top of the latest news, updates, and reports.\n")
                    case "Blog":
                        print("\nUnder construction.\n")
                    case "Careers":
                        print("\nUnder construction.\n")
                    case "Developers":
                        print("\nUnder construction.\n")
                    case "Back to Useful Links":
                        run = False
                        break
                    case __:  # <--- Else
                        raise ValueError
            except ValueError:
                print("Choice not found, please try again.\n")

    def usefulLinks(self):
        """
        Useful Links option
        """
        run = True
        while run:
            try:
                # Ask for user input
                choice = prompt({
                            "type": "list",
                            "message" : "Useful Links",
                            "choices": ["General", 
                                        "Browse InCollege", 
                                        "Business Solutions", 
                                        "Directories", 
                                        "Back to Main Menu"]
                })
                match choice[0]:
                    case "General":
                        self.generalLinks()
                    case "Browse InCollege":
                        print("\nUnder construction.\n")
                    case "Business Solutions":
                        print("\nUnder construction.\n")
                    case "Directories":
                        print("\nUnder construction.\n")
                    case "Back to Main Menu":
                        run = False
                        break
                    case __:    # <--- Else
                        raise ValueError
            except ValueError:
                print("Choice not found, please try again.\n")

    def importantLinks(self):
        """
        Important Links option
        """
        while True:
            try:
                # Ask for user input
                choice = prompt({
                            "type": "list",
                            "message" : "Important Links",
                            "choices": ["A Copyright Notice",
                                        "About",
                                        "Accessibility", 
                                        "User Agreement", 
                                        "Privacy Policy", 
                                        "Cookie Policy", 
                                        "Copyright Policy", 
                                        "Brand Policy", 
                                        "Guest Controls", 
                                        "Languages",
                                        "Back to Main Menu"]
                })
                match choice[0]:
                    case "A Copyright Notice":
                        print("\n© 2023 InCollege\n")

                    case "About":
                        print("\nWe're InCollege, a social networking solution made by college students for college students.\n")

                    case "Accessibility":
                        print("\nInCollege is designed with navigation, readability, and usability, which benefits all users. By adding alt text to images and ensuring a logical content structure we have achieved to be ADA compliant and all users including those with disabilities can enjoy our services.\n")

                    case "User Agreement":
                        print("\nDisclaimer: By using InCollege you agree to everything our policies say, including data being collected from you, the use of cookies on your computer, and copyright law applicable to you, among others. Please check our Privacy, Cookie, Copyright, and Brand policies for more detailed information.\n")

                    case "Privacy Policy":
                        print("\nThis Website collects some Personal Data from its Users. Among the types of Personal Data that this Website collects, by itself or through third parties, there are: email address; password; first name; last name; among various types of Data. The Owner takes appropriate security measures to prevent unauthorized access, disclosure, modification, or unauthorized destruction of the Data.\n")
                        if self.loggedIn == False:
                            print("\nYou need to be logged in to access guest controls.\n")
                        else:
                            self.guestControls()

                    case "Cookie Policy":
                        print("\nCookies are small data files that are placed on your computer or mobile device when you visit a website. Cookies are widely used by website owners in order to make their websites work, or to work more efficiently, as well as to provide reporting information. Cookies help us deliver our services, by using our services, you agree to our use of cookies in your computer.\n")

                    case "Copyright Policy":
                        print("\nExcept as permitted by the copyright law applicable to you, you may not reproduce or communicate any of the content on this website, including files downloadable from this website, without the permission of the copyright owner.\n")

                    case "Brand Policy":
                        print("\nInCollege understands how hard it is for students looking for a first job and will provide the tools that they need in order to be successful. Our goal is to continuously advance what's possibly in education and connect students from all around the world.\n")

                    case "Guest Controls":
                        if self.loggedIn == False:
                            print("\nYou need to be logged in to access guest controls.\n")
                        else:
                            self.guestControls()

                    case "Languages":
                        if self.loggedIn == False:
                            print("\nYou need to be logged in to change the language.\n")
                        else:
                            self.changeLanguage()

                    case "Back to Main Menu":
                        break

                    case __:  # <--- Else
                        raise ValueError

            except ValueError:
                    print("Choice not found, please try again.\n")

    def editJobExperience(self, id):
        while True:
            choice = prompt({
                    "type": "list",
                    "message": "Edit Job Experience",
                    "choices": ["Title", "Employer", "Date Started", "Date Ended", "Location", "Description", "Finish"]
                })

            if choice[0] == "Finish":
                if self.completeRow('experiences', ['experience_id', id]):
                    break
                else:
                    print("You have missing information. Complete each field before finishing.")
            
            else:
                if choice[0] == "Date Started" or choice[0] == "Date Ended":
                    entry = self.getDate()
                else:
                    entry = input(f"Change {choice[0]} to what? ")
                # add logic to verify/change input based on selection
                column = choice[0].lower().replace(' ', '_')
                self.changeEntry("experiences", column, entry, "experience_id", id)

    def jobExperience(self):
        options = []
        jobs = []
        ids = []
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                flag = 0
                try:
                    cursor.execute(f"""SELECT *
                                    FROM experiences
                                    WHERE user_id = '{self.userID}'""")
                    vals = cursor.fetchall()
                    if not vals:
                        raise Exception
                except:
                    options.append("Add Job Experience")
                    flag = 1
                if not flag:
                    vals = list(vals)

                    print("Current job experience:")
                    for val in vals:
                        print(f"""
                            Worked as a {val[2]} for {val[3]} , from {val[4]} to {val[5]}, at {val[6]}.\n
                            {val[7]}
                            """)
                        jobs.append(f"{val[2]} for {val[3]}")
                        ids.append(val[0])
                    options.append("Edit Job Experience")
                    if len(vals) < 3:
                        options.append("Add Job Experience")

        options.append("Go Back")

        try: 
            choice = prompt({
                "type": "list",
                "message" : "Job Experience:",
                "choices": options
            })

            match choice[0]:

                case "Go Back":
                    return
                case "Edit Job Experience":
                    if len(jobs) == 1:
                        id = ids[0]
                    else:
                        choice = prompt({
                            "type": "list",
                            "message" : "Edit Job Experience:",
                            "choices": jobs
                        })
                        id = ids[jobs.index(choice[0])]
                    self.editJobExperience(id)
                case "Add Job Experience":
                    with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
                        with connection.cursor() as cursor:
                            connection._set_autocommit(True)
                            cursor.execute(f"""
                                        INSERT INTO experiences (user_id)
                                        VALUES ('{self.userID}');
                                        """)
                            cursor.execute(f"""
                                           SELECT experience_id
                                           FROM experiences
                                           WHERE user_id = '{self.userID}';
                                           """)
                            self.editJobExperience(cursor.fetchall()[-1][0])
                case __:
                    raise ValueError
            
        except ValueError:              
            print("Invalid choice. Please enter a valid option.")

    def editEducation(self):
        while True:
            choice = prompt({
                    "type": "list",
                    "message": "Edit Education",
                    "choices": ["School Name", "Degree", "Year Started", "Year Ended", "Finish"]
                })
            
            if choice[0] == "Finish":
                if self.completeRow('educations'):
                    break
                else:
                    print("You have missing information. Complete each field before finishing.")

            else:
                while True:
                    entry = input(f"Change {choice[0].lower()} to what? ")
                    if choice[0] == "Year Started" or choice[0] == "Year Ended":
                        if entry.isnumeric():
                            if int(entry) > 1 and int(entry) < 9999:
                                break
                        print("Please input a valid year.")
                        continue
                    break

                # add logic to verify/change input based on selection
                column = choice[0].lower().replace(' ', '_')
                self.changeEntry("educations", column, entry)

    def education(self):

        options = []
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                flag = 0
                try:
                    cursor.execute(f"""SELECT *
                                    FROM educations
                                    WHERE user_id = '{self.userID}'""")
                    vals = cursor.fetchall()
                    if not vals:
                        raise Exception
                except:
                    options.append("Add Education")
                    flag = 1
                if not flag:
                    vals = list(vals[0])
                    print(f"""
                          Current education:
                          Attended {vals[2]} from {vals[4]} to {vals[5]} to obtain a {vals[3]}.
                          """)
                    options.append("Edit Education")

        options.append("Go Back")

        try: 
            choice = prompt({
                "type": "list",
                "message" : "Education:",
                "choices": options
            })

            match choice[0]:

                case "Go Back":
                    return
                case "Edit Education":
                    self.editEducation()
                case "Add Education":
                    with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
                        with connection.cursor() as cursor:
                            cursor.execute(f"""
                                        INSERT INTO educations (user_id)
                                        VALUES ('{self.userID}');
                                        """)
                    self.editEducation()
                case __:
                    raise ValueError
            
        except ValueError:              
            print("Invalid choice. Please enter a valid option.")

    def editProfile(self):
        while True:
            choice = prompt({
                    "type": "list",
                    "message": "Edit Profile",
                    "choices": ["First Name", "Last Name", "Title", "Major", "University", "About", "Education", "Job Experience", "Finish"]
                })
            
            if choice[0] == "Finish":
                break
            elif choice[0] == "Education":
                self.education()
            elif choice[0] == "Job Experience":
                self.jobExperience()
            else:
                entry = input(f"Change {choice[0]} to what? ")
                
                if choice[0] == "Major" or choice[0] == "University":
                    entry = entry.title()
                # add logic to verify/change input based on selection
                column = choice[0].lower().replace(' ', '_')
                table_map = {
                    "first_name": "users",
                    "last_name": "users",
                    "title": "profiles",
                    "major": "users",
                    "university": "users",
                    "about" : "profiles"
                }
                self.changeEntry(table_map.get(column), column, entry)

    def hasProfile(self, id):
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(f"""SELECT *
                                    FROM profiles
                                    WHERE user_id = '{id}'""")
                    if not cursor.fetchall():
                        raise Exception
                    return True
                except:
                    return False

    def viewProfile(self, id):
        
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(f"""SELECT (title, about)
                                    FROM profiles
                                    WHERE user_id = '{id}'""")
                    vals = list(cursor.fetchall()[0][0])
                    if not vals:
                        raise Exception
                except:
                    print("This user has not created a profile.")
                    return
                
                title, about = [vals[i] for i in range(2)]

                cursor.execute(f"""SELECT (first_name, last_name, university, major)
                                FROM users
                                WHERE user_id = '{id}'""")
                
                vals = list(cursor.fetchall()[0][0])
                first_name, last_name, university, major = [vals[i] for i in range(4)]

                flag = 0
                try:
                    cursor.execute(f"""SELECT (school_name, degree, year_started, year_ended)
                                    FROM educations
                                    WHERE user_id = '{id}'""")
                    vals = list(cursor.fetchall()[0][0])
                    if not vals:
                        raise Exception
                except:
                    school_name = degree = year_started = year_ended = ""
                    flag = 1
                    has_education = 0
                if not flag:
                    has_education = 1
                    school_name, degree, year_started, year_ended = [vals[i] for i in range(4)]

                flag = 0
                try:
                    cursor.execute(f"""SELECT (title, employer, date_started, date_ended, location, description)
                                    FROM experiences
                                    WHERE user_id = '{id}'""")
                    vals = list(cursor.fetchall())
                    if not vals:
                        raise Exception
                except:
                    has_experience = 0
                    flag = 1

                if not flag:
                    has_experience = 1

                    jobTitles = [None for i in range(len(vals))]
                    employers = [None for i in range(len(vals))]
                    dates_started = [None for i in range(len(vals))]
                    dates_ended = [None for i in range(len(vals))]
                    locations = [None for i in range(len(vals))]
                    descriptions = [None for i in range(len(vals))]

                    i = 0 
                    for val in vals:
                        jobTitles[i], employers[i], dates_started[i], dates_ended[i], locations[i], descriptions[i] = [val[0][j] for j in range(6)]
                        i += 1

        profile = f"""
                    {first_name} {last_name}
                    """
        if title:
            profile = profile + f"""
                    {title}
                    """

        if about:
            profile = profile + f"""
                    {about}
                    """

        profile = profile + f"""
                    University: {university}
                    Major: {major}
                    """

        if has_education:
            profile = profile + f"""
                    Attended {school_name} from {year_started} to {year_ended} to obtain a {degree}.
                    """

        if has_experience:
            for i in range(len(jobTitles)):
                profile = profile + f"""
                    Worked as a {jobTitles[i]} for {employers[i]}, from {dates_started[i]} to {dates_ended[i]}, at {locations[i]}:
                    {descriptions[i]}
                    """

        print(profile)

    def profile(self):
        options = []
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                flag = 0
                try:
                    cursor.execute(f"""SELECT (title, about)
                                    FROM profiles
                                    WHERE user_id = '{self.userID}'""")
                    vals = cursor.fetchall()
                    if not vals:
                        raise Exception
                except:
                    options.append("Create Profile")
                    flag = 1
                if not flag:
                    options.append("Edit Profile")
                    self.viewProfile(self.userID)

        options.append("Go Back")
        
        try: 
            choice = prompt({
                "type": "list",
                "message" : "Profile:",
                "choices": options
            })

            match choice[0]:
                
                case "Go Back":
                    return
                case "Edit Profile":
                    self.editProfile()
                    print("Profile Edited")
                case "Create Profile":
                    with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
                        with connection.cursor() as cursor:
                            cursor.execute(f"""
                                        INSERT INTO profiles (user_id)
                                        VALUES ('{self.userID}');
                                        """)
                    self.editProfile()
                    print("Profile Created")
                case __:
                    raise ValueError

        except ValueError:              
            print("Invalid choice. Please enter a valid option.")

    def mainMenu(self):
        """
        Displays the main menu to the user after they log in.
        """
        # loggedIn = True
        while True:
            membershipTier = str(self.tier)
            print("\nMembership: " + membershipTier)
            #Display current language
            print("Current Language: " + self.language)
            #Display preferences
            if self.has_email == True:
                emailPreference = "ON"
            elif self.has_email == False:
                emailPreference = "OFF"
            
            if self.has_sms == True:
                smsPreference = "ON"
            elif self.has_sms == False:
                smsPreference = "OFF"
            
            if self.has_ad == True:
                adsPreference = "ON"
            elif self.has_ad == False:
                adsPreference = "OFF"
            
            print("Current preferences (Emails: " + emailPreference + ", SMS: " + smsPreference + ", Advertising: " + adsPreference + ")")
            self.checkPendingRequests()
            self.checkPendingMessages()

            try: 
                choice = prompt({
                                "type": "list",
                                "message" : "Main Menu:",
                                "choices": ["Find someone you know", 
                                            "Job search/internship", 
                                            "Learn a new skill",
                                            "Useful Links", 
                                            "InCollege Important Links",
                                            "Profile",
                                            "View Pending Connection Requests",
                                            "Show my Network",
                                            "Disconnect from a Connection",
                                            "Send message",
                                            "Log out"]
                })
                
                match choice[0]:
                    case "Find someone you know":
                    # Call the searchExistingUsers function
                        self.searchExistingUsers()
                
                    case "Job search/internship":
                        while True:
                            try:
                                choice = prompt({
                                        "type": "list", 
                                        "message" : "Select one:",
                                        "choices": ["Search for a Job", "Post a Job", "Back to the main menu"]
                                })

                                match choice[0]:
                                    case "Search for a Job":
                                        print("\nunder construction.\n")
                                    case "Post a Job":
                                        self.addJob()
                                    case "Back to the main menu":
                                        break  
                                    case __:    # <--- Else
                                        raise ValueError
                            
                            except ValueError:              
                                print("Invalid choice. Please enter a valid option.")

                
                    case "Learn a new skill":
                        while True:
                            try:
                                choice = prompt({
                                        "type": "list",
                                        "message" : "Skills Available:",
                                        "choices": ["Team Work", "Clean Code", "Customer Service", "Marketing", "Management", "Back to the main menu"]
                                })
                                
                                match choice[0]:
                                    case "Team Work":
                                        print("\nunder construction.\n")
                                    case "Clean Code":
                                        print("\nunder construction.\n")
                                    case "Customer Service":
                                        print("\nunder construction.\n")
                                    case "Marketing":
                                        print("\nunder construction.\n")
                                    case "Management":
                                        print("\nunder construction.\n")
                                    case "Back to the main menu":
                                        break
                                    case __:    # <--- Else
                                        raise ValueError
                        
                            except ValueError:              
                                print("Invalid choice. Please enter a valid option.")
                        
                    case "Useful Links":
                        self.usefulLinks()
                    case "InCollege Important Links":
                        self.importantLinks() 
                    case "Profile":
                        self.profile()
                    case "View Pending Connection Requests":
                        self.viewPendingRequests()
                    case "Show my Network":
                        self.viewConnectedFriends()
                    case "Disconnect from a Connection":
                        self.disconnectFriend()
                    case "Send message":
                        self.MessageMenu()
                    case "Log out":
                        # Restore the variables
                        self.userID = ""
                        self.loggedIn = False
                        self.first_name = ""
                        self.last_name = ""
                        self.has_email = True
                        self.has_sms = True
                        self.has_ad = True
                        self.language = "English"

                        print("\nLogging out.\n")
                        break
                    case __:    # <--- Else
                        raise ValueError
            
            except ValueError:
                print("\nInvalid choice. Please enter a valid option.\n")

    def loginScreen(self):
        print("\n Welcome to InCollege!")
        print("\n======================================\n")
        print("Steven's story:\n")
        print("When I first started college during my freshman year I was very shy and didn’t really have many close friends or connections to other people besides my small circle of friends. On top of that, I was looking for a part-time job to help my parents pay my tuition for college, the problem was that I didn’t really had a resume to boast about or any real work history and no working professional really wanted to talk to me. That same freshman year a professor introduced us to InCollege during a class and I tried it out of curiosity, it made all the difference! InCollege allowed me to connect with other college students at other universities who were in my major and talk about school, jobs, and projects. Being online meant that even if I was shy I was still able to create relationships with real people and expand my connections. Having connections made all the difference when talking to people about job, salaries, and offers. InCollege understands that everyone's looking for a first job and will provide the tools that they need in order to be successful. Not only was I able to find a part-time job during my college years, but it even landed me a job I was not expecting. One of my friends I made during inCollege got the job first and after working there for a while referred me to his boss, I already had a position at a well-recognized company before I even graduated! By the time I transitioned to LinkedIn I had more experiences I could use on my resume. My time using InCollege really made all the difference for me and sure it will help you too. Whether it is creating an identity on inCollege, creating connections with other students from other universities, or accessing job information, inCollege will help provide you the tools you need.")
        print("\n======================================\n")
        while True:
            try:
                # Ask for user input
                choice = prompt({
                            "type": "list",
                            "message" : "Login page",
                            "choices": ["Learn why you should join InCollege", 
                                        "For Existing Users", 
                                        "To Create an Account", 
                                        "To Find an Existing User",
                                        "Useful Links",
                                        "InCollege Important Links",
                                        "Exit"]
                })
                match choice[0]:
                    case "For Existing Users":
                        self.signIn()
                        if self.loggedIn:
                            self.mainMenu()
                    case "To Create an Account":
                        self.signUp()
                        if self.loggedIn:
                            self.mainMenu()
                    case "To Find an Existing User":
                    # Call the searchExistingUsers function
                        self.searchExistingUsers()
                    case "Learn why you should join InCollege":
                        print("\n============================\n============================\n====Video is now playing====\n============================\n============================\n")
                    case "Useful Links":
                        self.usefulLinks()
                    case "InCollege Important Links":
                        self.importantLinks()
                    case "Exit":
                        print("Thank you, bye!\n")
                        break
                    case __:    # <--- Else
                        raise ValueError
            
            except ValueError:
                    print("Choice not found, please try again.\n")
    
    def sendConnectRequest(self, from_user_id, to_user_id):
        # Connect to the database
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                # Check if there's already a request or friendship between these two users
                check_query = """
                SELECT * FROM friendships 
                WHERE (student1_id = %s AND student2_id = %s) 
                OR (student1_id = %s AND student2_id = %s);
                """
                cursor.execute(check_query, (from_user_id, to_user_id, to_user_id, from_user_id))
                existing_friendship = cursor.fetchone()

                if existing_friendship:
                    if existing_friendship[3] == 'pending':
                        print("There's already a pending request.")
                    else:
                        print("You're already connected with this user.")
                    return

                # Insert the connection request into the table
                insert_query = """
                INSERT INTO friendships (student1_id, student2_id, status) 
                VALUES (%s, %s, 'pending');
                """
                cursor.execute(insert_query, (from_user_id, to_user_id))
                connection.commit()

        print(f"Connection request sent to user {to_user_id}!")
    
    def checkPendingRequests(self):
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                fetch_query = """
                SELECT student1_id 
                FROM friendships 
                WHERE student2_id = %s AND status = 'pending';
                """
                cursor.execute(fetch_query, (self.userID,))
                requests = cursor.fetchall()

        if requests:
            print(f"\nYou have {len(requests)} pending friend requests!")
            for request in requests:
                self.handleFriendRequest(request[0])  # request[0] is student1_id, who sent the request
               
    def handleFriendRequest(self, from_user_id):
        # Fetch the name of the person who sent the request for better UI
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                name_query = """
                SELECT first_name, last_name 
                FROM users 
                WHERE user_id = %s;
                """
                cursor.execute(name_query, (from_user_id,))
                name = cursor.fetchone()
        
        print(f"\nFriend request from: {name[0]} {name[1]}")

        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                while True:
                    choice = input("Do you want to accept this friend request? (yes/no): ").lower()
                    if choice == 'yes':
                        # Update the friendship status to confirmed
                        update_query = """
                        UPDATE friendships 
                        SET status = 'confirmed' 
                        WHERE student1_id = %s AND student2_id = %s;
                        """
                        cursor.execute(update_query, (from_user_id, self.userID))
                        print("Friend request accepted!")
                        break
                    elif choice == 'no':
                        # Delete the friend request record
                        delete_query = """
                        DELETE FROM friendships 
                        WHERE student1_id = %s AND student2_id = %s;
                        """
                        cursor.execute(delete_query, (from_user_id, self.userID))
                        print("Friend request rejected!")
                        break
                    else:
                        print("Unrecognized input. Please enter yes or no.")

    def viewPendingRequests(self):
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                fetch_query = """
                SELECT student1_id, first_name, last_name 
                FROM friendships JOIN users ON friendships.student1_id = users.user_id
                WHERE student2_id = %s AND status = 'pending';
                """
                cursor.execute(fetch_query, (self.userID,))
                requests = cursor.fetchall()

        if requests:
            print("\nPending Friend Requests:")
            for req in requests:
                print(f"User ID: {req[0]}, Name: {req[1]} {req[2]}")
        else:
            print("\nYou have no pending friend requests.")

    def viewConnectedFriends(self):
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                # Get friends where the current user is student1
                fetch_query_1 = """
                SELECT student2_id, first_name, last_name 
                FROM friendships JOIN users ON friendships.student2_id = users.user_id
                WHERE student1_id = %s AND status = 'confirmed';
                """
                cursor.execute(fetch_query_1, (self.userID,))
                friends_1 = cursor.fetchall()

                # Get friends where the current user is student2
                fetch_query_2 = """
                SELECT student1_id, first_name, last_name 
                FROM friendships JOIN users ON friendships.student1_id = users.user_id
                WHERE student2_id = %s AND status = 'confirmed';
                """
                cursor.execute(fetch_query_2, (self.userID,))
                friends_2 = cursor.fetchall()

        friends = friends_1 + friends_2
        options = []
        ids = []
        if friends:
            print("\nList of Friends:")
            for friend in friends:
                options.append(f"User ID: {friend[0]}, Name: {friend[1]} {friend[2]}")
                if self.hasProfile(friend[0]):
                    options[-1] = options[-1] + " (View Profile)"
                ids.append(friend[0])
            options.append("Go Back")

            choice = prompt({
                            "type": "list",
                            "message" : "Main Menu:",
                            "choices": options
                        })
            
            if choice[0] == "Go Back":
                return
            
            self.viewProfile(ids[options.index(choice[0])])

            while True:
                Userchoice = input("Do you want to send a message to this friend? (yes/no): ").lower()
                if Userchoice == 'yes':
                    self.addMessageToDatabase(from_user_id = self.userID, to_user_id = ids[options.index(choice[0])])
                    break
                elif Userchoice == 'no':
                    break
                else:
                    print("Unrecognized input. Please enter yes or no.")

            """
            I tried putting them into an inquirerPy but for some reason when selecting them they both say choice not found.

            while True:
                try:
                    choice = prompt({
                                "type": "list",
                                "message" : "What do you want to do?:",
                                "choices": ["View Profile", 
                                            "Send message", 
                                            "Go back"]
                    })
                    match choice[0]:
                        case "View Profile":
                            self.viewProfile(ids[options.index(choice[0])])
                        
                        case "Send message":
                            self.addMessageToDatabase(from_user_id = self.userID, to_user_id = ids[options.index(choice[0])])

                        case "Go back":
                            return

                        case __:    # <--- Else
                            raise ValueError
            
                except ValueError:
                        print("Choice not found, please try again.\n")

            """

        else:
            print("\nYou have no connections in the system.")

    def disconnectFriend(self):
        friend_id = input("Enter the User ID of the connection you want to disconnect from: ")

        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                # Check if the given user_id exists in the friend's list
                check_query = """
                SELECT * FROM friendships 
                WHERE (student1_id = %s AND student2_id = %s) OR (student1_id = %s AND student2_id = %s);
                """
                cursor.execute(check_query, (self.userID, friend_id, friend_id, self.userID))
                
                if cursor.fetchone():  # If exists
                    # Proceed to delete the friendship
                    delete_query = """
                    DELETE FROM friendships 
                    WHERE (student1_id = %s AND student2_id = %s) OR (student1_id = %s AND student2_id = %s);
                    """
                    cursor.execute(delete_query, (self.userID, friend_id, friend_id, self.userID))
                    print("Successfully disconnected!")
                else:
                    print("The given user is not in your connection list.")
    
    def MessageMenu(self):
        if self.tier == "Standard":
            #Standard members can only send messages from people who have accepted their friend requests
            self.sendMessageToFriend()
        elif self.tier == "Plus":
            #Plus members can generate a list of all the students who are in the system and can send a message to any of them
            while True:
                try:
                    choice = prompt({
                                "type": "list",
                                "message" : "Send message to:",
                                "choices": ["A friend", 
                                            "Show all students", 
                                            "Go back"]
                    })
                    match choice[0]:
                        case "A friend":
                            self.sendMessageToFriend()
                        
                        case "Show all students":
                            self.sendMessageToUser()

                        case "Go back":
                            return

                        case __:    # <--- Else
                            raise ValueError
            
                except ValueError:
                        print("Choice not found, please try again.\n")
    
    def sendMessageToFriend(self):
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                # Get friends where the current user is student1
                fetch_query_1 = """
                SELECT student2_id, first_name, last_name 
                FROM friendships JOIN users ON friendships.student2_id = users.user_id
                WHERE student1_id = %s AND status = 'confirmed';
                """
                cursor.execute(fetch_query_1, (self.userID,))
                friends_1 = cursor.fetchall()

                # Get friends where the current user is student2
                fetch_query_2 = """
                SELECT student1_id, first_name, last_name 
                FROM friendships JOIN users ON friendships.student1_id = users.user_id
                WHERE student2_id = %s AND status = 'confirmed';
                """
                cursor.execute(fetch_query_2, (self.userID,))
                friends_2 = cursor.fetchall()

        friends = friends_1 + friends_2
        options = []
        ids = []
        if friends:
            print("\nSend message to:")
            for friend in friends:
                options.append(f"User ID: {friend[0]}, Name: {friend[1]} {friend[2]}")
                ids.append(friend[0])
            options.append("Go Back")

            choice = prompt({
                            "type": "list",
                            "message" : "List of Friends:",
                            "choices": options
                        })
                
            if choice[0] == "Go Back":
                return

            self.addMessageToDatabase(from_user_id = self.userID, to_user_id = ids[options.index(choice[0])])

        else:
            print("\nYou have no connections in the system.")

    def sendMessageToUser(self):
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                # Construct the query
                fetch_query = f"""
                SELECT user_id, first_name, last_name 
                FROM users; 
                """
                cursor.execute(fetch_query)
                users = cursor.fetchall()
            
        options = []
        ids = []       
        if users:
            print("\nSend message to:")
            for user in users:
                options.append(f"User ID: {user[0]}, Name: {user[1]} {user[2]}")
                ids.append(user[0])
            options.append("Go Back")

            choice = prompt({
                    "type": "list",
                    "message" : "List of Users:",
                    "choices": options
                })
                
            if choice[0] == "Go Back":
                return

            self.addMessageToDatabase(from_user_id = self.userID, to_user_id = ids[options.index(choice[0])])

        else:
            print("\nYou have no connections in the system.")

    def addMessageToDatabase(self, from_user_id, to_user_id):
        message = input("Enter the message you want to send: \n")
        # Connect to the database
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                # Insert the message into the table
                insert_query = """
                INSERT INTO messages (sender, receiver, message_txt, status) 
                VALUES (%s, %s, %s, 'unread');
                """
                cursor.execute(insert_query, (from_user_id, to_user_id, message))
                connection.commit()

        print(f"\nMessage sent to user {to_user_id}!")
    
    def checkPendingMessages(self):
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                fetch_query = """
                SELECT sender 
                FROM messages 
                WHERE receiver = %s AND status = 'unread';
                """
                cursor.execute(fetch_query, (self.userID,))
                messages = cursor.fetchall()

        if messages:
            print(f"\nYou have {len(messages)} pending messages in your inbox!")

    def __init__(self, databaseName = DATABASE_NAME_, databaseUser = DATABASE_USER_, databasePassword = DATABASE_PASSWORD_, databaseHost = DATABASE_HOST_, databasePort = DATABASE_PORT_):
        self.DATABASE_NAME = databaseName
        self.DATABASE_USER = databaseUser
        self.DATABASE_PASSWORD = databasePassword
        self.DATABASE_HOST = databaseHost
        self.DATABASE_PORT = databasePort
        self.loginScreen()

def main():
    try:
        psycopg.connect(dbname=DATABASE_NAME_, user=DATABASE_USER_, password=DATABASE_PASSWORD_, host=DATABASE_HOST_, port=DATABASE_PORT_)
    except:
        print(f"Could not connect to database {DATABASE_NAME_}. Creating it locally...")
        helper.createDatabase(DATABASE_USER_, DATABASE_PASSWORD_, DATABASE_NAME_, DATABASE_HOST_, DATABASE_PORT_)
    
    InCollegeServer()

if __name__ == "__main__":
    main()


