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

def existingUser(existingUsersList, loggedIn):
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
            f"\nWelcome, {existingUserID}. You have successfully logged in.\n")
        loggedIn = True
        run = False
        return existingUserID

    print("\nIncorrect username / password, please try again\n")


def addToFile(UserCount, username, password, first, last, filename="Users.txt"):
  """
  : Adds the user's details to a file named "Users.txt".
  """
  with open(filename, "a") as file:
    file.write(f"{UserCount},{username},{password},{first},{last}\n")
  file.close()


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
                password, first, last)  # Save the new user information to the file
      print("\n============================\n")
      print("Thank you for creating an account.")
      print(f"\nWelcome, {userID}. You have successfully logged in.\n")
      loggedIn = True
      run = False
      mainMenu(UserCount, existingUsersList, jobsList, userID)  # Call the main menu function for logged-in users
    else:
      print(
          "\nYour username is already taken or the password doesn't meet requirements. Please start over\n"
      )


def mainMenu(UserCount, existingUsersList, jobsList, userID):
  """
   Displays the main menu to the user after they log in.
  """
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
                    "choices": ["Search for a Job", "Post a Job", "Return to the main menu"]
              })

              match choice[0]:
                case "Search for a Job":
                  print("\nunder construction.\n")

                case "Post a Job":
                  addJob(jobsList, userID)

                case "Return to the main menu":
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
                    "choices": ["Team Work", "Clean Code", "Customer Service", "Marketing", "Management", "Return to the main menu"]
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
            
                case "Return to the main menu":
                  break
                  
                case __:    # <--- Else
                  raise ValueError
            
            except ValueError:              
              print("Invalid choice. Please enter a valid option.")
        case "Useful Links":
            usefulLinks(UserCount, existingUsersList, jobsList, loggedIn = True)

        case "InCollege Important Links":
            importantLinks() 
        case "Log out":
          print("Logging out.\n")
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

def signIn(UserCount, existingUsersList, jobsList, loggedIn): 
  userID = existingUser(existingUsersList, loggedIn)
  mainMenu(UserCount, existingUsersList, jobsList, userID)  # Call the main menu function for logged-in users

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
                    signIn(UserCount, existingUsersList, jobsList, loggedIn)
                case "To Create an Account":
                    signUp(UserCount, existingUsersList, jobsList, loggedIn)
                case "Back to General":
                    run = False
                    break
                case __:  # <--- Else
                    raise ValueError
        except ValueError:
            print("Choice not found, please try again.\n") 

def importantLinks():
   pass #Still needs to be implemented              
################################################
# Main
##################################################
def main():
  print("\n Welcome to InCollege!")
  print("\n============================\n")
  print("Steven's story:\n")
  print("When I first started college during my freshman year I was very shy and didn’t really have many close friends or connections to other people besides my small circle of friends. On top of that, I was looking for a part-time job to help my parents pay my tuition for college, the problem was that I didn’t really had a resume to boast about or any real work history, so no working professional really wanted to talk to me. That same freshman year a professor introduced us to inCollege during a class and I tried it out of curiosity, it made all the difference. inCollege allowed me to connect with other college students at other universities who were in my major and talk about school, jobs, and projects. Being online meant that even if I was shy I was still able to create relationships with real people from outside my small circle of friends and expand my connections. Having a connection made all the difference when talking to people about job, salaries, and offers. inCollege understands that everyone's looking for a first job and will provide the tools that they need in order to be successful. Not only was I able to find a part-time job during my college years, but it even landed me a job I was not expecting. One of my friends I made during inCollege got the job first and after working there for a while referred me to his boss, I already had a position at a well-recognized company before I even graduated! By the time I transitioned to LinkedIn I had more experiences I could use on my resume. My time using inCollege really made all the difference for me and sure it will help you too. Whether it is creating an identity on inCollege, creating connections with other students from other universities, or accessing job information, inCollege will help provide you the tools you need.")
  print("\n============================\n")
  # initializing a list of tuples to store existing users:
  existingUsersList = []  # tuple = (index, userID, password)
  # storing information from the file to a tuple:
  filename = "Users.txt"
  UserCount = 0
  loggedIn = False #check if user is logged in
  with open(filename, "r") as file:
    for line in file:  # reading each line
      userIndex, stored_username, stored_password, first, last = line.strip().split(
          ',')  # parsing each line
      existingUsersList.append(
          (userIndex, stored_username,
           stored_password, first, last))  # adding it to the list of users
      UserCount += 1  # incrementing each user
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
          signIn(UserCount, existingUsersList, jobsList, loggedIn)
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
            importantLinks()
          
        case "Exit":
          print("Thank you, bye!\n")
          break
    
        case __:    # <--- Else
          raise ValueError
    
    except ValueError:
            print("Choice not found, please try again.\n")
      

if __name__ == "__main__":
  main()