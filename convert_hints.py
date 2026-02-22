#!/usr/bin/env python3
import re
import sys

def parse_hints_file(filename):
    """Parse the Inform6 hints file and extract menus and hints."""
    with open(filename, 'r') as f:
        content = f.read()
    
    menus = []
    hints = []
    
    # Find all Menu objects
    menu_pattern = r'Menu\s+(\w+)\s+"([^"]+)"'
    for match in re.finditer(menu_pattern, content):
        menu_id = match.group(1)
        menu_title = match.group(2)
        
        menus.append({
            'id': menu_id,
            'title': menu_title,
            'hints': []
        })
    
    # Find all Option (Hint) objects
    # Pattern: Option -> HintName "Title" ... with in_menu MenuName, the_hints "line1" "line2" ...
    hint_pattern = r'Option\s+(?:->)?\s*(\w+)\s+"([^"]+)".*?in_menu\s+(\w+).*?the_hints\s+((?:"[^"]*"\s*)+)'
    
    for match in re.finditer(hint_pattern, content, re.DOTALL):
        hint_id = match.group(1)
        hint_title = match.group(2)
        menu_id = match.group(3)
        hints_block = match.group(4)
        
        # Extract all quoted strings from the_hints block
        hint_lines = re.findall(r'"([^"]*)"', hints_block)
        
        hint_obj = {
            'id': hint_id,
            'title': hint_title,
            'lines': hint_lines,
            'menu': menu_id
        }
        
        hints.append(hint_obj)
        
        # Add this hint to its menu
        for menu in menus:
            if menu['id'] == menu_id:
                menu['hints'].append(hint_id)
                break
    
    return menus, hints

def generate_html(menus, hints):
    """Generate HTML with interactive blurred hints."""
    
    # Create a lookup dict for hints
    hints_dict = {h['id']: h for h in hints}
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Our Lady of Thorns - Hints</title>
    <style>
        body {
            font-family: Georgia, serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            line-height: 1.6;
            background: #f5f5f0;
            color: #333;
        }
        h1 {
            text-align: center;
            color: #5a3825;
            border-bottom: 2px solid #5a3825;
            padding-bottom: 10px;
        }
        .menu {
            background: white;
            margin: 20px 0;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .menu-title {
            font-size: 1.2em;
            font-weight: bold;
            color: #5a3825;
            cursor: pointer;
            padding: 10px;
            background: #f9f9f9;
            border-radius: 3px;
            user-select: none;
        }
        .menu-title:hover {
            background: #eee;
        }
        .menu-title::before {
            content: '▶ ';
            display: inline-block;
            transition: transform 0.3s;
        }
        .menu-title.active::before {
            transform: rotate(90deg);
        }
        .menu-content {
            display: none;
            margin-top: 15px;
        }
        .menu-content.active {
            display: block;
        }
        .hint-section {
            margin: 15px 0;
            padding: 10px;
            background: #fafafa;
            border-left: 3px solid #5a3825;
        }
        .hint-title {
            font-weight: bold;
            color: #5a3825;
            margin-bottom: 10px;
        }
        .hint-line {
            margin: 8px 0;
            padding: 8px;
            background: white;
            border-radius: 3px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .hint-line.blurred {
            filter: blur(8px);
            user-select: none;
        }
        .hint-line.blurred:hover {
            filter: blur(6px);
            background: #f0f0f0;
        }
        .hint-line.revealed {
            filter: none;
            background: #fff9e6;
        }
        .hint-number {
            display: inline-block;
            width: 30px;
            color: #888;
            font-weight: bold;
        }
        .instructions {
            background: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
            border-left: 4px solid #5a9ab8;
        }
    </style>
</head>
<body>
    <h1>Our Lady of Thorns<br><small style="font-size:0.6em; color: #888;">Hints</small></h1>
    
    <div class="instructions">
        <strong>How to use these hints:</strong><br>
        Click on a section title to expand it. Click on any blurred hint to reveal it. 
        Hints are ordered from gentle nudges to explicit solutions—try to use as few as possible!
    </div>
'''
    
    # Generate menu sections
    for menu in menus:
        if not menu['hints']:  # Skip empty menus
            continue
            
        html += f'    <div class="menu">\n'
        html += f'        <div class="menu-title" onclick="toggleMenu(this, \'{menu["id"]}\')">{menu["title"]}</div>\n'
        html += f'        <div class="menu-content" id="{menu["id"]}">\n'
        
        # Add hints for this menu
        for hint_id in menu['hints']:
            if hint_id in hints_dict:
                hint = hints_dict[hint_id]
                html += f'            <div class="hint-section">\n'
                html += f'                <div class="hint-title">{hint["title"]}</div>\n'
                
                for i, line in enumerate(hint['lines'], 1):
                    # Handle multiline strings and escape HTML
                    line_html = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    line_html = line_html.replace('^', '<br>')  # Inform uses ^ for newline
                    
                    html += f'                <div class="hint-line blurred" onclick="revealHint(this)">\n'
                    html += f'                    <span class="hint-number">{i}.</span> {line_html}\n'
                    html += f'                </div>\n'
                
                html += f'            </div>\n'
        
        html += f'        </div>\n'
        html += f'    </div>\n'
    
    html += '''
    <script>
        function toggleMenu(titleElement, menuId) {
            const menu = document.getElementById(menuId);
            menu.classList.toggle('active');
            titleElement.classList.toggle('active');
        }
        
        function revealHint(element) {
            element.classList.remove('blurred');
            element.classList.add('revealed');
            element.style.cursor = 'default';
        }
    </script>
</body>
</html>
'''
    
    return html

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_hints.py game_hints.inf")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = "html/hints.html"
    
    print(f"Parsing {input_file}...")
    menus, hints = parse_hints_file(input_file)
    
    print(f"Found {len(menus)} menus and {len(hints)} hints")
    
    print(f"Generating HTML...")
    html = generate_html(menus, hints)
    
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"Created {output_file}")

if __name__ == '__main__':
    main()
