import os
import re
import markdown

def main():
    md_files = [f for f in os.listdir('.') if re.match(r'^\d+-.*\.md$', f)]
    md_files.sort()
    
    sections = []
    nav_links = []
    
    for filename in md_files:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
            
        title_match = re.search(r'^#\s+(.*)', text, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
            # Increase all headings by 1 level to fit inside the page structure
            text = re.sub(r'^#', '##', text, flags=re.MULTILINE)
        else:
            title = filename.replace('.md', '').split('-', 1)[-1].replace('-', ' ').title()
            
        section_id = filename.replace('.md', '').split('-', 1)[-1]
        
        # parse markdown
        html_content = markdown.markdown(text, extensions=['fenced_code', 'tables'])
        # styling overrides for docs.html
        html_content = html_content.replace('<table>', '<table class="docs-table">')
        html_content = html_content.replace('<code>', '<code class="code-inline">')
        html_content = html_content.replace('<pre><code class="code-inline">', '<pre><code>')
        
        section_html = f'<section id="{section_id}" class="docs-section">\n{html_content}\n</section>'
        sections.append(section_html)
        
        nav_links.append(f'<a href="#{section_id}" class="nav-link">{title}</a>')

    nav_html = '<nav class="sidebar-nav">\n<div class="nav-group">\n<div class="nav-group-title">DOCUMENTATION</div>\n' + '\n'.join(nav_links) + '\n</div>\n</nav>'
    main_html = '''<main class="docs-content">
            <div class="docs-header">
                <h1 class="docs-main-title">Engram Documentation</h1>
                <p class="docs-version">CONNECT ANY AGENT. ANY TOOL. ANY API.</p>
            </div>
            <hr class="docs-divider">
''' + '\n<hr class="docs-divider">\n'.join(sections) + '''
            <div style="margin-top: 40px; font-size: 0.9em; color: #666; font-weight: 500; padding: 20px 0; border-top: 1px solid #eee;">
                <strong>Documentation Hub</strong>
            </div>
        </main>'''

    with open('docs.html', 'r', encoding='utf-8') as f:
        docs = f.read()
    
    docs = re.sub(r'<nav class="sidebar-nav">.*?</nav>', lambda m: nav_html, docs, flags=re.DOTALL)
    docs = re.sub(r'<main class="docs-content">.*?</main>', lambda m: main_html, docs, flags=re.DOTALL)
    
    with open('docs.html', 'w', encoding='utf-8') as f:
        f.write(docs)
    print("Done building docs.")

if __name__ == '__main__':
    main()
