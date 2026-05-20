import os

file_path = r"C:\Users\vince\OneDrive\Documents\Antigravity Skills\scotland-crime-map\index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update openDrawer signature
if "async function openDrawer" not in content:
    content = content.replace(
        "function openDrawer(data, rankIndex, isCity) {",
        "async function openDrawer(data, rankIndex, isCity) {"
    )

# 2. Insert Breakdown Logic into openDrawer
# We'll insert it after the totalIncidentsEl block
old_block = """            } else {
                totalIncidentsEl.innerText = data.total_crimes.toLocaleString();
                totalIncidentsEl.removeAttribute('title');
                totalIncidentsEl.style.cursor = "default";
            }"""

if "Crime Breakdown Logic" not in content:
    new_block = old_block + """

            // Crime Breakdown Logic
            const breakdownContainer = document.getElementById('breakdown-container');
            const breakdownLoading = document.getElementById('breakdown-loading');
            const yearSelector = document.getElementById('year-selector');
            const yearValue = yearSelector ? yearSelector.value : '2020';
            
            if (breakdownContainer) {
                breakdownContainer.innerHTML = '';
                if (isCity) {
                    if (breakdownLoading) breakdownLoading.classList.remove('hidden');
                    try {
                        const { data: stats, error } = await client
                            .from('crime_stats')
                            .select('crime_type, total_crimes')
                            .eq('region_id', data.regions.id)
                            .eq('period', yearValue)
                            .neq('crime_type', 'Total Crimes')
                            .neq('crime_type', 'Neighborhood Rank');

                        if (error) throw error;

                        if (stats && stats.length > 0) {
                            const total = data.total_crimes > 0 ? data.total_crimes : stats.reduce((acc, curr) => acc + curr.total_crimes, 0);
                            stats.sort((a, b) => b.total_crimes - a.total_crimes);
                            
                            stats.forEach(item => {
                                const percentage = total > 0 ? Math.round((item.total_crimes / total) * 100) : 0;
                                if (percentage === 0 && item.total_crimes === 0) return;

                                const row = document.createElement('div');
                                row.className = "space-y-1";
                                row.innerHTML = `
                                    <div class="flex justify-between items-center text-[9px] font-black uppercase tracking-wider">
                                        <span class="text-slate-600">${item.crime_type}</span>
                                        <span class="text-slate-400">${percentage}%</span>
                                    </div>
                                    <div class="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                                        <div class="h-full bg-indigo-500 rounded-full transition-all duration-1000" style="width: 0%"></div>
                                    </div>
                                `;
                                breakdownContainer.appendChild(row);
                                setTimeout(() => {
                                    const bar = row.querySelector('.bg-indigo-500');
                                    if (bar) bar.style.width = `${percentage}%`;
                                }, 100);
                            });
                        } else {
                            breakdownContainer.innerHTML = '<p class="text-[10px] font-medium text-slate-500 italic text-center py-2">No categorical data available.</p>';
                        }
                    } catch (err) {
                        console.error("Breakdown error:", err);
                        breakdownContainer.innerHTML = '<p class="text-[10px] font-medium text-red-400 italic text-center py-2">Failed to load breakdown.</p>';
                    } finally {
                        if (breakdownLoading) breakdownLoading.classList.add('hidden');
                    }
                } else {
                    breakdownContainer.innerHTML = '<p class="text-[10px] font-medium text-slate-400 italic">Detailed categorical breakdown is available at the City level.</p>';
                }
            }"""
    content = content.replace(old_block, new_block)

# 3. Update UI - Insert breakdown section
ui_old_block = """                    <p id="drawer-live-activity" class="text-sm font-black text-blue-700">0</p>
                </div>
            </div>"""

if "id=\"crime-breakdown-section\"" not in content:
    ui_new_section = """
            <div id="crime-breakdown-section" class="bg-slate-50 p-5 rounded-3xl border border-slate-100 space-y-4">
                <div class="flex items-center justify-between">
                    <h3 class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Crime Distribution Profile</h3>
                    <div id="breakdown-loading" class="hidden flex items-center gap-1">
                        <span class="w-1 h-1 rounded-full bg-indigo-500 animate-ping"></span>
                        <span class="text-[8px] font-black text-indigo-500 uppercase">Analyzing</span>
                    </div>
                </div>
                <div id="breakdown-container" class="space-y-3">
                    <p id="breakdown-msg" class="text-[10px] font-medium text-slate-500 italic text-center">Select a city for detailed categorical breakdown.</p>
                </div>
            </div>"""
    content = content.replace(ui_old_block, ui_old_block + ui_new_section)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated index.html with Crime Breakdown Intelligence.")
