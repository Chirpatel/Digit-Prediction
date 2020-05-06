import os
os.system('pip install --upgrade pip')
#os.system('pip install tensorflow==2.2.0rc4')

import random, string
from flask import Flask, render_template, request, jsonify
import base64
import numpy as np
import io
from PIL import Image
from base64 import decodestring
#import tensorflow as tf
from keras import backend as K
from flask import request
from flask import jsonify
from flask import Flask
import keras
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.io import imread
from skimage.transform import resize
import shutil

app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

ok_chars = string.ascii_letters + string.digits


@app.route('/')  # What happens when the user visits the site
def base_page():
	return render_template(
		'index.html',  # Template file path, starting from the templates folder. 
	)
@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)
model=0
def get_model():
    global model
    model = keras.models.load_model("num_reader.model")
    print(" * Model Loded!")

print(" * Loading Keras Model...")
get_model()

@app.route("/",methods=["POST"])
def predict():
    CATEGORIES=["NORMAL","CNV","DME","DRUSEN"]
    message = request.get_json(force=True)
    print(message)
    
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    bytesio=io.BytesIO(decoded)
    filename="test.png"
    with open(filename, "wb") as outfile:
        outfile.write(bytesio.getbuffer())
    num=find()
    response = {
        'prediction': str(num)
    }
    return jsonify(response)

def find():
	CATEGORIES=["NORMAL","CNV","DME","DRUSEN"]
	test=(np.array(resize(imread("test.png"),(28,28,1)))).reshape(1,28,28)
	prediction = model.predict(test)
	num=np.argmax(prediction[0])
	print(num)
	return  num





if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=5000,  # Randomly select the port the machine hosts on.
		threaded=False
	)