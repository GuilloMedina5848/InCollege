import re
from InquirerPy import prompt

##################################################
# Definitions of Function
##################################################

def getName(userID):
  file = open("Users.txt", "r")
  users = file.read().split('\n')
  i = 0
  for user in users:
    users[i] = user.split(',')
    i += 1
  file.close()

  i = 0
  
  for user in users:
    if user[1] == userID:
      break
    i += 1

  return user[3], user[4]

def addJob(jobsList, userID):
    """
    Allows a logged-in user to post a job.
    """
    if len(jobsList) >= 5:
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

    firstName, lastName = getName(userID)

    jobsList.append((firstName, lastName, title, description, employer, location, salary))
    saveJobs(jobsList)
    print("\nJob posted successfully!")

def saveJobs(jobsList, filename="Jobs.txt"):
    """
    Save the list of jobs to a file named "Jobs.txt".
    """
    with open(filename, "w") as file:
        for job in jobsList:
            file.write(",".join(job) + "\n")

def printJobs(jobsList):
    """
    Displays the list of posted jobs.
    """
    print("\n============================\n")
    if not jobsList:
        print("No jobs are currently posted.")
    else:
        print("Posted Jobs:")
        for i, job in enumerate(jobsList):
            _, title, description, employer, location, salary = job
            print(f"Job {i + 1}:")
            print(f"Title: {title}")
            print(f"Description: {description}")
            print(f"Employer: {employer}")
            print(f"Location: {location}")
            print(f"Salary: {salary}")
            print("\n------------------------\n")

def existingUser(existingUsersList):
  """
  allow existing user to log in
  """
  run = True
  while run:
    existingUserID = input("Please enter UserID: ")
    existingPassword = input("Please enter password: ")
    for line in existingUsersList:
      if line[1] == existingUserID and line[2] == existingPassword:
        print(
            f"\nWelcome, {existingUserID}. You have successfully logged in.")
        Email = line[5], SMS = line[6], Ads = line[7], Language = line[8]
        run = False
        return existingUserID, Email, SMS, Ads, Language

    print("\nIncorrect username / password, please try again\n")

def addToFile(UserCount, username, password, first, last, Email, SMS, Ads, Language, filename="Users.txt"):
  """
  : Adds the user's details to a file named "Users.txt".
  """
  with open(filename, "a") as file:
    file.write(f"{UserCount},{username},{password},{first},{last},{Email},{SMS},{Ads},{Language}\n")
  file.close()

def changePreference(userID, preference, setting):
  if preference == "Email":
     preference = 5
  elif preference == "SMS":
     preference = 6
  elif preference == "Ads":
     preference = 7
  elif preference == "Language":
     setting = setting+'\n'
     preference = 8
  
  file = open("Users.txt", "r").readlines()
  i = 0
  for line in file:
    file[i] = line.split(',')
    i += 1
  for line in file:
      if line[1] == userID:
        line[preference] = setting
  i = 0
  for line in file:
    file[i] = ','.join(str(v) for v in line)
    i += 1
  file = ''.join(file)
  open("Users.txt", "w").write(file)

def getPreference(userID, preference):
  if preference == "Email":
     preference = 5
  elif preference == "SMS":
     preference = 6
  elif preference == "Ads":
     preference = 7
  elif preference == "Language":
     preference = 8
  
  file = open("Users.txt", "r").readlines()
  i = 0
  for line in file:
    file[i] = line.split(',')
    i += 1
  for line in file:
      if line[1] == userID:
        return line[preference]

def UniqueUser(existingUsersList, UserID, password):
  """
  Checks if the provided UserID is unique
  Check if the provided password meets certain requirements
  """
  for line in existingUsersList:
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

