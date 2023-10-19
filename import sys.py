import sys

# Función para generar una consulta SQL para autenticar un usuario
def generate_query(username: str, password: str) -> str:
  """Genera una consulta SQL para autenticar un usuario.

  Args:
    username: El nombre de usuario del usuario a autenticar.
    password: La contraseña del usuario a autenticar.

  Returns:
    A string representing the SQL query.
  """

  query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
  return query

# Función para demostrar que la función de generación de consultas funciona como se espera
def test_query_generation():
  """Demuestra que la función de generación de consultas funciona como se espera.

  Genera un conjunto de casos de prueba (uno para cada miembro del equipo) que representen entradas válidas donde el nombre de usuario y la contraseña consisten en letras, números y guiones bajos. A continuación, crea una función que introduzca estos casos de prueba en la función de generación de consultas y muestre la consulta resultante.
  """

  # Generar un conjunto de casos de prueba
  username_test_cases = ["alice", "bob", "carol"]
  password_test_cases = ["password", "123456", "secret"]

  # Ejecutar los casos de prueba
  for username in username_test_cases:
    for password in password_test_cases:
      query = generate_query(username, password)
      print(query)

# Función para demostrar que la función de generación de consultas es vulnerable a ataques de inyección de SQL
def test_vulnerabilities():
  """Demuestra que la función de generación de consultas es vulnerable a ataques de inyección de SQL.

  Genera casos de prueba (nuevamente, uno para cada miembro del equipo) que demuestren un ataque de tautología, una consulta de unión, un ataque de declaración adicional y un ataque de comentarios.
  """

  # Ataque de tautología
  username = "1 OR 1=1 --"
  password = "password"
  query = generate_query(username, password)
  print(query)

  # Consulta de unión
  username = "1 UNION SELECT username, password FROM users --"
  password = "password"
  query = generate_query(username, password)
  print(query)

  # Ataque de declaración adicional
  username = "1; DROP TABLE users; --"
  password = "password"
  query = generate_query(username, password)
  print(query)

  # Ataque de comentarios
  username = "1 /* DROP TABLE users; */ --"
  password = "password"
  query = generate_query(username, password)
  print(query)

# Función para proporcionar una mitigación débil contra ataques de inyección de SQL
def weak_mitigation(input: str) -> str:
  """Proporciona una mitigación débil contra ataques de inyección de SQL.

  Esta función reemplaza todos los caracteres especiales que podrían ser utilizados en un ataque de inyección de SQL con sus correspondientes entidades HTML.

  Args:
    input: La entrada a filtrar.

  Returns:
    La entrada filtrada.
  """

  return input.replace("'", "\\'").replace("\"", "&quot;").replace(";", "&semi;").replace("--", "&mdash;").replace("%", "&percnt;").replace("(", "&lpar;").replace(")", "&rpar;")

# Función para proporcionar una mitigación fuerte contra ataques de inyección de SQL
def strong_mitigation(input: str) -> str:
  """Proporciona una mitigación fuerte contra ataques de inyección de SQL.

  Esta función utiliza la función `escape()` de la biblioteca `sqlalchemy` para escapar todos los caracteres especiales que podrían ser utilizados en un ataque de inyección de SQL.

  Args:
    input: La entrada a filtrar.

  Returns:
    La entrada filtrada.
  """

  from pymysql import escape_string

  return pymysql.escape_string(input)

# Función principal
def main():
  # Probar que la función de generación de consultas funciona como se espera
  test_query_generation()

  # Probar que la función de generación de consultas es vulnerable a ataques de inyección de SQL
  test_vulnerabilities()

  # Aplicar una mitigación débil
  print("Mitigation débil:")
  username = "1 OR 1=1 --"
  password = "password"
  sanitized_username = weak_mitigation(username)
  sanitized_password = weak_mitigation(password)
  query = generate_query(sanitized_username, sanitized_password)
  print(query)

  # Aplicar una mitigación fuerte
  print("Mitigation fuerte:")
  username = "1 OR 1=1 --"
  password = "password"
  sanitized_username = strong_mitigation(username)
  sanitized_password = strong_mitigation(password)
  query = generate_query(sanitized_username, sanitized_password)
  print(query)


if __name__ == "__main__":
  main()