# HealthCare Data Website

A static synthetic healthcare data portal built from generated HL7-style patient records.

## What This Project Includes

- A patient portal homepage with `200` synthetic patient records
- Individual patient detail pages under `portal/patients/`
- Synthetic raw HL7 files under `portal/raw_hl7/`
- A generated patient summary dataset in `portal/data/patients.json`
- A Python generator script that rebuilds the portal files

## Project Structure

- `build_hl7_portal.py` - Generates the portal pages, HL7 files, shared CSS, and patient JSON
- `inspect_data.py` - Small helper to inspect `portal/data/patients.json`
- `portal/index.html` - Main patient listing page
- `portal/styles.css` - Shared styling for the portal
- `portal/patients/` - Individual patient pages
- `portal/raw_hl7/` - Raw HL7 message files
- `portal/data/patients.json` - Generated patient summary data

## Run Locally

From the project root:

```bash
python3 -m http.server 3000 --directory portal
```

Then open:

```text
http://localhost:3000
```

## Rebuild The Portal

Use Python 3.10+ to regenerate the portal files:

```bash
python3.10 build_hl7_portal.py
```

This rebuilds:

- `portal/index.html`
- `portal/styles.css`
- `portal/patients/*.html`
- `portal/raw_hl7/*.hl7`
- `portal/data/patients.json`

## Notes

- All records are synthetic and intended for learning, UI demos, and healthcare data exploration.
- Large reference datasets were intentionally removed from the repo so the project can stay lightweight and GitHub-friendly.

## GitHub

Repository: <https://github.com/ManoHarshaSappa/HealthCare_DataWebsite>
