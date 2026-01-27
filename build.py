#!/usr/bin/env python3
"""Build script to generate index.html from HTML tools in the repository."""

import os
from pathlib import Path


def get_tool_name(filename: str) -> str:
    """Convert filename to display name (e.g., 'pairwise-ratings' -> 'Pairwise Ratings')."""
    name = filename.replace('.html', '').replace('-', ' ').replace('_', ' ')
    return name.title()


def get_description(html_file: Path) -> str | None:
    """Get description from companion .md file if it exists."""
    md_file = html_file.with_suffix('.md')
    if md_file.exists():
        with open(md_file, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            # Skip if it's a markdown header
            if first_line.startswith('#'):
                return None
            return first_line if first_line else None
    return None


def build_index(tools_dir: Path) -> str:
    """Generate index.html content."""
    html_files = sorted(tools_dir.glob('*.html'))
    # Exclude index.html itself
    html_files = [f for f in html_files if f.name != 'index.html']

    tools_list = []
    for html_file in html_files:
        name = get_tool_name(html_file.name)
        description = get_description(html_file)
        tools_list.append({
            'filename': html_file.name,
            'name': name,
            'description': description
        })

    # Generate HTML
    tools_html = ''
    for tool in tools_list:
        desc_html = f'<span class="description"> - {tool["description"]}</span>' if tool['description'] else ''
        tools_html += f'        <li><a href="{tool["filename"]}">{tool["name"]}</a>{desc_html}</li>\n'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fab AI Internal Tools</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            border-bottom: 2px solid #333;
            padding-bottom: 0.5rem;
        }}
        ul {{
            list-style: none;
            padding: 0;
        }}
        li {{
            padding: 0.75rem 0;
            border-bottom: 1px solid #eee;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
            font-weight: 500;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .description {{
            color: #666;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <h1>Fab AI Internal Tools</h1>
    <ul>
{tools_html}    </ul>
</body>
</html>
'''


def main():
    tools_dir = Path(__file__).parent
    index_content = build_index(tools_dir)

    index_path = tools_dir / 'index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)

    print(f'Generated {index_path}')


if __name__ == '__main__':
    main()
