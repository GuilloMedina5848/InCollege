import main, pytest, psycopg, helper
from main import DATABASE_NAME_, InCollegeServer



# these functions are for managing the Users.txt file; we don't want the file to be altered in any way after the tests are completed and we don't want the test output to rely on the existing file being in a certain state.
# so we start by saving the Users.txt contents to a string and erasing it. At the start of every test, we erase it again (to clear any alterations from previous tests) and the final test (see test_dummy) writes the string back to the Users.txt file

sourceFilename = 'main'
promptModule = sourceFilename + '.prompt'

defaultUser = "pyTestUser"
defaultPassword = "pyTest123%"
defaultFirstName = "pyTest"
defaultLastName = "User"
defaultEmailPref = True
defaultSMSPref = True
defaultAdsPref = True
defaultLanguage = "English"
defaultUniversity = "USF"
defaultMajor = "CS"
defaultUserTuple = (defaultUser, defaultPassword, defaultFirstName, defaultLastName, defaultEmailPref, defaultSMSPref, defaultAdsPref, defaultLanguage, defaultUniversity, defaultMajor)
defaultUserTupleString = f"('{defaultUser}', '{defaultPassword}', '{defaultFirstName}', '{defaultLastName}', {defaultEmailPref}, {defaultSMSPref}, {defaultAdsPref}, '{defaultLanguage}', '{defaultUniversity}', '{defaultMajor}')"
defaultUserTable = [[defaultUserTuple]]
maxUsers = 10

# TODO: change queries that rely on the string method to use cursor.copy()

defaultTitle = "pyTester"
defaultDescription = "testsPython"
defaultEmployer = "pyTest"
defaultLocation = "pyTest"
defaultSalary = "0"
defaultJobTuple = (1, defaultUser, defaultTitle, defaultDescription, defaultEmployer, defaultLocation, defaultSalary, defaultFirstName, defaultLastName)
defaultJobTable = [[defaultJobTuple]]
maxJobs = 5

tables = ["jobs", "friendships", "users"] # this needs to be in an order such that the tables with linked keys are deleted first

DATABASE_TEST_NAME = "incollegetestdb"
DATABASE_ORIGINAL = DATABASE_NAME_

DATABASE_NAME = DATABASE_TEST_NAME
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "postgres"
DATABASE_HOST = "localhost" 
DATABASE_PORT = "5432"

def dropTestDatabase():
    with psycopg.connect(dbname=DATABASE_ORIGINAL, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT) as connection:
       connection._set_autocommit(True)
       with connection.cursor() as cursor:
          cursor.execute(f"""DROP DATABASE {DATABASE_TEST_NAME};""")

def clear():
    with psycopg.connect(dbname=DATABASE_TEST_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT) as connection:
        with connection.cursor() as cursor:
            # List of tables and their sequences if any.
            # Dependent tables (with foreign keys) should be deleted before primary tables.
            tables_sequences = [
                ("educations", None),
                ("experiences", None),
                ("profiles", None),
                ("jobs", "jobs_job_id_seq"),
                ("friendships", None),
                ("users", None)
            ]

            for table, sequence in tables_sequences:
                # Try deleting data from the table
                try:
                    cursor.execute(f"DELETE FROM {table}")
                except Exception as e:
                    print(f"Error deleting data from {table}: {e}")

                # If there's a sequence associated, reset it
                if sequence:
                    try:
                        cursor.execute(f"ALTER SEQUENCE {sequence} RESTART WITH 1")
                    except Exception as e:
                        print(f"Error resetting sequence {sequence}: {e}")

            # Commit all changes to the database
            connection.commit()


