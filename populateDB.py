from app4 import app,db,Pizza

pizzas = [
    { "name": "Margarita", "price": "£15.99","description": "Cheese and tomato", "image": "margarita.jpg" },
    { "name": "Pepperoni","price": "£17.99",  "description": "Pepperoni, cheese and tomato", "image" : "pepperoni.jpg" },
    { "name": "Hawaiian", "price":"£17.99", "description": "Pineapple, ham, cheese and tomato", "image": "hawaiian.jpg" }
]


with app.app_context():
    db.create_all()
    for pizza in pizzas:
        newPizza = Pizza(name = pizza["name"], price = pizza["price"], description = pizza["description"], image = pizza["image"])
        db.session.add(newPizza)

    db.session.commit()