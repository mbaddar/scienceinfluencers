from flask import Flask
from flask import render_template
from flask import abort, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required, LoginManager

from auth import OAuthSignIn

from models.user import User
import pdb
app = Flask(__name__)
app.config.from_object('config')
#app.secret_key = 'this is very secret'
app.secret_key = 'PScUSeapwIlx2Q7VWHZLD8-R'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.find_by_id(id)

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    # Flask-Login function
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    username, email = oauth.callback()

    if email is None:
        # I need a valid email address for my user identification
        flash('Authentication failed.')
        return redirect(url_for('index'))

    # Look if the user already exists
    user = User.find_or_create_by_email(email)

    # Log in the user, by default remembering them for their next visit
    # unless they log out.
    login_user(user, remember=True)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html',
                           title='Sign In')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return render_template('login.html',
                           title='Sign In')
@app.route('/')
@login_required
def index():
  return render_template('index.html')

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
