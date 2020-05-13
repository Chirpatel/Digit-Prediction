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
import cv2
import keras
from PIL import Image
from io import BytesIO
import base64
import logging
from skimage.io import imread
from skimage.transform import resize

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
    model = keras.models.load_model("model_trained30.model")
    print(" * Model Loded!")

print(" * Loading Keras Model...")
get_model()

def data_uri_to_img(uri):
	try:
		image = base64.b64decode(uri.split(',')[0], validate=True)
		#print(image)
		# make the binary image, a PIL image
		image = Image.open(BytesIO(image))
		# convert to numpy array
		image = np.array(image); 
		return image
	except Exception as e:
		logging.exception(e);print('\n')
		return None

def preProcessing(img):
	img = np.array(img, dtype=np.uint8)
	img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#imageio.imwrite('filename1.png', img)
	img = cv2.equalizeHist(img)
	#imageio.imwrite('filename2.png', img)
	img = img/.255
	#imageio.imwrite('filename3.png', img)
	return img

import imageio

@app.route("/",methods=["POST"])
def predict():
		message = request.get_json(force=True)
		#print(message)
		encoded = message['image']
		image = data_uri_to_img(encoded) 
		if image is None:
			print("At run_algo(): image is None.")
			return 
		img = np.asarray(image)
		img.astype(np.float32)
		img = cv2.resize(img,(128,128))
		img = preProcessing(img)
		print(img.shape)
		imageio.imwrite('filename.png', img)
		img = img.reshape(1,128,128,1)
		print(img.shape)
		classIndex = int(model.predict_classes(img))
		#print(classIndex)
		predictions = model.predict(img)
		print(predictions)
		classIndex=np.argmax(predictions[0])
		probVal= np.amax(predictions)
		print(classIndex,probVal)
		if(probVal>0.60):
			response = {
					'prediction': str(classIndex),
					'prob': str(probVal*100)
			}
		else:
			response = {
					'prediction': str("Invalid"),
					'prob': "Invalid" 
			}
		print(response)
		return jsonify(response)


if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=5000,  # Randomly select the port the machine hosts on.
		threaded=False
	)