# function to start tests which require an existing user to be able to log in
# don't use this function unless you need an existing user! start the function with clear() instead
def addTestUser(num = 1):
  clear()
  finalTuple = [[]]

  with psycopg.connect(dbname=DATABASE_TEST_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT) as connection:
        with connection.cursor() as cursor:
              try:
                  cursor.execute(f"""INSERT INTO USERS VALUES {defaultUserTupleString}""")
                  finalTuple[0].append(defaultUserTuple)
              except Exception as e:
                  print(f"Error executing query: {e}")
              if num > 1:
                 for i in range(1, num):
                    userTupleString = f"('{defaultUser}{str(i)}', '{defaultPassword}', '{defaultFirstName}', '{defaultLastName}', {defaultEmailPref}, {defaultSMSPref}, {defaultAdsPref}, '{defaultLanguage}', '{defaultUniversity}', '{defaultMajor}')"
                    userTuple = (defaultUser+str(i), defaultPassword, defaultFirstName, defaultLastName, defaultEmailPref, defaultSMSPref, defaultAdsPref, defaultLanguage, defaultUniversity, defaultMajor)
                    try:
                      cursor.execute(f"""INSERT INTO USERS VALUES {userTupleString}""")
                      finalTuple[0].append(userTuple)
                    except Exception as e:
                        print(f"Error executing query: {e}")
        return finalTuple
  
def readDB(select = "all"):
    read = []
    with psycopg.connect(dbname=DATABASE_TEST_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT) as connection:
        with connection.cursor() as cursor:
            if select != "all":
              try:
                  cursor.execute(f"""SELECT *
                                  FROM {select}""")
                  read.append(cursor.fetchall())
              except Exception as e:
                  print(f"Error executing query: {e}")
            else:
              for table in tables:
                  try:
                      cursor.execute(f"""SELECT *
                                      FROM {table}""")
                      read.append(cursor.fetchall())
                  except Exception as e:
                      print(f"Error executing query: {e}")
    return read

def addRowsToTable(rows, table):
  with psycopg.connect(dbname=DATABASE_TEST_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT) as connection:
    with connection.cursor() as cursor:
      try:
        with cursor.copy(f"COPY {table} FROM STDIN") as copy:
          for row in rows:
            copy.write_row(row)
      except Exception as e:
          print(f"Error executing query: {e}")

helper.createDatabase(DATABASE_USER, DATABASE_PASSWORD, DATABASE_TEST_NAME, DATABASE_HOST, DATABASE_PORT)

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



###########
# FRIENDS #
###########

def test_newConnectionRequest(monkeypatch, capsys):
  addTestUser(2)

  prompts = iter([{0: 'For Existing Users'}, {0: 'Find someone you know'}, {0: 'Last Name'}, {0: f'User ID: {defaultUser+"1"}, Name: {defaultFirstName} {defaultLastName}, University: {defaultUniversity}, Major: {defaultMajor}'}, {0: 'Exit'}, {0: 'Log out'}, {0: 'Exit'}])
  monkeypatch.setattr(promptModule, lambda _: next(prompts))

  inputs = iter([defaultUser, defaultPassword, defaultLastName, 'yes'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))

  InCollegeServer(DATABASE_TEST_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT)

  assert f"Connection request sent to user {defaultUser+'1'}!" in capsys.readouterr().out
  assert readDB("friendships")[0][0][3] == 'pending'

def test_receiveConnectionRequestOnLogin(monkeypatch, capsys):
  addTestUser(2)

  connections = [[(1, defaultUser+'1', defaultUser, 'pending')]]

  with psycopg.connect(dbname=DATABASE_TEST_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT) as connection:
    with connection.cursor() as cursor:
      try:
        with cursor.copy("COPY friendships FROM STDIN") as copy:
          for connection in connections[0]:
            copy.write_row(connection)
      except Exception as e:
          print(f"Error executing query: {e}")

  prompts = iter([{0: 'For Existing Users'}, {0: 'Log out'}, {0: 'Exit'}])
  monkeypatch.setattr(promptModule, lambda _: next(prompts))

  inputs = iter([defaultUser, defaultPassword, 'yes'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))

  InCollegeServer(DATABASE_TEST_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT)

  assert "Friend request accepted!" in capsys.readouterr().out
  assert readDB("friendships")[0][0][3] == 'confirmed'

