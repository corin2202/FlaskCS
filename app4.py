from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, ValidationError
from wtforms.validators import NumberRange, Optional, DataRequired
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import json
import re

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = "pizzapizzapizza"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
db = SQLAlchemy(app)


class Pizza(db.Model):
    __tablename__ = "Pizzas"
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(32), index = True, unique = True)
    price = db.Column(db.String)
    description = db.Column(db.Text)
    image = db.Column(db.String(40))
    veggie = db.Column(db.Boolean)
    side = db.Column(db.Boolean)
    footprint = db.Column(db.Integer)
    rating = db.Column(db.Float)
    numratings = db.Column(db.Integer)


class ChoiceForm(FlaskForm):
    quantity = IntegerField("Enter the desired amount:",validators = [
        Optional(),
        NumberRange(min = 1,message = "Please enter a number greater than 0")
    ])

    submit = SubmitField('Submit')

def card_number_valid(form, field):
    # checks for 3 sets of 4 digits, followed by either space or hyphen, then checks for last 4 no space or hyphen on the end
    if re.match(r'^([0-9]{4}(-|\s)?){3}[0-9]{4}$',field.data) == None:
        raise ValidationError("Card does not match correct format")
    
    # performs luhn checksum, in reverse order
    index = 1
    total = 0
    for num in field.data[::-1]:
        if num != "-" and num != " ":
            if index % 2 == 0:
                doubled = int(num) * 2
                if doubled > 9:
                    for digit in str(doubled):
                        total += int(digit)
                else:
                    total += doubled
            else:
                total += int(num)
            index += 1

    if total % 10 != 0:
        raise ValidationError("Card is not a valid number sequence")
    
def exp_date_valid(form, field):
    if re.match(r'^(0?[1-9]|1[0-2])/[0-9]{2}$',field.data) == None:
        raise ValidationError("Expiry date does not match right format MM/YY")
    
def cvc_valid(form,field):
    if field.data < 100 or field.data > 999:
        raise ValidationError("CVC not a 3 digit number")
    

def sort_pizzas(sort_by, pizzaDict):
    if sort_by != "":
        for pizzas in pizzaDict.values():
            match sort_by:
                case "priceup":
                    pizzas.sort(key = lambda x: float(x.price[1:]))
                case "pricedown":
                    pizzas.sort(key = lambda x: float(x.price[1:]), reverse = True)
                case "footprintup":
                    pizzas.sort(key = lambda x: x.footprint)
                case "footprintdown":
                    pizzas.sort(key = lambda x: x.footprint, reverse = True)

class CardForm(FlaskForm):
    card_number = StringField("Card number", [DataRequired(), card_number_valid])
    exp_date = StringField("Expiry date", [DataRequired(), exp_date_valid])
    cvc = IntegerField("CVC",[DataRequired(),cvc_valid])
    submit = SubmitField('Pay now')

@app.route('/search',methods = ["GET","POST"])
def search():
    query1 = request.form.get('query', '').strip().lower()

    # returns pizza that has the entered string in it basic search
    searchedPizza = None
    for id in range(1,db.session.query(Pizza).count()):
        pizza = Pizza.query.get(id)
        if query1 in pizza.name.lower():
            searchedPizza = pizza
            break

    if searchedPizza is not None:
        return redirect(url_for('singleProductPage', pizzaName = searchedPizza.name, rating = round(searchedPizza.rating), numratings = searchedPizza.numratings))
    else:
        return redirect(url_for('galleryPage'))
    

@app.route('/', methods = ["GET","POST"])
def galleryPage():
    pizzas = Pizza.query.all()

    pizza_id = str(request.form.get('pizza_id'))
    increase = request.form.get('increase')
    
    if "basket" not in session:
        session["basket"] = {}

    # basket stores many dictionary of pizza_id and quantity
    if increase == "true":
        if pizza_id in session["basket"]:
            session["basket"][pizza_id] += 1
        else:
            session["basket"][pizza_id] = 1

    session.modified = True

    pizzaDict = {"Classics": [], "Veggie": [], "Sides": []}
    for pizza in pizzas:
        if not pizza.veggie and not pizza.side:
            pizzaDict["Classics"].append(pizza)
        elif pizza.veggie:
            pizzaDict["Veggie"].append(pizza)
        else:
            pizzaDict["Sides"].append(pizza)


    sort_by = request.args.get('sort_by')
    sort_pizzas(sort_by, pizzaDict)
    return render_template('index.html',pizzaDict = pizzaDict)

