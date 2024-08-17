from fastapi import HTTPException
from models import Pet, User
from database import users_collection

def get_user_pets(user: User):
    # Obtener todas las mascotas de un usuario
    user_data = users_collection.find_one({"username": user.username})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data.get("mascotas", [])

def create_pet(pet: Pet, user: User):
    # Añadir una nueva mascota al usuario
    users_collection.update_one({"username": user.username}, {"$push": {"mascotas": pet.dict()}})
    return pet

def update_pet(pet_name: str, pet_data: Pet, user: User):
    # Actualizar una mascota existente del usuario
    users_collection.update_one(
        {"username": user.username, "mascotas.name": pet_name},
        {"$set": {"mascotas.$": pet_data.dict()}}
    )
    updated_user = users_collection.find_one({"username": user.username})
    updated_pets = updated_user.get("mascotas", [])
    for pet in updated_pets:
        if pet["name"] == pet_name:
            return pet
    raise HTTPException(status_code=404, detail="Pet not found")

def delete_pet(pet_name: str, user: User):
    # Eliminar una mascota del usuario
    result = users_collection.update_one(
        {"username": user.username},
        {"$pull": {"mascotas": {"name": pet_name}}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Pet not found")
    return {"msg": "Pet deleted"}

def get_pet_by_name(user: User, pet_name: str):
    """Busca una mascota por su nombre en el documento del usuario."""
    pets = user.get("mascotas", [])
    for pet in pets:
        if pet["name"] == pet_name:
            return pet
    return None
