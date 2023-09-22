from main import main
import pytest

# these functions are for managing the Users.txt file; we don't want the file to be altered in any way after the tests are completed and we don't want the test output to rely on the existing file being in a certain state.

# so we start by saving the Users.txt contents to a string and erasing it. At the start of every test, we erase it again (to clear any alterations from previous tests) and the final test (see test_dummy) writes the string back to the Users.txt file

copy = ""


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
  open("Users.txt", "w").write("1,pyTestUser,pyTest123%")


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
# monkeypatch is used to mock keyboard input to the console
# capsys is used to capture the stdout stream
# capsys.readouterr() captures (and consumes) the current stdout and stderr streams
# we only care about the stdout stream (the print statements we want to look at), which we get with the .out object (which gives us a string)
# the .split('\n') string method changes the string into a list of strings separated by the newline character ("This is an example".split(' ') returns ['This', 'is', 'an', 'example'])
# finally, we use array subscripting to get the output string we're looking for. In most cases I've used the second-to-last string (the last string is empty), which should be "Logging out." for most test cases
# but we can target any string, so for example we can assert that the nth string will be "All permitted accounts have been created..." for a test case that tests the 5 user limit functionality


# tests if the main screen is correctly display, and if user can create an account and log out
def test_mainScreen(monkeypatch, capsys):
  userClear()

  inputs = iter(['2', 'pyTestUser', 'pyTest123%', '4'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))

  main()

  assert capsys.readouterr().out.split('\n')[-2] == "Logging out."


