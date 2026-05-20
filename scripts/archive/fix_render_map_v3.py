import os
import re

file_path = r'C:\Users\vince\OneDrive\Documents\Antigravity Skills\scotland-crime-map\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace heatmapLayer with markers in renderMap
html = html.replace('heatmapLayer.clearLayers();', 'markers.clearLayers();')

# Replace L.circle with L.circleMarker
circle_pattern = re.compile(r'const circle = L\.circle\(\[n\.regions\.latitude, n\.regions\.longitude\], \{.*?\}\);', re.DOTALL)
new_marker = '''const marker = L.circleMarker([n.regions.latitude, n.regions.longitude], {
                        radius: 8,
                        fillColor: color,
                        color: "#fff",
                        weight: 2,
                        opacity: 1,
                        fillOpacity: 0.8
                    });'''
html = circle_pattern.sub(new_marker, html)

# Replace other occurrences of 'circle' with 'marker' in renderMap
html = html.replace('circle.addTo(heatmapLayer);', 'markers.addLayer(marker);')
html = html.replace('mapCircles.set(n.regions.id, circle);', 'mapCircles.set(n.regions.id, marker);')
html = html.replace('circle.bindPopup(popupContent', 'marker.bindPopup(popupContent')

# Privacy-first wording
html = html.replace('>${n.regions.name}</h4>', '>Reported on or near ${n.regions.name}</h4>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)
