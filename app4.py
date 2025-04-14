from flask import Flask, render_template, request, session
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
                
                return render_template('SinglePizzaQuantity.html',pizza = pizza, quantity = quantity)
            else:
                return render_template('SinglePizza.html', pizza = pizza, form = form)
        
    return "Pizza not found", 404


@app.route('/basket')
def basketPage():
    basket = session["basket"]
    basketItems = []

    for pizza_id, quantity in basket.items():
        pizza = Pizza.query.get(int(pizza_id))
        if pizza:
            basketItems.append({
                "pizza": pizza,
                "quantity": quantity
            })


    return render_template('basket.html', basket = basketItems)
    

if __name__ == '__main__':
    app.run(debug=True)
