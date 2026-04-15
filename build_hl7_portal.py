import re
from datetime import datetime, timedelta
from pathlib import Path
from textwrap import dedent


OUTPUT_DIR = Path("portal")
RAW_DIR = OUTPUT_DIR / "raw_hl7"
PATIENTS_DIR = OUTPUT_DIR / "patients"


EXISTING_PATIENTS = [
    ("P100001", "James Alexander Smith", "james.smith01", "James@123", "1989-03-12", "M", "78 Cedar Ave", "Boston", "MA", "02118", "PEN", "Penicillin", "hypertension_monitor"),
    ("P100002", "Priya Ramesh Sharma", "priya.sharma02", "Priya@123", "1994-01-15", "F", "123 Main St", "Fairfax", "VA", "22030", "NKDA", "No Known Drug Allergies", "appendicitis_followup"),
    ("P100003", "Mohamed Ahmed Hassan", "mohamed.hassan03", "Mohamed@123", "1987-06-22", "M", "455 Palm Residence", "Houston", "TX", "77002", "SULFA", "Sulfonamide allergy", "pneumonia_admit_followup"),
    ("P100004", "Li Wei Zhang", "liwei.zhang04", "LiWei@123", "1992-10-08", "M", "10 Harbor View", "San Diego", "CA", "92101", "LATEX", "Latex allergy", "ankle_followup"),
    ("P100005", "Carlos Eduardo Martinez", "carlos.martinez05", "Carlos@123", "1985-12-19", "M", "910 Oak Terrace", "Phoenix", "AZ", "85004", "ASA", "Aspirin allergy", "diabetes_monitor"),
    ("P100006", "Anna Sofia Muller", "anna.muller06", "Anna@123", "1996-11-30", "F", "22 River Square", "Chicago", "IL", "60601", "DUST", "Dust mite allergy", "dermatitis_followup"),
    ("P100007", "Rajesh Kumar Gupta", "rajesh.gupta07", "Rajesh@123", "1978-07-04", "M", "14 Maple Heights", "Edison", "NJ", "08817", "SHELL", "Shellfish allergy", "chest_pain_ruleout"),
    ("P100008", "Fatima Noor Hassan", "fatima.hassan08", "Fatima@123", "1998-09-21", "F", "600 Crescent Park", "Seattle", "WA", "98101", "IBU", "Ibuprofen allergy", "migraine_med_adjust"),
    ("P100009", "Daniel Jose Rodriguez", "daniel.rodriguez09", "Daniel@123", "1990-02-11", "M", "81 Sunset Blvd", "Miami", "FL", "33101", "NKFA", "No Known Food Allergies", "gerd_stable"),
    ("P100010", "Hiroshi Takumi Yamamoto", "hiroshi.yamamoto10", "Hiroshi@123", "1983-02-27", "M", "350 Sakura Lane", "San Jose", "CA", "95112", "CODEINE", "Codeine allergy", "back_pain_followup"),
]


MANUAL_ADDITIONAL_PATIENTS = [
    ("Olivia Grace Bennett", "1991-05-08", "F", "19 Harbor Lane", "Providence", "RI", "02903", "LATEX", "Latex allergy", "routine_physical_single"),
    ("Arjun Vivek Patel", "1986-08-14", "M", "240 Ash Court", "Jersey City", "NJ", "07302", "NKDA", "No Known Drug Allergies", "diabetes_monitor"),
    ("Sophia Marie Johnson", "1993-07-18", "F", "55 Linden Street", "Atlanta", "GA", "30303", "PEN", "Penicillin", "cellulitis_followup"),
    ("Noah David Kim", "1988-02-09", "M", "901 Willow Drive", "Portland", "OR", "97204", "NKDA", "No Known Drug Allergies", "acute_uri_single"),
    ("Amina Yasmin Ali", "1995-11-27", "F", "63 Crescent Avenue", "Columbus", "OH", "43215", "SULFA", "Sulfonamide allergy", "anemia_monitor"),
    ("Ethan Michael Carter", "1984-09-03", "M", "410 River Bend", "Nashville", "TN", "37203", "NKDA", "No Known Drug Allergies", "asthma_escalation"),
    ("Isabella Rose Fernandez", "1992-04-29", "F", "77 Garden View", "Tampa", "FL", "33602", "ASA", "Aspirin allergy", "thyroid_stable"),
    ("Lucas Andre Silva", "1987-03-22", "M", "15 Quartz Way", "Denver", "CO", "80202", "NKDA", "No Known Drug Allergies", "renal_stone_followup"),
    ("Mei Lin Chen", "1990-12-16", "F", "81 Pearl Street", "Sacramento", "CA", "95814", "DUST", "Dust mite allergy", "dermatitis_followup"),
    ("Omar Khalid Farouk", "1974-06-11", "M", "510 Cedar Point", "Detroit", "MI", "48226", "NKDA", "No Known Drug Allergies", "copd_admit_followup"),
    ("Emma Louise Thompson", "1996-10-02", "F", "33 Pine Brook", "Charlotte", "NC", "28202", "IBU", "Ibuprofen allergy", "migraine_med_adjust"),
    ("Mateo Javier Rivera", "1989-01-19", "M", "610 Maple Grove", "San Antonio", "TX", "78205", "NKDA", "No Known Drug Allergies", "ankle_followup"),
    ("Sara Huda Rahman", "1994-03-30", "F", "144 Ocean Park", "Baltimore", "MD", "21202", "NKDA", "No Known Drug Allergies", "depression_med_adjust"),
    ("Benjamin Scott Walker", "1979-05-24", "M", "28 Summit Road", "Cleveland", "OH", "44114", "SHELL", "Shellfish allergy", "chest_pain_ruleout"),
    ("Nina Elise Novak", "1991-09-07", "F", "90 Birch Terrace", "Milwaukee", "WI", "53202", "NKFA", "No Known Food Allergies", "gerd_stable"),
    ("Abdul Rahman Siddiqui", "1977-02-03", "M", "212 Walnut Street", "Dallas", "TX", "75201", "PEN", "Penicillin", "hypertension_monitor"),
    ("Grace Helen Cooper", "1985-06-26", "F", "17 Ivy Court", "Richmond", "VA", "23219", "NKDA", "No Known Drug Allergies", "routine_physical_single"),
    ("Yusuf Ibrahim Malik", "1972-08-31", "M", "300 Stone Mill", "Buffalo", "NY", "14202", "NKDA", "No Known Drug Allergies", "ckd_monitor"),
    ("Chloe Anne Dubois", "1997-01-12", "F", "62 Magnolia Place", "New Orleans", "LA", "70112", "LATEX", "Latex allergy", "acute_uri_single"),
    ("Nathan Lee Parker", "1983-04-17", "M", "48 Canyon Ridge", "Boise", "ID", "83702", "CODEINE", "Codeine allergy", "back_pain_followup"),
    ("Leila Samira Haddad", "1992-02-25", "F", "81 Olive Street", "Orlando", "FL", "32801", "SULFA", "Sulfonamide allergy", "uti_escalation"),
    ("Aarav Nikhil Mehta", "1988-11-05", "M", "516 Elm Crossing", "Austin", "TX", "78701", "NKDA", "No Known Drug Allergies", "diabetes_monitor"),
    ("Mia Katherine Brooks", "1990-07-01", "F", "37 Harbor Point", "Kansas City", "MO", "64106", "NKDA", "No Known Drug Allergies", "thyroid_stable"),
    ("Samuel Aaron Davis", "1971-10-09", "M", "205 Pine Creek", "Pittsburgh", "PA", "15222", "ASA", "Aspirin allergy", "chf_admit_followup"),
    ("Zara Noor Khan", "1995-05-15", "F", "73 Auburn Way", "Minneapolis", "MN", "55401", "IBU", "Ibuprofen allergy", "migraine_med_adjust"),
    ("Julian Rafael Torres", "1986-09-20", "M", "410 Orchard Lane", "Albuquerque", "NM", "87102", "PEN", "Penicillin", "cellulitis_followup"),
    ("Hana Soo Park", "1993-12-03", "F", "14 Valley Point", "Madison", "WI", "53703", "NKDA", "No Known Drug Allergies", "anemia_monitor"),
    ("Ibrahim Tariq Saleh", "1969-04-28", "M", "64 Ironwood Dr", "St. Louis", "MO", "63101", "NKDA", "No Known Drug Allergies", "copd_admit_followup"),
    ("Elena Maria Petrova", "1987-06-13", "F", "229 Bay Shore", "Newark", "NJ", "07102", "DUST", "Dust mite allergy", "dermatitis_followup"),
    ("Victor Hugo Almeida", "1978-12-11", "M", "540 Lakeview Rd", "Tucson", "AZ", "85701", "SHELL", "Shellfish allergy", "chest_pain_ruleout"),
    ("Sofia Daniela Costa", "1994-08-04", "F", "81 Coral Street", "Fort Lauderdale", "FL", "33301", "NKFA", "No Known Food Allergies", "gerd_stable"),
    ("Mason Christopher Reed", "1982-11-18", "M", "311 Ridge Court", "Omaha", "NE", "68102", "NKDA", "No Known Drug Allergies", "renal_stone_followup"),
    ("Amira Layla Mahmoud", "1991-03-07", "F", "50 Lantern Way", "Cincinnati", "OH", "45202", "NKDA", "No Known Drug Allergies", "depression_med_adjust"),
    ("Leo Sebastian Ortiz", "1985-01-22", "M", "420 Oak Harbor", "Raleigh", "NC", "27601", "NKDA", "No Known Drug Allergies", "asthma_escalation"),
    ("Aisha Mariam Bello", "1996-09-09", "F", "16 Easton Place", "Jacksonville", "FL", "32202", "SULFA", "Sulfonamide allergy", "uti_escalation"),
    ("Henry Oliver Collins", "1976-07-29", "M", "87 Cedar Lake", "Louisville", "KY", "40202", "PEN", "Penicillin", "hypertension_monitor"),
    ("Camila Fernanda Vega", "1998-02-14", "F", "28 Pine Harbor", "Tempe", "AZ", "85281", "NKDA", "No Known Drug Allergies", "appendicitis_followup"),
    ("Min Jae Lee", "1989-10-26", "M", "340 Harbor East", "Irvine", "CA", "92602", "NKDA", "No Known Drug Allergies", "acute_uri_single"),
    ("Rohan Suresh Iyer", "1974-05-12", "M", "95 Granite Way", "Hartford", "CT", "06103", "NKDA", "No Known Drug Allergies", "ckd_monitor"),
    ("Eva Lucia Moreno", "1992-12-20", "F", "62 Meadow Lane", "El Paso", "TX", "79901", "LATEX", "Latex allergy", "routine_physical_single"),
]


