from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Créer une base de données vulnérable
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, 
username TEXT, password TEXT)")
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 
'password123')")
conn.commit()

@app.route("/")
def home():
    return '<h1>Bienvenue sur l\'application vulnérable</h1> <p><a 
href="/login">Connexion</a></p>'

@app.route("/login", methods=["GET", "POST"])
def login():
    form = '''
    <form method="post">
        Nom d'utilisateur: <input type="text" name="username"><br>
        Mot de passe: <input type="text" name="password"><br>
        <input type="submit" value="Se connecter">
    </form>
    '''
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # ⚠️ Vulnérabilité SQL Injection ⚠️
        query = f"SELECT * FROM users WHERE username = '{username}' AND 
password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        
        if user:
            return "<h2>Connexion réussie</h2>"
        else:
            return "<h2>Échec de connexion</h2>"
    
    return render_template_string(form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

