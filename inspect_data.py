from pathlib import Path

import json


DATA_FILE = Path("portal/data/patients.json")


def inspect_patients_json(file_path: Path) -> None:
    print(f"File: {file_path.name}")

    patients = json.loads(file_path.read_text())

    print(f"Patients: {len(patients)}")

    if not patients:
        return

    first_patient = patients[0]
    print("Sample keys:")
    print(sorted(first_patient.keys()))
    print("\nFirst patient:")
    print(json.dumps(first_patient, indent=2))


def main() -> None:
    if not DATA_FILE.exists():
        print(f"No patient data file found at {DATA_FILE.resolve()}")
        return

    inspect_patients_json(DATA_FILE)


if __name__ == "__main__":
    main()
