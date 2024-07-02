from flask import Flask, request, jsonify
from PIL import Image
import pytesseract

app = Flask(__name__)

"""
Creamos una aplicacion basica de Flask que tiene un endpoint /ocr.
Cuando enviamos una solicitud POST a este endpoint con un archivo de
imagen, extrae el archivo y utiliza el pytesseract envoltura para
realizar OCR usando su metodo "code_to_string()", y envia de vuelta el
texto extraido como parte de la respuesta.
"""
@app.route("/")
def home():
    return "Welcome to the OCR API"

@app.route("/ocr", methods = ['POST'])
def ocr_process():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({'status': 'error',
                            'message': 'No image part in the request'}), 400
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'status': 'error',
                            'message': 'No selected file'}), 400

        try:
            image_data = Image.open(image_file)

            # Realizando OCR usando PyTesseract, con configuracion en
            # español
            text = pytesseract.image_to_string(image_data, lang='spa')

            response = {
                'status': "success",
                'text': text
            }
            return jsonify(response)
        except Exception as e:
            return jsonify({'status': 'error',
                            'message': str(e)}), 500
