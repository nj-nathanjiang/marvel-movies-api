from flask import Flask, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///marvel.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    release_date = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    length_in_minutes = db.Column(db.Integer, nullable=False)


db.create_all()


@app.route("/")
def home():
    return "Welcome To My Marvel API"


@app.route("/random")
def random_movie():
    movie = random.choice(db.session.query(Movie).all())
    return jsonify(
        id=movie.id,
        name=movie.name,
        release_date=movie.release_date,
        description=movie.description,
        length_in_minutes=movie.length_in_minutes,
    )


@app.route("/find-by-name/<name>")
def find_by_name(name):
    name.replace("+", " ")
    movies = db.session.query(Movie).all()
    for movie in movies:
        if movie.name == name:
            return jsonify(
                id=movie.id,
                name=movie.name,
                release_date=movie.release_date,
                description=movie.description,
                length_in_minutes=movie.length_in_minutes,
            )

    return "Movie Not Found"


@app.route("/all")
def all_movies():
    movies = db.session.query(Movie).all()
    list_of_movie_details = []
    for movie in movies:
        list_of_movie_details.append(
            {
                "id": movie.id,
                "name": movie.name,
                "release_date": movie.release_date,
                "description": movie.description,
                "length_in_minutes": movie.length_in_minutes,
            }
        )
    return jsonify(movies=[movie_details for movie_details in list_of_movie_details])


if __name__ == "__main__":
    app.run(debug=True)


db.session.commit()
