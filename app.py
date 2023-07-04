from flask import Flask, render_template, request
import os 
from LP_recognition import lp_recognition
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')

db = client['license_plate']
collection = db['plate_number']

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH, 'static/upload/')

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        if 'image_name' in request.files:
            upload_file = request.files['image_name']
            filename = upload_file.filename
            path_save = os.path.join(UPLOAD_PATH, filename)
            upload_file.save(path_save)
            list_plate_number, list_probs = lp_recognition(path_save, filename)
            current_date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

            for index in range(len(list_plate_number)):
                plate_number = list_plate_number[index]
                if len(plate_number) >= 9 and len(plate_number) <= 10:
                    flag = True
                    check_plate = collection.find({"plate_number":plate_number}).sort("date", -1).limit(1)
                    for y in check_plate:
                        flag = False
                        for x in check_plate:
                            if (datetime.strptime(current_date, '%d/%m/%Y %H:%M:%S') - datetime.strptime(x["date"], '%d/%m/%Y %H:%M:%S')).seconds > (0):
                                collection.insert_one({"plate_number":plate_number, "path_save": 'static/upload/'+ filename, "date": current_date})
                        
                    if flag:
                        collection.insert_one({"plate_number":plate_number, "path_save": 'static/upload/'+ filename, "date": current_date})

            return render_template('index.html', upload=True, upload_image=filename, list_probs = list_probs, list_plate_number = list_plate_number, list_plate=False)
        
        if 'find_plate' in request.form:
            find_plate = request.form['find_plate']
            list_plate = collection.find({"plate_number":find_plate}).sort("date", -1)
            return render_template('index.html', upload=False, list_plate = list_plate)
    return render_template('index.html', upload=False)


if __name__ == "__main__":
    app.run()