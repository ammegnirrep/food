from flask import Flask, request, jsonify, render_template, redirect
import pusher
from database import db_session
from models import CupboardItem
from datetime import datetime
import os

app = Flask(__name__)

pusher_client = pusher.Pusher(
    app_id=os.getenv('PUSHER_APP_ID'),
    key=os.getenv('PUSHER_KEY'),
    secret=os.getenv('PUSHER_SECRET'),
    cluster=os.getenv('PUSHER_CLUSTER'),
    ssl=True)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    cupboard_items = CupboardItem.query.all()
    return render_template('index.html', cupboard_items=cupboard_items)

@app.route('/backend', methods=["POST", "GET"])
def backend():
    if request.method == "POST":
        name = request.form["name"]
        try:
            quantity = int(request.form["quantity"])
        except ValueError:
            abort(400, "Quantity must be a number")

        expiry_date = datetime.strptime(request.form['expiry_date'], '%d-%m-%Y %H:%M %p')

        new_cupboard_item = CupboardItem(name, quantity, expiry_date)
        db_session.add(new_cupboard_item)
        db_session.commit()

        data = {
                "id": new_cupboard_item.id,
                "name": name,
                "quantity": quantity,
                "expiry_date": request.form['expiry_date']}

        pusher_client.trigger('table', 'new-record', {'data': data })


        return redirect("/backend", code=302)
    else:
        cupboard_items = CupboardItem.query.all()
        return render_template('backend.html', cupboard_items=cupboard_items)

@app.route('/edit/<int:id>', methods=["POST", "GET"])
def update_record(id):
    if request.method == "POST":
        name = request.form["name"]
        try:
            quantity = int(request.form["quantity"])
        except ValueError:
            abort(400, "Quantity must be a number")
        expiry_date = datetime.strptime(request.form['expiry_date'], '%d-%m-%Y %H:%M %p')

        update_cupboard_item = CupboardItem.query.get(id)
        update_cupboard_item.name = name
        update_cupboard_item.quantity = quantity
        update_cupboard_item.expiry_date = expiry_date

        db_session.commit()

        data = {
            "id": id,
            "name": name,
            "quantity": quantity,
            "expiry_date": request.form['expiry_date'],
        }

        pusher_client.trigger('table', 'update-record', {'data': data })

        return redirect("/backend", code=302)
    else:
        new_cupboard_item = CupboardItem.query.get(id)
        new_cupboard_item.expiry_date = new_cupboard_item.expiry_date.strftime("%d-%m-%Y %H:%M %p")

        return render_template('update_cupboard_item.html', data=new_cupboard_item)

# run Flask app
if __name__ == "__main__":
    app.run()
