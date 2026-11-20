TCLS Yeshwanthpur Dashboard - Updated Package

Files:
- app.py: Streamlit dashboard, including a one-page PDF export button.
- units.csv, schools.csv, completion.csv, skills.csv, trainers.csv, trainer_detail.csv: dashboard data.
- requirements.txt: Python dependencies.

Deploy/update:
1. Extract this ZIP.
2. Upload/replace all files in the existing GitHub repository.
3. Commit the changes. Streamlit Community Cloud should redeploy automatically.

Using the PDF export:
1. Open the live dashboard.
2. Select the reporting units you want (all units are selected by default).
3. Click "Download full dashboard as one-page PDF" below the KPI cards.
4. The PDF is generated as one A3 landscape page and reflects the current unit filters.

The PDF is a static snapshot. The live Streamlit dashboard remains interactive.
