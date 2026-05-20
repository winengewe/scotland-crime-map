import os

file_path = r"C:\Users\vince\OneDrive\Documents\Antigravity Skills\scotland-crime-map\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update relatedNews logic in openDrawer
# Using a more robust matching strategy by looking for key parts of the function
start_marker = "const relatedNews = incidentsData.map(inc => {"
end_marker = "            });"

start_idx = content.find(start_marker)
if start_idx != -1:
    # Find the end of this specific block. It's followed by "const spatialCount"
    next_block_marker = "const spatialCount = relatedNews.filter(inc => inc.isSpatial).length;"
    end_idx = content.find(next_block_marker, start_idx)
    
    if end_idx != -1:
        # We want to replace from start_idx up to the line before next_block_marker
        # Let's find the actual end of the relatedNews assignment
        actual_end_idx = content.rfind("});", start_idx, end_idx) + 3
        
        new_drawer_code = """const relatedNews = incidentsData.map(inc => {
                let isSpatial = false;
                if (inc.latitude && inc.longitude && lat && lon) {
                    const dist = getDistance(lat, lon, inc.latitude, inc.longitude);
                    if (dist <= 1000) isSpatial = true;
                }
                return { ...inc, isSpatial };
            }).filter(inc => {
                if (isCity) {
                    const title = (inc.title || "").toLowerCase().trim();
                    const incidentCity = (inc.city || "").toLowerCase().trim();
                    if (!baseName || baseName.trim() === "") return false;
                    return (incidentCity === baseName) || title.includes(baseName);
                } else {
                    return inc.isSpatial;
                }
            });"""
        
        content = content[:start_idx] + new_drawer_code + content[actual_end_idx:]
        print("Successfully replaced openDrawer logic.")
    else:
        print("Could not find end of openDrawer logic.")
else:
    print("Could not find start of openDrawer logic.")

# 2. Update updateIntelligenceFeed logic (already done, but let's ensure it's correct)
# If it was already replaced, the old_feed_code won't be found.
# Let's check if the new code is already there.

new_feed_code_check = "const displayData = visibleIncidents;"
if new_feed_code_check in content:
    print("updateIntelligenceFeed logic already updated or found.")
else:
    # Try replacing again if not found
    old_feed_marker = "const displayData = visibleIncidents.length > 0 ? visibleIncidents : incidentsData.slice(0, 15);"
    if old_feed_marker in content:
        # Find the block
        f_start = content.find(old_feed_marker)
        f_end_marker = "displayData.forEach(inc => {"
        f_end = content.find(f_end_marker, f_start) + len(f_end_marker)
        
        new_feed_full = """const displayData = visibleIncidents;

            if (displayData.length === 0) {
                container.innerHTML = '<div class="p-4 text-center text-[10px] font-bold text-slate-400 uppercase tracking-widest">No local reports found for this view</div>';
                return;
            }

            container.innerHTML = '';
            displayData.forEach(inc => {"""
        
        content = content[:f_start] + new_feed_full + content[f_end:]
        print("Successfully replaced updateIntelligenceFeed logic.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("File written successfully.")
