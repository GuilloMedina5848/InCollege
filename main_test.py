from main import main
import pytest

# these functions are for managing the Users.txt file; we don't want the file to be altered in any way after the tests are completed and we don't want the test output to rely on the existing file being in a certain state.
# so we start by saving the Users.txt contents to a string and erasing it. At the start of every test, we erase it again (to clear any alterations from previous tests) and the final test (see test_dummy) writes the string back to the Users.txt file

copy = ""
defaultUser = "pyTestUser"
defaultPassword = "pyTest123%"
defaultFirstName = "pyTest"
defaultLastName = "User"
defaultUserString = f"1,{defaultUser},{defaultPassword},{defaultFirstName},{defaultLastName}\n"
maxUsers = 5

def userClear():
  open("Users.txt", "w").close(
  )  # opens the Users file in write mode, deleting its contents, then closes it


def userCut():
  global copy
  userFile = open("Users.txt", "r")
  copy = userFile.read(
  )  # make a copy of the file contents to rewrite to the file after the test is completed
  userFile.close()
  userClear()


def userPaste():
  userFile = open("Users.txt", "w")
  userFile.write(copy)
  userFile.close()


# function to start tests which require an existing user to be able to log in
# don't use this function unless you need an existing user! start the function with userClear() instead
def startTest():
  userClear()
  open("Users.txt", "w").write(defaultUserString)

userCut()  # program starts by saving a copy of the existing Users.txt file to be copied back later

###########
## TESTS ##
###########

# note that many of the inputs for these tests will look similar
# this is because we have to get the program to terminate to test the output stream; this is only possible by logging out in most cases

# pyTest basics:
# the file name MUST be "{filename}_test.py"
# each function to be executed by pyTest MUST begin with "test"
# pyTest will execute each such function itself; they do not need to (and should not) be called
# every pyTest function is basically a compound AND statement that each assert statement is true (which means that a pyTest with no assert statements will always pass!)

# 'monkeypatch' and 'capsys' are python fixtures; to use them they need to be included as function parameters
# monkeypatch is used to override functions - we can tell python to skip a function's normal behavior and return what we tell it to instead
# this is used for keyboard input (the input() builtin) and for prompt selection (InquirerPy's prompt() )
# capsys is used to capture the stdout stream
# capsys.readouterr() captures (and consumes) the current stdout and stderr streams
# we only care about the stdout stream (the print statements we want to look at), which we get with the .out object (which gives us a string)
# the .split('\n') string method changes the string into a list of strings separated by the newline character ("This is an example".split(' ') returns ['This', 'is', 'an', 'example'])
# finally, we use array subscripting to get the output string we're looking for. In most cases I've used the second-to-last string (the last string is empty), which should be "Logging out." for most test cases
# but we can target any string, so for example we can assert that the nth string will be "All permitted accounts have been created..." for a test case that tests the 5 user limit functionality


# tests if the main screen exits correctly
def test_mainScreen(monkeypatch, capsys):
  userClear()

  prompts = iter([{0: 'Exit'}])
  monkeypatch.setattr('main.prompt', lambda _: next(prompts))

  main()

  captured_output = capsys.readouterr().out
  assert captured_output.split('\n')[-2] == "Thank you, bye!"

# tests if the main screen prints the success story
def test_mainScreenStory(monkeypatch, capsys):
  userClear()

  prompts = iter([{0: 'Exit'}])
  monkeypatch.setattr('main.prompt', lambda _: next(prompts))

  main()

  captured_output = capsys.readouterr().out
  assert "When I first started college" in captured_output

# tests if the 'learn why you should join inCollege' option prints correctly
def test_mainScreenVideo(monkeypatch, capsys):
  userClear()

  prompts = iter([{0: 'Learn why you should join inCollege'}, {0: 'Exit'}])
  monkeypatch.setattr('main.prompt', lambda _: next(prompts))

  main()

  captured_output = capsys.readouterr().out
  assert "Video is now playing" in captured_output

# tests main screen existing user search
def test_mainScreenSearchUser(monkeypatch, capsys):
  startTest()

  prompts = iter([{0: 'Search for an existing user of inCollege'}, {0: 'Exit'}])
  monkeypatch.setattr('main.prompt', lambda _: next(prompts))

  inputs = iter([defaultFirstName, defaultLastName])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))

  main()

  assert "They are a part of the InCollege system." in capsys.readouterr().out

# tests main screen existing user search with name that is not registered with inCollege
def test_mainScreenSearchInvalidUser(monkeypatch, capsys):
  startTest()

  testNames = [["User", "pyTest"], ["pyTest", ""], ["", "User"], ["", ""]]

  for testName in testNames:

    prompts = iter([{0: 'Search for an existing user of inCollege'}, {0: 'Exit'}])
    monkeypatch.setattr('main.prompt', lambda _: next(prompts))

    inputs = iter([testName[0], testName[1]])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()

    assert "They are not yet a part of the InCollege system yet." in capsys.readouterr().out

