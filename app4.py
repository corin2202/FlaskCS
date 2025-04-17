from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import NumberRange, Optional
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

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




class ChoiceForm(FlaskForm):
    quantity = IntegerField("Enter the number of pizzas:",validators = [
        Optional(),
        NumberRange(min = 1,message = "Please enter a number greater than 0")
    ])

    submit = SubmitField('Submit')





@app.route('/')
def galleryPage():
    pizzas = Pizza.query.all()
    return render_template('index.html',pizzas = pizzas)




@app.route('/pizza/<pizzaName>',methods=['GET','POST'])
def singleProductPage(pizzaName):
    pizzas = Pizza.query.all()


    if "basket" not in session:
        session["basket"] = {}


    for pizza in pizzas:
        if pizza.name == pizzaName:

            form = ChoiceForm()

            if form.validate_on_submit():
                quantity = form.quantity.data

                
                if str(pizza.id) in session["basket"]:
                    session["basket"][str(pizza.id)] += quantity  
                else:
                    session["basket"][str(pizza.id)] = quantity 

               
                session.modified = True

                return redirect(url_for('singleProductPage', pizzaName = pizza.name))
                
                
            return render_template('SinglePizza.html', pizza = pizza, form = form)
        
    return "Pizza not found", 404


@app.route('/basket')
def basketPage():
    # stores a basketItems as many of pizzaId: quantity
    basketItems = []
    total_price = 0

    if "basket" in session.keys():
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

    return render_template('basket.html', basket = basketItems, total_price = round(total_price,2))
    

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

if __name__ == '__main__':
    app.run(debug=True)
