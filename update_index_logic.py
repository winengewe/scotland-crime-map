import os

file_path = r"C:\Users\vince\OneDrive\Documents\Antigravity Skills\scotland-crime-map\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update relatedNews logic in openDrawer
old_drawer_code = """            const relatedNews = incidentsData.map(inc => {
                let isSpatial = false;
                if (inc.latitude && inc.longitude && lat && lon) {
                    const dist = getDistance(lat, lon, inc.latitude, inc.longitude);
                    if (dist <= 800) isSpatial = true;
                }
                return { ...inc, isSpatial };
            }).filter(inc => {
                if (inc.isSpatial) return true;
                if (isCity) {
                    const title = inc.title.toLowerCase();
                    const location = (inc.location_name || "").toLowerCase();
                    const incidentCity = (inc.city || "").toLowerCase();
                    return title.includes(baseName) ||
                           location.includes(baseName) ||
                           (incidentCity && (incidentCity.includes(baseName) || incidentCity.includes(parentCity)));
                }
                return false;
            });"""

new_drawer_code = """            const relatedNews = incidentsData.map(inc => {
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

# 2. Update updateIntelligenceFeed logic
old_feed_code = """            const displayData = visibleIncidents.length > 0 ? visibleIncidents : incidentsData.slice(0, 15);

            if (displayData.length === 0) {
                container.innerHTML = '<div class="p-4 text-center text-[10px] font-bold text-slate-400 uppercase tracking-widest">No Recent Reports Found</div>';
                return;
            }

            container.innerHTML = '';
            displayData.forEach(inc => {"""

new_feed_code = """            const displayData = visibleIncidents;

            if (displayData.length === 0) {
                container.innerHTML = '<div class="p-4 text-center text-[10px] font-bold text-slate-400 uppercase tracking-widest">No local reports found for this view</div>';
                return;
            }

            container.innerHTML = '';
            displayData.forEach(inc => {"""

if old_drawer_code in content:
    content = content.replace(old_drawer_code, new_drawer_code)
    print("Successfully replaced openDrawer logic.")
else:
    print("Could not find old openDrawer logic.")

if old_feed_code in content:
    content = content.replace(old_feed_code, new_feed_code)
    print("Successfully replaced updateIntelligenceFeed logic.")
else:
    print("Could not find old updateIntelligenceFeed logic.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("File written successfully.")
