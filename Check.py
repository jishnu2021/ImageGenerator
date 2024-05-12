import io
import requests
from PIL import Image
from config import key  # Assuming key is stored in a config.py file

import openai
from flask import Flask, request  # Import request from Flask

app = Flask(__name__)

openai.api_key = key

def image_creation(text_prompt):
        
    response = openai.images.generate(
        prompt=text_prompt,
        n=1,
        size="256x256"
    )

    images = []

    for resp in response.data:
        image_url = resp.url
        image_content = requests.get(image_url).content
        image = Image.open(io.BytesIO(image_content))
        images.append(image_url)
        
    return images    


@app.route("/", methods=['GET', 'POST'])
def create_image():
    if request.method == 'POST':
        prompt = request.form['prompt']
        images = image_creation(prompt)
        return '\n'.join(images)
    return '''
        <form method="post">
            <label for="prompt">Enter the picture you want to create:</label><br>
            <input type="text" id="prompt" name="prompt"><br>
            <input type="submit" value="Submit">
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
