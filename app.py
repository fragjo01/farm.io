from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import db, Item

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def inventory():
    items = Item.query.all()
    return render_template("inventory.html", items=items)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        name = request.form["name"]
        image = request.form["image"]
        description = request.form["description"]
        price = float(request.form["price"])
        available = request.form.get("available") == "on"
        new_item = Item(name=name, image=image, description=description, price=price, available=available)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("admin"))
    items = Item.query.all()
    return render_template("admin.html", items=items)

@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == "POST":
        item.name = request.form["name"]
        item.image = request.form["image"]
        item.description = request.form["description"]
        item.price = float(request.form["price"])
        item.available = request.form.get("available") == "on"
        db.session.commit()
        return redirect(url_for("admin"))
    return render_template("edit.html", item=item)

@app.route("/delete/<int:item_id>")
def delete(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("admin"))

import logging
@app.route("/cart", methods=["GET", "POST"])
def cart():
    if "cart" not in session or not isinstance(session["cart"], dict):
        session["cart"] = {}
    if request.method == "POST":
        item_id = request.form["item_id"]
        if item_id in session["cart"]:
            session["cart"][item_id] += 1
        else:
            session["cart"][item_id] = 1
        session.modified = True
    cart_items = []
    grand_total = 0
    if session["cart"]:
        item_ids = [int(item_id) for item_id in session["cart"].keys()]
        cart_items = Item.query.filter(Item.id.in_(item_ids)).all()
        for item in cart_items:
            quantity = session["cart"].get(str(item.id), 0)
            item_total = item.price * quantity
            grand_total += item_total
            item.quantity = quantity
    return render_template("cart.html", cart_items=cart_items, grand_total=grand_total)

@app.route("/remove_from_cart/<int:item_id>")
def remove_from_cart(item_id):
    if "cart" in session and str(item_id) in session["cart"]:
        if session["cart"][str(item_id)] > 1:
            session["cart"][str(item_id)] -= 1
        else:
            del session["cart"][str(item_id)]
        session.modified = True
    return redirect(url_for("cart"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
