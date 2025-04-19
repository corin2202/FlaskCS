from app4 import app,db,Pizza

pizzas = [
    { "name": "Margarita", "price": "£15.99","description": "Cheese and tomato", "image": "margarita.jpg", "veggie": False, "side": False, "footprint": 1},
    { "name": "Pepperoni","price": "£17.99",  "description": "Pepperoni, cheese and tomato", "image" : "pepperoni.jpg", "veggie": False, "side": False, "footprint": 2 },
    { "name": "Hawaiian", "price":"£17.99", "description": "Pineapple, ham, cheese and tomato", "image": "hawaiian.jpg", "veggie": False, "side": False, "footprint": 2 },
    { "name": "Onion", "price": "£13.99", "description": "Onion", "image": "onion.jpg", "veggie": True, "side": False, "footprint": 1},
    { "name": "Chocolate chicken", "price": "£20.99", "description": "Chocolate sprinkles and smarties with roast chicken", "image": "chocchicken.jpg", "veggie": False, "side": False, "footprint": 4},
    { "name": "None pizza left beef", "price": "£9.99", "description": "Beef on the left", "image": "none.webp", "veggie": False, "side": False, "footprint": 1},
    { "name": "Kiwi", "price": "£13.99", "description": "Kiwi and cheese", "image": "kiwi.jpg", "veggie": True, "side": False, "footprint": 1},
    { "name": "Tomato", "price": "£8.99", "description": "Tomato", "image": "tomato.webp", "veggie": True, "side": False, "footprint": 2},
    { "name": "Zucchini", "price": "£13.99", "description": "Zucchini and cheese", "image": "zucchini.webp", "veggie": True, "side": False, "footprint": 1},
    { "name": "Pea-zza", "price": "£12.99", "description": "Peas cress and dirt", "image": "green.webp", "veggie": True, "side": False, "footprint": 1},
    { "name": "Primitive", "price": "£4.99", "description": "...", "image": "base.jpg", "veggie": True, "side": False, "footprint": 0},
    { "name": "Troll", "price": "£14.99", "description": "Beans and olives", "image": "troll.jpg", "veggie": True, "side": False, "footprint": 1},
    { "name": "Mozzarella sticks", "price": "£5.99", "description": "Mozzarella deep fried", "image": "mozzarella.jpg", "veggie": False, "side": True, "footprint": 3},
    { "name": "Garlic dip", "price": "£2.99", "description": "Garlic flavoured mayonnaise", "image": "garlicdip.png", "veggie": False, "side": True, "footprint": 1},
    { "name": "Garlic bread", "price": "£3.99", "description": "Garlic toasted flatbread", "image": "garlicbread.jpg", "veggie": False, "side": True, "footprint": 1},
    { "name": "Chicken strips", "price": "£5.99", "description": "Medium rare chicken strips", "image": "chickenstrips.jpg", "veggie": False, "side": True, "footprint": 3},
]


with app.app_context():
    db.drop_all()
    db.create_all()
    for pizza in pizzas:
        newPizza = Pizza(name = pizza["name"], price = pizza["price"], description = pizza["description"], image = pizza["image"], veggie = pizza["veggie"], side = pizza["side"], footprint = pizza["footprint"])
        db.session.add(newPizza)

    db.session.commit()