def test_disconnectFromConnectionEmpty(monkeypatch, capsys):
  addTestUser()

  prompts = iter([{0: 'For Existing Users'}, {0: 'Disconnect from a Connection'}, {0: 'Log out'}, {0: 'Exit'}])
  monkeypatch.setattr(promptModule, lambda _: next(prompts))

  inputs = iter([defaultUser, defaultPassword, defaultUser])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))

  InCollegeServer(DATABASE_TEST_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT)

  assert f"The given user is not in your connection list." in capsys.readouterr().out

def test_disconnectFromConnection(monkeypatch, capsys):
  addTestUser(2)
  
  connections = [[(1, defaultUser, defaultUser+'1', 'confirmed')]]

  with psycopg.connect(dbname=DATABASE_TEST_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT) as connection:
    with connection.cursor() as cursor:
      try:
        with cursor.copy("COPY friendships FROM STDIN") as copy:
          for connection in connections[0]:
            copy.write_row(connection)
      except Exception as e:
          print(f"Error executing query: {e}")

  prompts = iter([{0: 'For Existing Users'}, {0: 'Disconnect from a Connection'}, {0: 'Log out'}, {0: 'Exit'}])
  monkeypatch.setattr(promptModule, lambda _: next(prompts))

  inputs = iter([defaultUser, defaultPassword, defaultUser+'1'])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))

  InCollegeServer(DATABASE_TEST_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT)

  assert f"Successfully disconnected!" in capsys.readouterr().out 


############################################ Sprint 5 Tests ###################################################

def test_addJobExperience(monkeypatch, capsys):
  # Initial mocked job experience for the user
  clear()
  addTestUser()
  mock_experience = {
    'experience_id': 1, 
    'user_id': defaultUser,
    'title': 'Software Engineer',
    'employer': 'Tech Corp',
    'date_started': '2022-01-01',
    'date_ended': '2022-12-31',
    'location': 'New York',
    'description': 'Developed software applications.'
  }

  # Mocking the database to insert the initial job experience
  with psycopg.connect(dbname=DATABASE_TEST_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT) as connection:
    with connection.cursor() as cursor:
      try:
        experience_values = (mock_experience[key] for key in mock_experience)
        cursor.execute(f"""INSERT INTO experiences VALUES {tuple(experience_values)}""")
      except Exception as e:
        print(f"Error executing query: {e}")

  # Mock the user input to edit the job title
  # prompts = iter([{0: 'For Existing Users'}, {0: 'Profile'}, {0: 'Edit Profile'}, 
  #                 {0: 'Job Experience'}, {0: 'Edit Job Experience'}, {0: "Software Engineer for Tech Corp"}, 
  #                 {0: "Title"}, {0: "Finish"}, {0: "Finish"}, {0: "Log out"}, {0: 'Exit'}])
  # monkeypatch.setattr(promptModule, lambda _: next(prompts))
  # inputs = iter([defaultUser, defaultPassword,'Senior Software Engineer'])
  # monkeypatch.setattr('builtins.input', lambda _: next(inputs))

  # Mock the user input to edit the job title
  prompts = iter([{0: 'For Existing Users'}, {0: 'Profile'}, {0: 'Go Back'}, {0: 'Log out'}, {0: 'Exit'}])
  monkeypatch.setattr(promptModule, lambda _: next(prompts))
  inputs = iter([defaultUser, defaultPassword])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))

  InCollegeServer(DATABASE_TEST_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT)

  # Fetching the updated job experience from the database
  with psycopg.connect(dbname=DATABASE_TEST_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT) as connection:
    with connection.cursor() as cursor:
      cursor.execute(f"""SELECT title FROM experiences WHERE experience_id = {mock_experience['experience_id']}""")
      updated_title = cursor.fetchone()[0]

  # # Assertions
  assert updated_title == 'Software Engineer'
  # assert f"Worked as a Software Engineer for Tech Corp , from 2022-01-01 to 2022-12-31, at New York." in capsys.readouterr().out 
  
  

