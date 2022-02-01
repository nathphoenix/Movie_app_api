									PROJECT SET UP

After setting up your virtual environment
Run pip install -r requirements.txt

Navigate to the project directory and start the app by running
flask run or python app.py 

A postgress database was use in saving our favourite charcaters and quote on separate tables

hit the homepage to confirm if the app is working as expected by
hitting https://localhost:5000

OR

APPLICATION HAS BEEN DEPLOYED TO HEROKU, which is accessible through the link below
https://movieoneapi.herokuapp.com/

TO RUN THE TEST:
RUN pytest from the application folder and not from the test folder

									API CALLS ON POSTMAN

	POSTMAN DOCUMENTATION LINK : 
	https://documenter.getpostman.com/view/9827165/UVeCQTtS


add https://localhost:5000 as prefix to each of the route below, for example

https://localhost:5000 and this "/user/<int:user_id>" becomes 

https://localhost:5000/user/<int:user_id>


									VERY IMPORTANT
	Ensure you are register with a working email and then activate your account through an activatation link that 
	will be sent upon registration, then you can login, only authenticated user can actually have access to the movie world app

"/register"
	if successful, generates access token
	data = {
		"username": "myusername",
	    "email": "myemail",
		"password": "mypassword"
	}

"/login"
	if successful, generates access token
	data = {
		"username": "myusername",
		"password": "mypassword"
	}

"/refresh"
	this allows us to refresh a token when necessary

'/character'
	no data needed, just make a get request
	This get all the characters from the api


'/name'
	data = {
	     "name": "Algund"
	}

'/id'
	{
	    "_id": "5cd99d4bde30eff6ebccfe41"
	}


'/quotes'
	no data needed, just make a get request
	This get all the quote from the api

'/character_quotes'
	In order to get a quote from a particular, we use this endpoint
	data = {
	    "character": "5cd99d4bde30eff6ebccfea0"
	}

'/char_name'
	data = {'name': 'gandalf}

'/char_id'
	This allows us to favourite a charcter by their id which will save it to our postgress db
	data = {
	   "_id": "5cd99d4bde30eff6ebccfea0"
	}


'/favourite_quotes'
	This allows us to make a quote our favourite by accepting the quote
	Please note that you can only favourite a quote if the character is your favourite character, meaning his/her records has already been saved to our records
	data = {
	    "dialog": "Now come the days of the King. May they be blessed."
	}

'/book'
	no data needed, just make a get request

"/logout"
 	no data needed, just make a post request
