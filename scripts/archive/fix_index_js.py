import sys

file_path = r'C:\Users\vince\OneDrive\Documents\Antigravity Skills\scotland-crime-map\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix encoding/arrow
content = content.replace('Read More \u2192', 'Read More &rarr;')
content = content.replace('Read More 閳?', 'Read More &rarr;')

# Surgical update for marker click in renderMap
old_marker_logic = '''                        markers.addLayer(marker);
                        mapCircles.set(n.regions.id, marker);

                        const rank = TARGET_COUNT - rankVal + 1;
                        const gradeData = getSafetyGrade(rank - 1, TARGET_COUNT);'''

new_marker_logic = '''                        markers.addLayer(marker);
                        mapCircles.set(n.regions.id, marker);

                        const rank = TARGET_COUNT - rankVal + 1;
                        marker.on('click', () => openDrawer(n, rank - 1, false));
                        const gradeData = getSafetyGrade(rank - 1, TARGET_COUNT);'''

if 'marker.on(\'click\')' not in content:
    content = content.replace(old_marker_logic, new_marker_logic)

# Add button to popup
old_popup_end = '''                                    </div>
                                </div>
                            </div>
                        `;'''

new_popup_end = '''                                    </div>
                                    <button onclick="openDrawer(neighborhoodData[${i}], ${rank-1}, false)" class="w-full mt-4 bg-indigo-600 text-white text-[9px] font-black py-2 rounded-lg uppercase tracking-widest">Open Intelligence</button>
                                </div>
                            </div>
                        `;'''

if 'Open Intelligence' not in content:
    content = content.replace(old_popup_end, new_popup_end)

# Add fetchBoundaries call to renderMap
old_render_map_end = '''                });
            }

            incidentMarkers.clearLayers();'''

new_render_map_end = '''                });
                
                if (document.getElementById('show-boundaries-toggle')?.checked) {
                    fetchBoundaries();
                } else {
                    boundaryLayer.clearLayers();
                }
            }

            incidentMarkers.clearLayers();'''

if 'fetchBoundaries()' not in content:
    content = content.replace(old_render_map_end, new_render_map_end)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
