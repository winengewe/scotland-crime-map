import os

file_path = r"C:\Users\vince\OneDrive\Documents\Antigravity Skills\scotland-crime-map\index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. HTML Update
old_html = """            <div class="grid grid-cols-2 gap-4">
                <div class="bg-slate-50 p-4 rounded-2xl border border-slate-100">
                    <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-1">Safety Rank</p>
                    <p id="drawer-percentile" class="text-lg font-black text-slate-800">-</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-2xl border border-slate-100">
                    <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-1">Incidents</p>
                    <p id="drawer-total-incidents" class="text-lg font-black text-slate-800">-</p>
                </div>
            </div>

            <div>
                <h3 class="text-xs font-black text-slate-400 uppercase tracking-widest mb-4 italic">Local Incident Feed</h3>"""

new_html = """            <div class="grid grid-cols-2 gap-4">
                <div class="bg-slate-50 p-4 rounded-2xl border border-slate-100">
                    <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-1">Safety Rank</p>
                    <p id="drawer-percentile" class="text-lg font-black text-slate-800">-</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-2xl border border-slate-100">
                    <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-1">Incidents</p>
                    <p id="drawer-total-incidents" class="text-lg font-black text-slate-800">-</p>
                </div>
            </div>

            <div class="bg-indigo-50/50 p-6 rounded-3xl border border-indigo-100/50 relative overflow-hidden group">
                <div class="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                    <svg class="w-12 h-12 text-indigo-600" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/></svg>
                </div>
                <h3 class="text-[10px] font-black text-indigo-600 uppercase tracking-[0.2em] mb-3 flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
                    AI Safety Analyst
                </h3>
                <p id="drawer-ai-summary" class="text-xs font-medium text-slate-600 leading-relaxed italic">
                    Analyzing area data zone dynamics...
                </p>
            </div>

            <div>
                <h3 class="text-xs font-black text-slate-400 uppercase tracking-widest mb-4 italic">Local Incident Feed</h3>"""

if old_html in content:
    content = content.replace(old_html, new_html)
else:
    print("Could not find HTML injection point")

# 2. JS Update - generateAISummary function
# Insert before openDrawer or somewhere appropriate
js_func = """
        function generateAISummary(data, rankIndex, incidents) {
            const totalPool = neighborhoodData.length > 0 ? TARGET_COUNT : cityData.length;
            const gradeData = getSafetyGrade(rankIndex, totalPool);
            const areaName = data.regions.name;
            let summary = "";

            if (gradeData.grade === 'A+') {
                summary = `${areaName} is a top-tier safe haven. Statistically within the safest 5% of Scotland, it shows minimal crime density across all monitored categories.`;
            } else if (gradeData.grade === 'A' || gradeData.grade === 'B') {
                summary = `${areaName} maintains a strong safety profile. While minor incidents occur occasionally, the overall environment is significantly more secure than the national average.`;
            } else if (gradeData.grade === 'C' || gradeData.grade === 'D') {
                summary = `${areaName} exhibits moderate activity. We recommend standard situational awareness, especially during late hours, as incident density aligns with urban averages.`;
            } else if (gradeData.grade === 'F') {
                summary = `Caution recommended. ${areaName} is currently flagged for higher incident density. Data suggests prioritizing well-lit main routes and remaining vigilant of surroundings.`;
            }

            if (incidents.length > 0) {
                summary += " Note: Recent police activity has been detected in this sector; check the live feed below for details.";
            }

            return summary;
        }

        function closeDrawer() {"""

content = content.replace("        function closeDrawer() {", js_func)

# 3. JS Update - update openDrawer call
old_open_drawer_start = """        function openDrawer(data, rankIndex, isCity) {
            const drawer = document.getElementById('intel-drawer');
            const totalPool = isCity ? cityData.length : TARGET_COUNT;
            const gradeData = getSafetyGrade(rankIndex, totalPool);
            const percentile = Math.round(((totalPool - rankIndex) / totalPool) * 100);

            // Populate header
            document.getElementById('drawer-grade').innerText = gradeData.grade;
            document.getElementById('drawer-grade-box').className = `grade-badge ${gradeData.bg} ${gradeData.color} ${gradeData.border}`;
            document.getElementById('drawer-name').innerText = data.regions.name;

            // Populate stats
            document.getElementById('drawer-percentile').innerText = `Top ${percentile}% Safest`;
            document.getElementById('drawer-percentile').className = `text-lg font-black ${gradeData.color}`;
            document.getElementById('drawer-total-incidents').innerText = data.total_crimes.toLocaleString();

            // Filter news"""

new_open_drawer_start = """        function openDrawer(data, rankIndex, isCity) {
            const drawer = document.getElementById('intel-drawer');
            const totalPool = isCity ? cityData.length : TARGET_COUNT;
            const gradeData = getSafetyGrade(rankIndex, totalPool);
            const percentile = Math.round(((totalPool - rankIndex) / totalPool) * 100);

            // Populate header
            document.getElementById('drawer-grade').innerText = gradeData.grade;
            document.getElementById('drawer-grade-box').className = `grade-badge ${gradeData.bg} ${gradeData.color} ${gradeData.border}`;
            document.getElementById('drawer-name').innerText = data.regions.name;

            // Populate stats
            document.getElementById('drawer-percentile').innerText = `Top ${percentile}% Safest`;
            document.getElementById('drawer-percentile').className = `text-lg font-black ${gradeData.color}`;
            document.getElementById('drawer-total-incidents').innerText = data.total_crimes.toLocaleString();

            // Filter news"""

# I need to find where relatedNews is defined and then call generateAISummary
old_news_filter = """            const relatedNews = incidentsData.filter(inc =>
                inc.title.toLowerCase().includes(nameLower) ||
                (inc.location_name && inc.location_name.toLowerCase().includes(nameLower))
            );

            if (relatedNews.length === 0) {"""

new_news_filter = """            const relatedNews = incidentsData.filter(inc =>
                inc.title.toLowerCase().includes(nameLower) ||
                (inc.location_name && inc.location_name.toLowerCase().includes(nameLower))
            );

            // Update AI Summary
            document.getElementById('drawer-ai-summary').innerText = generateAISummary(data, rankIndex, relatedNews);

            if (relatedNews.length === 0) {"""

if old_news_filter in content:
    content = content.replace(old_news_filter, new_news_filter)
else:
    print("Could not find news filter injection point")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Update complete")
