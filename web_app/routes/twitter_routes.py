
# web_app/routes/twitter_routes.py

from flask import Blueprint, render_template, jsonify, request

from web_app.models import db, User, Tweet, parse_records
from web_app.services.twitter_service import twitter_api_client
from web_app.services.basilica_service import basilica_api_client

twitter_routes = Blueprint("twitter_routes", __name__)

def store_twitter_user_data(screen_name):
    # Get the username from the twitter api and save the
    # user and tweets objects
    api = twitter_api_client()
    twitter_user = api.get_user(screen_name)
    statuses = api.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)

    # Check to see if the user already exists in the db user table and 
    # if not then add it to the db user table
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()

    print("STATUS COUNT:", len(statuses))
    # Use the basilica api to turn the tweets (statuses) into numeric lists
    basilica_api = basilica_api_client()
    all_tweet_texts = [status.full_text for status in statuses]
    embeddings = list(basilica_api.embed_sentences(all_tweet_texts, model="twitter"))
    print("NUMBER OF EMBEDDINGS", len(embeddings))

    # Put all of the tweets in the db tweet table
    counter = 0
    for status in statuses:
        print(status.full_text)
        print("----")

        # Find or create database tweet:
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id # or db_user.id
        db_tweet.full_text = status.full_text
        embedding = embeddings[counter]
        print(len(embedding))
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        counter+=1
    db.session.commit()

    return db_user, statuses

@twitter_routes.route("/users")
@twitter_routes.route("/users.json")
def list_users():
    ## Can make different results for stacked decorators to reuse functionality
    #if request.path.endswith(".json"):
    #    return some json
    #else:
    #    render a template
    db_users = User.query.all()
    users = parse_records(db_users)
    return jsonify(users)

@twitter_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)
    db_user, statuses = store_twitter_user_data(screen_name)

    # return "OK"
    return render_template("users.html", user=db_user, tweets=statuses)

@twitter_routes.route("/adduser")
def add_user():
    return render_template("adduser.html")

@twitter_routes.route("/adduser/display", methods=["POST"])
def add_user_to_db():
    user = request.form["user"]
    db_user, statuses = store_twitter_user_data(user)
    return render_template("display.html", user=db_user, tweets=statuses)