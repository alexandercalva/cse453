import sqlite3

# Conectar a la base de datos (o crearla si no existe)
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Crear una tabla de usuarios
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)''')
# Insertar algunos usuarios de ejemplo
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('alice', 'pass123'))
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('bob', 'securePwd'))
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('alex', 'hola123'))
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('usuario', 'clave'))

# Confirmar los cambios y cerrar la conexión
connection.commit()
connection.close()

print("Database 'my_database.db' and 'users' table created.")