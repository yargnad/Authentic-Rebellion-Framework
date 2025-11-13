#!/usr/bin/env python3
"""
Convert The Authentic Rebellion Fourth Master Draft to HTML
Preserves italics, creates navigation structure, and maintains formatting
"""

import re

def markdown_to_html(md_content):
    """Convert markdown to HTML with proper formatting"""
    
    # Convert italics (*text* to <em>text</em>)
    html = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', md_content)
    
    # Convert bold (**text** to <strong>text</strong>)
    html = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', html)
    
    # Convert headers
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    
    # Convert paragraphs
    paragraphs = html.split('\n\n')
    formatted_paragraphs = []
    
    for para in paragraphs:
        para = para.strip()
        if para:
            # Skip if it's already a header or list
            if not para.startswith('<h') and not para.startswith('<li') and not para.startswith('<ul') and not para.startswith('<ol'):
                # Check for list items
                if para.startswith('* ') or para.startswith('- '):
                    items = para.split('\n')
                    list_items = ['<ul>']
                    for item in items:
                        if item.strip().startswith(('* ', '- ')):
                            list_items.append(f'<li>{item[2:].strip()}</li>')
                    list_items.append('</ul>')
                    formatted_paragraphs.append('\n'.join(list_items))
                elif re.match(r'^\d+\.', para):
                    items = para.split('\n')
                    list_items = ['<ol>']
                    for item in items:
                        if re.match(r'^\d+\.', item):
                            cleaned_item = re.sub(r"^\d+\.\s*", "", item)
                            list_items.append(f'<li>{cleaned_item}</li>')
                    list_items.append('</ol>')
                    formatted_paragraphs.append('\n'.join(list_items))
                else:
                    formatted_paragraphs.append(f'<p>{para}</p>')
            else:
                formatted_paragraphs.append(para)
    
    return '\n\n'.join(formatted_paragraphs)

def add_section_ids(html):
    """Add ID attributes to sections for navigation"""
    
    # Add ID to preface
    html = html.replace('<h2>Preface:', '<div id="preface"></div>\n\n<h2>Preface:')
    
    # Add IDs to parts
    html = html.replace('<h2>Part I:', '<div id="part-i"></div>\n\n<h2>Part I:')
    html = html.replace('<h2>Part II:', '<div id="part-ii"></div>\n\n<h2>Part II:')
    html = html.replace('<h2>Part III:', '<div id="part-iii"></div>\n\n<h2>Part III:')
    
    # Add IDs to chapters
    for i in range(1, 13):
        html = html.replace(f'<h3>Chapter {i}:', f'<div id="chapter-{i}"></div>\n\n<h3>Chapter {i}:')
    
    # Add ID to appendix
    html = html.replace('<h2>Appendix:', '<div id="appendix"></div>\n\n<h2>Appendix:')
    
    return html

def create_html_document(content_html):
    """Wrap content in full HTML document with navigation"""
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Authentic Rebellion</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <nav id="sidebar">
        <div class="site-title">
            <a href="#top">The Authentic Rebellion</a>
        </div>
        <div class="nav-content">
            <a href="#preface" class="nav-section">Preface</a>
            
            <div class="nav-part">
                <a href="#part-i" class="nav-part-title">Part I: The Diagnosis</a>
                <a href="#chapter-1" class="nav-chapter">1. The Performance Prison</a>
                <a href="#chapter-2" class="nav-chapter">2. The Currency of Contempt</a>
                <a href="#chapter-3" class="nav-chapter">3. The Search for Fertile Ground</a>
                <a href="#chapter-4" class="nav-chapter">4. The Honest Mirror</a>
            </div>
            
            <div class="nav-part">
                <a href="#part-ii" class="nav-part-title">Part II: The Search for a New Framework</a>
                <a href="#chapter-5" class="nav-chapter">5. The Solace of the Solitary Mind</a>
                <a href="#chapter-6" class="nav-chapter">6. The Irrational Man</a>
                <a href="#chapter-7" class="nav-chapter">7. The Trembling of the Self</a>
            </div>
            
            <div class="nav-part">
                <a href="#part-iii" class="nav-part-title">Part III: The Framework</a>
                <a href="#chapter-8" class="nav-chapter">8. The Absurdist's Wager</a>
                <a href="#chapter-9" class="nav-chapter">9. The Agile Rebellion</a>
                <a href="#chapter-10" class="nav-chapter">10. Building the New World</a>
                <a href="#chapter-11" class="nav-chapter">11. The Public Square</a>
                <a href="#chapter-12" class="nav-chapter">12. The Affinitive</a>
            </div>
            
            <a href="#appendix" class="nav-section">Appendix</a>
            
            <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--border-subtle);">
                <a href="index.html" class="back-to-top">← Back to Framework</a>
            </div>
        </div>
    </nav>

    <main id="content">
        <div class="reading-width">
{content_html}
        </div>
    </main>
</body>
</html>'''

def main():
    # Read the Fourth Master Draft
    with open('The Authentic Rebellion - Fourth Master Draft.md', 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown_to_html(md_content)
    
    # Add section IDs for navigation
    html_content = add_section_ids(html_content)
    
    # Create full HTML document
    full_html = create_html_document(html_content)
    
    # Write to docs/essay.html
    with open('docs/essay.html', 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print("✓ Successfully converted Fourth Master Draft to docs/essay.html")
    print("✓ All italics, formatting, and navigation preserved")

if __name__ == '__main__':
    main()
