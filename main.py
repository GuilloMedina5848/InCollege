import re


##################################################
# Definitions of Function
##################################################
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
            f"\nWelcome, {existingUserID}. You have successfully logged in.\n")
        run = False
        return True

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


def createUser(UserCount, existingUsersList):
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
      run = False
      mainMenu(existingUsersList)  # Call the main menu function for logged-in users
    else:
      print(
          "\nYour username is already taken or the password doesn't meet requirements. Please start over\n"
      )


def mainMenu(existingUsersList):
  """
   Displays the main menu to the user after they log in.
  """
  while True:
    print("\nMain Menu:")
    print("1. Find someone you know")
    print("2. Search for a job")
    print("3. Learn a new skill")
    print("4. Log out")
    mainMenuChoice = input("Enter your choice: ")

    if mainMenuChoice == '1':
      searchExistingUsers(existingUsersList)  # Call the searchExistingUsers function
    elif mainMenuChoice == '2':
      print("under construction.")
    elif mainMenuChoice == '3':
      while True:
        print("\nSkills Available:")
        print("1. Team Work")
        print("2. Clean Code")
        print("3. Customer Service")
        print("4. Marketing")
        print("5. Management")
        print("6. Return to the main menu")
        skillChoice = input("Enter your choice: ")
        if skillChoice in ['1', '2', '3', '4', '5']:
          print("under construction.")
        elif skillChoice == '6':
          break
        else:
          print("Invalid choice. Please enter a valid option.")
    elif mainMenuChoice == '4':
      print("Logging out.")
      break
    else:
      print("Invalid choice. Please enter a valid option.")

def searchExistingUsers(existingUsersList):
    #Search for existing users based on first and last names.
    first_name = input("Enter the user's first name: ")
    last_name = input("Enter the user's last name: ")

    found = False
    for line in existingUsersList:
        stored_first_name, stored_last_name = line[3], line[4]
        if first_name.lower() == stored_first_name.lower() and last_name.lower() == stored_last_name.lower():
            print("They are a part of the InCollege system.")
            found = True
            break

    if not found:
        print("They are not yet a part of the InCollege system yet.")


################################################
# Main
##################################################
def main():
  print("\n Welcome to InCollege!")
  print("============================\n")
  # initializing a list of tuples to store existing users:
  existingUsersList = []  # tuple = (index, userID, password)
  # storing information from the file to a tuple:
  filename = "Users.txt"
  UserCount = 0
  with open(filename, "r") as file:
    for line in file:  # reading each line
      userIndex, stored_username, stored_password, first, last = line.strip().split(
          ',')  # parsing each line
      existingUsersList.append(
          (userIndex, stored_username,
           stored_password, first, last))  # adding it to the list of users
      UserCount += 1  # incrementing each user

  # variable so that loops run until we tell it to stop
  run = True
  # loop that runs infinitely if given the wrong choice
  while run:
    print(
        "============================\nFor Existing Users Enter: 1 \nTo Create an Account Enter: 2\nTo Find an Existing User: 3\n============================\n"
    )
    # Ask for user input
    choice = input("Enter Your Choice: ")
    # if the correct choice then the loop stops
    if choice == '1':
      existingUser(existingUsersList)
      mainMenu(existingUsersList)  # Call the main menu function for logged-in users
      run = False
    elif choice == '2':
      # if statement to check if there are too many users:
      if UserCount >= 5:
        print(
            "\nAll permitted accounts have been created, please come back later\n"
        )
      else:
        UserCount += 1
        createUser(UserCount, existingUsersList)
        run = False
    elif choice == '3':
            searchExistingUsers(existingUsersList)  # Call the searchExistingUsers function
    else:
      print("Your input was incorrect. Please input a correct value.")
      pass


if __name__ == "__main__":
  main()