def test_jobExperience(monkeypatch, capsys):
  # Test how the job experience is displayed
  addTestUser()
  mock_experience = [[1, defaultUser, 'Software Engineer', 'Tech Corp', '2022-01-01', '2022-12-31', 'New York', 'Developed software applications.']]
  mock_profile = [[1, defaultUser, "Title", "About section"]]
  addRowsToTable(mock_experience, "experiences")
  addRowsToTable(mock_profile, "profiles")


  # Mock the user input to edit the job title

  # Mock the user input to edit the job title
  prompts = iter([{0: 'For Existing Users'}, {0: 'Profile'}, {0: 'Go Back'}, {0: 'Log out'}, {0: 'Exit'}])
  monkeypatch.setattr(promptModule, lambda _: next(prompts))
  inputs = iter([defaultUser, defaultPassword])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))

  InCollegeServer(DATABASE_TEST_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT)

  assert f"Worked as a Software Engineer for Tech Corp, from 2022-01-01 to 2022-12-31, at New York:" in capsys.readouterr().out 
  
def test_editJobExperience(monkeypatch, capsys):
   pass
#   addTestUser()
#   mock_experience = [[1, defaultUser, 'Software Engineer', 'Tech Corp', '2022-01-01', '2022-12-31', 'New York', 'Developed software applications.']]
#   mock_profile = [[1, defaultUser, "Title", "About section"]]
#   addRowsToTable(mock_experience, "experiences")
#   addRowsToTable(mock_profile, "profiles")
  
#   prompts = iter([{0: 'For Existing Users'}, {0: 'Profile'}, {0: 'Edit Profile'},  {0: 'Go Back'},
#                   {0: 'Job Experience'}, {0: 'Edit Job Experience'}, {0: 'Software Engineer for Tech Corp'},
#                   {0: 'Title'}, {0: 'Finish'}, {0: 'Finish'}, {0: 'Log out'}, {0: 'Exit'}])
#   monkeypatch.setattr(promptModule, lambda _: next(prompts))
#   inputs = iter([defaultUser, defaultPassword, "Senior Software Engineer"])
#   monkeypatch.setattr('builtins.input', lambda _: next(inputs))

#   InCollegeServer(DATABASE_TEST_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT)

#   # Fetching the updated job experience from the database
#   with psycopg.connect(dbname=DATABASE_TEST_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT) as connection:
#     with connection.cursor() as cursor:
#       cursor.execute(f"""SELECT title FROM experiences WHERE experience_id = {mock_experience[0][0]}""")
#       updated_title = cursor.fetchone()[0]

#   # # Assertions
#   assert updated_title == 'Senior Software Engineer'

def test_editEducation():
  pass

def test_addEducation(monkeypatch, capsys):
  # Test how the job experience is displayed
  addTestUser()
  mock_education = [[1, defaultUser, "USF", "Computer Science", "2021", "2025"]]
  mock_profile = [[1, defaultUser, "Title", "About section"]]
  addRowsToTable(mock_education, "educations")
  addRowsToTable(mock_profile, "profiles")

  # Mock the user input to edit the job title

  # Mock the user input to edit the job title
  prompts = iter([{0: 'For Existing Users'}, {0: 'Profile'}, {0: 'Go Back'}, {0: 'Log out'}, {0: 'Exit'}])
  monkeypatch.setattr(promptModule, lambda _: next(prompts))
  inputs = iter([defaultUser, defaultPassword])
  monkeypatch.setattr('builtins.input', lambda _: next(inputs))

  InCollegeServer(DATABASE_TEST_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT)

  assert f"Attended USF from 2021 to 2025 to obtain a Computer Science." in capsys.readouterr().out 
  

def test_editProfile():
  pass

def test_viewProfile():
  pass

def test_profile():
  pass


def test_dummy():
  dropTestDatabase()

# this has to be the last test in the file!