def sanitize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def build_additional_patient_records() -> list[dict]:
    records = []
    for offset, row in enumerate(MANUAL_ADDITIONAL_PATIENTS, start=11):
        name, dob, gender, street, city, state, zip_code, allergy_code, allergy_text, track = row
        patient_id = f"P{100000 + offset}"
        first_name = sanitize(name.split()[0])
        last_name = sanitize(name.split()[-1])
        records.append(
            {
                "patient_id": patient_id,
                "name": name,
                "user_id": f"{first_name}.{last_name}{offset:02d}",
                "password": f"{name.split()[0]}@{offset:02d}",
                "dob": dob,
                "gender": gender,
                "address_street": street,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "phone": f"(555)010-{offset:04d}",
                "allergy_code": allergy_code,
                "allergy_text": allergy_text,
                "track": track,
            }
        )
    return records


GENERATED_FIRST_NAMES = [
    "Aiden", "Mila", "Elias", "Nora", "Kian", "Layla", "Jonah", "Ivy", "Owen", "Zain",
    "Riya", "Seth", "Leona", "Micah", "Ava", "Ruben", "Tara", "Dev", "Mina", "Caleb",
    "Elise", "Rafael", "Huda", "Rowan", "Sana", "Diego", "Anika", "Cole", "Mariam", "Theo",
]

GENERATED_MIDDLE_NAMES = [
    "James", "Marie", "Noor", "David", "Grace", "Kumar", "Elena", "Rose", "Javier", "Amir",
    "Louise", "Nikhil", "Sofia", "Lee", "Amina", "Victor", "Daniel", "Rae", "Ibrahim", "Skye",
]

GENERATED_LAST_NAMES = [
    "Turner", "Nakamura", "Hassan", "Brooks", "Patel", "Morales", "Chowdhury", "Reyes", "Bennett", "Siddiqui",
    "Campos", "Keller", "Wallace", "Farah", "Morrison", "Vega", "Santos", "Nguyen", "Salazar", "Khan",
]

GENERATED_CITIES = [
    ("Mesa", "AZ", "85201"),
    ("Plano", "TX", "75024"),
    ("Irvine", "CA", "92612"),
    ("Tallahassee", "FL", "32301"),
    ("Des Moines", "IA", "50309"),
    ("Reno", "NV", "89501"),
    ("Tulsa", "OK", "74103"),
    ("Boulder", "CO", "80302"),
    ("Savannah", "GA", "31401"),
    ("Spokane", "WA", "99201"),
]

GENERATED_STREETS = [
    "Maple Crest", "Riverstone", "Cedar Point", "Oak Hollow", "Sunrise Park", "Willow Bend",
    "Harbor Ridge", "Lakeside", "Pine Grove", "Meadow Run",
]

GENERATED_ALLERGIES = [
    ("NKDA", "No Known Drug Allergies"),
    ("PEN", "Penicillin"),
    ("LATEX", "Latex allergy"),
    ("SULFA", "Sulfonamide allergy"),
    ("ASA", "Aspirin allergy"),
    ("IBU", "Ibuprofen allergy"),
    ("SHELL", "Shellfish allergy"),
    ("NKFA", "No Known Food Allergies"),
]

TRACK_SEQUENCE = [
    "hypertension_monitor",
    "appendicitis_followup",
    "pneumonia_admit_followup",
    "ankle_followup",
    "diabetes_monitor",
    "dermatitis_followup",
    "chest_pain_ruleout",
    "migraine_med_adjust",
    "gerd_stable",
    "back_pain_followup",
    "routine_physical_single",
    "acute_uri_single",
    "asthma_escalation",
    "ckd_monitor",
    "copd_admit_followup",
    "uti_escalation",
    "thyroid_stable",
    "cellulitis_followup",
    "depression_med_adjust",
    "anemia_monitor",
    "chf_admit_followup",
    "renal_stone_followup",
]


def build_generated_patient_records(start_offset: int, count: int) -> list[dict]:
    records = []
    for index in range(count):
        offset = start_offset + index
        first_name = GENERATED_FIRST_NAMES[index % len(GENERATED_FIRST_NAMES)]
        middle_name = GENERATED_MIDDLE_NAMES[(index * 3) % len(GENERATED_MIDDLE_NAMES)]
        last_name = GENERATED_LAST_NAMES[(index * 7) % len(GENERATED_LAST_NAMES)]
        city, state, zip_code = GENERATED_CITIES[index % len(GENERATED_CITIES)]
        street = f"{120 + index} {GENERATED_STREETS[(index * 5) % len(GENERATED_STREETS)]} Drive"
        allergy_code, allergy_text = GENERATED_ALLERGIES[index % len(GENERATED_ALLERGIES)]
        name = f"{first_name} {middle_name} {last_name}"
        patient_id = f"P{100000 + offset}"
        user_id = f"{sanitize(first_name)}.{sanitize(last_name)}{offset:02d}"
        password = f"{first_name}@{offset:02d}"
        birth_year = 1970 + (index % 29)
        birth_month = (index % 12) + 1
        birth_day = (index % 27) + 1
        gender = "M" if index % 2 == 0 else "F"
        track = TRACK_SEQUENCE[index % len(TRACK_SEQUENCE)]

        records.append(
            {
                "patient_id": patient_id,
                "name": name,
                "user_id": user_id,
                "password": password,
                "dob": f"{birth_year:04d}-{birth_month:02d}-{birth_day:02d}",
                "gender": gender,
                "address_street": street,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "phone": f"(555)010-{offset:04d}",
                "allergy_code": allergy_code,
                "allergy_text": allergy_text,
                "track": track,
            }
        )
    return records


def build_existing_patient_records() -> list[dict]:
    return [
        {
            "patient_id": patient_id,
            "name": name,
            "user_id": user_id,
            "password": password,
            "dob": dob,
            "gender": gender,
            "address_street": street,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "phone": f"(555)010-{index:04d}",
            "allergy_code": allergy_code,
            "allergy_text": allergy_text,
            "track": track,
        }
        for index, (patient_id, name, user_id, password, dob, gender, street, city, state, zip_code, allergy_code, allergy_text, track) in enumerate(EXISTING_PATIENTS, start=1)
    ]


PATIENTS = (
    build_existing_patient_records()
    + build_additional_patient_records()
    + build_generated_patient_records(start_offset=51, count=100)
)


def slugify(value: str) -> str:
    return value.upper().replace(" ", "_").replace("-", "_")


