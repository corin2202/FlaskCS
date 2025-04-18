from app4 import app,db,Pizza

pizzas = [
    { "name": "Margarita", "price": "£15.99","description": "Cheese and tomato", "image": "margarita.jpg", "veggie": False, "side": False},
    { "name": "Pepperoni","price": "£17.99",  "description": "Pepperoni, cheese and tomato", "image" : "pepperoni.jpg", "veggie": False, "side": False },
    { "name": "Hawaiian", "price":"£17.99", "description": "Pineapple, ham, cheese and tomato", "image": "hawaiian.jpg", "veggie": False, "side": False },
    { "name": "Onion", "price": "£13.99", "description": "Onion", "image": "onion.jpg", "veggie": True, "side": False},
    { "name": "Chocolate chicken", "price": "£20.99", "description": "Chocolate sprinkles and smarties with roast chicken", "image": "chocchicken.jpg", "veggie": False, "side": False},
    { "name": "None pizza left beef", "price": "£9.99", "description": "Beef on the left", "image": "none.webp", "veggie": False, "side": False},
    { "name": "Kiwi", "price": "£13.99", "description": "Kiwi and cheese", "image": "kiwi.jpg", "veggie": True, "side": False},
    { "name": "Tomato", "price": "£8.99", "description": "Tomato", "image": "tomato.webp", "veggie": True, "side": False},
    { "name": "Zucchini", "price": "£13.99", "description": "Zucchini and cheese", "image": "zucchini.webp", "veggie": True, "side": False},
    { "name": "Pea-zza", "price": "£12.99", "description": "Peas cress and dirt", "image": "green.webp", "veggie": True, "side": False},
    { "name": "Primitive", "price": "£4.99", "description": "...", "image": "base.jpg", "veggie": True, "side": False},
    { "name": "Troll", "price": "£14.99", "description": "Beans and olives", "image": "troll.jpg", "veggie": True, "side": False},
    { "name": "Mozzarella sticks", "price": "£5.99", "description": "Mozzarella deep fried", "image": "mozzarella.jpg", "veggie": False, "side": True},
    { "name": "Garlic dip", "price": "£2.99", "description": "Garlic flavoured mayonnaise", "image": "garlicdip.png", "veggie": False, "side": True},
    { "name": "Garlic bread", "price": "£3.99", "description": "Garlic toasted flatbread", "image": "garlicbread.jpg", "veggie": False, "side": True},
    { "name": "Chicken strips", "price": "£5.99", "description": "Medium rare chicken strips", "image": "chickenstrips.jpg", "veggie": False, "side": True},


]


with app.app_context():
    db.drop_all()
    db.create_all()
    for pizza in pizzas:
        newPizza = Pizza(name = pizza["name"], price = pizza["price"], description = pizza["description"], image = pizza["image"], veggie = pizza["veggie"], side = pizza["side"])
        db.session.add(newPizza)

    db.session.commit()