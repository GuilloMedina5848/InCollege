import re
from InquirerPy import prompt
import psycopg
from psycopg.rows import dict_row

# Connect to your PostgreSQL server
DATABASE_NAME_ = "incollegedb"
DATABASE_USER_ = "postgres"
DATABASE_PASSWORD_ = "postgres"
DATABASE_HOST_ = "localhost" 
DATABASE_PORT_ = "5432"  # default PostgreSQL port

# If the database doesn't exist, create it
# Should put this function in a module and import it here/to the test

def createDatabase():
    with psycopg.connect(user=DATABASE_USER_, password=DATABASE_PASSWORD_) as connection:
       connection._set_autocommit(True)
       with connection.cursor() as cursor:
          cursor.execute(f"""CREATE DATABASE {DATABASE_NAME_};""")
    with psycopg.connect(dbname=DATABASE_NAME_, user=DATABASE_USER_, password=DATABASE_PASSWORD_, host=DATABASE_HOST_, port=DATABASE_PORT_) as connection:
        with connection.cursor() as cursor:
          cursor.execute("""CREATE TABLE users (
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
                          );""")

class InCollegeServer():
    DATABASE_NAME = ""
    DATABASE_USER = ""
    DATABASE_PASSWORD = ""
    DATABASE_HOST = ""
    DATABASE_PORT = ""

    loggedIn = False
    userID = ""
    firstName = ""
    lastName = ""

    Email = True
    SMS = True
    Ads = True
    Language = "English"

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

    # def addToFile(self, username, password, first, last, Email, SMS, Ads, Language):
    #     with open(self.usersFilename, "a") as file:
    #         file.write(f"{self.userCount + 1},{username},{password},{first},{last},{Email},{SMS},{Ads},{Language}\n")
    #     file.close()

    # def addToJobFile(self, title, description, employer, location, salary):
    #     with open(self.jobsFilename, "a") as file:
    #         file.write(f"{self.firstName},{self.lastName},{title},{description},{employer},{location},{salary}\n")
    #     file.close()

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

        # jobsList.append((self.firstName, self.lastName, title, description, employer, location, salary))
        # saveJobs(jobsList)

        # Connect to the database
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                # Insert job details into the jobs table
                insert_query = """
                INSERT INTO jobs (title, description, employer, location, salary, user_id, first_name, last_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(insert_query, (title, description, employer, location, salary, self.userID, self.firstName, self.lastName))

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
                self.firstName = user['first_name']
                self.lastName = user['last_name']
                self.Email = user['has_email']
                self.SMS = user['has_sms']
                self.Ads = user['has_ad']
                self.Language = user['language']
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
                                INSERT INTO users (user_id, password, first_name, last_name, has_email, has_sms, has_ad, university, major)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                                """
                                cursor.execute(insert_query, (userID, password, first, last, has_email, has_sms, has_ad, university, major))

                        print("\n============================\n")
                        print("Thank you for creating an account.")

                        self.userID = userID
                        self.first = first
                        self.last = last
                        self.loggedIn = True
                        self.Email = True
                        self.SMS = True
                        self.Ads = True
                        self.Language = "English"
                        
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

    # Fixed
    def changePreference(self, preference, setting):
        # Define a mapping of preference names to database column names
        column_map = {
            "Email": "has_email",
            "SMS": "has_sms",
            "Ads": "has_ad",
            "Language": "language"
        }

        # Use the mapped column name
        column_name = column_map.get(preference)

        # Update class attributes
        if preference in ["Email", "SMS", "Ads"]:
            setattr(self, preference, setting)
        elif preference == "Language":
            self.Language = setting

        # Connect to the database and execute the UPDATE statement
        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                # Update the user's preference in the database
                update_query = f"""
                UPDATE users SET {column_name} = %s WHERE user_id = %s;
                """
                cursor.execute(update_query, (setting, self.userID))

    def changeLanguage(self):
        print("\nCurrent Language: " + self.Language + "\n")

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
                        if self.Language == "English":
                            print("\nCurrent Language is already in English\n")
                        else:
                            self.changePreference("Language", "English")
                            print("\nLanguage changed to English\n")
                        
                    case "Spanish":
                        if self.Language == "Spanish":
                            print("\nCurrent Language is already in Spanish\n")
                        else:
                            self.changePreference("Language", "Spanish")
                            print("\nLanguage changed to Spanish\n")

                    case "Back to Important Links":
                        break

                    case __:  # <--- Else
                        raise ValueError

            except ValueError:
                print("Choice not found, please try again.\n")

    def guestControls(self):
        while True:
            if self.Email == True:
                emailPreference = "ON"
            elif self.Email == False:
                emailPreference = "OFF"

            if self.SMS == True:
                smsPreference = "ON"
            elif self.SMS == False:
                smsPreference = "OFF"
            
            if self.Ads == True:
                adsPreference = "ON"
            elif self.Ads == False:
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
                            self.changePreference("Email", True)
                            print("\nYou will keep receiving InCollege emails\n")
                        elif emailChoice == "no":
                            self.changePreference("Email", False)
                            print("\nYou will stop receiving InCollege emails\n")
                        else: 
                            print("\nPlease type yes or no\n")

                    case "SMS":
                        SMSChoice = input("\nDo you want to receive InCollege SMS's? Type yes or no.\n").lower()

                        if SMSChoice == "yes":
                            self.changePreference("SMS", True)
                            print("\nYou will keep receiving InCollege SMS's\n")
                        elif SMSChoice == "no":
                            self.changePreference("SMS", False)
                            print("\nYou will stop receiving InCollege SMS's\n")
                        else: 
                            print("\nPlease type yes or no\n")

                    case "Advertising":
                        adsChoice = input("\nDo you want to receive InCollege advertising? Type yes or no.\n").lower()

                        if adsChoice == "yes":
                            self.changePreference("Ads", True)
                            print("\nYou will keep receiving InCollege advertising\n")    
                        elif adsChoice == "no":
                            self.changePreference("Ads", False)
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

    def mainMenu(self):
        """
        Displays the main menu to the user after they log in.
        """
        # loggedIn = True
        while True:
            #Display current language
            print("\nCurrent Language: " + self.Language)
            #Display preferences
            if self.Email == True:
                emailPreference = "ON"
            elif self.Email == False:
                emailPreference = "OFF"
            
            if self.SMS == True:
                smsPreference = "ON"
            elif self.SMS == False:
                smsPreference = "OFF"
            
            if self.Ads == True:
                adsPreference = "ON"
            elif self.Ads == False:
                adsPreference = "OFF"
            
            print("Current preferences (Emails: " + emailPreference + ", SMS: " + smsPreference + ", Advertising: " + adsPreference + ")")
            self.checkPendingRequests()

            try: 
                choice = prompt({
                                "type": "list",
                                "message" : "Main Menu:",
                                "choices": ["Find someone you know", 
                                            "Job search/internship", 
                                            "Learn a new skill",
                                            "Useful Links", 
                                            "InCollege Important Links",
                                            "View Pending Connection Requests",
                                            "Show my Network",
                                            "Disconnect from a Connection",
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
                    case "View Pending Connection Requests":
                        self.viewPendingRequests()
                    case "Show my Network":
                        self.viewConnectedFriends()
                    case "Disconnect from a Connection":
                        self.disconnectFriend()
                    case "Log out":
                        # Restore the variables
                        self.userID = ""
                        self.loggedIn = False
                        self.firstName = ""
                        self.lastName = ""
                        self.Email = True
                        self.SMS = True
                        self.Ads = True
                        self.Language = "English"

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
        print("When I first started college during my freshman year I was very shy and didn’t really have many close friends or connections to other people besides my small circle of friends. On top of that, I was looking for a part-time job to help my parents pay my tuition for college, the problem was that I didn’t really had a resume to boast about or any real work history, so no working professional really wanted to talk to me. That same freshman year a professor introduced us to inCollege during a class and I tried it out of curiosity, it made all the difference. inCollege allowed me to connect with other college students at other universities who were in my major and talk about school, jobs, and projects. Being online meant that even if I was shy I was still able to create relationships with real people from outside my small circle of friends and expand my connections. Having a connection made all the difference when talking to people about job, salaries, and offers. inCollege understands that everyone's looking for a first job and will provide the tools that they need in order to be successful. Not only was I able to find a part-time job during my college years, but it even landed me a job I was not expecting. One of my friends I made during inCollege got the job first and after working there for a while referred me to his boss, I already had a position at a well-recognized company before I even graduated! By the time I transitioned to LinkedIn I had more experiences I could use on my resume. My time using inCollege really made all the difference for me and sure it will help you too. Whether it is creating an identity on inCollege, creating connections with other students from other universities, or accessing job information, inCollege will help provide you the tools you need.")
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

        choice = input("Do you want to accept this friend request? (yes/no): ").lower()

        with psycopg.connect(dbname=self.DATABASE_NAME, user=self.DATABASE_USER, password=self.DATABASE_PASSWORD, host=self.DATABASE_HOST, port=self.DATABASE_PORT) as connection:
            with connection.cursor() as cursor:
                if choice == 'yes':
                    # Update the friendship status to confirmed
                    update_query = """
                    UPDATE friendships 
                    SET status = 'confirmed' 
                    WHERE student1_id = %s AND student2_id = %s;
                    """
                    cursor.execute(update_query, (from_user_id, self.userID))
                    print("Friend request accepted!")
                else:
                    # Delete the friend request record
                    delete_query = """
                    DELETE FROM friendships 
                    WHERE student1_id = %s AND student2_id = %s;
                    """
                    cursor.execute(delete_query, (from_user_id, self.userID))
                    print("Friend request rejected!")


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
        if friends:
            print("\nList of Friends:")
            for friend in friends:
                print(f"User ID: {friend[0]}, Name: {friend[1]} {friend[2]}")
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
        createDatabase()
    
    InCollegeServer()

if __name__ == "__main__":
    main()