def split_name(name: str) -> tuple[str, str, str]:
    parts = name.split()
    return parts[0], " ".join(parts[1:-1]), parts[-1]


def dt(base: datetime, days: int, hour: int = 9, minute: int = 0) -> datetime:
    return (base + timedelta(days=days)).replace(hour=hour, minute=minute)


def fmt(dt_value: datetime) -> str:
    return dt_value.strftime("%Y%m%d%H%M")


def obs(code: str, text: str, value: str, unit: str, normal_range: str, flag: str, value_type: str = "NM") -> dict:
    return {
        "code": code,
        "text": text,
        "value": value,
        "unit": unit,
        "range": normal_range,
        "flag": flag,
        "type": value_type,
    }


def visit(
    when: datetime,
    patient_class: str,
    facility: str,
    lab_facility: str,
    provider_first: str,
    provider_last: str,
    specialty: str,
    diagnosis_code: str,
    diagnosis_text: str,
    order_code: str,
    order_text: str,
    observations: list[dict],
    medication: dict | None = None,
    note: str | None = None,
    message_type: str = "ADT^A04",
    location: str = "CLINIC^01^01",
) -> dict:
    return {
        "message_type": message_type,
        "message_datetime": fmt(when),
        "admit_datetime": fmt(when - timedelta(minutes=30)),
        "patient_class": patient_class,
        "location": location,
        "facility": facility,
        "lab_facility": lab_facility,
        "provider_first": provider_first,
        "provider_last": provider_last,
        "specialty": specialty,
        "diagnosis_code": diagnosis_code,
        "diagnosis_text": diagnosis_text,
        "order_code": order_code,
        "order_text": order_text,
        "observations": observations,
        "medication": medication,
        "note": note,
    }


def scenario_hypertension_monitor(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 9, 15), "O", "CardioCare Clinic", "Metro Lab", "Emily", "Carter", "CARD", "I10", "Essential hypertension", "BPCHK", "Hypertension panel", [obs("BP_SYS", "Blood Pressure Systolic", str(154 - variant * 2), "mmHg", "90-120", "H"), obs("GLU", "Glucose", str(109 + variant * 2), "mg/dL", "70-110", "N")], {"code": "RX100", "text": "Lisinopril", "dose": "10 mg daily", "route": "PO"}, "Initial blood pressure management visit."),
        visit(dt(base, 90, 10, 0), "O", "CardioCare Clinic", "Metro Lab", "Emily", "Carter", "CARD", "I10", "Essential hypertension", "BPCHK", "Medication follow-up", [obs("BP_SYS", "Blood Pressure Systolic", str(145 - variant), "mmHg", "90-120", "H"), obs("GLU", "Glucose", str(106 + variant), "mg/dL", "70-110", "N")], {"code": "RX101", "text": "Lisinopril", "dose": "20 mg daily", "route": "PO"}, "Dose increased after incomplete blood pressure control.", message_type="ADT^A08"),
        visit(dt(base, 185, 8, 45), "O", "CardioCare Clinic", "Metro Lab", "Emily", "Carter", "CARD", "I10", "Essential hypertension", "BPCHK", "Chronic monitoring panel", [obs("BP_SYS", "Blood Pressure Systolic", str(132 + variant), "mmHg", "90-120", "H"), obs("GLU", "Glucose", str(101 + variant), "mg/dL", "70-110", "N")], {"code": "RX102", "text": "Lisinopril/Hydrochlorothiazide", "dose": "20/12.5 mg daily", "route": "PO"}, "Blood pressure improving on maintenance regimen.", message_type="ADT^A08"),
    ]


def scenario_appendicitis_followup(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 13, 10), "E", "Inova Hospital", "Inova Lab", "John", "Miller", "SURG", "K35.80", "Acute appendicitis", "CBC", "Complete Blood Count", [obs("WBC", "White Blood Cell Count", str(14800 + variant * 400), "cells/uL", "4000-11000", "H"), obs("TEMP", "Body Temperature", f"{101.2 + variant * 0.1:.1f}", "F", "97-99", "H")], {"code": "RX201", "text": "Ceftriaxone", "dose": "1 g IV", "route": "IV"}, "Emergency presentation with abdominal pain.", message_type="ADT^A01", location="ER^01^01"),
        visit(dt(base, 14, 9, 30), "O", "Inova Surgical Follow-Up", "Inova Lab", "John", "Miller", "SURG", "Z09", "Follow-up examination after appendectomy", "POSTOP", "Post-operative review", [obs("WBC", "White Blood Cell Count", str(8200 + variant * 120), "cells/uL", "4000-11000", "N"), obs("TEMP", "Body Temperature", "98.6", "F", "97-99", "N")], {"code": "RX202", "text": "Acetaminophen", "dose": "500 mg every 6 hours as needed", "route": "PO"}, "Surgical follow-up with improving symptoms.", message_type="ADT^A08"),
    ]


def scenario_pneumonia_admit_followup(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 15, 25), "E", "Houston Medical Center", "Houston Diagnostic Lab", "Sarah", "Hughes", "PULM", "J18.9", "Pneumonia, unspecified organism", "CXR", "Chest X-Ray review", [obs("O2SAT", "Oxygen Saturation", str(91 - variant), "%", "95-100", "L"), obs("RESP", "Respiratory Rate", str(24 + variant), "/min", "12-20", "H")], {"code": "RX301", "text": "Azithromycin", "dose": "500 mg daily", "route": "PO"}, "Presented to emergency department with cough and hypoxia.", message_type="ADT^A01", location="ER^01^01"),
        visit(dt(base, 2, 10, 20), "I", "Houston Medical Center", "Houston Diagnostic Lab", "Sarah", "Hughes", "PULM", "J18.9", "Community-acquired pneumonia", "ABG", "Respiratory monitoring", [obs("O2SAT", "Oxygen Saturation", str(94 - variant), "%", "95-100", "L"), obs("RESP", "Respiratory Rate", str(20 + variant), "/min", "12-20", "H")], {"code": "RX302", "text": "Ceftriaxone", "dose": "1 g daily", "route": "IV"}, "Admitted for intravenous antibiotics and oxygen support.", message_type="ADT^A01", location="MEDSURG^03^12"),
        visit(dt(base, 21, 11, 0), "O", "Houston Pulmonary Associates", "Houston Diagnostic Lab", "Sarah", "Hughes", "PULM", "Z09", "Follow-up after pneumonia treatment", "FOLLOW", "Pulmonary follow-up", [obs("O2SAT", "Oxygen Saturation", "97", "%", "95-100", "N"), obs("RESP", "Respiratory Rate", "16", "/min", "12-20", "N")], {"code": "RX303", "text": "Albuterol inhaler", "dose": "2 puffs as needed", "route": "INH"}, "Breathing normalized on follow-up.", message_type="ADT^A08"),
    ]


def scenario_ankle_followup(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 14, 0), "E", "Pacific Care Hospital", "Pacific Imaging Center", "Maria", "Lopez", "EMED", "S93.401A", "Right ankle sprain", "ANKXR", "Ankle imaging review", [obs("PAIN", "Pain Score", str(7 + variant), "/10", "0-10", "H"), obs("SWELL", "Ankle Swelling", "Moderate", "", "", "A", "ST")], {"code": "RX401", "text": "Ibuprofen", "dose": "400 mg every 8 hours", "route": "PO"}, "Twisting injury during recreational activity.", message_type="ADT^A01", location="ER^02^01"),
        visit(dt(base, 12, 8, 50), "O", "Pacific Sports Medicine", "Pacific Imaging Center", "Maria", "Lopez", "ORTH", "Z09", "Follow-up after ankle sprain", "REHAB", "Mobility reassessment", [obs("PAIN", "Pain Score", str(3 + variant), "/10", "0-10", "N"), obs("SWELL", "Ankle Swelling", "Mild", "", "", "N", "ST")], {"code": "RX402", "text": "Naproxen", "dose": "250 mg twice daily as needed", "route": "PO"}, "Follow-up visit after bracing and rest.", message_type="ADT^A08"),
    ]