# returns the description when hovered
@app.route('/pizza-info/<pizzaId>')
def hover_info(pizzaId):
    pizza = Pizza.query.get(pizzaId)
    if pizza:
        return pizza.description


@app.route('/pizza/<pizzaName>',methods=['GET','POST'])
def singleProductPage(pizzaName):
    pizzas = Pizza.query.all()

    if "basket" not in session:
        session["basket"] = {}

    # updates basket total with amount entered
    for pizza in pizzas:
        if pizza.name == pizzaName:

            rating = round(pizza.rating)
            form = ChoiceForm()

            if form.validate_on_submit():
                quantity = form.quantity.data

                if str(pizza.id) in session["basket"]:
                    session["basket"][str(pizza.id)] += quantity  
                else:
                    session["basket"][str(pizza.id)] = quantity 

                session.modified = True

                return redirect(url_for('singleProductPage', pizzaName = pizza.name, rating = rating, numratings = pizza.numratings))
            return render_template('SinglePizza.html', pizza = pizza, form = form, rating = rating, numratings = pizza.numratings)
        
    return "Pizza not found", 404


@app.route('/basket', methods = ["GET","POST"])
def basketPage():
    # stores a basketItems as many of pizzaId: quantity
    basketItems = []
    total_price = 0
    
    # updates total price of basket total
    if "basket" in session.keys():
        checkout = request.form.get('checkout_value')
        basket = session["basket"]
        for pizza_id, quantity in basket.items():
            pizza = Pizza.query.get(int(pizza_id))
            if pizza:
                price = pizza.price
                total_price += float(price[1:]) * quantity
                basketItems.append({
                    "pizza": pizza,
                    "quantity": quantity
                })

        if checkout == "yes":
            return redirect(url_for('checkout',total_price = round(total_price,2)))


    return render_template('basket.html', basket = basketItems, total_price = round(total_price,2))
    

@app.route('/checkout/<total_price>', methods = ["GET","POST"])
def checkout(total_price):
    form = CardForm()
    receipt_list = []

    # creates a receipt of [[pizzaname, quantity, total price]]
    if "basket" in session.keys():
        basket = session["basket"]
        for pizza_id, quantity in basket.items():
            pizza = Pizza.query.get(int(pizza_id))
            if pizza:
                newItem = []
                newItem.append(pizza.name)
                newItem.append(quantity)
                newItem.append(round(float(pizza.price[1:]) * quantity,2))
                receipt_list.append(newItem)
        
        session.modified = True

    if form.validate_on_submit():
        return redirect(url_for('leave_review'))

    return render_template('checkout.html', total_price = total_price, form = form, receipt_list = receipt_list)


@app.route('/review', methods = ["GET","POST"])
def leave_review():
    pizzas_bought = []

    # creates list of [pizza] that were bought
    if "basket" in session.keys():
        basket = session["basket"]
        for pizza_id, quantity in basket.items():
            pizza = Pizza.query.get(int(pizza_id))
            if pizza:
                pizzas_bought.append(pizza)

    # receives the star ratings from user and updates the new average in database
    ratings_json = request.form.get("ratings_json")
    if ratings_json != None:
        if ratings_json != "":
            ratings = json.loads(ratings_json)
            for id, rating in ratings.items():
                pizza = Pizza.query.get(int(id))
                current_rating = pizza.rating
                num_ratings = pizza.numratings
                new_rating = ((current_rating * num_ratings) + rating) / (num_ratings + 1) 
                pizza.rating = new_rating
                pizza.numratings += 1
        
            db.session.commit()
            del session["basket"]
            return redirect(url_for('galleryPage'))
    
    
    return render_template('checkoutSuccess.html', pizzas = pizzas_bought)


