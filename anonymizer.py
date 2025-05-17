import os
import hashlib
import pydicom
from explorer import get_dicom_files


def generate_uid_from_patient_id(patient_id, base_uid="1.2.826.0.1.3680043.9.7433"):
    """
    Generate a reproducible DICOM UID based on a PatientID.

    Parameters:
        patient_id (str): PatientID to hash for UID generation.
        base_uid (str): Base UID to prepend for uniqueness. Default is a public root.

    Returns:
        str: A reproducible DICOM UID.
    """
    # Ensure PatientID is a string
    patient_id = str(patient_id)
    hash_object = hashlib.md5(patient_id.encode())  # Hash the PatientID
    # Use decimal representation to ensure UID contains only digits
    hash_int = int.from_bytes(hash_object.digest(), "big")
    hash_suffix = str(hash_int)[:24]  # Limit to 24 digits
    return f"{base_uid}.{hash_suffix}"


def anonymize_dicom_files(input_dir, output_dir, base_uid="1.2.826.0.1.3680043.9.7433"):
    """
    Anonymizes all DICOM files in the input directory and generates reproducible UIDs
    based on PatientID.

    Parameters:
        input_dir (str): Directory containing the original DICOM files.
        output_dir (str): Directory to save anonymized DICOM files.
        base_uid (str): Base UID for reproducible UID generation.
    """
    # Retrieve all DICOM files from the input directory
    dicom_files = get_dicom_files(input_dir)
    print(f"Found {len(dicom_files)} DICOM files to anonymize.")

    for file_path in dicom_files:
        try:
            # Read the DICOM file
            dicom = pydicom.dcmread(file_path)

            # Extract PatientID (default to empty string if not present)
            patient_id = getattr(dicom, "PatientID", "default")

            # Anonymize fields containing PHI
            anonymized_fields = {
                "PatientName": "Anonymous",
                "PatientID": generate_uid_from_patient_id(
                    patient_id, base_uid
                ),  # Reproducible UID
                "PatientBirthDate": "",
                "PatientAddress": "",
                "InstitutionName": "Anonymized Institution",
                "ReferringPhysicianName": "Anonymized Physician",
                "StudyDate": "",
                "SeriesDate": "",
                "AcquisitionDate": "",
                "ContentDate": "",
                "StudyTime": "",
                "SeriesTime": "",
                "AcquisitionTime": "",
                "ContentTime": "",
            }

            for field, value in anonymized_fields.items():
                if hasattr(dicom, field):
                    setattr(dicom, field, value)

            # Replace UIDs with reproducible UIDs based on PatientID
            dicom.StudyInstanceUID = generate_uid_from_patient_id(
                patient_id + "Study", base_uid
            )
            dicom.SeriesInstanceUID = generate_uid_from_patient_id(
                patient_id + "Series", base_uid
            )
            dicom.SOPInstanceUID = generate_uid_from_patient_id(
                patient_id + "SOP", base_uid
            )

            # Remove private tags
            dicom.remove_private_tags()

            # Preserve folder structure
            relative_path = os.path.relpath(file_path, input_dir)
            output_path = os.path.join(output_dir, relative_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Save the anonymized DICOM file
            dicom.save_as(output_path)
            print(f"Anonymized and saved: {output_path}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
