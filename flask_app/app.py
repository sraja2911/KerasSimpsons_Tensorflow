from flask import Flask
import jinja2

env = jinja2.Environment(loader=jinja2.PackageLoader('flask_app', 'templates'))

app = Flask(__name__)

@app.route('/')
def home():
    template = env.get_template('index.html')
    renderedTemplate = template.render()
    return renderedTemplate