def createUser(UserCount, existingUsersList, jobsList, loggedIn):
  """
   Registers a new user, provided the UserID is unique and the 
   password meets the requirements.
  """
  print("\n============================\n")
  # variable to store user ID
  run = True
  while run:
    userID = input("Please enter UserID: ")
    print(
        "===============================\n1) Password must be 8 - 12 characters\n2) Must contain at least one capital letter\n3) Must contain a number\n4) Must contain a special character\n ================================="
    )
    password = input("Please enter password: ")
    first = input("Please enter your first name: ")
    last = input("Please enter your last name: ")
    if UniqueUser(existingUsersList, userID, password):
      print(
          "\nYour username is unique and the password meets all the requirements.\n"
      )
      addToFile(UserCount, userID,
                password, first, last, True, True, True, "English")# Save the new user information to the file
      print("\n============================\n")
      print("Thank you for creating an account.")
      print(f"\nWelcome, {userID}. You have successfully logged in.\n")
      loggedIn = True
      run = False
      mainMenu(UserCount, existingUsersList, jobsList, userID, loggedIn, True, True, True, "English")  # Call the main menu function for logged-in users
    else:
      print(
          "\nYour username is already taken or the password doesn't meet requirements. Please start over\n"
      )

def mainMenu(UserCount, existingUsersList, jobsList, userID, loggedIn, Email, SMS, Ads, Language):
  """
   Displays the main menu to the user after they log in.
  """
  #Display current language
  print("Current language: " + Language)
  #Display preferences
  if Email == True:
    PEmails = "ON"
  elif Email == False:
    PEmails = "OFF"
  
  if SMS == True:
    PSMS = "ON"
  elif SMS == False:
    PSMS = "OFF"
  
  if Ads == True:
    PAds = "ON"
  elif Ads == False:
    PAds = "OFF"
    
  print("Current preferences (Emails: " + PEmails + ", SMS: " + PSMS + ", Advertising: " + PAds + ")")

  loggedIn = True
  while True:
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
          searchExistingUsers(existingUsersList)
    
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
                  addJob(jobsList, userID)

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
            usefulLinks(UserCount, existingUsersList, jobsList, loggedIn, userID)

        case "InCollege Important Links":
            importantLinks(loggedIn, Email, SMS, Ads, userID) 

        case "Log out":
            print("\nLogging out.\n")
            break
    
        case __:    # <--- Else
              raise ValueError
    
    except ValueError:
      print("\nInvalid choice. Please enter a valid option.\n")

def searchExistingUsers(existingUsersList):
    #Search for existing users based on first and last names.
    first_name = input("Enter the user's first name: ")
    last_name = input("Enter the user's last name: ")

    found = False
    for line in existingUsersList:
        stored_first_name, stored_last_name = line[3], line[4]
        if first_name.lower() == stored_first_name.lower() and last_name.lower() == stored_last_name.lower():
            print("\nThey are a part of the InCollege system.\n")
            found = True
            break

    if not found:
        print("\nThey are not yet a part of the InCollege system yet.\n")

def signIn(UserCount, existingUsersList, jobsList):
  userID, Email, SMS, Ads, Language = existingUser(existingUsersList)
  print("finished calling existing users")
  mainMenu(UserCount, existingUsersList, jobsList, userID, True, Email, SMS, Ads, Language)  # Call the main menu function for logged-in users

def signUp(UserCount, existingUsersList, jobsList, loggedIn):
  if UserCount >= 5:
    print(
      "\nAll permitted accounts have been created, please come back later\n"
    )
  else:
    UserCount += 1
    createUser(UserCount, existingUsersList, jobsList, loggedIn)
  
def usefulLinks(UserCount, existingUsersList, jobsList, loggedIn):
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
            generalLinks(UserCount, existingUsersList, jobsList, loggedIn)
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

def generalLinks(UserCount, existingUsersList, jobsList, loggedIn):
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
                    if loggedIn:
                      print("\nYou are already logged in!\n")
                    else:
                      signInOrUp(UserCount, existingUsersList, jobsList, loggedIn)
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

def signInOrUp(UserCount, existingUsersList, jobsList, loggedIn):
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
                    signIn(UserCount, existingUsersList, jobsList)

                case "To Create an Account":
                    signUp(UserCount, existingUsersList, jobsList, loggedIn)

                case "Back to General":
                    run = False
                    break
                    
                case __:  # <--- Else
                    raise ValueError

        except ValueError:
            print("Choice not found, please try again.\n") 

