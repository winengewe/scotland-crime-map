
import re

file_path = r"C:\Users\vince\OneDrive\Documents\Antigravity Skills\scotland-crime-map\index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add getDistance helper function before openDrawer
get_distance_js = """
        function getDistance(lat1, lon1, lat2, lon2) {
            const R = 6371e3; // metres
            const φ1 = lat1 * Math.PI / 180;
            const φ2 = lat2 * Math.PI / 180;
            const Δφ = (lat2 - lat1) * Math.PI / 180;
            const Δλ = (lon2 - lon1) * Math.PI / 180;
            const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
                      Math.cos(φ1) * Math.cos(φ2) *
                      Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
            return R * c;
        }

        function openDrawer(data, rankIndex, isCity) {"""

content = content.replace("        function openDrawer(data, rankIndex, isCity) {", get_distance_js)

# 2. Update generateAISummary to include spatial incident message
old_ai_summary_logic = """            if (incidents.length > 0) {
                summary += " Note: Recent police activity has been detected in this sector; check the live feed below for details.";
            }"""

new_ai_summary_logic = """            const spatialCount = incidents.filter(inc => inc.isSpatial).length;
            if (spatialCount > 0) {
                summary += ` System detected [${spatialCount}] recent police interventions within 800m of this location.`;
            } else if (incidents.length > 0) {
                summary += " Note: Recent police activity has been detected in this sector; check the live feed below for details.";
            }"""

content = content.replace(old_ai_summary_logic, new_ai_summary_logic)

# 3. Update openDrawer logic for incident filtering
old_open_drawer_filtering = """            // Filter news - Logic Fix: Broader matching
            const fullName = data.regions.name;
            const baseName = fullName.split(' - ')[0].trim().toLowerCase();
            const parentCity = (data.cityName || "").toLowerCase();

            const relatedNews = incidentsData.filter(inc => {
                const title = inc.title.toLowerCase();
                const location = (inc.location_name || "").toLowerCase();
                const incidentCity = (inc.city || "").toLowerCase();

                return title.includes(baseName) ||
                       location.includes(baseName) ||
                       (incidentCity && (incidentCity.includes(baseName) || incidentCity.includes(parentCity)));
            });"""

new_open_drawer_filtering = """            // Filter news - Spatial Incident Matching
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
                
                // Fallback to name matching for cities or if no coordinates
                const title = inc.title.toLowerCase();
                const location = (inc.location_name || "").toLowerCase();
                const incidentCity = (inc.city || "").toLowerCase();

                if (isCity) {
                    return title.includes(baseName) || 
                           location.includes(baseName) || 
                           (incidentCity && (incidentCity.includes(baseName) || incidentCity.includes(parentCity)));
                }
                return false; // For neighborhood zones, we strictly use 800m spatial matching now
            });
            
            const spatialCount = relatedNews.filter(inc => inc.isSpatial).length;
            document.getElementById('drawer-live-activity').innerText = spatialCount;"""

content = content.replace(old_open_drawer_filtering, new_open_drawer_filtering)

# 4. Update Drawer UI to add "Recent Activity (Live)"
old_stats_grid = """            <div class="grid grid-cols-2 gap-4">
                <div class="bg-slate-50 p-4 rounded-2xl border border-slate-100">
                    <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-1">Safety Rank</p>
                    <p id="drawer-percentile" class="text-lg font-black text-slate-800">-</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-2xl border border-slate-100">
                    <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-1">Incidents</p>
                    <p id="drawer-total-incidents" class="text-lg font-black text-slate-800">-</p>
                </div>
            </div>"""

new_stats_grid = """            <div class="grid grid-cols-3 gap-3">
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

content = content.replace(old_stats_grid, new_stats_grid)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated index.html with Spatial Incident Matching.")
