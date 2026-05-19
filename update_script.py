import sys

file_path = r"C:\Users\vince\OneDrive\Documents\Antigravity Skills\scotland-crime-map\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_string = """        function handleSearch(e) {
            const query = e.target.value.toLowerCase();
            const resultsContainer = document.getElementById('search-results-container');

            if (!query || query.length < 2) {
                resultsContainer.style.display = 'none';
                return;
            }

            const results = neighborhoodData
                .filter(n => n.regions.name.toLowerCase().includes(query) || n.cityName.toLowerCase().includes(query))
                .slice(0, 20);

            resultsContainer.innerHTML = '';
            if (results.length > 0) {
                resultsContainer.style.display = 'block';
                results.forEach(function(n) {
                    const div = document.createElement('div');
                    div.className = 'p-4 hover:bg-slate-50 cursor-pointer border-b border-slate-50 last:border-0 transition-all';
                    div.onclick = function() {
                        map.setView([n.regions.latitude, n.regions.longitude], 15);
                        const circle = mapCircles.get(n.regions.id);
                        if (circle) circle.openPopup();
                        resultsContainer.style.display = 'none';
                    };
                    div.innerHTML = `
                        <div class="text-[10px] font-black text-indigo-500 uppercase tracking-wider">${n.cityName}</div>
                        <div class="text-sm font-bold text-slate-800 uppercase">${n.regions.name}</div>
                    `;
                    resultsContainer.appendChild(div);
                });
            } else {
                resultsContainer.innerHTML = '<div class="p-6 text-center text-xs font-bold text-slate-400 uppercase tracking-widest">No results found</div>';
                resultsContainer.style.display = 'block';
            }
        }"""

new_string = """        async function handleSearch(e) {
            const query = e.target.value.trim();
            const resultsContainer = document.getElementById('search-results-container');

            if (!query || query.length < 2) {
                resultsContainer.style.display = 'none';
                return;
            }

            // Postcode Regex (UK)
            const postcodeRegex = /^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$/i;
            
            if (postcodeRegex.test(query)) {
                resultsContainer.innerHTML = '<div class="p-4 text-center text-xs font-bold text-indigo-500 animate-pulse uppercase tracking-widest">Searching Postcode...</div>';
                resultsContainer.style.display = 'block';
                
                try {
                    const response = await fetch(`https://api.postcodes.io/postcodes/${encodeURIComponent(query)}`);
                    const data = await response.json();
                    
                    if (data.status === 200 && data.result) {
                        const { latitude, longitude, postcode } = data.result;
                        map.setView([latitude, longitude], 15);
                        
                        if (window.searchMarker) map.removeLayer(window.searchMarker);
                        window.searchMarker = L.marker([latitude, longitude]).addTo(map)
                            .bindPopup(`<div class="p-2 font-black uppercase text-xs">Postcode: ${postcode}</div>`)
                            .openPopup();
                        
                        resultsContainer.style.display = 'none';
                        return;
                    } else {
                        resultsContainer.innerHTML = '<div class="p-6 text-center text-xs font-bold text-rose-500 uppercase tracking-widest">Invalid Postcode</div>';
                        resultsContainer.style.display = 'block';
                        return;
                    }
                } catch (error) {
                    console.error('Postcode search error:', error);
                    resultsContainer.innerHTML = '<div class="p-6 text-center text-xs font-bold text-rose-500 uppercase tracking-widest">Error searching postcode</div>';
                    resultsContainer.style.display = 'block';
                    return;
                }
            }

            const lowerQuery = query.toLowerCase();
            const results = neighborhoodData
                .filter(n => n.regions.name.toLowerCase().includes(lowerQuery) || n.cityName.toLowerCase().includes(lowerQuery))
                .slice(0, 20);

            resultsContainer.innerHTML = '';
            if (results.length > 0) {
                resultsContainer.style.display = 'block';
                results.forEach(function(n) {
                    const div = document.createElement('div');
                    div.className = 'p-4 hover:bg-slate-50 cursor-pointer border-b border-slate-50 last:border-0 transition-all';
                    div.onclick = function() {
                        map.setView([n.regions.latitude, n.regions.longitude], 15);
                        const circle = mapCircles.get(n.regions.id);
                        if (circle) circle.openPopup();
                        resultsContainer.style.display = 'none';
                    };
                    div.innerHTML = `
                        <div class="text-[10px] font-black text-indigo-500 uppercase tracking-wider">${n.cityName}</div>
                        <div class="text-sm font-bold text-slate-800 uppercase">${n.regions.name}</div>
                    `;
                    resultsContainer.appendChild(div);
                });
            } else {
                resultsContainer.innerHTML = '<div class="p-6 text-center text-xs font-bold text-slate-400 uppercase tracking-widest">No results found</div>';
                resultsContainer.style.display = 'block';
            }
        }"""

if old_string in content:
    content = content.replace(old_string, new_string)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Success")
else:
    print("Old string not found")