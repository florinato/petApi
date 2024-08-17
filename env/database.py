
from pymongo import MongoClient

# Conexión a la base de datos MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["virtual_pet_db"]

# Verificar si la colección `users` existe; si no, crearla
if "users" not in db.list_collection_names():
    db.create_collection("users")

# Colección de usuarios donde ahora también almacenaremos las mascotas
users_collection = db["users"]





