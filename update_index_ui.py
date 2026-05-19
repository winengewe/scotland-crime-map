import sys

file_path = r'C:\Users\vince\OneDrive\Documents\Antigravity Skills\scotland-crime-map\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add Drawer CSS
if '#intel-drawer {' not in content:
    old_style = '.grade-badge-sm {'
    new_style = '''/* Intelligence Drawer */
        #intel-drawer {
            position: fixed;
            top: 0;
            right: 0;
            width: 400px;
            height: 100%;
            background: white;
            z-index: 2000;
            box-shadow: -10px 0 50px rgba(0,0,0,0.1);
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border-left: 1px solid #f1f5f9;
            display: flex;
            flex-direction: column;
        }
        #intel-drawer.translate-x-full {
            transform: translateX(100%);
        }
        ''' + old_style
    content = content.replace(old_style, new_style)

# Add Toggle in Header (next to year selector)
if 'id="show-boundaries-toggle"' not in content:
    old_header = '<select id="year-selector"'
    new_header = '''<div class="flex items-center gap-2 bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-200 mr-2">
                        <input type="checkbox" id="show-boundaries-toggle" onchange="renderMap()" class="w-3 h-3 text-indigo-600 border-slate-300 rounded focus:ring-indigo-500 cursor-pointer">
                        <label for="show-boundaries-toggle" class="text-[9px] font-black text-slate-500 uppercase tracking-widest cursor-pointer">Show Boundaries</label>
                    </div>''' + old_header
    content = content.replace(old_header, new_header)

# Add Drawer HTML
if 'id="intel-drawer"' not in content:
    drawer_html = '''
    <!-- Intelligence Drawer -->
    <div id="intel-drawer" class="translate-x-full">
        <div class="p-6 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
            <div class="flex items-center gap-4">
                <div id="drawer-grade-box" class="grade-badge">
                    <span id="drawer-grade">-</span>
                </div>
                <div>
                    <h2 id="drawer-name" class="text-lg font-black text-slate-800 uppercase leading-tight">Area Name</h2>
                    <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Intelligence Profile</p>
                </div>
            </div>
            <button onclick="closeDrawer()" class="p-2 hover:bg-slate-200 rounded-full transition-all text-slate-400">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
        </div>
        
        <div class="flex-1 overflow-y-auto custom-scrollbar p-6 space-y-8">
            <div class="grid grid-cols-2 gap-4">
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
                <h3 class="text-xs font-black text-slate-400 uppercase tracking-widest mb-4 italic">Local Incident Feed</h3>
                <div id="drawer-feed" class="space-y-3">
                    <!-- Populated by JS -->
                </div>
            </div>
        </div>
    </div>
'''
    content = content.replace('</body>', drawer_html + '\n</body>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
