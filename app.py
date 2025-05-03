from flask import Flask, request, send_file
from PIL import Image, ImageEnhance
import io

app = Flask(__name__)

@app.route('/')
def home():
    return "Ghibli Bot Flask Server is Running!"

@app.route('/generate_image', methods=['POST'])
def generate_image():
    if 'image' not in request.files or 'style' not in request.form:
        return "Missing data", 400

    image_file = request.files['image']
    style = request.form['style']

    try:
        image = Image.open(image_file.stream)

        # Apply style
        if style == "ghibli":
            image = ImageEnhance.Color(image).enhance(2.0)
        elif style == "anime":
            image = ImageEnhance.Brightness(image).enhance(1.3)

        output = io.BytesIO()
        image.save(output, format='JPEG')
        output.seek(0)

        return send_file(output, mimetype='image/jpeg')
    except Exception as e:
        return f"Error processing image: {str(e)}", 500

# Render handles host/port automatically, so no need to specify them
if __name__ == '__main__':
    app.run()