# tests new user creation with valid username/password
def test_newUser(monkeypatch, capsys):
  userClear()

  testUsernamesPasswords = [["pyTestUser", "pyTest123%"],
                            ["pyTestUser2", "PYTEST123!"],
                            ["thisIsALongTestStringPyTestUser3", "1aBcd&&&&"],
                            ["4", "999ZZZZ^"], ["b", "kOp0`-2fwe"]]

  users = ""
  i = 1

  for testUsernamePassword in testUsernamesPasswords:

    prompts = iter([{0: 'To Create an Account'}, {0: 'Log out'}])
    monkeypatch.setattr('main.prompt', lambda _: next(prompts))

    inputs = iter([testUsernamePassword[0], testUsernamePassword[1], defaultFirstName, defaultLastName])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()
    assert capsys.readouterr().out.split('\n')[-2] == "Logging out."
    users += f"{str(i)},{testUsernamePassword[0]},{testUsernamePassword[1]},{defaultFirstName},{defaultLastName}\n"
    assert open("Users.txt", "r").read() == users
    i += 1

# tests new user creation with invalid password due to character requirements
def test_newUserInvalidCharacter(monkeypatch, capsys):
  userClear()

  testPasswords = [
      "pytest123%", "PYTEST123", "aBcd&&&&", "999ZZZZ", "kop0`-2fwe"
  ]

  for testPassword in testPasswords:

    prompts = iter([{0: 'To Create an Account'}, {0: 'Log out'}])
    monkeypatch.setattr('main.prompt', lambda _: next(prompts))

    inputs = iter(
        [defaultUser, testPassword, defaultFirstName, defaultLastName, defaultUser, defaultPassword, defaultFirstName, defaultLastName])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()

    assert "Your username is already taken or the password doesn't meet requirements. Please start over" in capsys.readouterr().out
    assert open("Users.txt", "r").read() == defaultUserString
    userClear()

# test new user creation with invalid password due to length requirements
def test_newUserInvalidLength(monkeypatch, capsys):
  userClear()

  testPasswords = ["pyTes7!", "pyTest13!!!!!", "pyTestVeryLongPassword!"]

  for testPassword in testPasswords:
    # simulate inputs: choose to create an account, provide a username and the test password, then provide a valid username and password combo to terminate the program

    prompts = iter([{0: 'To Create an Account'}, {0: 'Log out'}])
    monkeypatch.setattr('main.prompt', lambda _: next(prompts))

    inputs = iter([defaultUser, testPassword, defaultFirstName, defaultLastName, defaultUser, defaultPassword, defaultFirstName, defaultLastName])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()

    # test if the output informs the user of the invalid password
    assert "Your username is already taken or the password doesn't meet requirements. Please start over" in capsys.readouterr().out

    # make sure no new users were added to the Users.txt file with invalid input
    assert open("Users.txt", "r").read() == defaultUserString
    userClear()

# tests new user creation with existing username
# kind of an inelegant implementation but works
def test_newUserInvalidExisting(monkeypatch, capsys):
  userClear()

  testUsernames = [
      "pyTestUser1", "pyTestUser2", "thisIsALongTestStringPyTestUser3", "4"
  ]

  users = ""
  i = 1

  for testUsername in testUsernames:
    users += str(i) + ',' + testUsername + ',' + defaultPassword + ',' + defaultFirstName + ',' + defaultLastName + '\n'
    i += 1

  file = open("Users.txt", "w")
  file.write(users)
  file.close()

  for testUsername in testUsernames:

    prompts = iter([{0: 'To Create an Account'}, {0: 'Log out'}])
    monkeypatch.setattr('main.prompt', lambda _: next(prompts))

    inputs = iter([testUsername, defaultPassword, defaultFirstName, defaultLastName, defaultUser, defaultPassword, defaultFirstName, defaultLastName])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()
    assert capsys.readouterr().out.split('\n')[-2] == "Logging out."
    assert open("Users.txt", "r").read() == users + f"{str(i)},{defaultUser},{defaultPassword},{defaultFirstName},{defaultLastName}\n"
    file = open("Users.txt", "w")
    file.write(users)
    file.close()

# tests new user creation with maximum number of users
def test_newUserExceedsLimit(monkeypatch, capsys):
  userClear()

  # fill Users.txt with the maximum number of users
  with open("Users.txt", "w") as file:
    file.write(defaultUserString)
    for i in range(2,maxUsers+1):
      file.write(f"{i},{defaultUser}{i},{defaultPassword},{defaultFirstName},{defaultLastName}\n")

  # create the 6th account
  prompts = iter([{0: 'To Create an Account'}, {0: 'For Existing Users'}, {0: 'Log out'}])
  monkeypatch.setattr('main.prompt', lambda _: next(prompts))

  inputs = iter([defaultUser, defaultPassword])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
  main()

  # Check if the expected error message is displayed to the user
  captured_output = capsys.readouterr().out
  assert "All permitted accounts have been created, please come back later" in captured_output
    
  # Check if the new user was not added to the Users.txt file
  with open("Users.txt", "r") as file:
    users = file.readlines()
    assert len(users) == maxUsers # Ensure there are only 5 users in the file

