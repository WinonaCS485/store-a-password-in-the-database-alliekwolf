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


# Function searches for user within database
"""
def user_lookup(username, pwd):
    try:
        with connection.cursor() as cursor:
            sql_search = 'SELECT * FROM Passwords WHERE {username} = Username'
            
            # execute SQL command
            cursor.execute(sql_search)
            
            cursor.close()
            
    #if username == Passwords.username:
    #    salt = Passwords.Salt
    #    salted_pwd = salt + pwd
    #    hashed_pwd = str( hashlib.sha256(str.encode(salted_pwd)).hexdigest() )
    #    
    #    if hashed_pwd == Passwords.Hash:
    #        return TRUE
    #    else:
    #        return FALSE
    #else:
    #    return FALSE
"""


# MAIN PROGRAM

invalid_length_msg = '* Invalid password length. Password\n  must be at least 6 characters long\n  and no more than 30 characters.'

# Prompt user to create an account with username and password
print('--------------------------------\n'
      ' Create new account\n'
      '--------------------------------')

# This while loop gets input for new username
while True:
    username = input('Enter a new username: ')
    
    # search database for username availability
      # CHANGE TO something like, "if username exists in table:"
    if username != username:
        print('\n* Sorry, username is taken.\n')
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
hashed_password = str( hashlib.sha256(str.encode(password)).hexdigest() )

print(f'{salt}')
print(f'{salted_password}')
print(f'{hashed_password}\n')

print(f'** Welcome, {username}! **\n')


# Insert user data into Passwords Table

try:
    with connection.cursor() as cursor:
        sql_insert = 'INSERT INTO Passwords (Hash, Salt, Username) VALUES (%s, %s, %s);'
        sql_values = (hashed_password, salt, username)
        
        # Execute SQL command
        cursor.execute(sql_insert, sql_values)
        table = cursor.fetchall()
        
        connection.commit()
        
        for row in table:
            print(row)
        cursor.close()
        
finally:
    connection.close()


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
    
        if confirm_pwd != password:
            print('\n* Passwords do not match. Try again.')
        else:
            user_lookup(username, password)
            
            
            
            
    else:
        print(f'\n{invalid_length_msg}\n')



# END OF PROGRAM



        # If you INSERT, UPDATE or CREATE, the connection is not autocommit by default.
        # So you must commit to save your changes. 
        # connection.commit()
        



