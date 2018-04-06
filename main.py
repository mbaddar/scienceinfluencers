import base64
#import http.client
#import inspect
import pdb
import urllib.error
import urllib.parse
import urllib.request
#from pprint import pprint
import xml.etree.ElementTree as ET
import requests
from flask import (Flask, abort, redirect, render_template, request, session,
                   url_for, flash)
import pandas as pd
#import numpy as np
from auth import OAuthSignIn
from flask_login import UserMixin as UserBase
#from models.user import User as UserBase
#from flask.ext.login import login_user, logout_user, current_user, login_required, LoginManager
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from flask_navigation import Navigation
from flask_wtf import FlaskForm
#from json2table import convert
from wtforms import TextField, validators
from html.parser import HTMLParser
import re
from bs4 import BeautifulSoup
import datetime as dt


# Need to move that class
class User(UserBase):
  
    def __init__(self, email, username = None, authenticated = False):
        self.__email = email
        self.__id = email
        self.__username = username if username is not None else None
        self.__authenticated = authenticated
        super().__init__()
    
    @property
    def authenticated(self):
        return self.__authenticated
    @authenticated.setter
    def authenticated(self, authenticated):
        self.__authenticated = authenticated

    @property
    def id(self):
        return self.__email
    @id.setter
    def id(self, id):
        self.__email = id

    @property
    def username(self):
        return self.__username
    @username.setter
    def username(self, username):
        self.__username = username    
    
    @property
    def email(self):
        return self.__email
    @email.setter
    def email(self, email):
        self.__email = email    

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True
    def is_anonymous(self):
        return True
    
    @staticmethod
    def find_or_create_by_email( email, username = None):
        return User(email, username, True)
    @staticmethod
    def find_by_id( id):
        return User(id, id.split("@")[0], True)

class MessageForm(FlaskForm):
    search_text = TextField(u'Search for a cool paper!',
                             [validators.Optional(), validators.length(max=200)
                              ])

app = Flask(__name__)
app.config.from_object('config')
#app.secret_key = 'this is very secret'
app.secret_key = 'PScUSeapwIlx2Q7VWHZLD8-R'

nav = Navigation(app)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

## Implement
@login_manager.user_loader
def load_user(id):
    return User.find_by_id(id)

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    # if email is not None:
    #     print("email: " + email)
    # if email not in users:
    #     return

    user = User(email)
    # user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    # user.is_authenticated = request.form['password'] == users[email]['password']

    return user

# nav.Bar('top', [
#     nav.Item('Home!','index'),
#     nav.Item('Login', 'login'),
#     nav.Item('API Test', 'testapi')
# ])

#pdb.set_trace()
#inspect.getmembers(current_user, predicate=inspect.ismethod)
if not current_user:
    #current_user = User("guest")
    nav.Bar('top', [
        nav.Item('Home!','index'),
        nav.Item('Login', 'login'),
        nav.Item('API Test', 'tesarxiv')
    ])
else:
    nav.Bar('top', [
        nav.Item('Home!','index'),
        nav.Item('Logout', 'logout'),
        nav.Item('API Test', 'tesarxiv')
    ])
    

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
    if not username:
        username = email.split("@")[0] 
    # print("Username, email = ("+ username + ","+ email + ")")
    if email is None:
        # I need a valid email address for my user identification
        #flash('Authentication failed.')
        return redirect(url_for('index'))
    #flash('Login successful!')
    # Look if the user already exists
    user = User.find_or_create_by_email(email, username)

    # Log in the user, by default remembering them for their next visit
    # unless they log out.
    login_user(user, remember=True)
    return redirect(url_for('index') )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.email is not None \
        and current_user.is_authenticated:
        return redirect(url_for('index', authenticated = 'yes'))
    return render_template('login.html',
                           title='Sign In')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index') )
@app.route('/')
#@login_required
def index():
  return render_template('index.html')

