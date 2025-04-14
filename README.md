# Django URL Shortener (Rest API) App

A simple and efficient URL shortening application built with Django. This app allows users to shorten long URLs, track their usage, and manage the links.

## Features

-	Shorten long URLs into concise, shareable links.
-	Redirect users seamlessly from the shortened URL to the original URL.
-	Track the number of clicks on each shortened link.
-	User authentication and ownership for secure link management.
-	API endpoints for creating, retrieving, and deleting shortened links.

## Installation

#### 	1.	Clone the repository:
```
git clone git@github.com:mertcan-tas/django-url-shortener.git
```

#### 	2.	Set up a virtual environment (optional):
```
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

#### 	3.	Install project requirements:
```
pip install -r requirements.txt
```

#### 	4.	Apply database migrations:
```
python manage.py makemigrations
python manage.py migrate
```

#### 	5.	Run the development server:
```
python manage.py runserver
```

#### 	6.	Access the app:
Open your browser and go to http://127.0.0.1:8000.


## Redirect Behavior
The redirection logic is implemented in ShortenedLinkGetAPIView. You can modify it to include custom logging, analytics, or additional features.


Future Enhancements
-	Add analytics for detailed tracking of clicks by date and location.
-	Implement bulk link creation for advanced users.
-	Add expiration dates to links with automatic cleanup.
-	Enhance the frontend for a user-friendly experience.

## Contributing
We welcome contributions! Please fork this repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.