# tests the main screen for inputs out of range [1,2]
def test_mainScreenRange(monkeypatch, capsys):
  startTest()

  testInts = [3, -1, 999999, 200, -999999]

  for testInt in testInts:

    inputs = iter([testInt, '1', 'pyTestUser', 'pyTest123%', '4'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()

    assert capsys.readouterr().out.split(
        '\n')[9] == "Your input was incorrect. Please input a correct value."
    assert open("Users.txt", "r").read() == "1,pyTestUser,pyTest123%"


# tests the main screen for char inputs
def test_mainScreenChar(monkeypatch, capsys):
  startTest()

  testChars = ['a', 'b', '\n', '#', '.']

  for testChar in testChars:

    inputs = iter([testChar, '1', 'pyTestUser', 'pyTest123%', '4'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()

    assert capsys.readouterr().out.split(
        '\n')[9] == "Your input was incorrect. Please input a correct value."
    assert open("Users.txt", "r").read() == "1,pyTestUser,pyTest123%"


# tests the main screen for float inputs
def test_mainScreenFloat(monkeypatch, capsys):
  startTest()

  testFloats = [1.01, 2.00, -1.0101, .43252, -934.123456]

  for testFloat in testFloats:

    inputs = iter([testFloat, '1', 'pyTestUser', 'pyTest123%', '4'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()

    assert capsys.readouterr().out.split(
        '\n')[9] == "Your input was incorrect. Please input a correct value."
    assert open("Users.txt", "r").read() == "1,pyTestUser,pyTest123%"


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

    inputs = iter(["2", testUsernamePassword[0], testUsernamePassword[1], "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()
    assert capsys.readouterr().out.split('\n')[-2] == "Logging out."
    users += str(i) + ',' + testUsernamePassword[
        0] + ',' + testUsernamePassword[1] + '\n'
    assert open("Users.txt", "r").read() == users
    i += 1


# tests new user creation with invalid password due to character requirements
def test_newUserInvalidCharacter(monkeypatch, capsys):
  userClear()

  testPasswords = [
      "pytest123%", "PYTEST123", "aBcd&&&&", "999ZZZZ", "kop0`-2fwe"
  ]

  for testPassword in testPasswords:
    inputs = iter(
        ["2", "pyTestUser", testPassword, "pyTestUser", "pyTest123%", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()

    assert capsys.readouterr().out.split(
        '\n'
    )[19] == "Your username is already taken or the password doesn't meet requirements. Please start over"
    assert open("Users.txt", "r").read() == "1,pyTestUser,pyTest123%\n"
    userClear()


# test new user creation with invalid password due to length requirements
def test_newUserInvalidLength(monkeypatch, capsys):
  userClear()

  testPasswords = ["pyTes7!", "pyTest13!!!!!", "pyTestVeryLongPassword!"]

  for testPassword in testPasswords:
    # simulate inputs: choose to create an account, provide a username and the test password, then provide a valid username and password combo to terminate the program
    inputs = iter(
        ["2", "testUser", testPassword, "pyTestUser", "pyTest123%", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()

    # test if the output informs the user of the invalid password
    assert capsys.readouterr().out.split(
        '\n'
    )[19] == "Your username is already taken or the password doesn't meet requirements. Please start over"

    # make sure no new users were added to the Users.txt file with invalid input
    assert open("Users.txt", "r").read() == "1,pyTestUser,pyTest123%\n"
    userClear()


# tests new user creation with existing username
# kind of an inelegant implementation but works
def test_newUserInvalidExisting(monkeypatch, capsys):
  userClear()

  testUsernames = [
      "pyTestUser", "pyTestUser2", "thisIsALongTestStringPyTestUser3", "4"
  ]

  users = ""
  i = 1

  for testUsername in testUsernames:
    users += str(i) + ',' + testUsername + ',' + "pyTest123%" + '\n'
    i += 1

  file = open("Users.txt", "w")
  file.write(users)
  file.close()

  for testUsername in testUsernames:
    inputs = iter([
        "2", testUsername, "pyTest123%", "terminationUser", "pyTest123%", "4"
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()
    assert capsys.readouterr().out.split('\n')[-2] == "Logging out."
    assert open("Users.txt", "r").read(
    ) == users + str(i) + ',' + "terminationUser" + ',' + "pyTest123%" + '\n'
    file = open("Users.txt", "w")
    file.write(users)
    file.close()


# tests new user creation with maximum number of users
def test_newUserExceedsLimit(monkeypatch, capsys):
  userClear()
  # fill Users.txt with 5 users
  with open("Users.txt", "w") as file:
    for i in range (5):
      file.write(f"{i},pyTestUser{i},password{i}%\n")

  # create the 6th account
  inputs = iter(["2", "1", "pyTestUser1", "password1%", "4"])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
  main()

  # Check if the expected error message is displayed to the user
  captured_output = capsys.readouterr().out
  assert "All permitted accounts have been created, please come back later" in captured_output
    
  # Check if the new user was not added to the Users.txt file
  with open("Users.txt", "r") as file:
    users = file.readlines()
    assert len(users) == 5  # Ensure there are only 5 users in the file

 

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
    users += str(i) + ',' + testUsernamePassword[
        0] + ',' + testUsernamePassword[1] + '\n'
    i += 1

  file = open("Users.txt", "w")
  file.write(users)
  file.close()

  for testUsernamePassword in testUsernamesPasswords:
    inputs = iter(["1", testUsernamePassword[0], testUsernamePassword[1], "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()
    assert capsys.readouterr().out.split('\n')[-2] == "Logging out."
    assert open("Users.txt", "r").read() == users


# tests login attempt with invalid username.
def test_loginInvalidUsername(monkeypatch, capsys):
  userClear()
  # Add a known user
  with open("Users.txt", "w") as file:
    file.write("1,knownUser,knownPassword%\n")
  
  inputs = iter(["1", "invalidUser", "knownPassword%", "knownUser", "knownPassword%", "4"])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))

  main()

  captured_output = capsys.readouterr().out
  assert "\nIncorrect username / password, please try again\n" in captured_output



# tests login attempt with valid username but incorrect password
def test_loginInvalidPassword(monkeypatch, capsys):
  userClear()
  
  # Add a known user
  with open("Users.txt", "w") as file:
    file.write("1,knownUser,knownPassword%\n")
 
  inputs = iter(["1", "knownUser", "invalidPassword%", "knownUser", "knownPassword%", "4"])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))

  main()

  captured_output = capsys.readouterr().out
  assert "\nIncorrect username / password, please try again\n" in captured_output


# tests the search user function
def test_searchUser(monkeypatch, capsys):
  startTest()

  inputs = iter(["1", "pyTestUser", "pyTest123%", "1", "4"])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))

  main()

  assert capsys.readouterr().out.split('\n')[-2] == "Logging out."


# tests the search job feature
def test_searchJob(monkeypatch, capsys):
  startTest()

  inputs = iter(["1", "pyTestUser", "pyTest123%", "2", "4"])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))

  main()

  assert capsys.readouterr().out.split('\n')[-2] == "Logging out."


# tests the search skill feature
def test_searchSkill(monkeypatch, capsys):
  startTest()

  for i in range(1, 5):

    inputs = iter(['1', 'pyTestUser', 'pyTest123%', '3', i, '6', '4'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()

    assert capsys.readouterr().out.split('\n')[-2] == "Logging out."


# workaround for pytest terminating after the last test function; userPaste needs to be called to recover the original data in Users.txt


def test_dummy():
  userPaste()


# this has to be the last test in the file!
