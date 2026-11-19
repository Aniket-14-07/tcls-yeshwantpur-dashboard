# TCLS Yeshwanthpur Dashboard
A lightweight Streamlit dashboard built from the 8 submitted DOCX reports.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publish a shareable link
1. Create a GitHub repository and upload all files in this folder.
2. Open https://share.streamlit.io/ and connect your GitHub account.
3. Select the repository, branch, and `app.py`.
4. Deploy. Streamlit Community Cloud will provide a shareable URL.

People with the URL can interact with filters and charts. To edit the dashboard's code or underlying CSV data, grant them access to the GitHub repository. A public app URL alone does not grant edit permissions.

## Important reporting notes
- Commerce is set to 330 classes as explicitly requested, although the source document says "330 Hrs".
- Total students = sum of all unit-level reported headcounts; potential overlap is not deduplicated.
- Skill counts retain source-document units and are not assumed to be directly comparable.
