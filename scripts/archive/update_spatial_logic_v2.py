
import re

file_path = r"C:\Users\vince\OneDrive\Documents\Antigravity Skills\scotland-crime-map\index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add getDistance helper function (using plain ASCII variable names)
# We already added it once, but let's make sure it's correct and not duplicated or broken.
# If it's there but broken, we'll replace it.

get_distance_code = """
        function getDistance(lat1, lon1, lat2, lon2) {
            const R = 6371e3; // metres
            const phi1 = lat1 * Math.PI / 180;
            const phi2 = lat2 * Math.PI / 180;
            const deltaPhi = (lat2 - lat1) * Math.PI / 180;
            const deltaLambda = (lon2 - lon1) * Math.PI / 180;
            const a = Math.sin(deltaPhi / 2) * Math.sin(deltaPhi / 2) +
                      Math.cos(phi1) * Math.cos(phi2) *
                      Math.sin(deltaLambda / 2) * Math.sin(deltaLambda / 2);
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
            return R * c;
        }
"""

# Remove any existing getDistance (to fix potential encoding issues)
content = re.sub(r'function getDistance\(.*?\)\s*\{.*?\}', '', content, flags=re.DOTALL)

# Insert it before openDrawer
content = content.replace("function openDrawer(data, rankIndex, isCity) {", get_distance_code + "\n        function openDrawer(data, rankIndex, isCity) {")

# 2. Update generateAISummary
# Use a more targeted replacement
old_ai_part = 'if (incidents.length > 0) {\n                summary += " Note: Recent police activity has been detected in this sector; check the live feed below for details.";\n            }'
new_ai_part = """            const spatialCount = incidents.filter(inc => inc.isSpatial).length;
            if (spatialCount > 0) {
                summary += ` System detected [${spatialCount}] recent police interventions within 800m of this location.`;
            } else if (incidents.length > 0) {
                summary += " Note: Recent police activity has been detected in this sector; check the live feed below for details.";
            }"""

if old_ai_part in content:
    content = content.replace(old_ai_part, new_ai_part)
else:
    # Try with different whitespace if needed
    content = re.sub(r'if \(incidents\.length > 0\) \{.*?\}', new_ai_part, content, flags=re.DOTALL, count=1)

# 3. Update openDrawer filtering logic
# We'll target from "const fullName = data.regions.name;" down to "const relatedNews = incidentsData.filter(...});"
# But it's safer to just replace the whole block between "feed.innerHTML = '';" and "// Update AI Summary"

new_filtering_logic = """            feed.innerHTML = '';
            // Filter news - Spatial Incident Matching
            const lat = data.regions.latitude;
            const lon = data.regions.longitude;
            const fullName = data.regions.name;
            const baseName = fullName.split(' - ')[0].trim().toLowerCase();
            const parentCity = (data.cityName || "").toLowerCase();

            const relatedNews = incidentsData.map(inc => {
                let isSpatial = false;
                if (lat && lon && inc.latitude && inc.longitude) {
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
            });
            
            const spatialCount = relatedNews.filter(inc => inc.isSpatial).length;
            const liveActivityEl = document.getElementById('drawer-live-activity');
            if (liveActivityEl) liveActivityEl.innerText = spatialCount;

            // Update AI Summary"""

content = re.sub(r"feed\.innerHTML = '';.*?// Update AI Summary", new_filtering_logic, content, flags=re.DOTALL)

# 4. Update stats grid if not already updated
if 'id="drawer-live-activity"' not in content:
    old_grid = re.search(r'<div class="grid grid-cols-2 gap-4">.*?</div>\s*</div>', content, re.DOTALL)
    if old_grid:
        new_grid = """<div class="grid grid-cols-3 gap-3">
                <div class="bg-slate-50 p-3 rounded-2xl border border-slate-100">
                    <p class="text-[8px] font-black text-slate-400 uppercase tracking-widest mb-1 leading-tight">Safety<br>Rank</p>
                    <p id="drawer-percentile" class="text-sm font-black text-slate-800">-</p>
                </div>
                <div class="bg-slate-50 p-3 rounded-2xl border border-slate-100">
                    <p class="text-[8px] font-black text-slate-400 uppercase tracking-widest mb-1 leading-tight">Yearly<br>Reports</p>
                    <p id="drawer-total-incidents" class="text-sm font-black text-slate-800">-</p>
                </div>
                <div class="bg-slate-50 p-3 rounded-2xl border border-indigo-100 bg-indigo-50/30">
                    <div class="flex items-center gap-1 mb-1">
                        <span class="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse"></span>
                        <p class="text-[8px] font-black text-blue-600 uppercase tracking-widest leading-tight">Recent<br>Activity</p>
                    </div>
                    <p id="drawer-live-activity" class="text-sm font-black text-blue-700">0</p>
                </div>
            </div>"""
        content = content.replace(old_grid.group(0), new_grid)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated index.html with improved logic and fixed encoding.")
