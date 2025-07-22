from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer,String, Float
from flask import Flask,redirect,render_template
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,FloatField
from wtforms.validators import DataRequired,NumberRange

app = Flask(__name__)
app.config["SECRET_KEY"] = "dalsknljo3noitrjqpimfamdlksanf"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_book.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#--------------Database Configuration-------------------#

db = SQLAlchemy(app)

class Base(DeclarativeBase):
    pass

class Book(db.Model):
    __tablename__ = "books"
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    title:Mapped[str] = mapped_column(String(250),nullable=False,unique=True)
    author:Mapped[str]=mapped_column(String(250),nullable=False)
    rating:Mapped[float]=mapped_column(Float,nullable=False)



@app.route("/")
def home():
    return render_template("index.html",books = Book.query.all())


#------------------Add the book Form Setup------------------#
class AddBook(FlaskForm):
    name = StringField("Book Name ",validators=[DataRequired()])
    author = StringField("Author Name ",validators=[DataRequired()])
    rating = FloatField("Rating ", validators=[DataRequired(),NumberRange(min=0,max=10)])
    submit =  SubmitField("Add Book")

@app.route("/add",methods=["POST","GET"])
def add_book():
    form = AddBook()
    if form.validate_on_submit():
        db.session.add(Book(title=form.name.data,author=form.author.data,rating =float(form.rating.data)))
        db.session.commit()
        return redirect("/")

    return render_template("add.html",form = form)

#---------Delete the book---------#
@app.route("/delete?id=<int:book_id>")
def delete_the_book(book_id):
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect("/")


#-------Edit the Book Rating---------

class EditBookRating(FlaskForm):
    new_rating = FloatField("Enter the new Rating",validators=[DataRequired(),NumberRange(min=0,max=10)])
    submit = SubmitField("Edit the Rating")

@app.route("/edit_rating?id=<int:book_id>",methods=["GET","POST"])
def edit_the_rating(book_id):
    book = Book.query.get_or_404(book_id)
    form = EditBookRating()
    if form.validate_on_submit():
        book.rating = float(form.new_rating.data)
        db.session.commit()
        return redirect("/")
    return render_template("edit.html",form=form,book_id = book_id)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,use_reloader=False)