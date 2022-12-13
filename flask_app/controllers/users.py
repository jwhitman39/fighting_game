from flask_app import app
from flask import redirect, session, render_template, request
from flask_app.models import user, game, fighter
from flask_app.controllers import games, fighters
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

# Posts the registration
@app.route('/users/register', methods=['POST'])
def register_user():
    print('Got post info')
    if not user.User.validate_register(request.form)==True:
        print('the credentials are not correct')
        return redirect('/')
    # if not user.User.validate_unique(request.form):
    #     print('there is a problem')
    #     return redirect('/')
    else:
        pw_hash=bcrypt.generate_password_hash(request.form['password'])
        print('pw_hash')
        data={
            'first_name':request.form['first_name'],
            'last_name':request.form['last_name'],
            'email':request.form['email'],
            'password': pw_hash
        }
        id = user.User.add_user_to_db(data)
        session['user_id']=id
        return redirect('/dashboard')

@app.route('/users/login', methods=['POST'])
def login_user():
    if not user.User.validate_login(request.form):
        return redirect('/')
    else:
        email_data={
            'email': request.form['email']
        }
        found_user= user.User.get_one_user_by_email(email_data)
        session['user_id']=found_user.id
        print('New user made!')
        return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    if 'user_id' in session:
        data={
                'id' : session['user_id']
            }
    print(data)
    print('about to retrieve users and fighters...')
    return (
        render_template(
            'dashboard.html', 
            this_user=user.User.get_one_user(data),
            all_fighters= fighter.Fighter.get_all_fighters_with_users()))