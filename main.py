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


#------------------Form Setup------------------#
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





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,use_reloader=False)