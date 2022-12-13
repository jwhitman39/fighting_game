from crypt import methods
from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user, game, fighter
from flask_app.controllers import fighters, users
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

# New fighter (form)
@app.route('/fighters/new')
def add_new_fighter():
    if 'user_id'not in session:
        return redirect('/')
    if 'user_id' in session:
        data={
                'id' : session['user_id']
            }
    return render_template('create_fighter.html', this_user=user.User.get_one_user(data))

# Send fighter form to database
@app.route('/fighters/submit', methods=['POST'])
def submit_fighter():
    if 'user_id'not in session:
        return redirect('/')
    print(request.form)
    print('Got post info')
    if not fighter.Fighter.validate_fighter(request.form)==True:
        print('the credentials are not correct')
        return redirect('/fighters/new')
    # if not user.User.validate_unique(request.form):
    #     print('there is a problem')
    #     return redirect('/')
    else:
        data={
            'name':request.form['name'],
            'type':request.form['type'],
            'description': request.form['description'],
            'user_id': session['user_id']
        }
        fighter.Fighter.add_fighter_to_db(data)
        print(data)
        print('fighter successfully added to database! Hooray!')
        return redirect('/dashboard')

