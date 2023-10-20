import sqlite3

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