from flask import Flask, render_template, send_file, session, redirect, url_for, request
import json
import os

# Load .env file for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from document_manager import scan_documents, scan_documents_by_folder, get_document_path, group_documents_by_type, get_document_content, get_conference_entries

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

def get_current_lang():
    """Get current language: URL param overrides session (for reliable switching)."""
    lang = request.args.get('lang')
    if lang in ('mk', 'en'):
        session['lang'] = lang
        return lang
    return session.get('lang', 'mk')

@app.context_processor
def inject_globals():
    lang = get_current_lang()
    raw  = load_translations()

    def flatten(section):
        return {k: v.get(lang, v.get('mk', k)) for k, v in section.items()}

    nav    = flatten(raw.get('nav',    {}))
    common = flatten(raw.get('common', {}))
    footer = flatten(raw.get('footer', {}))
    pages  = flatten(raw.get('pages',  {}))
    copy   = flatten(raw.get('copy',   {}))

    return {
        'lang':   lang,
        'nav':    nav,
        'common': common,
        'footer': footer,
        'pages':  pages,
        'copy':   copy,
    }

# ── Language switch ────────────────────────────────────────────────────────

@app.route('/set-lang/<code>')
def set_lang(code):
    if code in ('mk', 'en'):
        session['lang'] = code
    next_url = request.args.get('next')
    if next_url and next_url.startswith('/'):
        target = next_url
    elif request.referrer and request.referrer.strip():
        target = request.referrer
    else:
        target = url_for('index')
    # Append ?lang= to ensure language sticks even if session cookie is not persisted
    sep = '&' if '?' in target else '?'
    return redirect(target + sep + 'lang=' + code)

# ── Pages ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    lang    = get_current_lang()
    content = load_content()
    t       = load_translations()
    home_vlings = content.get('home_vlings', {})
    return render_template('index.html',
                           active_page='home',
                           title=t.get('pages', {}).get('home', {}).get(lang, 'Почетна'),
                           content=get_page(content, 'home', lang),
                           home_vlings=home_vlings,
                           lang=lang)

@app.route('/about')
def about():
    lang    = get_current_lang()
    content = load_content()
    t       = load_translations()
    return render_template('about.html',
                           active_page='about',
                           title=t.get('pages', {}).get('about', {}).get(lang, 'За проектот'),
                           content=get_page(content, 'about', lang),
                           lang=lang)

@app.route('/research')
def research():
    lang    = get_current_lang()
    content = load_content()
    t       = load_translations()
    return render_template('research.html',
                           active_page='research',
                           title=t.get('pages', {}).get('research', {}).get(lang, 'Истражување'),
                           content=get_page(content, 'research', lang),
                           lang=lang)

@app.route('/team')
def team():
    lang    = get_current_lang()
    content = load_content()
    t       = load_translations()
    team_content = get_page(content, 'team', lang)
    members = team_content.get('members', []) if isinstance(team_content, dict) else []
    all_cvs = [m.get('cv') for m in members]
    return render_template('team.html',
                           active_page='team',
                           title=t.get('pages', {}).get('team', {}).get(lang, 'Тим'),
                           content=team_content,
                           all_cvs=all_cvs,
                           lang=lang)

@app.route('/gallery')
def gallery():
    lang    = get_current_lang()
    content = load_content()
    t       = load_translations()
    return render_template('gallery.html',
                           active_page='gallery',
                           title=t.get('pages', {}).get('gallery', {}).get(lang, 'Галерија'),
                           content=get_page(content, 'gallery', lang),
                           lang=lang)

@app.route('/publications')
def publications():
    lang = get_current_lang()
    content = load_content()
    t = load_translations()
    return render_template('publications.html',
                           active_page='publications',
                           title=t.get('pages', {}).get('publications', {}).get(lang, 'Публикации'),
                           content=get_page(content, 'publications', lang),
                           lang=lang)

@app.route('/presentations')
def presentations():
    lang = get_current_lang()
    content = load_content()
    t = load_translations()
    return render_template('presentations.html',
                           active_page='presentations',
                           title=t.get('pages', {}).get('presentations', {}).get(lang, 'Презентации'),
                           content=get_page(content, 'presentations', lang),
                           lang=lang)

@app.route('/news')
def news():
    lang = get_current_lang()
    content = load_content()
    t = load_translations()
    return render_template('news.html',
                           active_page='news',
                           title=t.get('pages', {}).get('news', {}).get(lang, 'Вести и настани'),
                           content=get_page(content, 'news', lang),
                           lang=lang)

@app.route('/conferences')
def conferences():
    lang = get_current_lang()
    t = load_translations()
    conf_entries = get_conference_entries()
    return render_template('conferences.html',
                           active_page='news',
                           title=t.get('pages', {}).get('news', {}).get(lang, 'Конференции'),
                           entries=conf_entries,
                           lang=lang)

@app.route('/documents/conference-image/<path:filepath>')
def conference_image(filepath):
    """Serve images from conference subfolders (e.g. Rabotilnica.../pic 1.jpeg)."""
    import mimetypes
    conf_dir = os.path.abspath(os.path.join(app.root_path, 'documents', 'Conferences'))
    fp = os.path.normpath(os.path.join(conf_dir, filepath))
    if not os.path.isfile(fp) or not os.path.abspath(fp).startswith(conf_dir):
        return "Not found", 404
    mime = mimetypes.guess_type(fp)[0] or 'image/jpeg'
    return send_file(fp, mimetype=mime)

@app.route('/contact')
def contact():
    lang = get_current_lang()
    t = load_translations()
    return render_template('contact.html',
                           active_page='contact',
                           title=t.get('pages', {}).get('contact', {}).get(lang, 'Контакт'),
                           lang=lang)

@app.route('/documents')
def documents():
    lang              = get_current_lang()
    all_documents     = scan_documents()
    grouped_documents = group_documents_by_type(all_documents)
    by_folder         = scan_documents_by_folder()
    content           = load_content()
    t                 = load_translations()
    return render_template('documents.html',
                           active_page='documents',
                           title=t.get('pages', {}).get('materials', t.get('pages', {}).get('documents', {})).get(lang, 'Материјали'),
                           documents=all_documents,
                           grouped_documents=grouped_documents,
                           by_folder=by_folder,
                           content=get_page(content, 'documents', lang),
                           lang=lang)

@app.route('/documents/download/<path:filename>')
def download_document(filename):
    file_path = get_document_path(filename)
    if file_path:
        return send_file(file_path, as_attachment=True)
    return "Document not found", 404

@app.route('/documents/view/<path:filename>')
def view_document(filename):
    lang      = get_current_lang()
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
