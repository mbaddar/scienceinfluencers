from flask import Flask
from flask import render_template, request
from flask_navigation import Navigation

from flask_wtf import FlaskForm
from wtforms import TextField, validators
import requests
import http.client, urllib.request, urllib.parse, urllib.error, base64
from pprint import pprint

class MessageForm(FlaskForm):
    message = TextField(u'What is on your mind?', [validators.optional(), validators.length(max=200)])


app = Flask(__name__)
app.secret_key = 'sooperdoopersecretkey_required_for_csrf!'


nav = Navigation(app)

nav.Bar('top', [
    nav.Item('Home!','index'),
    nav.Item('Sentiment Analysis', 'sentiment')
])

@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")


mood_to_picture = {
'neutral':'neutral_em.png',
'pos' : 'positive_em.png',
'neg' : 'negative_em.png',
'error' : 'error_em.png'
}

@app.route('/emotion/', methods=['GET','POST'])
def sentiment():
	form = MessageForm(request.form)
	if request.method == 'POST' and form.validate():
		msg = form.message.data
		api_url = 'http://text-processing.com/api/sentiment/'
		response = requests.post(api_url, data = {'text': msg})
		returned_mood='error' # the default is error! unless things go well!
		if response.status_code==200:
			#returned_mood=response.json().get('label')
			returned_mood = 'neg'
			#prob = float(response.json().get('probability')["pos"])
			prob = float(response.json()['probability']['pos'])
			print("prob=%.4f"%prob)
			if prob > 0.5:
				returned_mood ='pos'
			#print( dir(response) )
			#print('response.status_code = {%s}'% response.status_code)


		which_picture = mood_to_picture[returned_mood]

		return render_template("my_form.html", picture=which_picture, form=form)

	return render_template('my_form.html',picture='placeholder_300x225.png', form=form)

@app.route('/emotion2/', methods=['GET','POST'])
def sentiment2():
	form = MessageForm(request.form)
	sentiment_api_url='https://westeurope.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment'
	if request.method == 'POST' and form.validate():
		msg = form.message.data
		# API2
		headers = {
		    # Request headers
		    'Content-Type': 'application/json',
		    'Ocp-Apim-Subscription-Key': '26c33c70467d4419acf3ab6dcd443b87',
		}

		documents = {'documents' : [
		  {'id': '1', 'language': 'en', 'text': msg},
		]}
		response  = requests.post(sentiment_api_url, headers=headers, json=documents)		    
		returned_mood='error' # the default is error! unless things go well!
		print('Response status_code: '+ str(response.status_code) )
		if response.status_code==200:
			#returned_mood=response.json().get('label')
			returned_mood = 'neg'
			#Assuing 1 id
			print(response.json().get('documents'))
			prob = float( response.json().get('documents')[0]["score"])
			print("prob=%.4f"%prob)
			if prob > 0.5:
				returned_mood ='pos'
			#print( dir(response) )
			#print('response.status_code = {%s}'% response.status_code)


		which_picture = mood_to_picture[returned_mood]

		return render_template("my_form.html", picture=which_picture, form=form)

	return render_template('my_form.html',picture='placeholder_300x225.png', form=form)


@app.route('/emotion3/', methods=['GET','POST'])
def sentiment3():
	form = MessageForm(request.form)
	sentiment_api_url='https://community-sentiment.p.mashape.com/text/'
	if request.method == 'POST' and form.validate():
		msg = form.message.data
		# API2
		headers={
		    "X-Mashape-Key": "H6yafy92t2mshNqA1ZIr7nkLG20Zp1mrO06jsnnAyh512iDpGU",
		    "Content-Type": "application/x-www-form-urlencoded",
		    "Accept": "application/json"
		}
		params={
		    "txt": msg
		}

		# documents = {'documents' : [
		#   {'id': '1', 'language': 'en', 'text': msg},
		# ]}
		# response  = requests.post(sentiment_api_url, headers=headers, params=params)		    
		response = unirest.post("https://community-sentiment.p.mashape.com/text/",
		  headers={
		    "X-Mashape-Key": "H6yafy92t2mshNqA1ZIr7nkLG20Zp1mrO06jsnnAyh512iDpGU",
		    "Content-Type": "application/x-www-form-urlencoded",
		    "Accept": "application/json"
		  },
		  params={
		    "txt": "stupid and smart"
		  }
		)
		returned_mood='error' # the default is error! unless things go well!
		print('Response status_code: '+ str(response.status_code) )
		if response.status_code==200:
			#returned_mood=response.json().get('label')
			returned_mood = 'neg'
			#Assuing 1 id
			#prob = float( response.json().get('result')["confidence"])
			print(response.json())
			if prob > 50:
				returned_mood ='pos'
			#print( dir(response) )
			#print('response.status_code = {%s}'% response.status_code)


		which_picture = mood_to_picture[returned_mood]

		return render_template("my_form.html", picture=which_picture, form=form)

	return render_template('my_form.html',picture='placeholder_300x225.png', form=form)

if __name__ == "__main__":
	app.run(host='0.0.0.0')
