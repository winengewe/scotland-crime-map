import sys
import re

file_path = r'C:\Users\vince\OneDrive\Documents\Antigravity Skills\scotland-crime-map\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add boundaryLayer declaration and Drawer functions
js_init = '''        const mapCircles = new Map();
        const boundaryLayer = L.layerGroup().addTo(map);

        function closeDrawer() {
            document.getElementById('intel-drawer').classList.add('translate-x-full');
        }

        function openDrawer(data, rankIndex, isCity) {
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

            // Filter news
            const feed = document.getElementById('drawer-feed');
            feed.innerHTML = '';
            const nameLower = data.regions.name.toLowerCase();
            const relatedNews = incidentsData.filter(inc => 
                inc.title.toLowerCase().includes(nameLower) || 
                (inc.location_name && inc.location_name.toLowerCase().includes(nameLower))
            );

            if (relatedNews.length === 0) {
                feed.innerHTML = '<div class="p-8 text-center text-xs font-bold text-slate-400 uppercase tracking-widest">No local reports found for this area</div>';
            } else {
                relatedNews.forEach(inc => {
                    const status = getIncidentStatus(inc.title);
                    const item = document.createElement('div');
                    item.className = 'p-4 bg-slate-50/50 rounded-2xl border border-slate-100 mb-3 hover:border-indigo-200 transition-all cursor-pointer group';
                    item.onclick = () => window.open(inc.url, '_blank');
                    item.innerHTML = `
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-[8px] font-black ${status.color} px-2 py-0.5 rounded-full uppercase">${status.label}</span>
                            <span class="text-[9px] font-bold text-slate-400">${new Date(inc.created_at).toLocaleDateString()}</span>
                        </div>
                        <h4 class="text-xs font-bold text-slate-800 leading-tight mb-2 uppercase group-hover:text-indigo-600 transition-colors">${inc.title}</h4>
                        <span class="text-[9px] font-black text-indigo-500 uppercase tracking-widest hover:underline">Read More →</span>
                    `;
                    feed.appendChild(item);
                });
            }

            drawer.classList.remove('translate-x-full');
        }
'''
if 'const boundaryLayer' not in content:
    content = content.replace('        const mapCircles = new Map();', js_init)

# Update renderMap to include boundaries and drawer interaction
render_map_old = '''                neighborhoodData.forEach((n, i) => {
                    if (n.regions.latitude) {
                        const rankVal = n.total_crimes;
                        const color = rankVal > 5000 ? '#10b981' : (rankVal > 2000 ? '#f59e0b' : '#ef4444');

                        const marker = L.circleMarker([n.regions.latitude, n.regions.longitude], {
                            radius: 8,
                            fillColor: color,
                            color: "#fff",
                            weight: 2,
                            opacity: 1,
                            fillOpacity: 0.8
                        });

                        markers.addLayer(marker);
                        mapCircles.set(n.regions.id, marker);

                        const rank = TARGET_COUNT - rankVal + 1;
                        const gradeData = getSafetyGrade(rank - 1, TARGET_COUNT);
                        const popupContent = `
                            <div class="p-4 min-w-[240px]">
                                <div class="flex justify-between items-start mb-4">
                                    <div>
                                        <div class="text-[9px] font-black text-indigo-500 uppercase mb-1 tracking-wider">${n.cityName}</div>
                                        <h4 class="text-sm font-black text-slate-800 leading-tight uppercase">Reported on or near ${n.regions.name}</h4>
                                    </div>
                                    <div class="grade-badge ${gradeData.bg} ${gradeData.color} ${gradeData.border} border-2">
                                        ${gradeData.grade}
                                    </div>
                                </div>

                                <div class="space-y-2 border-t border-slate-100 pt-3">
                                    <div class="flex items-center justify-between">
                                        <span class="text-[10px] font-bold text-slate-400 uppercase">National Rank</span>
                                        <span class="text-xs font-black text-slate-800">#${rank.toLocaleString()} / ${TARGET_COUNT.toLocaleString()}</span>
                                    </div>
                                    <div class="flex items-center justify-between">
                                        <span class="text-[10px] font-bold text-slate-400 uppercase">Safety Rating</span>
                                        <span class="text-[10px] font-black ${gradeData.color} uppercase">Top ${Math.round(((TARGET_COUNT - rank) / TARGET_COUNT) * 100)}% Safest</span>  
                                    </div>
                                </div>
                            </div>
                        `;
                        marker.bindPopup(popupContent, { className: 'custom-popup' });
                    }
                });'''

