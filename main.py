from starlette.responses import FileResponse
from fastapi import FastAPI, Body
from pymongo import MongoClient
import base64
import uuid


MONGO_USER = "zackblack"
MONGO_PASSWORD = "alohomora1234"

client = MongoClient()
client = MongoClient(f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@db:27017/?authMechanism=DEFAULT')

db = client.projeto
db_user = db.users

app = FastAPI(title="User-image FastAPI")


@app.post("/add-user")
def add_user(name: str):
    treated_name = name.strip().title()
    if len(treated_name) < 2:
        return {"Status": "Error", "Message": "The name must be greater than 1 char or not empty"}
    user = {"_id": str(uuid.uuid4()), "name": treated_name}
    try:
        db_user.insert_one(user)
    except:
        return {"Status": "Error", "Message": "User not added"}
    return {"id": user["_id"], "name": user["name"]}


@app.put("/update-user")
def update_user(id: str, name: str):
    treated_name = name.strip().title()
    if len(treated_name) < 2:
        return {"Status": "Error", "Message": "The name must be greater than 1 char or not empty"}
    try:
        db_user.update_one({"_id": id}, {"$set": {"name": treated_name}})
        data = db_user.find_one({"_id": id})
    except:
        return {"Status": "Error", "Message": "User not updated"}
    try:
        if data["_id"] == id:
            return {"id": data["_id"], "name": data["name"]}
    except TypeError:
        return {"Status": "Error", "Message": "ID not found"}


@app.put("/add-user-image")
def add_user_image(id: str, photo_base64: str = Body(...)):
    if photo_base64.strip() == "":
        return {"Status": "Error", "Message": "Base64 invalid"}
    data = db_user.find_one({"_id": id})
    try:
        if data["_id"] != id:
            pass
    except TypeError:
        return {"Status": "Error", "Message": "ID not found"}
    id_photo = str(uuid.uuid4())
    photo_data = {"photo": [{"photo_id": id_photo, "photo_base64": photo_base64}]}
    db_user.update_one({"_id": id}, {"$set": photo_data})
    return {"id_photo": id_photo}


@app.get("/get-user-image")
def get_user_image(id: str, photo_id: str):
    data = db_user.find_one({"_id": id})
    try:
        if data["photo"][0]["photo_id"] == photo_id and data["_id"] == id:
            return {"photo_base64": data["photo"][0]["photo_base64"]}
    except TypeError:
        return {"Status": "Error", f"Message": f"ID not found"}
    return {"Status": "Error", "Message": "ID not found"}


@app.get("/get-user-image-thumbnail")
def get_user_image_thumbnail(id: str):
    data = db_user.find_one({"_id": id})
    try:
        if data["_id"] != id:
            pass
    except TypeError:
        return {"Status": "Error", "Message": "ID not found"}
    encoded_b64 = str(data["photo"][0]["photo_base64"])
    imgdata = base64.b64decode(encoded_b64)
    filename = 'user_image.jpg'
    with open(filename, 'wb') as f:
        f.write(imgdata)
    return FileResponse(filename, media_type='application/octet-stream', filename=filename)


@app.put("/update-user-image")
def update_user_image(id: str, photo_id: str, photo_base64: str = Body(...)):
    data = db_user.find_one({"_id": id})
    if photo_base64.strip() == "":
        return {"Status": "Error", "Message": "Base64 invalid"}
    new_data = {"photo": [{"photo_id": str(uuid.uuid4()), "photo_base64": photo_base64}]}
    try:
        if data["photo"][0]["photo_id"] != photo_id:
            return {"Status": "Error", "Message": "ID not found"}
    except TypeError:
        return {"Status": "Error", "Message": "ID not found"}
    db_user.update_one({"_id": id}, {"$set": new_data})
    return {"Photo_ID": new_data["photo"][0]["photo_id"]}


@app.delete("/delete-user-image")
def delete_user_image(id: str, photo_id: str):
    data = db_user.find_one({"_id": id})
    try:
        name = data["name"]
    except TypeError:
        return {"Status": "Error", "Message": "ID not found"}
    if data["_id"] == id and data["photo"][0]["photo_id"] == photo_id:
        db_user.delete_one({"_id": id})
        return {"Status": "Success", "Message": f"User: {name} deleted successfully"}
    return {"Status": "Error", "Message": "ID not found"}
