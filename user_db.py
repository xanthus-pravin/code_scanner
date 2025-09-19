import sqlite3

def check_user_credentials(username, password):
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    
    # VULNERABILITY: The username is inserted directly into the query string.
    # An attacker could use the username "' OR '1'='1" to log in as any user.
    # testing asda tasasdasd sdsd as huuuh zxxsds asas sjsdjsdj asdasdS
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    result = cursor.fetchone()
    return result is not None