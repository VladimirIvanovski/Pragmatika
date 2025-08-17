from flask import Flask, render_template
import json
import os

app = Flask(__name__)

def load_content():
    """Load content from JSON file"""
    content_path = os.path.join(app.root_path, 'content', 'site_content.json')
    try:
        with open(content_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.route('/')
def index():
    content = load_content()
    return render_template('index.html', 
                         active_page='home', 
                         title='Почетна',
                         content=content.get('home', {}))

@app.route('/about')
def about():
    content = load_content()
    return render_template('about.html', 
                         active_page='about', 
                         title='За проектот',
                         content=content.get('about', {}))

@app.route('/research')
def research():
    content = load_content()
    return render_template('research.html', 
                         active_page='research', 
                         title='Истражување',
                         content=content.get('research', {}))

@app.route('/team')
def team():
    content = load_content()
    return render_template('team.html', 
                         active_page='team', 
                         title='Тим',
                         content=content.get('team', {}))

@app.route('/gallery')
def gallery():
    content = load_content()
    return render_template('gallery.html', 
                         active_page='gallery', 
                         title='Галерија',
                         content=content.get('gallery', {}))


if __name__ == '__main__':
    app.run(debug=True)