@app.route('/update_quantity', methods = ["POST"])
def update_quantity():
    pizza_id = request.form.get('pizza_id').strip()
    action = request.form.get('action')

    if 'basket' in session.keys():
        basket = session["basket"]
        if pizza_id in basket:
            if action == "increase":
                basket[pizza_id] += 1
            elif action == "decrease":
                basket[pizza_id] -= 1
                if basket[pizza_id] <= 0:
                    del basket[pizza_id]
            elif action == "remove":
                del basket[pizza_id]

            session["basket"] = basket

    return redirect(url_for('basketPage'))


pizzas = [
    { "name": "Margarita", "price": "£15.99","description": "Cheese and tomato", "image": "margarita.jpg", "veggie": False, "side": False, "footprint": 1, "rating": 0.0, "numratings": 0},
    { "name": "Pepperoni","price": "£17.99",  "description": "Pepperoni, cheese and tomato", "image" : "pepperoni.jpg", "veggie": False, "side": False, "footprint": 2, "rating": 0.0, "numratings": 0 },
    { "name": "Hawaiian", "price":"£17.99", "description": "Pineapple, ham, cheese and tomato", "image": "hawaiian.jpg", "veggie": False, "side": False, "footprint": 2, "rating": 0.0, "numratings": 0 },
    { "name": "Onion", "price": "£13.99", "description": "Onion", "image": "onion.jpg", "veggie": True, "side": False, "footprint": 1, "rating": 0.0, "numratings": 0},
    { "name": "Chocolate chicken", "price": "£20.99", "description": "Chocolate sprinkles and smarties with roast chicken", "image": "chocchicken.jpg", "veggie": False, "side": False, "footprint": 4, "rating": 0.0, "numratings": 0},
    { "name": "None pizza left beef", "price": "£9.99", "description": "Beef on the left", "image": "none.webp", "veggie": False, "side": False, "footprint": 1, "rating": 0.0, "numratings": 0},
    { "name": "Kiwi", "price": "£13.99", "description": "Kiwi and cheese", "image": "kiwi.jpg", "veggie": True, "side": False, "footprint": 1, "rating": 0.0, "numratings": 0},
    { "name": "Tomato", "price": "£8.99", "description": "Tomato", "image": "tomato.webp", "veggie": True, "side": False, "footprint": 2, "rating": 0.0, "numratings": 0},
    { "name": "Zucchini", "price": "£13.99", "description": "Zucchini and cheese", "image": "zucchini.webp", "veggie": True, "side": False, "footprint": 1, "rating": 0.0, "numratings": 0},
    { "name": "Pea-zza", "price": "£12.99", "description": "Peas cress and dirt", "image": "green.webp", "veggie": True, "side": False, "footprint": 1, "rating": 0.0, "numratings": 0},
    { "name": "Primitive", "price": "£4.99", "description": "...", "image": "base.jpg", "veggie": True, "side": False, "footprint": 0, "rating": 0.0, "numratings": 0},
    { "name": "Troll", "price": "£14.99", "description": "Beans and olives", "image": "troll.jpg", "veggie": True, "side": False, "footprint": 1, "rating": 0.0, "numratings": 0},
    { "name": "Mozzarella sticks", "price": "£5.99", "description": "Mozzarella deep fried", "image": "mozzarella.jpg", "veggie": False, "side": True, "footprint": 3, "rating": 0.0, "numratings": 0},
    { "name": "Garlic dip", "price": "£2.99", "description": "Garlic flavoured mayonnaise", "image": "garlicdip.png", "veggie": False, "side": True, "footprint": 1, "rating": 0.0, "numratings": 0},
    { "name": "Garlic bread", "price": "£3.99", "description": "Garlic toasted flatbread", "image": "garlicbread.jpg", "veggie": False, "side": True, "footprint": 1, "rating": 0.0, "numratings": 0},
    { "name": "Chicken strips", "price": "£5.99", "description": "Medium rare chicken strips", "image": "chickenstrips.jpg", "veggie": False, "side": True, "footprint": 3, "rating": 0.0, "numratings": 0},
]


with app.app_context():
    db.create_all()
    if not Pizza.query.first():
        for pizza in pizzas:
            newPizza = Pizza(name = pizza["name"], price = pizza["price"], description = pizza["description"], image = pizza["image"], veggie = pizza["veggie"], side = pizza["side"], footprint = pizza["footprint"], rating = pizza["rating"], numratings = pizza["numratings"])
            db.session.add(newPizza)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
