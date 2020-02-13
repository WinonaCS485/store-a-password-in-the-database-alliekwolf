import pymysql.cursors
import uuid
import hashlib

# Connect to the database
connection = pymysql.connect(host='mrbartucz.com',
                             user='nn4263xb',
                             passwd='G00d4Gr34t!!!4',
                             db='nn4263xb_Passwords',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



# METHOD searches to see if username is avaialable; returns True or False
def username_availability(username):
    
    result = False    # <-- result initialized to False
    
    try:
        with connection.cursor() as cursor:
            
            sql_search = f'SELECT * FROM Passwords WHERE Username = %s'
            
            cursor.execute(sql_search, username)
            record = cursor.fetchall()
            
            # If no record has been found, username is available; return True.
            if not record:
                result = True
                cursor.close()
            # Otherwise, if record HAS been found, username is unavailable; return False.
            else:
                result = False
            
            return result
            
    except:
        connection.close()

# END METHOD



# METHOD to insert user data into Passwords Table
def add_user(hashed_pwd, salt, username):
    try:
        with connection.cursor() as cursor:
            sql_insert = 'INSERT INTO Passwords (Hash, Salt, Username) VALUES (%s, %s, %s);'
            sql_values = (hashed_pwd, salt, username)
            
            # Execute SQL command and commit changes
            cursor.execute(sql_insert, sql_values)
            connection.commit()
            
            cursor.close()
    except:
        connection.close()

# END METHOD



# METHOD searches for user within database; returns True or False
def enter_password(username, pwd):
    
    result = False    # <-- result initialized to False
    
    try:
        with connection.cursor() as cursor:
            
            sql_search = f'SELECT * FROM Passwords WHERE Username = %s'
            
            # execute SQL command
            cursor.execute(sql_search, username)
            records = cursor.fetchall()
            
            for row in records:
                usr = row['Username']
                slt = row['Salt']
                hsh = row['Hash']
            
            # If a username is not found, return False
            if not cursor.rowcount:
                result = False
            
            # Otherwise, if user has been found...
            else:
                slt_pwd = slt + pwd
                hsh_pwd = str( hashlib.sha256(str.encode(slt_pwd)).hexdigest() )
                
                # If hashed password == stored hash, then login was successful.
                if hsh_pwd == hsh:
                    # Result = True; print user info
                    result = True
                    for row in records:
                        usr = row['Username']
                        slt = row['Salt']
                        hsh = row['Hash']
                        print(f'Username: {usr}')
                        print(f'Salt: {slt}')
                        print(f'Hash: {hsh}')
                        
                    cursor.close()    # <-- Successful search; close cursor and go to return statement.
                    
                # If hashes do not match, then login was unsuccessful.
                else:
                    result = False
                
            # End if/else statements
            
            return result    # <-- Return result either True or False
            
    except:
        connection.close()

# END METHOD



# MAIN PROGRAM

invalid_length_msg = '** Invalid password length. Password \n   must be at least 6 characters long\n   and no more than 30 characters.    **'

# Prompt user to create an account with username and password
print('--------------------------------\n'
      ' Create new account\n'
      '--------------------------------')

# This while loop gets input for new username
while True:
    username = input('Enter a new username: ')
    
    # search database for username availability
    available = username_availability(username)
    
    if not available:
        print('\n** Sorry, username is taken. **\n')
    else:
        break

while True:
    password = input('Enter a new password: ')
    print()
    
    if len(password) >= 6 and len(password) <= 30:
        break
    else:
        print(f'{invalid_length_msg}\n')

# Generate salt, add to password, and hash
salt = str(uuid.uuid4())
salted_password = salt + password
hashed_password = str( hashlib.sha256(str.encode(salted_password)).hexdigest() )

# Print new user information
print(f'Username: {username}')
print(f'Salt: {salt}')
print(f'Salt + Password: {salted_password}')
print(f'Hash: {hashed_password}\n')

# Insert user data into Passwords Table
add_user(hashed_password, salt, username)

"""
try:
    with connection.cursor() as cursor:
        sql_insert = 'INSERT INTO Passwords (Hash, Salt, Username) VALUES (%s, %s, %s);'
        sql_values = (hashed_password, salt, username)
        
        # Execute SQL command and commit changes
        cursor.execute(sql_insert, sql_values)
        connection.commit()
        
        cursor.close()
        
except:
    connection.close()
"""


print(f'** Welcome, {username}! **\n')



# Prompt user to login with their newly created account
print('--------------------------------\n'
      ' Login\n'
      '--------------------------------')

while True:
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    
    if len(password) >= 6 and len(password) <= 30:
        confirm_pwd = input('Confirm password: ')
        print()
        
        # If password confirmation unsuccessful, print message and loop back to ask again.
        if confirm_pwd != password:
            print('** Passwords do not match. Try again. **\n')
        
        # Otherwise, if passwords match, look up user in database.
        else:
            # Call enter_password method to find user
            result = enter_password(username, password)
            
            # If result from enter_password() method == False, user not found.
            if result == False:
                print('** Sorry, user not found. **\n')
            # Otherwise, user was found.
            else:
                print(f'\n** Welcome back, {username}! **\n')
                break
    # Otherwise, if password was an invalid length...
    else:
        print(f'\n{invalid_length_msg}\n')


# Close connection to database
connection.close()


# END OF PROGRAM

