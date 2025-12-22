from flask import Flask, render_template, send_file, jsonify
import json
import os
from document_manager import scan_documents, get_document_path, group_documents_by_type, get_document_content

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

@app.route('/documents')
def documents():
    """Display all documents"""
    all_documents = scan_documents()
    grouped_documents = group_documents_by_type(all_documents)
    content = load_content()
    return render_template('documents.html',
                         active_page='documents',
                         title='Документи',
                         documents=all_documents,
                         grouped_documents=grouped_documents,
                         content=content.get('documents', {}))

@app.route('/documents/download/<filename>')
def download_document(filename):
    """Download a document"""
    file_path = get_document_path(filename)
    if file_path:
        return send_file(file_path, as_attachment=True)
    return "Document not found", 404

@app.route('/documents/view/<filename>')
def view_document(filename):
    """View a document with extracted content"""
    file_path = get_document_path(filename)
    if not file_path:
        return "Document not found", 404
    
    file_ext = os.path.splitext(filename)[1].lower()
    
    # For PDFs, serve the file directly
    if file_ext == '.pdf':
        return send_file(file_path)
    
    # For Word and PowerPoint, extract and display content
    content = get_document_content(filename)
    if 'error' in content:
        return f"Error processing document: {content['error']}", 500
    
    return render_template('document_viewer.html',
                         filename=filename,
                         content=content,
                         active_page='documents')

if __name__ == '__main__':
    app.run(debug=True)