def scenario_diabetes_monitor(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 9, 40), "O", "Phoenix Endocrine Center", "Phoenix Endocrine Lab", "Linda", "Nguyen", "ENDO", "E11.9", "Type 2 diabetes mellitus", "A1C", "Glycemic control panel", [obs("A1C", "Hemoglobin A1c", f"{8.4 + variant * 0.2:.1f}", "%", "4.0-5.6", "H"), obs("GLUFAST", "Fasting Glucose", str(172 + variant * 6), "mg/dL", "70-99", "H")], {"code": "RX501", "text": "Metformin", "dose": "500 mg twice daily", "route": "PO"}, "New diabetes follow-up with elevated A1c."),
        visit(dt(base, 95, 10, 10), "O", "Phoenix Endocrine Center", "Phoenix Endocrine Lab", "Linda", "Nguyen", "ENDO", "E11.9", "Type 2 diabetes mellitus", "A1C", "Diabetes medication review", [obs("A1C", "Hemoglobin A1c", f"{7.8 + variant * 0.2:.1f}", "%", "4.0-5.6", "H"), obs("GLUFAST", "Fasting Glucose", str(154 + variant * 5), "mg/dL", "70-99", "H")], {"code": "RX502", "text": "Metformin", "dose": "1000 mg twice daily", "route": "PO"}, "Metformin increased due to persistent hyperglycemia.", message_type="ADT^A08"),
        visit(dt(base, 190, 9, 15), "O", "Phoenix Endocrine Center", "Phoenix Endocrine Lab", "Linda", "Nguyen", "ENDO", "E11.9", "Type 2 diabetes mellitus", "A1C", "Chronic diabetes monitoring", [obs("A1C", "Hemoglobin A1c", f"{7.1 + variant * 0.1:.1f}", "%", "4.0-5.6", "H"), obs("GLUFAST", "Fasting Glucose", str(131 + variant * 4), "mg/dL", "70-99", "H")], {"code": "RX503", "text": "Metformin + Glipizide", "dose": "1000 mg BID + 5 mg daily", "route": "PO"}, "Added second agent for chronic disease control.", message_type="ADT^A08"),
    ]


def scenario_dermatitis_followup(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 11, 15), "O", "Chicago Specialty Center", "Chicago Allergy Lab", "Amit", "Patel", "DERM", "L20.9", "Atopic dermatitis", "ALLPAN", "Allergy evaluation", [obs("IGE", "IgE", str(210 + variant * 12), "IU/mL", "0-100", "H"), obs("RASH", "Rash Severity Score", str(6 + variant), "/10", "0-10", "H")], {"code": "RX601", "text": "Hydrocortisone cream", "dose": "Apply twice daily", "route": "TOP"}, "Initial dermatitis flare evaluation."),
        visit(dt(base, 45, 8, 30), "O", "Chicago Specialty Center", "Chicago Allergy Lab", "Amit", "Patel", "DERM", "L20.9", "Atopic dermatitis", "FOLLOW", "Dermatology follow-up", [obs("IGE", "IgE", str(168 + variant * 10), "IU/mL", "0-100", "H"), obs("RASH", "Rash Severity Score", str(3 + variant), "/10", "0-10", "N")], {"code": "RX602", "text": "Tacrolimus ointment", "dose": "Apply nightly", "route": "TOP"}, "Skin inflammation improved after treatment.", message_type="ADT^A08"),
    ]


def scenario_chest_pain_ruleout(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 16, 5), "E", "Garden State Heart Center", "Garden State Cardio Lab", "Thomas", "Reed", "CARD", "R07.9", "Chest pain, unspecified", "TROP", "Chest pain rule-out panel", [obs("TROP", "Troponin I", f"{0.02 + variant * 0.01:.2f}", "ng/mL", "0.00-0.04", "N"), obs("HR", "Heart Rate", str(101 + variant * 3), "bpm", "60-100", "H")], {"code": "RX701", "text": "Nitroglycerin", "dose": "0.4 mg as needed", "route": "SL"}, "Presented to ER with acute chest discomfort.", message_type="ADT^A01", location="ER^04^01"),
        visit(dt(base, 1, 9, 20), "I", "Garden State Heart Center", "Garden State Cardio Lab", "Thomas", "Reed", "CARD", "R07.9", "Observation for chest pain", "ECHO", "Cardiac observation panel", [obs("TROP", "Troponin I", "0.01", "ng/mL", "0.00-0.04", "N"), obs("HR", "Heart Rate", str(92 + variant), "bpm", "60-100", "N")], {"code": "RX702", "text": "Metoprolol", "dose": "25 mg daily", "route": "PO"}, "Observed overnight; no infarction identified.", message_type="ADT^A01", location="OBS^02^03"),
        visit(dt(base, 18, 10, 30), "O", "Garden State Cardiology", "Garden State Cardio Lab", "Thomas", "Reed", "CARD", "R07.89", "Other chest pain", "FOLLOW", "Cardiology follow-up", [obs("TROP", "Troponin I", "0.01", "ng/mL", "0.00-0.04", "N"), obs("HR", "Heart Rate", str(78 + variant), "bpm", "60-100", "N")], {"code": "RX703", "text": "Metoprolol", "dose": "25 mg daily", "route": "PO"}, "Symptoms stable after rule-out evaluation.", message_type="ADT^A08"),
    ]


def scenario_migraine_med_adjust(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 10, 40), "O", "Seattle Neuro Clinic", "Seattle Diagnostic Lab", "Natalie", "Brown", "NEUR", "G43.909", "Migraine, unspecified", "NEURO", "Headache assessment", [obs("PAIN", "Headache Severity", str(8 + variant), "/10", "0-10", "H"), obs("SLEEP", "Sleep Hours", str(4 + variant), "hours", "6-8", "L")], {"code": "RX801", "text": "Sumatriptan", "dose": "50 mg as needed", "route": "PO"}, "Migraine symptoms interfering with sleep."),
        visit(dt(base, 40, 9, 30), "O", "Seattle Neuro Clinic", "Seattle Diagnostic Lab", "Natalie", "Brown", "NEUR", "G43.909", "Migraine, unspecified", "FOLLOW", "Medication review", [obs("PAIN", "Headache Severity", str(5 + variant), "/10", "0-10", "H"), obs("SLEEP", "Sleep Hours", str(6 + variant), "hours", "6-8", "N")], {"code": "RX802", "text": "Sumatriptan + Topiramate", "dose": "50 mg PRN + 25 mg nightly", "route": "PO"}, "Preventive medication added after partial response.", message_type="ADT^A08"),
        visit(dt(base, 100, 8, 55), "O", "Seattle Neuro Clinic", "Seattle Diagnostic Lab", "Natalie", "Brown", "NEUR", "G43.909", "Migraine, unspecified", "FOLLOW", "Neurology follow-up", [obs("PAIN", "Headache Severity", str(2 + variant), "/10", "0-10", "N"), obs("SLEEP", "Sleep Hours", "7", "hours", "6-8", "N")], {"code": "RX803", "text": "Topiramate", "dose": "50 mg nightly", "route": "PO"}, "Headache frequency reduced on preventive regimen.", message_type="ADT^A08"),
    ]


def scenario_gerd_stable(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 8, 40), "O", "Digestive Health Clinic", "Central GI Lab", "Elena", "Garcia", "GAST", "K21.9", "Gastro-esophageal reflux disease", "GIWK", "Digestive symptoms workup", [obs("REFLUX", "Reflux Symptom Score", str(6 + variant), "/10", "0-10", "H"), obs("ALT", "Alanine Aminotransferase", str(32 + variant), "U/L", "7-56", "N")], {"code": "RX901", "text": "Omeprazole", "dose": "20 mg daily", "route": "PO"}, "Routine reflux evaluation."),
        visit(dt(base, 75, 9, 0), "O", "Digestive Health Clinic", "Central GI Lab", "Elena", "Garcia", "GAST", "K21.9", "Gastro-esophageal reflux disease", "FOLLOW", "GERD follow-up", [obs("REFLUX", "Reflux Symptom Score", str(4 + variant), "/10", "0-10", "N"), obs("ALT", "Alanine Aminotransferase", str(31 + variant), "U/L", "7-56", "N")], {"code": "RX902", "text": "Omeprazole", "dose": "20 mg daily", "route": "PO"}, "Symptoms improved and stable.", message_type="ADT^A08"),
        visit(dt(base, 160, 9, 10), "O", "Digestive Health Clinic", "Central GI Lab", "Elena", "Garcia", "GAST", "K21.9", "Gastro-esophageal reflux disease", "FOLLOW", "Maintenance review", [obs("REFLUX", "Reflux Symptom Score", str(4 + variant), "/10", "0-10", "N"), obs("ALT", "Alanine Aminotransferase", str(30 + variant), "U/L", "7-56", "N")], {"code": "RX903", "text": "Omeprazole", "dose": "20 mg daily", "route": "PO"}, "Stable repeat visit for chronic symptoms.", message_type="ADT^A08"),
    ]


