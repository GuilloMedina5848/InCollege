import re
from InquirerPy import prompt
import psycopg2

# Connect to your PostgreSQL server
DATABASE_NAME = "incollegedb"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "postgres"
DATABASE_HOST = "localhost" 
DATABASE_PORT = "5432"  # default PostgreSQL port

# Connect to the database
with psycopg2.connect(dbname=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT) as connection:
    with connection.cursor() as cursor:
        try:
            cursor.execute("""SELECT schemaname, tablename 
                            FROM pg_tables
                            WHERE schemaname NOT IN ('pg_catalog', 'information_schema');""")
            tables = cursor.fetchall()

            if not tables:
                print("No tables found.")
            else:
                for schema, table in tables:
                    print(f"{schema}.{table}")

        except Exception as e:
            print(f"Error executing query: {e}")

class InCollegeServer():
    DATABASE_NAME = "incollegedb"
    DATABASE_USER = "postgres"
    DATABASE_PASSWORD = "postgres"
    DATABASE_HOST = "127.0.0.1" 
    DATABASE_PORT = "5432"  # default PostgreSQL port

    loggedIn = False
    userID = ""
    firstName = ""
    lastName = ""

    Email = True
    SMS = True
    Ads = True
    Language = "English"

    jobsFilename = "Jobs.txt"
    usersFilename = "Users.txt"

    jobsList = []
    jobsCount = 0
    maxJobs = 5

    userList = []
    userCount = 0
    maxUsers = 10

    def updateUserList(self):
        self.userList = []
        count = 0
        with open(self.usersFilename, "r") as file:
            for line in file:  # reading each line
                userIndex, stored_username, stored_password, first, last, Email, SMS, Ads, Language = line.strip().split(',')
                # parsing each line
                self.userList.append((userIndex, stored_username,stored_password, first, last, Email, SMS, Ads, Language))  # adding it to the list of users
                count += 1  # incrementing each user
        self.userCount = count

    def updateJobList(self):
        self.jobsList = []
        count = 0
        try:
            with open(self.jobsFilename, "r") as jobsFile:
                for line in jobsFile:
                    firstName, lastName, title, description, employer, location, salary = line.strip().split(',')
                    self.jobsList.append((firstName, lastName, title, description, employer, location, salary))
                    count += 1
        except FileNotFoundError:
            pass  # If the file doesn't exist, start with an empty jobs list
        self.jobsCount = count

    def validUser(self, UserID, password):
        """
        Checks if the provided UserID is unique
        Check if the provided password meets certain requirements
        """
        for line in self.userList:
            if line[1] == UserID:
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

    def addToFile(self, username, password, first, last, Email, SMS, Ads, Language):
        with open(self.usersFilename, "a") as file:
            file.write(f"{self.userCount + 1},{username},{password},{first},{last},{Email},{SMS},{Ads},{Language}\n")
        file.close()

    def addToJobFile(self, title, description, employer, location, salary):
        with open(self.jobsFilename, "a") as file:
            file.write(f"{self.firstName},{self.lastName},{title},{description},{employer},{location},{salary}\n")
        file.close()

    def addJob(self):
        """
        Allows a logged-in user to post a job.
        """
        if self.jobsCount >= self.maxJobs:
            print("You have reached the maximum number of job postings.")
            return

        print("\n============================\n")
        title = input("Please enter the job title: ")
        description = input("Please enter the job description: ")
        employer = input("Please enter the employer: ")
        location = input("Please enter the location: ")
        while True:
            try:
                salary = f"${'{:,.2f}'.format(float(input('Please enter the salary: ')))}"
            except:
                print("\nPlease enter a number.\n")
                continue
            break

        # jobsList.append((self.firstName, self.lastName, title, description, employer, location, salary))
        # saveJobs(jobsList)

        self.addToJobFile(title, description, employer, location, salary)
        self.updateJobList()

        print("\nJob posted successfully!")

    def signIn(self):
        """
        allow existing user to log in
        """
        while True:
            existingUserID = input("Please enter UserID: ")
            existingPassword = input("Please enter password: ")
            for line in self.userList:
                if line[1] == existingUserID and line[2] == existingPassword:
                    self.userID = existingUserID
                    self.firstName = line[3]
                    self.lastName = line[4]
                    self.Email = line[5] == 'True'
                    self.SMS = line[6] == 'True'
                    self.Ads = line[7] == 'True'
                    self.Language = line[8].strip('\n')
                    self.loggedIn = True
                    print(
                        f"\nWelcome, {existingUserID}. You have successfully logged in.")
                    
                    return # existingUserID, Email == 'True', SMS == 'True', Ads == 'True', Language
            print("\nIncorrect username / password, please try again\n")

    def signUp(self):
        try: 
            if self.userCount >= self.maxUsers:
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
                        with psycopg2.connect(dbname= self.DATABASE_NAME, user= self.DATABASE_USER, password= self.DATABASE_PASSWORD, host= self.DATABASE_HOST, port= self.DATABASE_PORT) as connection:
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
        #Search for existing users based on first and last names.
        first_name = input("Enter the user's first name: ")
        last_name = input("Enter the user's last name: ")

        found = False
        for line in self.userList:
            stored_first_name, stored_last_name = line[3], line[4]
            if first_name.lower() == stored_first_name.lower() and last_name.lower() == stored_last_name.lower():
                print("\nThey are a part of the InCollege system.\n")
                found = True
                break
        if not found:
            print("\nThey are not yet a part of the InCollege system yet.\n")

    # Fixed
    def changePreference(self, preference, setting):
        # Mapping of preference to its corresponding index in the file
        preference_map = {
            "Email": 5,
            "SMS": 6,
            "Ads": 7,
            "Language": 8
        }

        # Update class attributes
        if preference in ["Email", "SMS", "Ads"]:
            setattr(self, preference, setting)
        elif preference == "Language":
            self.Language = setting

        # Update the user's preference in the file
        updated_file_content = []
        with open(self.usersFilename, "r") as file:
            for line in file:
                parts = line.strip().split(',')
                if parts[1] == self.userID:
                    parts[preference_map[preference]] = str(setting)  # Ensure setting is a string before assignment
                updated_file_content.append(','.join(parts))

        with open(self.usersFilename, "w") as file:
            file.write('\n'.join(updated_file_content) + '\n')  # Ensure there's a newline character at the end


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

            try: 
                choice = prompt({
                                "type": "list",
                                "message" : "Main Menu:",
                                "choices": ["Find someone you know", 
                                            "Job search/internship", 
                                            "Learn a new skill",
                                            "Useful Links", 
                                            "InCollege Important Links",
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
                    case "Log out":
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

    def __init__(self):
        self.updateUserList()
        self.updateJobList()
        self.loginScreen()


def main():
    InCollegeServer()

if __name__ == "__main__":
    main()


