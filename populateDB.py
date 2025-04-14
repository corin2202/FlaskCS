from app4 import app,db,Pizza

pizzas = [
    { "name": "Margarita", "price": "£15.99","description": "Cheese and tomato", "image": "margarita.jpg", "veggie": False },
    { "name": "Pepperoni","price": "£17.99",  "description": "Pepperoni, cheese and tomato", "image" : "pepperoni.jpg", "veggie": False },
    { "name": "Hawaiian", "price":"£17.99", "description": "Pineapple, ham, cheese and tomato", "image": "hawaiian.jpg", "veggie": False },
    { "name": "Onion", "price": "£13.99", "description": "Onion", "image": "onion.jpg", "veggie": True},
    { "name": "Chocolate chicken", "price": "£20.99", "description": "Chocolate sprinkles and smarties with roast chicken", "image": "chocchicken.jpg", "veggie": False},
    { "name": "Kiwi", "price": "£13.99", "description": "Kiwi", "image": "kiwi.jpg", "veggie": True},
    { "name": "Troll", "price": "£14.99", "description": "Beans and olives", "image": "troll.jpg", "veggie": True},
]


with app.app_context():
    db.drop_all()
    db.create_all()
    for pizza in pizzas:
        newPizza = Pizza(name = pizza["name"], price = pizza["price"], description = pizza["description"], image = pizza["image"], veggie = pizza["veggie"])
        db.session.add(newPizza)

    db.session.commit()