# Sea-Breeze Detection & Spatial Analysis Algorithm

This Python script identifies and analyzes sea-breeze days over the Rome metropolitan area using 5-minute meteorological station data (2020–2025).

### Workflow & Methodology
1. **Seasonal Filtering:** Filters observations based on customizable seasonal time windows and target months.
2. **Multi-Proxy Breeze Detection:** Classifies a sea-breeze day when hourly thresholds are met across four physical criteria:
   - **Wind Speed:** Sustained breeze intensity between $1\text{ m/s}$ and $6\text{ m/s}$.
   - **Wind Direction:** Vector-averaged onshore flow ($220^\circ < \theta < 270^\circ$).
   - **Solar Radiation:** Clear-sky ratio ($\text{Rad} / \text{ClearSky} \ge 0.75$), automatically skipped if pyranometer data is unavailable.
   - **Precipitation:** Strictly dry conditions ($\text{Rain} = 0$) throughout the target window.
3. **Thermal Gradient & Diurnal Comparison:** Computes hourly linear regressions of temperature versus distance from the coast ($^\circ\text{C/km}$) across multiple stations and generates comparative 24-hour thermal/wind profiles between coastal and inland sites.
