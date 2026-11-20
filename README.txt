TCLS Yeshwanthpur Dashboard — updated dataset release
Academic Year 2026–27 | Odd Semester

Contents:
- app.py: Streamlit interactive dashboard
- requirements.txt: runtime packages
- units.csv: headline and UG/PG data by reporting unit
- schools.csv: grouped school totals
- trainers.csv and trainer_detail.csv: trainer counts
- skills.csv: all skill rows as listed in source documents
- completion.csv: one-skill/two-skill completion entries

Deploy:
1. Replace the existing repository files with all files in this folder.
2. Commit the changes to the same GitHub repository.
3. Streamlit Community Cloud should redeploy the existing app.

IMPORTANT SOURCE DATA NOTES:
- 2,542 students; 45 classes; 77 skills by sum of headline totals; 79 trainers by sum of unit trainer totals.
- UG 2,357 + PG 185 = 2,542.
- Skill detail rows sum to 80, not 77. Individual document inconsistencies are documented in the app.
- Completion-table numeric class entries sum to 57, exceeding the 45 headline classes.
- See the dashboard expander "Detailed source figures and data-quality notes" before official circulation.
