# app.py

from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from random import randint
from datetime import datetime
from db import *
from utils import generate_random_profit_loss
from bson import json_util


app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['traders']
traders_collection = db['traders']


@app.route('/')
def home():
    return redirect(url_for('admin_dashboard'))

@app.route('/user/<username>', methods=['GET'])
def user_dashboard(username):
    trader_data = traders_collection.find_one({'username': username})

    if trader_data:
        profit_loss_data = list(profit_loss_collection.find({'trader_id': str(trader_data['_id'])}))
        print(profit_loss_data)
        profit_loss_data_json = json_util.dumps(profit_loss_data)
        return render_template('user_dashboard.html', trader_data=trader_data, profit_loss_data=profit_loss_data_json)
    else:
        return 'Trader not found'

@app.route('/admin', methods=['GET'])
def admin_dashboard():
    traders = list(traders_collection.find())
    return render_template('admin_dashboard.html', traders=traders)

def populate_db():
    traders_collection.delete_many({})  # Clear existing traders

    traders = ['trader1', 'trader2', 'trader3', 'trader4', 'trader5',
               'trader6', 'trader7', 'trader8', 'trader9', 'trader10']

    for trader in traders:
        trader_data = {'username': trader}
        inserted_trader = traders_collection.insert_one(trader_data)

        for _ in range(10):  # Generate 10 profit/loss values for each trader
            profit_loss_data = {
                'trader_id': str(inserted_trader.inserted_id),
                'timestamp': datetime.now(),
                'profit_loss': generate_random_profit_loss()
            }
            profit_loss_collection.insert_one(profit_loss_data)

    return 'Database populated successfully!'



@app.route('/delete_all_traders', methods=['POST'])
def delete_all_traders():
    traders_collection.delete_many({})
    return 'All traders have been deleted.'

if __name__ == '__main__':
    populate_db()  # Call the function to populate the database
    app.run(debug=True)
