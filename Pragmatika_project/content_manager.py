#!/usr/bin/env python3
"""
Simple Content Management System for the Intercultural Pragmatics Website
Usage: python content_manager.py
"""

import json
import os
from typing import Dict, Any

CONTENT_FILE = 'content/site_content.json'

def load_content() -> Dict[str, Any]:
    """Load existing content from JSON file"""
    if os.path.exists(CONTENT_FILE):
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_content(content: Dict[str, Any]) -> None:
    """Save content to JSON file"""
    os.makedirs(os.path.dirname(CONTENT_FILE), exist_ok=True)
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    print(f"Content saved to {CONTENT_FILE}")

def add_team_member() -> None:
    """Add a new team member"""
    content = load_content()
    if 'team' not in content:
        content['team'] = {'title': 'Тим', 'members': []}
    
    print("\n=== Додавање нов член на тимот ===")
    name = input("Име и презиме: ")
    role = input("Улога (опционално): ")
    affiliation = input("Институција: ")
    bio = input("Кратка биографија (опционално): ")
    image = input("Патека до слика (опционално): ")
    
    member = {
        "name": name,
        "role": role if role else None,
        "affiliation": affiliation,
        "image": image if image else None,
        "bio": bio if bio else None
    }
    
    content['team']['members'].append(member)
    save_content(content)
    print(f"✅ Додаден е членот: {name}")

def add_gallery_image() -> None:
    """Add a new image to gallery"""
    content = load_content()
    if 'gallery' not in content:
        content['gallery'] = {'title': 'Галерија', 'sections': []}
    
    print("\n=== Додавање нова слика во галеријата ===")
    
    # Show existing sections
    if content['gallery']['sections']:
        print("Постоечки секции:")
        for i, section in enumerate(content['gallery']['sections']):
            print(f"{i+1}. {section['title']}")
    
    section_choice = input("Избери секција (број) или внеси име за нова секција: ")
    
    try:
        section_idx = int(section_choice) - 1
        if 0 <= section_idx < len(content['gallery']['sections']):
            section = content['gallery']['sections'][section_idx]
        else:
            raise ValueError
    except ValueError:
        # Create new section
        section = {
            'title': section_choice,
            'images': []
        }
        content['gallery']['sections'].append(section)
    
    src = input("Патека до сликата (нпр. /static/img/research/slika1.jpg): ")
    alt = input("Alt текст за сликата: ")
    caption = input("Опис на сликата (опционално): ")
    
    image = {
        "src": src,
        "alt": alt,
        "caption": caption if caption else None
    }
    
    section['images'].append(image)
    save_content(content)
    print(f"✅ Додадена е сликата во секцијата: {section['title']}")

def add_research_section() -> None:
    """Add a new research section"""
    content = load_content()
    if 'research' not in content:
        content['research'] = {'title': 'Опис на истражување', 'sections': []}
    
    print("\n=== Додавање нова секција во истражувањето ===")
    title = input("Наслов на секцијата: ")
    
    print("Внесете содржина (притиснете Enter два пати за завршување):")
    paragraphs = []
    while True:
        line = input()
        if line == "" and paragraphs and paragraphs[-1] == "":
            break
        paragraphs.append(line)
    
    # Remove empty last paragraph
    if paragraphs and paragraphs[-1] == "":
        paragraphs.pop()
    
    section = {
        "title": title,
        "content": paragraphs
    }
    
    content['research']['sections'].append(section)
    save_content(content)
    print(f"✅ Додадена е секцијата: {title}")

def view_content() -> None:
    """View current content structure"""
    content = load_content()
    print("\n=== Преглед на содржината ===")
    print(json.dumps(content, ensure_ascii=False, indent=2))

def main():
    """Main menu"""
    while True:
        print("\n" + "="*50)
        print("СИСТЕМ ЗА УПРАВУВАЊЕ СО СОДРЖИНА")
        print("="*50)
        print("1. Додај член на тимот")
        print("2. Додај слика во галеријата")  
        print("3. Додај секција во истражувањето")
        print("4. Прегледај ја содржината")
        print("5. Излез")
        
        choice = input("\nИзбери опција (1-5): ")
        
        if choice == '1':
            add_team_member()
        elif choice == '2':
            add_gallery_image()
        elif choice == '3':
            add_research_section()
        elif choice == '4':
            view_content()
        elif choice == '5':
            print("Довидување!")
            break
        else:
            print("❌ Невалиден избор. Обиди се повторно.")

if __name__ == '__main__':
    main()
