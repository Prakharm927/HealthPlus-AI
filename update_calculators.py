# Quick script to update all calculator pages with new theme
import os
import re

calc_dir = r"c:/Users/prakh/OneDrive/Desktop/health ai/OpenHealth/templates/calculators"

files = ["diabetes.html", "liver.html", "breast_cancer.html", "parkinsons.html", "kidney.html", "brain_tumor.html"]

for filename in files:
    filepath = os.path.join(calc_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix navbar - move home link to left
    content = re.sub(
        r'<div class="nav-content">\s*<div class="logo">',
        '<div class="nav-content">\n            <a href="/" class="back-link">← Home</a>\n            <div class="logo">',
        content
    )
    content = re.sub(
        r'</div>\s*<a href="/" style="color: rgba\(255,255,255,0\.7\); text-decoration: none; font-size: 14px;">← Home</a>',
        '</div>',
        content
    )
    
    # Update nav-content styling
    content = re.sub(
        r'justify-content: space-between;\s*align-items: center;',
        'align-items: center;\n            gap: 24px;',
        content
    )
    
    # Add margin-left: auto to logo
    content = re.sub(
        r'(\.logo \{[^}]*gap: 8px;)',
        r'\1\n            margin-left: auto;',
        content
    )
    
    # Update badge color to purple gradient
    content = re.sub(
        r'background: #007AFF;(\s*padding: 2px 8px;)',
        r'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\1',
        content
    )
    
    # Add back-link styles after badge
    if '.back-link' not in content:
        content = re.sub(
            r'(\.badge \{[^}]*\})',
            r'\1\n        .back-link {\n            color: rgba(255,255,255,0.8);\n            text-decoration: none;\n            font-size: 14px;\n            font-weight: 500;\n            transition: all 0.2s;\n        }\n        .back-link:hover {\n            color: #fff;\n        }',
            content
        )
    
    # Update button color to purple gradient
    content = re.sub(
        r'background: #007AFF;(\s*color: #fff;\s*padding: 14px)',
        r'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\1',
        content
    )
    
    # Update button hover
    content = re.sub(
        r'background: #0051D5;\s*transform: translateY\(-1px\);',
        'background: linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%);\n            transform: translateY(-1px);\n            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);',
        content
    )
    
    # Update input focus border
    content = re.sub(
        r'border-color: #007AFF;',
        'border-color: #667eea;',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {filename}")

print("\n🎉 All calculator pages updated!")