def importantLinks(loggedIn, Email, SMS, Ads, userID = ""):
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
            print("\nIn College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide.\n")

          case "Accessibility":
            print("\nInCollege is designed with navigation, readability, and usability, which benefits all users. By adding alt text to images and ensuring a logical content structure we have achieved to be ADA compliant and all users including those with disabilities can enjoy our services.\n")

          case "User Agreement":
            print("\nDisclaimer: By using InCollege you agree to everything our policies say, including data being collected from you, the use of cookies on your computer, and copyright law applicable to you, among others. Please check our Privacy, Cookie, Copyright, and Brand policies for more detailed information.\n")

          case "Privacy Policy":
            print("\nThis Website collects some Personal Data from its Users. Among the types of Personal Data that this Website collects, by itself or through third parties, there are: email address; password; first name; last name; among various types of Data. The Owner takes appropriate security measures to prevent unauthorized access, disclosure, modification, or unauthorized destruction of the Data.\n")
            if loggedIn == False:
              print("\nYou need to be logged in to access guest controls.\n")
            else:
              guestControls(Email, SMS, Ads, userID)

          case "Cookie Policy":
            print("\nCookies are small data files that are placed on your computer or mobile device when you visit a website. Cookies are widely used by website owners in order to make their websites work, or to work more efficiently, as well as to provide reporting information. Cookies help us deliver our services, by using our services, you agree to our use of cookies in your computer.\n")

          case "Copyright Policy":
            print("\nExcept as permitted by the copyright law applicable to you, you may not reproduce or communicate any of the content on this website, including files downloadable from this website, without the permission of the copyright owner.\n")

          case "Brand Policy":
            print("\nUnder construction.\n")

          case "Guest Controls":
            if loggedIn == False:
              print("\nYou need to be logged in to access guest controls.\n")
            else:
              guestControls(Email, SMS, Ads, userID)

          case "Languages":
            if loggedIn == False:
              print("\nYou need to be logged in to change the language.\n")
            else:
              changeLanguage(userID)

          case "Back to Main Menu":
            break

          case __:  # <--- Else
            raise ValueError

      except ValueError:
            print("Choice not found, please try again.\n")

def guestControls(Email, SMS, Ads, userID):
  while True:
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
            Email = input("\nDo you want to receive InCollege emails? Type yes or no.\n").lower()

            if Email == "yes":
              print("\nYou will keep receiving InCollege emails\n")
              changePreference(userID, "Email", True)
              Email = True
            elif Email == "no":
              print("\nYou will stop receiving InCollege emails\n")
              changePreference(userID, "Email", False)
              Email = False
            else: 
              print("\nPlease type yes or no\n")

          case "SMS":
            SMS = input("\nDo you want to receive InCollege SMS's? Type yes or no.\n").lower()

            if SMS == "yes":
              print("\nYou will keep receiving InCollege SMS's\n")
              changePreference(userID, "SMS", True)
              SMS = True
            elif SMS == "no":
              print("\nYou will stop receiving InCollege SMS's\n")
              changePreference(userID, "SMS", False)
              SMS = False
            else: 
              print("\nPlease type yes or no\n")

          case "Advertising":
            Ads = input("\nDo you want to receive InCollege advertising? Type yes or no.\n").lower()

            if Ads == "yes":
              print("\nYou will keep receiving InCollege advertising\n")
              changePreference(userID, "Ads", True)
              Ads = True
            elif Ads == "no":
              print("\nYou will stop receiving InCollege advertising\n")
              changePreference(userID, "Ads", False)
              Ads = False
            else: 
              print("\nPlease type yes or no\n")

          case "Back to Important Links":
            break

          case __:  # <--- Else
            raise ValueError

    except ValueError:
        print("Choice not found, please try again.\n")