# tests existing user login with valid username/password
def test_loginExistingUser(monkeypatch, capsys):
  userClear()

  testUsernamesPasswords = [["pyTestUser", "pytest123%"],
                            ["pyTestUser2", "PYTEST123"],
                            ["thisIsALongTestStringPyTestUser3", "aBcd&&&&"],
                            ["4", "999ZZZZ"], ["b", "kop0`-2fwe"]]

  users = ""
  i = 1

  for testUsernamePassword in testUsernamesPasswords:
    users += f"{str(i)},{testUsernamePassword[0]},{testUsernamePassword[1]},{defaultFirstName},{defaultLastName}\n"
    i += 1

  file = open("Users.txt", "w")
  file.write(users)
  file.close()

  for testUsernamePassword in testUsernamesPasswords:

    prompts = iter([{0: 'For Existing Users'}, {0: 'Log out'}])
    monkeypatch.setattr('main.prompt', lambda _: next(prompts))

    inputs = iter([testUsernamePassword[0], testUsernamePassword[1], defaultFirstName, defaultLastName])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()
    assert capsys.readouterr().out.split('\n')[-2] == "Logging out."
    assert open("Users.txt", "r").read() == users

# tests login attempt with invalid username.
def test_loginInvalidUsername(monkeypatch, capsys):
  startTest()
  
  testUsernames = ["pytestuser", "PYTESTUSER", "invaliduser", "1234567", ""]

  for testUsername in testUsernames:

    prompts = iter([{0: 'For Existing Users'}, {0: 'Log out'}])
    monkeypatch.setattr('main.prompt', lambda _: next(prompts))

    inputs = iter([testUsername, defaultPassword, defaultUser, defaultPassword])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()

    captured_output = capsys.readouterr().out
    assert "\nIncorrect username / password, please try again\n" in captured_output

# tests login attempt with valid username but incorrect password
def test_loginInvalidPassword(monkeypatch, capsys):
  startTest()
  
  testPasswords = ["pyTest123", "pytest123%", "PYTEST123%", "pyTest12%", ""]

  for testPassword in testPasswords:

    prompts = iter([{0: 'For Existing Users'}, {0: 'Log out'}])
    monkeypatch.setattr('main.prompt', lambda _: next(prompts))

    inputs = iter([defaultUser, "invalidPassword%", defaultUser, defaultPassword])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()

    captured_output = capsys.readouterr().out
    assert "\nIncorrect username / password, please try again\n" in captured_output

# tests the search user function
def test_searchUser(monkeypatch, capsys):
  startTest()

  prompts = iter([{0: 'For Existing Users'}, {0: 'Find someone you know'}, {0: 'Log out'}])
  monkeypatch.setattr('main.prompt', lambda _: next(prompts))

  inputs = iter([defaultUser, defaultPassword, defaultFirstName, defaultLastName])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))

  main()

  assert "They are a part of the InCollege system." in capsys.readouterr().out

# tests the search user function with a name that is not registered with inCollege
def test_searchInvalidUser(monkeypatch, capsys):
  startTest()

  testNames = [["User", "pyTest"], ["pyTest", ""], ["", "User"], ["", ""]]

  for testName in testNames:

    prompts = iter([{0: 'For Existing Users'}, {0: 'Find someone you know'}, {0: 'Log out'}])
    monkeypatch.setattr('main.prompt', lambda _: next(prompts))

    inputs = iter([defaultUser, defaultPassword, testName[0], testName[1]])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()

    assert "They are not yet a part of the InCollege system yet." in capsys.readouterr().out

# tests the search job feature
def test_searchJob(monkeypatch, capsys):
  startTest()

  prompts = iter([{0: 'For Existing Users'}, {0: 'Search for a Job'}, {0: 'Log out'}])
  monkeypatch.setattr('main.prompt', lambda _: next(prompts))

  inputs = iter([defaultUser, defaultPassword])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))

  main()

  assert capsys.readouterr().out.split('\n')[-2] == "Logging out."

# tests the search skill feature
def test_searchSkill(monkeypatch, capsys):
  startTest()

  skills = ['Team Work', 'Clean Code', 'Customer Service', 'Marketing', 'Management']

  for skill in skills:

    prompts = iter([{0: 'For Existing Users'}, {0: 'Learn a new skill'}, {0: skill}, {0: 'Return to the main menu'}, {0: 'Log out'}])
    monkeypatch.setattr('main.prompt', lambda _: next(prompts))

    inputs = iter([defaultUser, defaultPassword])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()

    assert capsys.readouterr().out.split('\n')[-2] == "Logging out."

# workaround for pytest terminating after the last test function; userPaste needs to be called to recover the original data in Users.txt

def test_dummy():
  userPaste()

# this has to be the last test in the file!
