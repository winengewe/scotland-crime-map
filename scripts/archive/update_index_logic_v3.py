import re
import os

file_path = r"C:\Users\vince\OneDrive\Documents\Antigravity Skills\scotland-crime-map\index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update loadData to filter incidents by year
old_loaddata_fetch = """                // Fetch latest incidents
                const { data: incidents } = await client.from('incidents')
                    .select('*')
                    .order('created_at', { ascending: false })
                    .limit(50);
                incidentsData = incidents || [];"""

new_loaddata_fetch = """                // Fetch latest incidents
                let incidentsQuery = client.from('incidents').select('*').order('created_at', { ascending: false });
                
                if (year !== 'Overall') {
                    const startYear = year.split('/')[0];
                    const endYear = year.split('/')[1] || startYear;
                    const startDate = `${startYear}-01-01`;
                    const endDate = `${endYear}-12-31`;
                    incidentsQuery = incidentsQuery.gte('created_at', startDate).lte('created_at', endDate);
                } else {
                    incidentsQuery = incidentsQuery.limit(50);
                }
                
                const { data: incidents } = await incidentsQuery;
                incidentsData = incidents || [];"""

content = content.replace(old_loaddata_fetch, new_loaddata_fetch)

# 2. Update openDrawer fallback message
old_opendrawer_fallback = """            if (relatedNews.length === 0) {
                feed.innerHTML = '<div class="p-8 text-center text-xs font-bold text-slate-400 uppercase tracking-widest">No local reports found for this area</div>';
            }"""

new_opendrawer_fallback = """            if (relatedNews.length === 0) {
                const year = document.getElementById('year-selector').value;
                const msg = year !== 'Overall' ? 'No archived news found for this period' : 'No local reports found for this area';
                feed.innerHTML = `<div class="p-8 text-center text-xs font-bold text-slate-400 uppercase tracking-widest">${msg}</div>`;
            }"""

content = content.replace(old_opendrawer_fallback, new_opendrawer_fallback)

# 3. Update updateIntelligenceFeed fallback message
old_intel_fallback = """            if (displayData.length === 0) {
                container.innerHTML = '<div class="p-4 text-center text-[10px] font-bold text-slate-400 uppercase tracking-widest">No local reports found for this view</div>';
                return;
            }"""

new_intel_fallback = """            if (displayData.length === 0) {
                const year = document.getElementById('year-selector').value;
                const msg = year !== 'Overall' ? 'No archived news found for this period' : 'No local reports found for this view';
                container.innerHTML = `<div class="p-4 text-center text-[10px] font-bold text-slate-400 uppercase tracking-widest">${msg}</div>`;
                return;
            }"""

content = content.replace(old_intel_fallback, new_intel_fallback)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated index.html with year-based filtering logic.")
