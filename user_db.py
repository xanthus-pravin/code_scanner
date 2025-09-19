import sqlite3

def check_user_credentials(username, password):
    """
    Securely checks user credentials against a database using parameterized queries.
    This function is safe from SQL injection attacks.
    """
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    
    # The SQL query uses '?' as placeholders for user-supplied values.
    # This separates the command (the SQL query) from the data (user input).
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    
    # The user input is passed as a separate tuple of arguments.
    # The database driver safely handles the values, preventing SQL injection.
    cursor.execute(query, (username, password))
    
    result = cursor.fetchone()
    db.close()
    
    return result is not None

# # vulnerable
# def check_user_credentials(username, password):
#     db = sqlite3.connect("users.db")
#     cursor = db.cursor()
    
#     # VULNERABILITY: The username is inserted directly into the query string.
#     # An attacker could use the username "' OR '1'='1" to log in as any user.
#     # testing asda tasasdasd sdsd as huuuh zxxsds asas sjsdjsdasdSsddasddsds  dsd
#     query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
#     cursor.execute(query)
    
#     result = cursor.fetchone()
#     return result is not None