def scenario_back_pain_followup(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 11, 0), "O", "Bay Ortho Medical", "Bay Imaging Lab", "Grace", "Wilson", "ORTH", "M54.50", "Low back pain", "SPXR", "Spine evaluation", [obs("PAIN", "Back Pain Score", str(6 + variant), "/10", "0-10", "H"), obs("MOB", "Mobility Assessment", "Reduced", "", "", "A", "ST")], {"code": "RX1001", "text": "Naproxen", "dose": "500 mg twice daily", "route": "PO"}, "Mechanical back pain after lifting injury."),
        visit(dt(base, 28, 10, 30), "O", "Bay Ortho Medical", "Bay Imaging Lab", "Grace", "Wilson", "ORTH", "M54.50", "Low back pain", "FOLLOW", "Orthopedic follow-up", [obs("PAIN", "Back Pain Score", str(3 + variant), "/10", "0-10", "N"), obs("MOB", "Mobility Assessment", "Improving", "", "", "N", "ST")], {"code": "RX1002", "text": "Cyclobenzaprine", "dose": "5 mg nightly as needed", "route": "PO"}, "Symptoms improving after home exercise program.", message_type="ADT^A08"),
    ]


def scenario_routine_physical_single(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 8, 20), "O", "PrimaryCare Associates", "Regional Preventive Lab", "Megan", "Ross", "FM", "Z00.00", "Adult general medical examination", "ANNUAL", "Annual physical screening", [obs("CHOL", "Total Cholesterol", str(184 + variant * 6), "mg/dL", "<200", "N"), obs("BMI", "Body Mass Index", f"{25.1 + variant * 0.8:.1f}", "kg/m2", "18.5-24.9", "H")], None, "Routine annual physical with preventive screening."),
    ]


def scenario_acute_uri_single(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 12, 15), "O", "Downtown Urgent Care", "Regional Rapid Lab", "Megan", "Ross", "FM", "J06.9", "Acute upper respiratory infection", "RESP", "Respiratory symptom review", [obs("TEMP", "Body Temperature", f"{99.4 + variant * 0.2:.1f}", "F", "97-99", "H"), obs("PULSE", "Pulse Rate", str(88 + variant * 3), "bpm", "60-100", "N")], {"code": "RX1101", "text": "Benzonatate", "dose": "100 mg three times daily as needed", "route": "PO"}, "Single urgent care visit for viral symptoms."),
    ]


def scenario_asthma_escalation(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 10, 20), "O", "Respiratory Care Clinic", "Metro Pulmonary Lab", "Sarah", "Hughes", "PULM", "J45.20", "Mild intermittent asthma", "SPIRO", "Pulmonary assessment", [obs("PEAK", "Peak Flow", str(380 - variant * 15), "L/min", "400-600", "L"), obs("O2SAT", "Oxygen Saturation", str(95 - variant), "%", "95-100", "N")], {"code": "RX1201", "text": "Albuterol inhaler", "dose": "2 puffs every 6 hours as needed", "route": "INH"}, "Baseline asthma visit with mild symptoms."),
        visit(dt(base, 60, 17, 10), "E", "Respiratory Care Hospital", "Metro Pulmonary Lab", "Sarah", "Hughes", "PULM", "J45.901", "Asthma with acute exacerbation", "ABG", "Emergency respiratory panel", [obs("PEAK", "Peak Flow", str(295 - variant * 10), "L/min", "400-600", "L"), obs("O2SAT", "Oxygen Saturation", str(90 - variant), "%", "95-100", "L")], {"code": "RX1202", "text": "Prednisone", "dose": "40 mg daily for 5 days", "route": "PO"}, "Returned with worsening wheeze and shortness of breath.", message_type="ADT^A01", location="ER^05^01"),
        visit(dt(base, 80, 9, 45), "O", "Respiratory Care Clinic", "Metro Pulmonary Lab", "Sarah", "Hughes", "PULM", "J45.40", "Moderate persistent asthma", "FOLLOW", "Pulmonary follow-up", [obs("PEAK", "Peak Flow", str(420 - variant * 8), "L/min", "400-600", "N"), obs("O2SAT", "Oxygen Saturation", "97", "%", "95-100", "N")], {"code": "RX1203", "text": "Fluticasone inhaler", "dose": "2 puffs twice daily", "route": "INH"}, "Maintenance therapy started after exacerbation.", message_type="ADT^A08"),
    ]


def scenario_ckd_monitor(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 8, 35), "O", "Renal Care Group", "Renal Diagnostics", "Aaron", "Cole", "NEPH", "N18.2", "Chronic kidney disease stage 2", "RENAL", "Renal function panel", [obs("CREAT", "Creatinine", f"{1.4 + variant * 0.1:.1f}", "mg/dL", "0.6-1.3", "H"), obs("EGFR", "Estimated GFR", str(61 - variant * 3), "mL/min", ">60", "L")], {"code": "RX1301", "text": "Losartan", "dose": "25 mg daily", "route": "PO"}, "Chronic kidney disease monitoring visit."),
        visit(dt(base, 85, 9, 0), "O", "Renal Care Group", "Renal Diagnostics", "Aaron", "Cole", "NEPH", "N18.2", "Chronic kidney disease stage 2", "RENAL", "Repeat renal function panel", [obs("CREAT", "Creatinine", f"{1.6 + variant * 0.1:.1f}", "mg/dL", "0.6-1.3", "H"), obs("EGFR", "Estimated GFR", str(54 - variant * 3), "mL/min", ">60", "L")], {"code": "RX1302", "text": "Losartan", "dose": "50 mg daily", "route": "PO"}, "Renal function worsened slightly; medication adjusted.", message_type="ADT^A08"),
        visit(dt(base, 150, 8, 50), "O", "Renal Care Group", "Renal Diagnostics", "Aaron", "Cole", "NEPH", "N18.2", "Chronic kidney disease stage 2", "RENAL", "Kidney disease surveillance", [obs("CREAT", "Creatinine", f"{1.5 + variant * 0.1:.1f}", "mg/dL", "0.6-1.3", "H"), obs("EGFR", "Estimated GFR", str(56 - variant * 2), "mL/min", ">60", "L")], {"code": "RX1303", "text": "Losartan", "dose": "50 mg daily", "route": "PO"}, "Close follow-up after medication adjustment.", message_type="ADT^A08"),
        visit(dt(base, 240, 9, 10), "O", "Renal Care Group", "Renal Diagnostics", "Aaron", "Cole", "NEPH", "N18.2", "Chronic kidney disease stage 2", "RENAL", "Longitudinal renal follow-up", [obs("CREAT", "Creatinine", f"{1.3 + variant * 0.1:.1f}", "mg/dL", "0.6-1.3", "N"), obs("EGFR", "Estimated GFR", str(63 - variant * 2), "mL/min", ">60", "N")], {"code": "RX1304", "text": "Losartan", "dose": "50 mg daily", "route": "PO"}, "Kidney function stabilized on repeat follow-up.", message_type="ADT^A08"),
    ]


def scenario_copd_admit_followup(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 18, 0), "E", "Metro Pulmonary Hospital", "Metro Pulmonary Lab", "Elias", "Stone", "PULM", "J44.1", "COPD with acute exacerbation", "RESP", "COPD exacerbation panel", [obs("O2SAT", "Oxygen Saturation", str(88 - variant), "%", "95-100", "L"), obs("RESP", "Respiratory Rate", str(25 + variant), "/min", "12-20", "H")], {"code": "RX1401", "text": "Ipratropium/Albuterol", "dose": "Nebulized every 4 hours", "route": "INH"}, "Emergency visit for worsening shortness of breath.", message_type="ADT^A01", location="ER^06^01"),
        visit(dt(base, 2, 9, 15), "I", "Metro Pulmonary Hospital", "Metro Pulmonary Lab", "Elias", "Stone", "PULM", "J44.1", "COPD with acute exacerbation", "FOLLOW", "Inpatient respiratory monitoring", [obs("O2SAT", "Oxygen Saturation", str(92 - variant), "%", "95-100", "L"), obs("RESP", "Respiratory Rate", str(21 + variant), "/min", "12-20", "H")], {"code": "RX1402", "text": "Prednisone", "dose": "40 mg daily", "route": "PO"}, "Admitted after persistent hypoxia.", message_type="ADT^A01", location="MEDSURG^04^08"),
        visit(dt(base, 28, 10, 0), "O", "Metro Pulmonary Clinic", "Metro Pulmonary Lab", "Elias", "Stone", "PULM", "J44.9", "Chronic obstructive pulmonary disease", "FOLLOW", "Pulmonary follow-up", [obs("O2SAT", "Oxygen Saturation", "95", "%", "95-100", "N"), obs("RESP", "Respiratory Rate", "18", "/min", "12-20", "N")], {"code": "RX1403", "text": "Tiotropium inhaler", "dose": "1 capsule inhaled daily", "route": "INH"}, "Outpatient follow-up after inpatient treatment.", message_type="ADT^A08"),
    ]