def changeLanguage(userID):
  currentLanguage = getPreference(userID, "Language")
  print("\nCurrent Language: " + currentLanguage + "\n")

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
              if currentLanguage == "English":
                print("\nCurrent Language is already in English\n")
              else:
                print("\nLanguage changed to English\n")
                changePreference(userID, "Language", "English")

            case "Spanish":
              if currentLanguage == "Spanish":
                print("\nCurrent Language is already in Spanish\n")
              else:
                print("\nLanguage changed to Spanish\n")
                changePreference(userID, "Language", "Spanish")

            case "Back to Important Links":
              break

            case __:  # <--- Else
              raise ValueError

      except ValueError:
          print("Choice not found, please try again.\n")

################################################
# Main
##################################################
def main():
  print("\n Welcome to InCollege!")
  PEmails, PSMS, Pads = "ON", "ON", "ON"
  print("\n======================================\n")
  print("Steven's story:\n")
  print("When I first started college during my freshman year I was very shy and didn’t really have many close friends or connections to other people besides my small circle of friends. On top of that, I was looking for a part-time job to help my parents pay my tuition for college, the problem was that I didn’t really had a resume to boast about or any real work history, so no working professional really wanted to talk to me. That same freshman year a professor introduced us to inCollege during a class and I tried it out of curiosity, it made all the difference. inCollege allowed me to connect with other college students at other universities who were in my major and talk about school, jobs, and projects. Being online meant that even if I was shy I was still able to create relationships with real people from outside my small circle of friends and expand my connections. Having a connection made all the difference when talking to people about job, salaries, and offers. inCollege understands that everyone's looking for a first job and will provide the tools that they need in order to be successful. Not only was I able to find a part-time job during my college years, but it even landed me a job I was not expecting. One of my friends I made during inCollege got the job first and after working there for a while referred me to his boss, I already had a position at a well-recognized company before I even graduated! By the time I transitioned to LinkedIn I had more experiences I could use on my resume. My time using inCollege really made all the difference for me and sure it will help you too. Whether it is creating an identity on inCollege, creating connections with other students from other universities, or accessing job information, inCollege will help provide you the tools you need.")
  print("\n======================================\n")
  # initializing a list of tuples to store existing users:
  existingUsersList = []  # tuple = (index, userID, password)
  # storing information from the file to a tuple:
  filename = "Users.txt"
  UserCount = 0
  loggedIn = False #check if user is logged in
  with open(filename, "r") as file:
    for line in file:  # reading each line
      userIndex, stored_username, stored_password, first, last, Email, SMS, Ads, Language = line.strip().split(
          ',')  # parsing each line
      existingUsersList.append(
          (userIndex, stored_username,
           stored_password, first, last, Email, SMS, Ads, Language))  # adding it to the list of users
      UserCount += 1  # incrementing each user
  
  Email, SMS, Ads = True, True, True
  
  jobsList = []
    # Load jobs from the file if available
  jobsFilename = "Jobs.txt"
  try:
      with open(jobsFilename, "r") as jobsFile:
          for line in jobsFile:
              firstName, lastName, title, description, employer, location, salary = line.strip().split(',')
              jobsList.append((firstName, lastName, title, description, employer, location, salary))
  except FileNotFoundError:
      pass  # If the file doesn't exist, start with an empty jobs list

  # variable so that loops run until we tell it to stop
  run = True
  # loop that runs infinitely if given the wrong choice
  while run:
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
          signIn(UserCount, existingUsersList, jobsList)
        case "To Create an Account":
          signUp(UserCount, existingUsersList, jobsList, loggedIn)
    
        case "To Find an Existing User":
          # Call the searchExistingUsers function
          searchExistingUsers(existingUsersList)

        case "Learn why you should join InCollege":
          print(            "\n============================\n============================\n====Video is now playing====\n============================\n============================\n"
               )
          
        case "Useful Links":
            usefulLinks(UserCount, existingUsersList, jobsList, loggedIn)

        case "InCollege Important Links":
            importantLinks(loggedIn, Email, SMS, Ads)
          
        case "Exit":
          print("Thank you, bye!\n")
          break
    
        case __:    # <--- Else
          raise ValueError
    
    except ValueError:
            print("Choice not found, please try again.\n")

if __name__ == "__main__":
  main()