def format_date (str_date):
    """
    Ex: 2018-04-04T00:00:00-04:00
        ^  ^ ^^ ^^
    """
    year = int(str_date[0:4])
    month = int(str_date[5:7])
    day = int(str_date[8:10])
    date = dt.datetime(year, month, day)
    return date.strftime('%d, %b %Y')

def check_url( url ):
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return True if regex.match( url ) is not None else False 

def HTMLInject  ( html ):
    """
    Injects a tags for URLs
    """
    soup = BeautifulSoup(html, 'html.parser')
    item_string = ""
    for item in soup.find_all('td'):
        item_string = item.string
        if check_url(item_string):
             item.string = ''
             tag = soup.new_tag('a', href=item_string , target = "_blank")
             tag.string = item_string
             item.append(tag)
    # print(soup.prettify())
    return soup.prettify()


@app.route('/arxiv/', methods=['GET', 'POST'])
def tesarxiv():
    form = MessageForm(request.form)
    search_text = form.search_text.data
    # if not search_text:
    #     # Do nothing
    #     flash("Please enter something to search for!")
    #     return redirect(url_for('tesarxiv') )
        
    aton_object = None
    # Create a dataframe for the information displayed to the user
    ids = []
    updated = []
    published = []
    title = []
    summary = []
    citation_velocity = []
    summary_html = ""
    summary_df = pd.DataFrame()
    
    if request.method == 'POST' and form.validate():
        # Should have pagination
        api_url = 'http://export.arxiv.org/api/query?search_query=all:' +\
                    (search_text if search_text else 'machine And all:learning') +\
                    '&start=0&max_results=10'
        response = requests.get(api_url)
        if response.status_code==200:
            xml_root = ET.fromstring(response.text)
            for entry in xml_root.findall('{http://www.w3.org/2005/Atom}entry'):
                element_id = entry.find('{http://www.w3.org/2005/Atom}id').text
                arxiv_id = "arXiv:"+ element_id.split('/')[-1]
                #citation_velocity.append( semantic_scolar_velocity( arxiv_id) )
                citation_velocity.append( "https://api.semanticscholar.org/" + arxiv_id )
                ids.append( element_id ) #URL
                updated.append( format_date( entry.find('{http://www.w3.org/2005/Atom}updated').text))
                published.append( format_date( entry.find('{http://www.w3.org/2005/Atom}published').text))
                title.append(entry.find('{http://www.w3.org/2005/Atom}title').text)
                # ids.append( "<a href='" + entry.find('{http://www.w3.org/2005/Atom}id').text +\
                #             "'>" + entry.find('{http://www.w3.org/2005/Atom}id').text +"</a>") #URL
                # Summary truncated
                summary.append(entry.find('{http://www.w3.org/2005/Atom}summary').text[:300] )
            summary_dict = {'Paper URL': ids,
                            'Updated': updated,
                            'Published': published, 
                            'Title': title,
                            'Summary': summary,
                            'Semantic Scholar': citation_velocity}
            summary_df = pd.DataFrame(summary_dict)
            summary_html = summary_df.to_html( index = False, classes="table table-striped table-hover") 
            summary_html = HTMLInject( summary_html ) 
    return render_template("my_form.html", picture='positive_em.png',\
                            form=form, render = summary_html )
         
def semantic_scolar_velocity( arxiv_id):
    api_url = 'https://api.semanticscholar.org/v1/paper/'+ arxiv_id
    response = requests.get(api_url)
    #response = requests.post(api_url, data = {'text': msg})
    #returned_mood='error' # the default is error! unless things go well!
    json_object = {}
    if response.status_code==200:
        json_object = response.json()
    citationVelocity = json_object['citationVelocity'] if json_object else 0
    return citationVelocity 
    # build_direction = "LEFT_TO_RIGHT"
    # table_attributes = {"style" : "width:100%", "class" : "table table-striped"}
    # html = convert( json_object, build_direction=build_direction,\
    #                 table_attributes=table_attributes)
    # return render_template("my_form.html", picture='positive_em.png',\
    #     form=form, render = html )


if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
