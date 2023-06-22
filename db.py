from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['trader_dashboard']
traders_collection = db['traders']
profit_loss_collection = db['profit_loss']
