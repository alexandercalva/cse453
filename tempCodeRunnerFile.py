cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('bob', 'securePwd'))