def scenario_uti_escalation(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 11, 30), "O", "Women's Health Clinic", "Regional Micro Lab", "Julia", "Ng", "FM", "N39.0", "Urinary tract infection", "URINE", "Urinalysis", [obs("UAWBC", "Urine WBC", str(22 + variant * 2), "/HPF", "0-5", "H"), obs("NITRITE", "Nitrite", "Positive", "", "", "A", "ST")], {"code": "RX1501", "text": "Nitrofurantoin", "dose": "100 mg twice daily for 5 days", "route": "PO"}, "Initial urinary symptoms treated outpatient."),
        visit(dt(base, 7, 17, 20), "E", "Regional Medical Center", "Regional Micro Lab", "Julia", "Ng", "FM", "N10", "Acute pyelonephritis", "CBC", "Infection evaluation", [obs("TEMP", "Body Temperature", f"{101.8 + variant * 0.2:.1f}", "F", "97-99", "H"), obs("UAWBC", "Urine WBC", str(35 + variant * 2), "/HPF", "0-5", "H")], {"code": "RX1502", "text": "Ciprofloxacin", "dose": "500 mg twice daily for 7 days", "route": "PO"}, "Returned with flank pain and worsening infection.", message_type="ADT^A01", location="ER^03^02"),
        visit(dt(base, 21, 9, 10), "O", "Women's Health Clinic", "Regional Micro Lab", "Julia", "Ng", "FM", "Z09", "Follow-up after urinary infection treatment", "URINE", "Repeat urinalysis", [obs("TEMP", "Body Temperature", "98.7", "F", "97-99", "N"), obs("UAWBC", "Urine WBC", str(3 + variant), "/HPF", "0-5", "N")], {"code": "RX1503", "text": "Cranberry supplement", "dose": "Once daily", "route": "PO"}, "Resolved symptoms after antibiotic change.", message_type="ADT^A08"),
    ]


def scenario_thyroid_stable(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 8, 30), "O", "Endocrine Wellness Center", "Hormone Reference Lab", "Linda", "Nguyen", "ENDO", "E03.9", "Hypothyroidism, unspecified", "TSH", "Thyroid function panel", [obs("TSH", "Thyroid Stimulating Hormone", f"{5.8 + variant * 0.3:.1f}", "uIU/mL", "0.4-4.0", "H"), obs("FREE_T4", "Free T4", f"{0.8 + variant * 0.1:.1f}", "ng/dL", "0.8-1.8", "N")], {"code": "RX1601", "text": "Levothyroxine", "dose": "50 mcg daily", "route": "PO"}, "Initial thyroid maintenance visit."),
        visit(dt(base, 75, 8, 50), "O", "Endocrine Wellness Center", "Hormone Reference Lab", "Linda", "Nguyen", "ENDO", "E03.9", "Hypothyroidism, unspecified", "TSH", "Medication adjustment follow-up", [obs("TSH", "Thyroid Stimulating Hormone", f"{3.2 + variant * 0.2:.1f}", "uIU/mL", "0.4-4.0", "N"), obs("FREE_T4", "Free T4", "1.0", "ng/dL", "0.8-1.8", "N")], {"code": "RX1602", "text": "Levothyroxine", "dose": "75 mcg daily", "route": "PO"}, "Dose adjusted after elevated TSH.", message_type="ADT^A08"),
        visit(dt(base, 165, 9, 5), "O", "Endocrine Wellness Center", "Hormone Reference Lab", "Linda", "Nguyen", "ENDO", "E03.9", "Hypothyroidism, unspecified", "TSH", "Chronic thyroid surveillance", [obs("TSH", "Thyroid Stimulating Hormone", f"{2.5 + variant * 0.2:.1f}", "uIU/mL", "0.4-4.0", "N"), obs("FREE_T4", "Free T4", "1.1", "ng/dL", "0.8-1.8", "N")], {"code": "RX1603", "text": "Levothyroxine", "dose": "75 mcg daily", "route": "PO"}, "Stable repeat monitoring visit.", message_type="ADT^A08"),
    ]


def scenario_cellulitis_followup(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 13, 45), "O", "Community Wound Clinic", "Regional Infection Lab", "Nora", "Jensen", "FM", "L03.116", "Cellulitis of left lower limb", "CRP", "Inflammatory marker review", [obs("CRP", "C-Reactive Protein", str(38 + variant * 4), "mg/L", "0-10", "H"), obs("PAIN", "Pain Score", str(6 + variant), "/10", "0-10", "H")], {"code": "RX1701", "text": "Cephalexin", "dose": "500 mg four times daily", "route": "PO"}, "Initial cellulitis diagnosis with erythema and swelling."),
        visit(dt(base, 10, 9, 20), "O", "Community Wound Clinic", "Regional Infection Lab", "Nora", "Jensen", "FM", "Z09", "Follow-up after cellulitis treatment", "CRP", "Repeat inflammatory marker review", [obs("CRP", "C-Reactive Protein", str(8 + variant), "mg/L", "0-10", "N"), obs("PAIN", "Pain Score", str(2 + variant), "/10", "0-10", "N")], {"code": "RX1702", "text": "Cephalexin", "dose": "Complete current course", "route": "PO"}, "Marked improvement after antibiotic therapy.", message_type="ADT^A08"),
    ]


def scenario_depression_med_adjust(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 10, 10), "O", "Behavioral Health Associates", "Behavioral Metrics Lab", "Laura", "Kim", "PSY", "F32.A", "Depression, unspecified", "MENTAL", "Behavioral health assessment", [obs("PHQ9", "PHQ-9 Score", str(16 + variant), "score", "0-27", "H"), obs("SLEEP", "Sleep Hours", str(4 + variant), "hours", "6-8", "L")], {"code": "RX1801", "text": "Sertraline", "dose": "25 mg daily", "route": "PO"}, "Initial behavioral health intake."),
        visit(dt(base, 35, 9, 0), "O", "Behavioral Health Associates", "Behavioral Metrics Lab", "Laura", "Kim", "PSY", "F32.A", "Depression, unspecified", "FOLLOW", "Medication follow-up", [obs("PHQ9", "PHQ-9 Score", str(11 + variant), "score", "0-27", "H"), obs("SLEEP", "Sleep Hours", str(6 + variant), "hours", "6-8", "N")], {"code": "RX1802", "text": "Sertraline", "dose": "50 mg daily", "route": "PO"}, "Mood partially improved; dose increased.", message_type="ADT^A08"),
        visit(dt(base, 95, 8, 45), "O", "Behavioral Health Associates", "Behavioral Metrics Lab", "Laura", "Kim", "PSY", "F32.A", "Depression, unspecified", "FOLLOW", "Behavioral follow-up", [obs("PHQ9", "PHQ-9 Score", str(6 + variant), "score", "0-27", "N"), obs("SLEEP", "Sleep Hours", "7", "hours", "6-8", "N")], {"code": "RX1803", "text": "Sertraline", "dose": "50 mg daily", "route": "PO"}, "Sustained improvement on repeat visit.", message_type="ADT^A08"),
    ]


def scenario_anemia_monitor(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 8, 55), "O", "Women's Health Clinic", "Regional Hematology Lab", "Helen", "Morris", "HEME", "D64.9", "Anemia, unspecified", "ANEMIA", "Anemia workup", [obs("HGB", "Hemoglobin", f"{10.2 + variant * 0.2:.1f}", "g/dL", "12.0-16.0", "L"), obs("FERR", "Ferritin", str(12 + variant * 3), "ng/mL", "15-150", "L")], {"code": "RX1901", "text": "Ferrous sulfate", "dose": "325 mg daily", "route": "PO"}, "Low hemoglobin identified during evaluation."),
        visit(dt(base, 55, 9, 15), "O", "Women's Health Clinic", "Regional Hematology Lab", "Helen", "Morris", "HEME", "D64.9", "Anemia, unspecified", "FOLLOW", "Repeat anemia panel", [obs("HGB", "Hemoglobin", f"{11.1 + variant * 0.2:.1f}", "g/dL", "12.0-16.0", "L"), obs("FERR", "Ferritin", str(22 + variant * 3), "ng/mL", "15-150", "N")], {"code": "RX1902", "text": "Ferrous sulfate", "dose": "325 mg daily", "route": "PO"}, "Gradual response after iron therapy.", message_type="ADT^A08"),
        visit(dt(base, 120, 8, 50), "O", "Women's Health Clinic", "Regional Hematology Lab", "Helen", "Morris", "HEME", "D64.9", "Anemia, unspecified", "FOLLOW", "Longitudinal anemia follow-up", [obs("HGB", "Hemoglobin", f"{12.0 + variant * 0.1:.1f}", "g/dL", "12.0-16.0", "N"), obs("FERR", "Ferritin", str(35 + variant * 4), "ng/mL", "15-150", "N")], {"code": "RX1903", "text": "Ferrous sulfate", "dose": "325 mg every other day", "route": "PO"}, "Laboratory values normalized over time.", message_type="ADT^A08"),
    ]