render_map_new = '''                neighborhoodData.forEach((n, i) => {
                    if (n.regions.latitude) {
                        const rankVal = n.total_crimes;
                        const color = rankVal > 5000 ? '#10b981' : (rankVal > 2000 ? '#f59e0b' : '#ef4444');

                        const marker = L.circleMarker([n.regions.latitude, n.regions.longitude], {
                            radius: 8,
                            fillColor: color,
                            color: "#fff",
                            weight: 2,
                            opacity: 1,
                            fillOpacity: 0.8
                        });

                        markers.addLayer(marker);
                        mapCircles.set(n.regions.id, marker);

                        const rank = TARGET_COUNT - rankVal + 1;
                        marker.on('click', () => openDrawer(n, rank - 1, false));
                        
                        const gradeData = getSafetyGrade(rank - 1, TARGET_COUNT);
                        const popupContent = `
                            <div class="p-4 min-w-[240px]">
                                <div class="flex justify-between items-start mb-4">
                                    <div>
                                        <div class="text-[9px] font-black text-indigo-500 uppercase mb-1 tracking-wider">${n.cityName}</div>
                                        <h4 class="text-sm font-black text-slate-800 leading-tight uppercase">Reported on or near ${n.regions.name}</h4>
                                    </div>
                                    <div class="grade-badge ${gradeData.bg} ${gradeData.color} ${gradeData.border} border-2">
                                        ${gradeData.grade}
                                    </div>
                                </div>

                                <div class="space-y-2 border-t border-slate-100 pt-3">
                                    <div class="flex items-center justify-between">
                                        <span class="text-[10px] font-bold text-slate-400 uppercase">National Rank</span>
                                        <span class="text-xs font-black text-slate-800">#${rank.toLocaleString()} / ${TARGET_COUNT.toLocaleString()}</span>
                                    </div>
                                    <div class="flex items-center justify-between">
                                        <span class="text-[10px] font-bold text-slate-400 uppercase">Safety Rating</span>
                                        <span class="text-[10px] font-black ${gradeData.color} uppercase">Top ${Math.round(((TARGET_COUNT - rank) / TARGET_COUNT) * 100)}% Safest</span>  
                                    </div>
                                    <button onclick="openDrawer(neighborhoodData[${i}], ${rank-1}, false)" class="w-full mt-4 bg-indigo-600 text-white text-[9px] font-black py-2 rounded-lg uppercase tracking-widest">Open Intelligence</button>
                                </div>
                            </div>
                        `;
                        marker.bindPopup(popupContent, { className: 'custom-popup' });
                    }
                });

                if (document.getElementById('show-boundaries-toggle')?.checked) {
                    fetchBoundaries();
                } else {
                    boundaryLayer.clearLayers();
                }'''

if 'fetchBoundaries()' not in content:
    content = content.replace(render_map_old, render_map_new)

# Add fetchBoundaries and renderBoundaries functions
boundary_js = '''
        async function fetchBoundaries() {
            const bounds = map.getBounds();
            // Fetch top 500 regions with boundaries
            const { data, error } = await client.from('regions')
                .select('id, name, boundary')
                .not('boundary', 'is', null)
                .limit(500);

            if (error) {
                console.error('Error fetching boundaries:', error);
                return;
            }
            renderBoundaries(data);
        }

        function renderBoundaries(regionsWithBoundaries) {
            boundaryLayer.clearLayers();
            regionsWithBoundaries.forEach(reg => {
                const nData = neighborhoodData.find(n => n.regions.id === reg.id);
                if (!nData) return;

                const rankVal = nData.total_crimes;
                const rank = TARGET_COUNT - rankVal + 1;
                const color = rankVal > 5000 ? '#10b981' : (rankVal > 2000 ? '#f59e0b' : '#ef4444');
                
                const geojson = L.geoJSON(reg.boundary, {
                    style: {
                        fillColor: color,
                        weight: 1,
                        opacity: 1,
                        color: 'white',
                        fillOpacity: 0.2
                    }
                });
                
                geojson.on('click', (e) => {
                    L.DomEvent.stopPropagation(e);
                    openDrawer(nData, rank - 1, false);
                });
                
                boundaryLayer.addLayer(geojson);
            });
        }
'''
if 'function fetchBoundaries()' not in content:
    content = content.replace('        function renderTop10s() {', boundary_js + '\n        function renderTop10s() {')

# Update renderInsightList to call openDrawer
old_insight_click = '''                item.onclick = function() {
                    if(d.regions.latitude) {
                        map.setView([d.regions.latitude, d.regions.longitude], isCity ? 11 : 15);
                        if (!isCity) {
                            const circle = mapCircles.get(d.regions.id);
                            if (circle) circle.openPopup();
                        }
                    }
                };'''
new_insight_click = '''                item.onclick = function() {
                    if(d.regions.latitude) {
                        map.setView([d.regions.latitude, d.regions.longitude], isCity ? 11 : 15);
                        openDrawer(d, iValue, isCity);
                    }
                };'''
content = content.replace(old_insight_click, new_insight_click)

# Update handleSearch to call openDrawer
old_search_click = '''                    div.onclick = function() {
                        map.setView([n.regions.latitude, n.regions.longitude], 15);
                        const circle = mapCircles.get(n.regions.id);
                        if (circle) circle.openPopup();
                        resultsContainer.style.display = 'none';
                    };'''
new_search_click = '''                    div.onclick = function() {
                        map.setView([n.regions.latitude, n.regions.longitude], 15);
                        const rank = TARGET_COUNT - n.total_crimes;
                        openDrawer(n, rank, false);
                        resultsContainer.style.display = 'none';
                    };'''
content = content.replace(old_search_click, new_search_click)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
