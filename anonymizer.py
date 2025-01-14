import os
import pydicom
from pydicom.uid import generate_uid
from explorer import get_dicom_files


def anonymize_dicom_files(input_dir, output_dir):
    """
    Anonymizes all DICOM files from the input directory (including nested folders)
    and saves them to the output directory with the same structure.

    Parameters:
        input_dir (str): Directory containing the original DICOM files.
        output_dir (str): Directory to save anonymized DICOM files.
    """
    # Retrieve all DICOM files from the input directory
    dicom_files = get_dicom_files(input_dir)
    print(f"Found {len(dicom_files)} DICOM files to anonymize.")

    for file_path in dicom_files:
        try:
            # Read the DICOM file
            dicom = pydicom.dcmread(file_path)

            # Anonymize fields containing PHI
            anonymized_fields = {
                "PatientName": "Anonymous",
                "PatientID": generate_uid(),  # Use a unique ID
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