def scenario_chf_admit_followup(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 17, 40), "E", "Heart Failure Institute", "Cardio Biomarker Lab", "Thomas", "Reed", "CARD", "I50.9", "Heart failure, unspecified", "BNP", "Heart failure biomarker panel", [obs("BNP", "B-Type Natriuretic Peptide", str(940 + variant * 40), "pg/mL", "<100", "H"), obs("WT", "Weight", str(208 + variant * 4), "lb", "", "A")], {"code": "RX2001", "text": "Furosemide", "dose": "20 mg daily", "route": "PO"}, "Emergency presentation with fluid overload.", message_type="ADT^A01", location="ER^07^01"),
        visit(dt(base, 2, 9, 0), "I", "Heart Failure Institute", "Cardio Biomarker Lab", "Thomas", "Reed", "CARD", "I50.9", "Acute decompensated heart failure", "BNP", "Inpatient heart failure management", [obs("BNP", "B-Type Natriuretic Peptide", str(780 + variant * 30), "pg/mL", "<100", "H"), obs("WT", "Weight", str(205 + variant * 4), "lb", "", "A")], {"code": "RX2002", "text": "Furosemide", "dose": "40 mg daily", "route": "PO"}, "Admitted for diuresis and medication optimization.", message_type="ADT^A01", location="CARD^05^11"),
        visit(dt(base, 24, 10, 15), "O", "Heart Failure Institute", "Cardio Biomarker Lab", "Thomas", "Reed", "CARD", "I50.9", "Heart failure, unspecified", "BNP", "Cardiology follow-up", [obs("BNP", "B-Type Natriuretic Peptide", str(540 + variant * 25), "pg/mL", "<100", "H"), obs("WT", "Weight", str(201 + variant * 3), "lb", "", "A")], {"code": "RX2003", "text": "Furosemide + Carvedilol", "dose": "40 mg daily + 3.125 mg BID", "route": "PO"}, "Early outpatient follow-up after discharge.", message_type="ADT^A08"),
        visit(dt(base, 90, 9, 25), "O", "Heart Failure Institute", "Cardio Biomarker Lab", "Thomas", "Reed", "CARD", "I50.9", "Heart failure, unspecified", "BNP", "Longitudinal heart failure monitoring", [obs("BNP", "B-Type Natriuretic Peptide", str(410 + variant * 20), "pg/mL", "<100", "H"), obs("WT", "Weight", str(197 + variant * 3), "lb", "", "A")], {"code": "RX2004", "text": "Furosemide + Carvedilol", "dose": "40 mg daily + 6.25 mg BID", "route": "PO"}, "Stable repeat visit with continued medication titration.", message_type="ADT^A08"),
    ]


def scenario_renal_stone_followup(base: datetime, variant: int) -> list[dict]:
    return [
        visit(dt(base, 0, 16, 45), "E", "Regional Medical Center", "Urology Imaging Lab", "Marcus", "Bell", "UROL", "N20.0", "Kidney stone", "CTABD", "Renal colic imaging review", [obs("PAIN", "Pain Score", str(9 - variant), "/10", "0-10", "H"), obs("HEMAT", "Hematuria", "Present", "", "", "A", "ST")], {"code": "RX2101", "text": "Tamsulosin", "dose": "0.4 mg daily", "route": "PO"}, "Emergency renal colic presentation.", message_type="ADT^A01", location="ER^08^01"),
        visit(dt(base, 14, 9, 35), "O", "Regional Urology Clinic", "Urology Imaging Lab", "Marcus", "Bell", "UROL", "Z87.442", "Personal history of urinary calculi", "FOLLOW", "Post-stone follow-up", [obs("PAIN", "Pain Score", "1", "/10", "0-10", "N"), obs("HEMAT", "Hematuria", "Resolved", "", "", "N", "ST")], {"code": "RX2102", "text": "Hydration plan", "dose": "Increase fluids to 2 liters daily", "route": "PO"}, "Symptoms resolved after stone passage.", message_type="ADT^A08"),
    ]


SCENARIO_BUILDERS = {
    "hypertension_monitor": scenario_hypertension_monitor,
    "appendicitis_followup": scenario_appendicitis_followup,
    "pneumonia_admit_followup": scenario_pneumonia_admit_followup,
    "ankle_followup": scenario_ankle_followup,
    "diabetes_monitor": scenario_diabetes_monitor,
    "dermatitis_followup": scenario_dermatitis_followup,
    "chest_pain_ruleout": scenario_chest_pain_ruleout,
    "migraine_med_adjust": scenario_migraine_med_adjust,
    "gerd_stable": scenario_gerd_stable,
    "back_pain_followup": scenario_back_pain_followup,
    "routine_physical_single": scenario_routine_physical_single,
    "acute_uri_single": scenario_acute_uri_single,
    "asthma_escalation": scenario_asthma_escalation,
    "ckd_monitor": scenario_ckd_monitor,
    "copd_admit_followup": scenario_copd_admit_followup,
    "uti_escalation": scenario_uti_escalation,
    "thyroid_stable": scenario_thyroid_stable,
    "cellulitis_followup": scenario_cellulitis_followup,
    "depression_med_adjust": scenario_depression_med_adjust,
    "anemia_monitor": scenario_anemia_monitor,
    "chf_admit_followup": scenario_chf_admit_followup,
    "renal_stone_followup": scenario_renal_stone_followup,
}


def build_visits(patient: dict, patient_index: int) -> list[dict]:
    base = datetime(2025, 1, 6, 9, 0) + timedelta(days=patient_index * 5)
    variant = patient_index % 3
    return SCENARIO_BUILDERS[patient["track"]](base, variant)


def hl7_message(patient: dict, visits: list[dict], patient_index: int) -> str:
    first, middle, last = split_name(patient["name"])
    blocks = []
    for visit_index, item in enumerate(visits, start=1):
        facility = slugify(item["facility"])
        lab_facility = slugify(item["lab_facility"])
        provider = f"{item['provider_last']}^{item['provider_first']}"
        message_control_id = f"MSG{patient_index:03d}{visit_index:02d}"
        order_id = f"OB{patient_index:03d}{visit_index:02d}"
        segments = [
            f"MSH|^~\\&|EHR_SYSTEM|{facility}|LAB_SYSTEM|{lab_facility}|{item['message_datetime']}||{item['message_type']}|{message_control_id}|P|2.5",
            f"EVN|{item['message_type'].split('^')[-1]}|{item['message_datetime']}",
            f"PID|1||{patient['patient_id']}^^^{facility}^MR||{last}^{first}^{middle}||{patient['dob'].replace('-', '')}|{patient['gender']}||2106-3|{patient['address_street']}^^{patient['city']}^{patient['state']}^{patient['zip_code']}^USA||{patient['phone']}|||S||AC{patient_index:06d}|999-88-{patient_index:04d}",
            f"PV1|1|{item['patient_class']}|{item['location']}^{facility}|||{provider}|||{item['specialty']}||||V{patient_index:04d}{visit_index:02d}|||{provider}|||||||||||||||||||||||||{item['admit_datetime']}",
            f"DG1|1||{item['diagnosis_code']}^{item['diagnosis_text']}^ICD-10||{item['message_datetime']}|A",
        ]

        if item["medication"]:
            med = item["medication"]
            segments.append(f"RXE|^^^{med['code']}^{med['text']}|{med['dose']}|{med['route']}")

        segments.append(f"OBR|1||{order_id}|{item['order_code']}^{item['order_text']}|||{item['admit_datetime']}")

        for obs_index, observation in enumerate(item["observations"], start=1):
            segments.append(
                f"OBX|{obs_index}|{observation['type']}|{observation['code']}^{observation['text']}||{observation['value']}|{observation['unit']}|{observation['range']}|{observation['flag']}|||F"
            )

        if item["note"]:
            segments.append(f"NTE|1||{item['note']}")

        segments.append(f"AL1|1||{patient['allergy_code']}^{patient['allergy_text']}")
        blocks.append("\n".join(segments))

    return "\n\n".join(blocks)


