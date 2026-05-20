# 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland Safety Finder | 2026 Edition

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/winengewe/scotland-crime-map/blob/main/LICENSE)
[![Status](https://img.shields.io/badge/status-v1.0--Stable-emerald.svg)]()

An interactive, high-intelligence crime mapping platform for Scotland. Built to democratize public safety data and provide real-time situational awareness for residents, house-hunters, and travelers.

**Live Application:** [https://winengewe.github.io/scotland-crime-map/](https://winengewe.github.io/scotland-crime-map/)

---

## 🚀 Key Features

- **Live 2026 Radar:** Real-time tracking of police appeals and reported incidents across Scotland.
- **Historical Analysis (2020-2025):** Detailed trend analysis based on official government statistics.
- **Intelligence Profiles:** Deep-dive safety audits for 6,976+ data zones, including national percentile rankings.
- **Multi-Mode Visualization:** Switch between precise **Markers** and high-density **Heatmaps**.
- **Real-Time Geolocation:** Instant "Locate Me" function for a 1km safety audit of your current surroundings.
- **Postcode-Level Search:** Dual-engine search bar powered by local intelligence and `postcodes.io`.

## 📊 Data & Methodology

### **Transparency of Sources**
Data is aggregated and normalized from official verified channels:
- **Police Scotland:** Open Data Portal (Live incidents & Appeals).
- **Scottish Government:** SIMD (Scottish Index of Multiple Deprivation) statistical datasets.
- **National Records of Scotland:** Census population data for per-capita normalization.

### **The Safety Scale**
We use **Per Capita Normalization** to calculate safety grades (A+ to F). Areas are ranked against all 6,976 data zones in Scotland to ensure a quiet village and a busy city center are compared fairly.

### **Understanding the Intelligence Layers**
To provide the most accurate picture of safety, this platform uses two distinct data layers:

1. **Major Incidents (The Area Feed):** This layer tracks "High-Signal" events such as police appeals, serious assaults, and major news stories. Minor crimes (like low-level antisocial behavior) are typically excluded from this feed to maintain clarity and focus on immediate threats.
2. **Statistical Trends (The Safety Grade):** This layer uses aggregated government data (SIMD) to calculate the A+ to F grades. Unlike the feed, this includes **all reported crimes**, including minor ones like vandalism, shoplifting, and antisocial behavior, to give a long-term "baseline" safety profile of an area.

## 🛠️ Tech Stack

- **Frontend:** HTML5, Tailwind CSS, JavaScript (ES6+).
- **Maps:** Leaflet.js with CartoDB Voyager tiles.
- **Backend/DB:** Supabase (PostgreSQL + Real-time).
- **APIs:** Postcodes.io for high-precision geolocation search.

## 🛡️ Privacy & Security

- **No Tracking:** We do not store user location data; geolocation is handled entirely on the client side.
- **Official Data:** We do not host private or identifiable information about victims; all incident data is sourced from public police reports.

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Found a bug or have a data discrepancy? Please report it via the [GitHub Issues](https://github.com/winengewe/scotland-crime-map/issues) page.

---
*Created with ❤️ by **winengewe***
