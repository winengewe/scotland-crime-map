
import re

file_path = r"C:\Users\vince\OneDrive\Documents\Antigravity Skills\scotland-crime-map\index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the double-replacement in generateAISummary
bad_pattern = r'const spatialCount = incidents\.filter\(inc => inc\.isSpatial\)\.length;\s*if \(spatialCount > 0\) \{\s*summary \+= ` System detected \[\$\{spatialCount\}\] recent police interventions within 800m of this location\.`;\s*\} else\s*const spatialCount = incidents\.filter\(inc => inc\.isSpatial\)\.length;\s*if \(spatialCount > 0\) \{\s*summary \+= ` System detected \[\$\{spatialCount\}\] recent police interventions within 800m of this location\.`;\s*\}'

good_code = r'const spatialCount = incidents.filter(inc => inc.isSpatial).length;\n            if (spatialCount > 0) {\n                summary += ` System detected [${spatialCount}] recent police interventions within 800m of this location.`;\n            }'

content = re.sub(bad_pattern, good_code, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleaned up generateAISummary duplication.")