def index_html(cards: list[str], total_patients: int) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>HealthDataX Patients</title>
    <link rel="stylesheet" href="./styles.css" />
  </head>
  <body>
    <main class="page">
      <header class="topbar">
        <div class="topbar-left">
          <strong>HealthDataX</strong>
        </div>
        <nav class="topbar-right">
          <a class="creator-link" href="https://www.linkedin.com/in/manoharshasappa/" target="_blank" rel="noreferrer">Connect with Creator</a>
        </nav>
      </header>

      <section class="welcome-banner">
        <div class="welcome-copy">
          <strong>Welcome</strong>
          <p>
            People are welcome to explore and scrape this website, create beautiful insights, and use the synthetic healthcare records for learning and analysis.
          </p>
        </div>
        <a class="github-link" href="https://github.com/ManoHarshaSappa/HealthCare_DataWebsite" target="_blank" rel="noreferrer">
          View GitHub Repository
        </a>
      </section>

      <section class="hero">
        <p class="eyebrow">Synthetic HL7 Patient Portal</p>
        <h1>Synthetic Healthcare Data Platform</h1>
        <p class="subtitle">
          Explore longitudinal HL7 patient records and clinical data insights across {total_patients} synthetic patients.
        </p>
      </section>

      <section class="records-table-wrap">
        <table class="records-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Username</th>
              <th>Password</th>
              <th>Visits</th>
            </tr>
          </thead>
          <tbody>
        {''.join(cards)}
          </tbody>
        </table>
      </section>
    </main>
  </body>
</html>
"""


def patient_card(patient: dict, visit_count: int) -> str:
    return f"""
            <tr class="record-row" onclick="window.location.href='./patients/{patient['patient_id']}.html'">
              <td class="record-name">{patient['name']}</td>
              <td>{patient['user_id']}</td>
              <td>{patient['password']}</td>
              <td>{visit_count} visit{'s' if visit_count != 1 else ''}</td>
            </tr>
"""


def patient_detail_html(patient: dict, raw_file: str, visit_count: int) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{patient['name']} | HealthDataX</title>
    <link rel="stylesheet" href="../styles.css" />
  </head>
  <body>
    <main class="page detail-page">
      <a class="back-link" href="../index.html">Back to Patients</a>

      <section class="detail-header">
        <div>
          <p class="eyebrow">Patient HL7 Record</p>
          <h1>{patient['name']}</h1>
          <p class="subtitle">Username: {patient['user_id']} | Password: {patient['password']} | Visits: {visit_count}</p>
        </div>
      </section>

      <section class="hl7-panel">
        <div class="hl7-top">
          <strong>Raw HL7 Message History</strong>
          <span>{patient['patient_id']}</span>
        </div>
        <pre id="hl7-output" class="hl7-output" data-source="../raw_hl7/{raw_file}">Loading HL7...</pre>
      </section>
    </main>

    <script>
      const output = document.getElementById("hl7-output");
      fetch(output.dataset.source)
        .then((response) => response.text())
        .then((text) => {{
          output.textContent = text;
        }})
        .catch((error) => {{
          output.textContent = "Unable to load HL7: " + error.message;
        }});
    </script>
  </body>
</html>
"""


def styles_css() -> str:
    return """:root {
  --blue: #2563eb;
  --bg: #f8fafc;
  --surface: #ffffff;
  --border: #e2e8f0;
  --text: #0f172a;
  --muted: #64748b;
  --shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Inter, Roboto, "Segoe UI", sans-serif;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  color: var(--text);
}

a {
  color: inherit;
  text-decoration: none;
}

.page {
  width: calc(100% - 24px);
  margin: 0 auto;
  padding: 0 0 36px;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 10px;
  padding: 12px 16px;
  background: linear-gradient(90deg, #eff6ff 0%, #dbeafe 100%);
  border: 0;
  border-radius: 16px;
  box-shadow: none;
}

.topbar-left strong {
  display: block;
  font-size: 1.05rem;
}

.topbar-right {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.creator-link {
  color: var(--blue);
  font-weight: 700;
  padding: 0.55rem 0.9rem;
  border-radius: 999px;
  background: rgba(37, 99, 235, 0.08);
}

.welcome-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 16px;
  padding: 16px 18px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 18px;
  box-shadow: var(--shadow);
}

.welcome-copy strong {
  display: block;
  font-size: 1rem;
  margin-bottom: 6px;
}

.welcome-copy p {
  margin: 0;
  color: var(--muted);
  line-height: 1.7;
}

.github-link {
  flex-shrink: 0;
  color: var(--blue);
  font-weight: 700;
}

.hero,
.detail-header {
  margin-bottom: 18px;
}

.eyebrow {
  margin: 0 0 10px;
  color: var(--blue);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

h1 {
  margin: 0;
  font-size: clamp(2.4rem, 4vw, 4rem);
  line-height: 0.95;
}

.subtitle {
  margin: 12px 0 0;
  color: var(--muted);
  font-size: 1rem;
  line-height: 1.7;
}

.records-table-wrap,
.hl7-panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 22px;
  box-shadow: var(--shadow);
}

.records-table-wrap {
  overflow: hidden;
}

.records-table {
  width: 100%;
  border-collapse: collapse;
}

.records-table thead {
  background: #f8fbff;
}

.records-table th,
.records-table td {
  padding: 1rem 1.25rem;
  text-align: left;
  border-bottom: 1px solid #eef2f7;
}

.records-table th {
  color: var(--muted);
  font-size: 0.82rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.record-row {
  transition: background 140ms ease;
  font-size: 0.97rem;
  cursor: pointer;
}

.records-table tbody tr:last-child td {
  border-bottom: 0;
}

.record-row:hover {
  background: rgba(37, 99, 235, 0.05);
}

.record-name {
  font-weight: 700;
  color: var(--text);
}

.record-row span:not(.record-name) {
  color: var(--muted);
}

.back-link {
  display: inline-block;
  margin-bottom: 20px;
  color: var(--blue);
  font-weight: 600;
}

.hl7-panel {
  overflow: hidden;
}

.hl7-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}

.hl7-top strong {
  font-size: 1rem;
}

.hl7-top span {
  color: var(--muted);
  font-size: 0.9rem;
}

.hl7-output {
  margin: 0;
  min-height: 620px;
  padding: 20px;
  overflow: auto;
  background: #0b1220;
  color: #dbeafe;
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  font-size: 0.95rem;
  line-height: 1.8;
  white-space: pre-wrap;
}

@media (max-width: 720px) {
  .page {
    width: calc(100% - 12px);
    padding-top: 0;
  }

  .topbar {
    flex-direction: column;
    align-items: start;
  }

  .topbar-right {
    flex-wrap: wrap;
  }

  .welcome-banner {
    flex-direction: column;
    align-items: start;
  }

  .records-table thead {
    display: none;
  }

  .record-row {
    display: block;
  }

  .records-table tbody,
  .records-table tr,
  .records-table td {
    display: block;
    width: 100%;
  }

  .records-table td {
    padding: 0.45rem 1rem;
    border-bottom: 0;
  }

  .records-table tbody tr {
    padding: 0.55rem 0;
    border-bottom: 1px solid #eef2f7;
  }

  .hl7-top {
    flex-direction: column;
    align-items: start;
    gap: 6px;
  }
}
"""


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PATIENTS_DIR.mkdir(parents=True, exist_ok=True)

    cards = []
    for patient_index, patient in enumerate(PATIENTS, start=1):
        visits = build_visits(patient, patient_index)
        raw_name = f"{patient['patient_id']}.hl7"
        raw_path = RAW_DIR / raw_name
        message_text = hl7_message(patient, visits, patient_index)
        raw_path.write_text(message_text, encoding="utf-8")

        detail_path = PATIENTS_DIR / f"{patient['patient_id']}.html"
        detail_path.write_text(patient_detail_html(patient, raw_name, len(visits)), encoding="utf-8")

        cards.append(patient_card(patient, len(visits)))

    (OUTPUT_DIR / "index.html").write_text(index_html(cards, len(PATIENTS)), encoding="utf-8")
    (OUTPUT_DIR / "styles.css").write_text(styles_css(), encoding="utf-8")

    print(f"Built HealthDataX with {len(PATIENTS)} patients.")


if __name__ == "__main__":
    main()
