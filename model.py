"""Models and database functions"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from random import randint


##############################################################################
# Model definitions

class User(db.Model):
    """ Users of the site"""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    genres = db.relationship('Genre', secondary="users_genres", backref='users')

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<User user_id=%s name=%s>" % (self.user_id, self.name)

    # def is_authenticated(self):
    #     """required for flask_login"""
    #     return True

    # def is_active(self):
    #     """required for flask_login"""
    #     return True

    # def is_anonymous(self):
    #     """required for flask_login"""
    #     return False

    # def get_id(self):
    #     """required for flask_login"""
    #     return str(self.user_id)


class UserGenre(db.Model):
    """association table for users and genres"""
    __tablename__ = "users_genres"

    user_genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<UserGenre user_genre_id=%s user_id=%s>" % (
            self.user_genre_id, self.user_id)


class Rating(db.Model):
    """Ratings users have given a book"""
    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(20000), nullable=True)

    book = db.relationship('Book', backref='ratings')
    user = db.relationship('User', backref='ratings')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Rating rating_id=%s user_id=%s book_id=%s score=%s>" % (
            self.rating_id, self.user_id, self.book_id, self.score)


class Book(db.Model):
    """Book info scraped from Goodreads."""

    __tablename__ = "books"

    book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    avg_rating = db.Column(db.Float, nullable=False)
    pic_url = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.String(10000), nullable=False)

    genres = db.relationship('Genre', secondary="books_genres", backref='books')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Book book_id=%s title=%s>" % (self.book_id, self.title)


class BookGenre(db.Model):
    """ Genre-book association table"""
    __tablename__ = "books_genres"

    book_genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<BookGenre book_genre_id=%s book_id=%s genre_id=%s>" % (self.bookgenre_id, self.book_id, self.genre_id)


class Genre(db.Model):
    """ Genres of books, scraped from Goodreads."""
    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Genre genre_id=%s name=%s>" % (self.genre_id, self.name)


##############################################################################
# Helper functions

def recommend(user):
    """Given a user, recommend a book or books for them"""

    book_genre_dict = {}

    recommended_genres = user.genres

    # add genres belonging to books the user has rated highly to into a list of genres the user has favorited
    # this is in order to take the user's ratings into account
    if user.ratings:
        for rating in user.ratings:
            if rating.score == 4 or rating.score == 5:
                if len(rating.book.genres) <= 1:
                    recommended_genres.append(rating.book.genres)
                else:
                    recommended_genres.extend(rating.book.genres)

    # creates a dictionary where the key is a book object and the value is a list of genres which that book belongs to

    for genre in recommended_genres:
        for book in genre.books:
            if book in book_genre_dict:
                book_genre_dict[book].append(genre)
            else:
                book_genre_dict[book] = [genre]

    list_of_recommendations = []

    for book in book_genre_dict.keys():
        # if there are books which have ALL the genres a user has favorited,
        # then add those books to the rec list
        if set(user.genres) <= set(book.genres):
            list_of_recommendations.append(book)
        # if there are books that have two or more genres in common with the user's list of genres
        # add those books to the rec list as well
        elif len(set(user.genres) & set(book.genres)) > 2:
            list_of_recommendations.append(book)

    return list_of_recommendations


def generate_colors():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    a = randint(0, 255)

    return "rgba(%s,%s,%s,%s)" % (r, g, b, a)

# def find_words():
#     """Find a review with some of the words from the list of feature words"""

#     json_string = open("review_words.json").read()
#     review_dict = json.loads(json_string)

#     # neg_words = []
#     # pos_words = []

#     # for item in review_dict["neg"]:
#     #     neg_words.append(item[1])

#     # for item in review_dict["pos"]:
#     #     pos_words.append(item[1])

#     reviews = Rating.query.filter(Rating.score != 3).all()

#     for review in reviews:
#         words = review.text.split()
#         if "dnf"


def example_data():
    """Creates example data for testing purposes"""

    #creates sample users
    buffy = User(user_id=1, name="Buffy Summers", email="slayer@slayer.com", password="bangel4eva97")
    giles = User(user_id=2, name="Rupert 'Ripper' Giles", email="watcherlibrarian@slayer.com", password="greenmug63")

    #creates sample book
    slayer_guide = Book(book_id=1,
                        title="A Slayer's Guide to Slaying",
                        author="The Council of Watchers",
                        avg_rating=2.53,
                        pic_url='https://vignette.wikia.nocookie.net/buffy/images/d/d3/Vampyr.jpg/revision/latest?cb=20120314223316',
                        summary='In every generation there is a chosen one. She alone will stand against the vampires, the demons, and the forces of darkness. She is the slayer.',
                        )

    #creates sample genre
    vampires = Genre(genre_id=1, name='vampires')

    db.session.add_all([buffy, giles, slayer_guide, vampires])
    db.session.commit()

    #must have two separate commits because of foreign key dependencies

    #creates sample rating
    rating = Rating(rating_id=1, book_id=1, user_id=1, score=1, text="Hated this. DNF.")

    #creates sample book-genre
    book_genre = BookGenre(book_genre_id=1, book_id=1, genre_id=1)

    #creates sample user-genre
    user_genre = UserGenre(user_genre_id=1, user_id=1, genre_id=1)

    db.session.add_all([rating, book_genre, user_genre])
    db.session.commit()


def connect_to_db(app, db_uri='postgresql:///goodreads'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
