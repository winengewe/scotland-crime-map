import os
import re

file_path = r"C:\Users\vince\OneDrive\Documents\Antigravity Skills\scotland-crime-map\index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Try to find the relatedNews assignment and the if check following it
pattern = r"(const relatedNews = incidentsData\.filter\(inc =>.*?inc\.title\.toLowerCase\(\)\.includes\(nameLower\).*?\).*?;)\s+(if \(relatedNews\.length === 0\) {)"

def replace_func(match):
    related_news_code = match.group(1)
    if_check_code = match.group(2)
    return f"{related_news_code}\n\n            // Update AI Summary\n            document.getElementById('drawer-ai-summary').innerText = generateAISummary(data, rankIndex, relatedNews);\n\n            {if_check_code}"

new_content = re.sub(pattern, replace_func, content, flags=re.DOTALL)

if new_content != content:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Update complete")
else:
    print("Could not find insertion point with regex")
