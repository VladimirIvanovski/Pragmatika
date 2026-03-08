from flask import Flask, render_template, send_file, session, redirect, url_for, request
import json
import os
from document_manager import scan_documents, get_document_path, group_documents_by_type, get_document_content

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'pragmatika-ugd-2025')

# ── Helpers ────────────────────────────────────────────────────────────────

def load_content():
    content_path = os.path.join(app.root_path, 'content', 'site_content.json')
    try:
        with open(content_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def load_translations():
    path = os.path.join(app.root_path, 'content', 'translations.json')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def get_page(full_content, key, lang):
    """Return language-specific page content, falling back to mk."""
    section = full_content.get(key, {})
    if 'mk' in section or 'en' in section:
        return section.get(lang, section.get('mk', {}))
    return section

@app.context_processor
def inject_globals():
    lang = session.get('lang', 'mk')
    raw  = load_translations()

    def flatten(section):
        return {k: v.get(lang, v.get('mk', k)) for k, v in section.items()}

    nav    = flatten(raw.get('nav',    {}))
    common = flatten(raw.get('common', {}))
    footer = flatten(raw.get('footer', {}))
    pages  = flatten(raw.get('pages',  {}))

    return {
        'lang':   lang,
        'nav':    nav,
        'common': common,
        'footer': footer,
        'pages':  pages,
    }

# ── Language switch ────────────────────────────────────────────────────────

@app.route('/set-lang/<code>')
def set_lang(code):
    if code in ('mk', 'en'):
        session['lang'] = code
    return redirect(request.referrer or url_for('index'))

# ── Pages ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    lang    = session.get('lang', 'mk')
    content = load_content()
    t       = load_translations()
    return render_template('index.html',
                           active_page='home',
                           title=t.get('pages', {}).get('home', {}).get(lang, 'Почетна'),
                           content=get_page(content, 'home', lang),
                           lang=lang)

@app.route('/about')
def about():
    lang    = session.get('lang', 'mk')
    content = load_content()
    t       = load_translations()
    return render_template('about.html',
                           active_page='about',
                           title=t.get('pages', {}).get('about', {}).get(lang, 'За проектот'),
                           content=get_page(content, 'about', lang),
                           lang=lang)

@app.route('/research')
def research():
    lang    = session.get('lang', 'mk')
    content = load_content()
    t       = load_translations()
    return render_template('research.html',
                           active_page='research',
                           title=t.get('pages', {}).get('research', {}).get(lang, 'Истражување'),
                           content=get_page(content, 'research', lang),
                           lang=lang)

@app.route('/team')
def team():
    lang    = session.get('lang', 'mk')
    content = load_content()
    t       = load_translations()
    return render_template('team.html',
                           active_page='team',
                           title=t.get('pages', {}).get('team', {}).get(lang, 'Тим'),
                           content=get_page(content, 'team', lang),
                           lang=lang)

@app.route('/gallery')
def gallery():
    lang    = session.get('lang', 'mk')
    content = load_content()
    t       = load_translations()
    return render_template('gallery.html',
                           active_page='gallery',
                           title=t.get('pages', {}).get('gallery', {}).get(lang, 'Галерија'),
                           content=get_page(content, 'gallery', lang),
                           lang=lang)

@app.route('/publications')
def publications():
    lang = session.get('lang', 'mk')
    content = load_content()
    t = load_translations()
    return render_template('publications.html',
                           active_page='publications',
                           title=t.get('pages', {}).get('publications', {}).get(lang, 'Публикации'),
                           content=get_page(content, 'publications', lang),
                           lang=lang)

@app.route('/presentations')
def presentations():
    lang = session.get('lang', 'mk')
    content = load_content()
    t = load_translations()
    return render_template('presentations.html',
                           active_page='presentations',
                           title=t.get('pages', {}).get('presentations', {}).get(lang, 'Презентации'),
                           content=get_page(content, 'presentations', lang),
                           lang=lang)

@app.route('/news')
def news():
    lang = session.get('lang', 'mk')
    content = load_content()
    t = load_translations()
    return render_template('news.html',
                           active_page='news',
                           title=t.get('pages', {}).get('news', {}).get(lang, 'Вести и настани'),
                           content=get_page(content, 'news', lang),
                           lang=lang)

@app.route('/contact')
def contact():
    lang = session.get('lang', 'mk')
    t = load_translations()
    return render_template('contact.html',
                           active_page='contact',
                           title=t.get('pages', {}).get('contact', {}).get(lang, 'Контакт'),
                           lang=lang)

@app.route('/documents')
def documents():
    lang            = session.get('lang', 'mk')
    all_documents   = scan_documents()
    grouped_documents = group_documents_by_type(all_documents)
    content         = load_content()
    t               = load_translations()
    return render_template('documents.html',
                           active_page='documents',
                           title=t.get('pages', {}).get('documents', {}).get(lang, 'Документи'),
                           documents=all_documents,
                           grouped_documents=grouped_documents,
                           content=get_page(content, 'documents', lang),
                           lang=lang)

@app.route('/documents/download/<filename>')
def download_document(filename):
    file_path = get_document_path(filename)
    if file_path:
        return send_file(file_path, as_attachment=True)
    return "Document not found", 404

@app.route('/documents/view/<filename>')
def view_document(filename):
    lang      = session.get('lang', 'mk')
    file_path = get_document_path(filename)
    if not file_path:
        return "Document not found", 404

    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext == '.pdf':
        return send_file(file_path)

    content = get_document_content(filename)
    if 'error' in content:
        return f"Error processing document: {content['error']}", 500

    return render_template('document_viewer.html',
                           filename=filename,
                           content=content,
                           active_page='documents',
                           lang=lang)

if __name__ == '__main__':
    port  = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
