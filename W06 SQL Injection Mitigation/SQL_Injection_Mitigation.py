import re

def testValid(function):
    '''Runs a set of test cases that represents valid input through the function passed as parameter.'''

    # Valid test cases [USERNAME, PASSWORD]
    valid_tests = [
        ["Emilio_Ordonez123","P@ssw0rd_456"],
        ["Chandler_Wright456", "Ch@ndler_789"],
        ["DylanRuppell_42","Dyl@n123_Rp"],
        ["John_Stennett87","J0hnSt3nnet_!"],
        ["Alex_Calva_555","Al3x_Calva_123"]
    ]

    print()
    print("Valid Input Test Cases:")
    print()
    counter = 1
    for test in valid_tests:
        query = function(test[0],test[1])
        print(f'{counter}. USERNAME: {test[0]}    PASSWORD: {test[1]}')
        print(f'   RESULTING QUERY: {query}\n')
        counter += 1

def testTautology(function):
    '''Runs a set of test cases that represents tautology attacks through the function passed as parameter.'''

    # Tautology test cases [USERNAME, PASSWORD]
    tautology_test = [
        ["Emilio_Ordonez123' OR '1'='1","P@ssw0rd_456"],
        ["Chandler_Wright456' OR 'x'='x","Ch@ndler_789"],
        ["DylanRuppell_42' OR 'a'='a","Dyl@n123_Rp"],
        ["John_Stennett87","' OR '2'='2"],
        ["Alex_Calva_555","' OR 'x'='x"]
    ]

    print()
    print("Tautology Attack Test Cases:")
    print()
    counter = 1
    for test in tautology_test:
        query = function(test[0], test[1])
        print(f'{counter}. USERNAME: {test[0]}    PASSWORD: {test[1]}')
        print(f'   RESULTING QUERY: {query}\n')
        counter += 1

def testAddState(function):
    '''Runs a set of test cases that represents additional statements attacks through the function passed as a parameter.'''
    
    # Additional statement cases [USERNAME, PASSWORD]
    add_statement_tests = [
        ["Emilio_Ordonez123", "pass'; INSERT INTO users (username, password) VALUES 'Mike', '1234"],
        ["Chandler_Wright456","pass'; INSERT INTO users (username, password) VALUES 'Jason', '1234"],
        ["DylanRuppell_42", "pass'; DELETE users"],
        ["John_Stennet87", "pass'; DELETE users WHERE username = 'EmilioOrdonez123"],
        ["Alex_Calva_555", "pass'; DELETE users WHERE username = 'DylanRuppell_42"]
    ]

    print()
    print("Additional Statement Attack Test Cases:")
    print()
    counter = 1
    for test in add_statement_tests:
        query = function(test[0], test[1])
        print(f'{counter}. USERNAME: {test[0]}    PASSWORD: {test[1]}') 
        print(f'    RESULTING QUERY: {query}\n')
        counter += 1

def testComment(function):
    '''Runs a set of test cases that represents comment attacks through the function passed as a parameter.'''

    comment_attack_tests = [
        # The first 3 tests assume the username is known by the attacker
        ["Emilio_Ordonez123'; -- ","doesntmatter"],
        ["Chandler_Wright456'; -- ", "itsnullanyway"],
        ["DylanRuppell_42'; -- ","nothingspecial"],
        # This test will check to see if 'Admin' is a valid username
        ["Admin'; -- ","thiswillbeignored"],
        # This test will search for the Root user, part of all SQL databases
        ["Root'; -- ","thanksfortheaccess"]
    ]

    print()
    print("Comment Attack Test Cases:")
    print()
    counter = 1
    for test in comment_attack_tests:
        query = function(test[0], test[1])
        print(f'{counter}. USERNAME: {test[0]} PASSWORD: {test[1]}') 
        print(f'    RESULTING QUERY: {query}\n')
        counter += 1

def testUnion(function):
    '''Runs a set of test cases that represents union query attacks through the function passed as a parameter.'''

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

    print()
    print("Union Query Attack Test Cases:")
    print()
    counter = 1
    for test in union_query_attack_tests:
        query = function(test[0], test[1])
        print(f'{counter}. USERNAME: {test[0]}     PASSWORD: {test[1]}')
        print(f'RESULTING QUERY: {query}\n')
        counter += 1

# Function to create the SQL query (vulnerable)
def genQuery(username, password):
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}';"
    return query

# Function for a weak mitigation
def genQueryWeak(username, password):
    union_pattern = "[Uu][Nn][Ii][Oo][Nn]"
    additional_statement_pattern = ";"
    comment_pattern = "--"
    quote_pattern = "[\'\"]"

    username = re.sub(union_pattern, "", username)
    username = re.sub(additional_statement_pattern, "", username)
    username = re.sub(comment_pattern, "", username)
    username = re.sub(quote_pattern, "", username)

    password = re.sub(union_pattern, "", password)
    password = re.sub(additional_statement_pattern, "", password)
    password = re.sub(comment_pattern, "", password)
    password = re.sub(quote_pattern, "", password)

    return genQuery(username, password)

# Function for a strong mitigation 
def genQueryStrong(username, password):
    whitelist_pattern = "[^\w\^\[\]\\~`!@#$%&*()+={}|:<>,.?/]"

    username = re.sub(whitelist_pattern, "", username)
    password = re.sub(whitelist_pattern, "", password)
    return genQuery(username, password)

# Menu options for the main function
def displayMenu():
    print("SQL Injection Mitigation Lab")
    print("1. Test Valid Input Test Cases")
    print("2. Tautology Attack Test Cases")
    print("3. Union Query Attack Test Cases")
    print("4. Additional Statement Attack Test Cases")
    print("5. Comment Attack Test Cases")
    print("6. Weak Mitigation Function")
    print("7. Strong Mitigation Function")
    print("8. Exit")

# Main function with menu
def main():
    while True:
        displayMenu()
        choice = input("Select an option: ")
        match choice:
            case '1':
                testValid(genQuery)
            case '2': 
                testTautology(genQuery)
            case '3':
                testUnion(genQuery)
            case '4':
                testAddState(genQuery)
            case '5':
                testComment(genQuery)
            case '6':
                testValid(genQueryWeak)
                testTautology(genQueryWeak)
                testUnion(genQueryWeak)
                testAddState(genQueryWeak)
                testComment(genQueryWeak)
            case '7':
                testValid(genQueryStrong)
                testTautology(genQueryStrong)
                testUnion(genQueryStrong)
                testAddState(genQueryStrong)
                testComment(genQueryStrong)
            case '8':
                break
        
if __name__ == "__main__":
    main()