import sqlite3

# Valid test cases
valid_tests = [
    ["Emilio_Ordonez123","P@ssw0rd_456"],
    ["Chandler_Wright456", "Ch@ndler_789"],
    ["DylanRuppell_42","Dyl@n123_Rp"],
    ["John_Stennett87","J0hnSt3nnet_!"],
    ["Alex_Calva_555","Al3x_Calva_123"]
]

comment_attack_tests = [
    # The first 3 tests assume the username is known
    ["Emilio_Ordonez123'; -- ","doesntmatter"],
    ["Chandler_Wright456'; -- ", "itsnullanyway"],
    ["DylanRuppell_42'; -- ","nothingspecial"],
    # This test will check to see if 'Admin' is a valid username
    ["Admin'; -- ","thiswillbeignored"],
    # This test will search for the Root user, part of all SQL databases
    ["Root'; -- ","thanksfortheaccess"]
]

union_query_attack_tests = [
    # Pull a list of passwords
    ["Emilio_Ordonez123","password' UNION SELECT password FROM users"],
    # Pull a list of usernames
    ["Chandler_Wright456", "unimportant' UNION SELECT username FROM users"],
    # Pull a list of usernames and passwords, put together for easier use
    ["DylanRuppell_42","test' UNION SELECT concat(username, password) FROM users"],
    # This Union Query would help the attacker identify the name of the database, which will aid in other attacks
    ["John_Stennett87","weak' UNION SELECT schema_name FROM information_schema.schemata"],
    # This Union Query would add a username and password to the database
    ["Alex_Calva_555","helloworld' UNION INSERT INTO users (username, password) VALUES ('HackerUsername', 'HackedYou428!')"]
]

# Function to create the SQL query (vulnerable)
def generate_query(username, password):
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    return query

# Function to test the different test cases
def test_case(username, password):
    query = generate_query(username, password)
    print(f"Username: {username}, Password: {password}")
    print(f"Generated Query: {query}")
    print()

# Function for a tautology attack
def tautology_attack(username, password):
    tautology_query = f"' OR '1'='1"
    test_case(username, tautology_query)

# Function for a union query attack
def union_query_attack(username, password):
    union_query = f"' UNION SELECT null, password FROM users--"
    test_case(username, union_query)

# Function for a additional statement attack
def additional_statement_attack(username, password):
    additional_statement_query = "'; DELETE FROM users--"
    test_case(username, additional_statement_query)

# Function for a comment attack
def comment_attack(username, password):
    comment_query = "' OR 1=1 --"
    test_case(username, comment_query)

# Function for a weak mitigation
def weak_mitigation(input_str):
    return input_str.replace("'", "''")

# Function for a strong mitigation (utilizando SQLite)
def strong_mitigation(username, password):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    
    connection.close()
    return result
def show_database():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    connection.close()
    return result

# Main function with menu
def main():
    print("SQL Injection Testing Program")
    print("1. Test Valid Input")
    print("2. Tautology Attack")
    print("3. Union Query Attack")
    print("4. Additional Statement Attack")
    print("5. Comment Attack")
    print("6. Weak Mitigation")
    print("7. Strong Mitigation (SQLite)")
    print("8. Show database users")
    print("9. Exit")

    while True:
        choice = input("Select an option: ")
        if choice == '1':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            test_case(username, password)
        elif choice == '2':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            tautology_attack(username, password)
        elif choice == '3':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            union_query_attack(username, password)
        elif choice == '4':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            additional_statement_attack(username, password)
        elif choice == '5':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            comment_attack(username, password)
        elif choice == '6':
            input_str = input("Enter a string: ")
            sanitized_input = weak_mitigation(input_str)
            print(f"Sanitized Input: {sanitized_input}")
        elif choice == '7':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            result = strong_mitigation(username, password)
            if result:
                print("Authentication successful.")
            else:
                print("Authentication failed.")
        elif choice == '8':
            result = show_database()
            print(result)
        elif choice == '9':
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()