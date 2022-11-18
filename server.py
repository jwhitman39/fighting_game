from flask_app import app
from flask_app.controllers import fighters, games, users
app.secret_key = '321FIGHT'

if __name__ == '__main__':
    app.run(debug=True)
