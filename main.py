import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


# class AddCafe(FlaskForm):
#     name = StringField('name', validators=[DataRequired()])
#     map_url = StringField('map_url', validators=[DataRequired()])
#     img_url = StringField('img_url', validators=[DataRequired()])
#     location = StringField('loc', validators=[DataRequired()])
#     seats = StringField('seats', validators=[DataRequired()])
#     has_toilet = BooleanField('toilet', validators=[DataRequired()])
#     has_wifi = BooleanField('wifi', validators=[DataRequired()])
#     has_sockets = BooleanField('sockets', validators=[DataRequired()])
#     can_take_calls = BooleanField('calls', validators=[DataRequired()])
#     coffee_price = StringField('coffee_price', validators=[DataRequired()])
#     submit = SubmitField('Add Cafe')


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route('/random')
def get_random_cafe():
    all_cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route('/all')
def get_all_cafes():
    all_cafes = db.session.query(Cafe).all()
    all_cafes_to_lst = [cafe.to_dict() for cafe in all_cafes]
    return jsonify(cafes=all_cafes_to_lst)


@app.route('/search')
def find_cafe():
    query_location = request.args.get('loc')
    cafe = db.session.query(Cafe).filter_by(location=query_location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    return jsonify(error={"Not Found": "Sorry, we don't have a cafe at the location."})

## HTTP POST - Create Record
@app.route('/add', methods=['POST'])
def add_cafe():
    new_cafe = Cafe(
        name = request.form.get('name'),
        map_url = request.form.get('map_url'),
        img_url = request.form.get('img_url'),
        location = request.form.get("location"),
        seats = request.form.get('seats'),
        has_toilet = bool(request.form.get('toilet')),
        has_wifi = bool(request.form.get('wifi')),
        has_sockets = bool(request.form.get('sockets')),
        can_take_calls = bool(request.form.get('calls')),
        coffee_price = request.form.get('coffee_price'),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


## HTTP PUT/PATCH - Update Record
@app.route('/update-price/<cafe_id>')
def patch(cafe_id):
    new_price = request.form.get('new_price')
    cafe_to_update = Cafe.query.get(cafe_id)
    cafe_to_update.coffee_price = new_price
    db.session.commit()
    return jsonify(response={"success": "Successfully updated the coffee price."})
## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
