import os
import json

from dotenv import load_dotenv

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure



def get_database():

    print("="*50)

    connection_string = os.getenv("MONGO_CONNECTION_STRING")

    if connection_string:
        print("Utilizzo MONGO_CONNECTION_STRING fornita.")
        print("="*50)
    else:
        raise ValueError("Connection string non correttamente fornita!")


    try:
        client = MongoClient(connection_string)

        # Pinga il server per verificare la connessione
        client.admin.command('ping')
        print(f"Connesso con successo a MongoDB.")
        print("="*50)

        # Accedi al database specificato dalla variabile d'ambiente MONGO_DB_NAME
        db = client["prova_new_db"]

        return db

    except ConnectionFailure as e:
        print(f"☠️ Errore: Impossibile connettersi a MongoDB. Dettagli: {e}")
        print("Controlla le tue variabili d'ambiente (MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASSWORD, MONGO_CONNECTION_STRING) e che il server MongoDB sia in esecuzione.")
        return None
    except Exception as e:
        print(f"❌ Si è verificato un errore generico: {e}")
        return None


# ====== Products ======

def add_product(
        db,
        new_item
        ):
    
    items_collection = db["items"]

    try:
        if items_collection.count_documents({"nome": new_item["nome"]}) == 0:
            insert_result = items_collection.insert_one(new_item)
            print(f"Item inserito con ID: {insert_result.inserted_id}")
        else:
            print(f"Item '{new_item['nome']}' già presente.")
        
        item_trovato = items_collection.find_one({"nome": new_item["nome"]})

        if item_trovato:
            print(f"Item trovato: {item_trovato}")

    except Exception as e:
        print(f"Errore durante le operazioni sul database: {e}")

    return 0


def get_all_items(db):
    """
    Retrieve all items from the 'items' collection.
    """
    items_collection = db["items"]
    try:
        items = list(items_collection.find())
        for item in items:
            item["_id"] = str(item["_id"])  # Convert ObjectId to string for JSON serialization
        return items
    except Exception as e:
        print(f"Errore durante il recupero degli items: {e}")
        return []


def get_items_by_category(db, category):
    """
    Retrieve items from the 'items' collection filtered by category.
    """
    items_collection = db["items"]
    try:
        items = list(items_collection.find({"category": category}))
        for item in items:
            item["_id"] = str(item["_id"])
        return items
    except Exception as e:
        print(f"Errore durante il recupero degli items per categoria: {e}")
        return []


# ====== Users ======

def get_user(db, username):

    users_collection = db["users"]

    try:
        user = users_collection.find_one({"username": username})
        if user:
            user["_id"] = str(user["_id"])  # Convert ObjectId to string for JSON serialization
            return user
        return None
    except Exception as e:
        print(f"Errore durante il recupero dello user: {e}")
        return None
    

def add_user(db, new_user):
    users_collection = db["users"]
    try:
        if users_collection.count_documents({"name": new_user["name"]}) == 0:
            insert_result = users_collection.insert_one(new_user)
            print(f"User inserito con ID: {insert_result.inserted_id}")
        else:
            print(f"User '{new_user['name']}' già presente.")
        user_trovato = users_collection.find_one({"name": new_user["name"]})
        if user_trovato:
            print(f"User trovato: {user_trovato}")
        return user_trovato
    except Exception as e:
        print(f"Errore durante le operazioni sul database utenti: {e}")
        return None


def find_user(db, name):
    users_collection = db["users"]
    try:
        user = users_collection.find_one({"name": name})
        if user:
            user["_id"] = str(user["_id"])
        return user
    except Exception as e:
        print(f"Errore durante la ricerca dell'utente: {e}")
        return None


def delete_item(db, nome):
    items_collection = db["items"]
    try:
        result = items_collection.delete_one({"nome": nome})
        if result.deleted_count > 0:
            print(f"Item '{nome}' eliminato con successo.")
            return True
        else:
            print(f"Item '{nome}' non trovato.")
            return False
    except Exception as e:
        print(f"Errore durante l'eliminazione dell'item: {e}")
        return False


def get_mean_price_by_category(db):
    """
    Calculate the mean price of items grouped by category.
    """
    items_collection = db["items"]
    try:
        pipeline = [
            {"$group": {"_id": "$category", "mean_price": {"$avg": "$prezzo"}}}
        ]
        results = list(items_collection.aggregate(pipeline))
        # Format output as a list of dicts with 'category' and 'mean_price'
        return [{"category": r["_id"], "mean_price": r["mean_price"]} for r in results]
    except Exception as e:
        print(f"Errore durante il calcolo della media dei prezzi per categoria: {e}")
        return []







    