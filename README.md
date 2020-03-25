# my-web-app-12

## Setup

Fork and clone the repo, then navigate there from the command-line:

```sh
cd my-web-app-12/
```

Setup and activate the virtual environment, and install package dependencies:

```sh
pipenv install
pipenv shell
```

Setup the database:

```sh
FLASK_APP=web_app flask db init
FLASK_APP=web_app flask db migrate
FLASK_APP=web_app flask db upgrade
```

## Usage

Run the app:

```sh
FLASK_APP=web_app flask run
```

Then visit localhost:5000 in the browser!
