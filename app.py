from flask import Flask, request, send_file
from PIL import Image, ImageEnhance
import io

app = Flask(__name__)

@app.route('/generate_image', methods=['POST'])
def generate_image():
    if 'image' not in request.files or 'style' not in request.form:
        return "Missing data", 400

    image_file = request.files['image']
    style = request.form['style']

    image = Image.open(image_file.stream)

    # Simulated "Ghibli/Anime" effect
    if style == "ghibli":
        image = ImageEnhance.Color(image).enhance(2.0)
    elif style == "anime":
        image = ImageEnhance.Brightness(image).enhance(1.3)

    output = io.BytesIO()
    image.save(output, format='JPEG')
    output.seek(0)

    return send_file(output, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
