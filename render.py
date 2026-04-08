import markdown
import re

def render_docs():
    with open('c:/Users/galan/landing_page/docs.html', 'r', encoding='utf-8') as f:
        text = f.read()

    # Convert markdown to HTML
    html_content = markdown.markdown(text, extensions=['fenced_code', 'tables', 'toc'])

    # Build the full HTML template
    template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Engram Documentation</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Mono:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-body: #ffffff;
            --bg-sidebar: #fafafa;
            --border-color: #eaeaea;
            --text-main: #222222;
            --text-muted: #666666;
            --accent: #f5c518;
            --accent-bg: #fffbf0;
            --code-bg: #f5f5f5;
            --hl-active-bg: #fff;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-body);
            color: var(--text-main);
            font-family: 'Inter', -apple-system, sans-serif;
            display: flex;
            min-height: 100vh;
            line-height: 1.6;
            letter-spacing: -0.01em;
        }

        .layout-container {
            display: flex;
            width: 100%;
            margin: 0 auto;
        }

        /* Left Sidebar */
        .sidebar {
            width: 260px;
            background-color: var(--bg-sidebar);
            border-right: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            height: 100vh;
            overflow-y: auto;
            padding: 32px 0;
            flex-shrink: 0;
        }

        .sidebar-nav {
            display: flex;
            flex-direction: column;
        }

        .nav-item {
            padding: 10px 24px;
            text-decoration: none;
            color: var(--text-main);
            font-size: 14px;
            font-weight: 500;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s;
        }
        
        .nav-item:hover {
            background-color: #efefef;
        }

        .nav-item.active {
            font-weight: 600;
            background-color: var(--hl-active-bg);
            border-left: 3px solid var(--accent);
            color: var(--accent);
            text-shadow: 0 0 1px rgba(245, 197, 24, 0.5);
        }

        .nav-item-icon::after {
            content: "›";
            font-size: 18px;
            color: #999;
        }

        /* Sub nav items */
        .sub-nav {
            padding-left: 12px;
            display: flex;
            flex-direction: column;
        }
        .sub-nav .nav-item {
            font-size: 13px;
            padding: 8px 24px 8px 36px;
            color: #555;
            font-weight: 400;
            border-left: none;
        }
        .sub-nav .nav-item.active {
            color: var(--accent);
            font-weight: 500;
            background: transparent;
        }

        /* Main Content */
        .main-content {
            flex: 1;
            padding: 48px 80px;
            max-width: 900px;
        }

        .breadcrumbs {
            font-family: 'Space Mono', monospace;
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 32px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .breadcrumbs span.active {
            color: var(--accent);
            font-weight: 700;
        }

        h1 {
            font-size: 42px;
            font-weight: 700;
            letter-spacing: -1.5px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        h1 code {
            background-color: #f0f0f0;
            padding: 2px 16px;
            border-radius: 8px;
            font-size: 38px;
            font-family: 'Space Mono', monospace;
            color: #111;
        }

        h2 {
            font-size: 28px;
            font-weight: 600;
            letter-spacing: -0.5px;
            margin-top: 56px;
            margin-bottom: 24px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 16px;
        }

        h3 {
            font-size: 20px;
            font-weight: 600;
            margin-top: 32px;
            margin-bottom: 16px;
        }

        p {
            margin-bottom: 20px;
            font-size: 16px;
            color: #333;
        }

        ul, ol {
            margin-bottom: 24px;
            padding-left: 24px;
            color: #333;
        }

        li {
            margin-bottom: 10px;
        }

        code {
            font-family: 'Space Mono', monospace;
            background-color: var(--code-bg);
            padding: 3px 6px;
            border-radius: 4px;
            font-size: 0.85em;
            color: #d13a82; 
        }

        pre {
            background-color: #1a1a1a;
            color: #f8f8f2;
            padding: 24px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 24px 0;
            font-family: 'Space Mono', monospace;
            font-size: 14px;
            line-height: 1.5;
        }

        pre code {
            background-color: transparent;
            padding: 0;
            border-radius: 0;
            color: inherit;
        }

        blockquote {
            border-left: 4px solid var(--text-muted);
            background-color: var(--bg-sidebar);
            padding: 16px 24px;
            margin: 24px 0;
            border-radius: 0 8px 8px 0;
            color: #555;
        }

        blockquote p {
            margin-bottom: 0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 24px 0;
        }

        th, td {
            text-align: left;
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-color);
        }

        th {
            background-color: var(--bg-sidebar);
            font-weight: 600;
            font-size: 14px;
        }

        /* Right Sidebar (TOC) */
        .toc-sidebar {
            width: 280px;
            position: sticky;
            top: 0;
            height: 100vh;
            padding: 48px 32px;
            overflow-y: auto;
            border-left: 1px solid var(--border-color);
            flex-shrink: 0;
            background: #ffffff;
        }

        .toc-title {
            font-size: 13px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 16px;
            font-family: 'Inter', sans-serif;
        }

        .toc-nav {
            list-style: none;
            padding-left: 0;
        }

        .toc-link {
            display: block;
            text-decoration: none;
            color: #555;
            font-size: 13px;
            margin-bottom: 12px;
            transition: color 0.2s;
            line-height: 1.4;
        }

        .toc-link:hover {
            color: var(--text-main);
        }

        .toc-link.active {
            color: var(--accent);
            font-weight: 600;
        }

        /* Responsive */
        @media (max-width: 1200px) {
            .toc-sidebar {
                display: none;
            }
        }

        @media (max-width: 768px) {
            .sidebar {
                display: none;
            }
            .main-content {
                padding: 32px 24px;
            }
        }
    </style>
</head>
<body>
    <div class="layout-container">
        <!-- Left Sidebar -->
        <aside class="sidebar">
            <nav class="sidebar-nav">
                <a href="#" class="nav-item">Getting Started <span class="nav-item-icon"></span></a>
                <a href="#" class="nav-item active">Using Engram <span class="nav-item-icon"></span></a>
                <div class="sub-nav">
                    <a href="#quickstart" class="nav-item">Quickstart</a>
                    <a href="#installation" class="nav-item">Installation</a>
                    <a href="#docker-kubernetes-setup" class="nav-item">Docker & Kubernetes</a>
                </div>
                <a href="#" class="nav-item">Features <span class="nav-item-icon"></span></a>
                <a href="#" class="nav-item">Messaging Platforms <span class="nav-item-icon"></span></a>
                <a href="#" class="nav-item">Integrations <span class="nav-item-icon"></span></a>
                <a href="#" class="nav-item">Guides & Tutorials <span class="nav-item-icon"></span></a>
                <a href="#" class="nav-item">Developer Guide <span class="nav-item-icon"></span></a>
            </nav>
        </aside>

        <!-- Main Content -->
        <main class="main-content">
            <div class="breadcrumbs">
                ⌂ &rsaquo; Using Engram &rsaquo; <span class="active">Documentation</span>
            </div>

            <div class="docs-body-content">
                {{content}}
            </div>
        </main>

        <!-- Right Sidebar (TOC) -->
        <aside class="toc-sidebar">
            <div class="toc-title">On this page</div>
            <nav class="toc-nav">
                <a href="#quickstart" class="toc-link">Quickstart</a>
                <a href="#1-install-engram" class="toc-link">Install Engram</a>
                <a href="#2-start-the-gateway" class="toc-link">Start the Gateway</a>
                <a href="#3-register-your-first-tool" class="toc-link">Register Your First Tool</a>
                <a href="#installation" class="toc-link">Installation</a>
                <a href="#docker-kubernetes-setup" class="toc-link">Docker & K8s Setup</a>
            </nav>
        </aside>
    </div>
</body>
</html>
"""

    # For replacing headers correctly to add ids if markdown module didn't correctly add them or we want styling
    html_file = template.replace('{{content}}', html_content)

    with open('c:/Users/galan/landing_page/docs.html', 'w', encoding='utf-8') as f:
        f.write(html_file)

if __name__ == "__main__":
    render_docs()
