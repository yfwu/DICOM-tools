"""Utilities for anonymizing DICOM files by removing patient information."""

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


def anonymize_dataset(dicom, patient_id, base_uid):
    """Anonymize a single DICOM dataset in place.

    Parameters
    ----------
    dicom : pydicom.dataset.Dataset
        Dataset to anonymize.
    patient_id : str
        Identifier used to generate reproducible UIDs.
    base_uid : str
        UID root used when generating deterministic UIDs.

    Returns
    -------
    pydicom.dataset.Dataset
        The anonymized dataset (same object as ``dicom``).
    """

    anonymized_fields = {
        "PatientName": "Anonymous",
        "PatientID": generate_uid_from_patient_id(patient_id, base_uid),
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

    dicom.StudyInstanceUID = generate_uid_from_patient_id(
        patient_id + "Study", base_uid
    )
    dicom.SeriesInstanceUID = generate_uid_from_patient_id(
        patient_id + "Series", base_uid
    )
    dicom.SOPInstanceUID = generate_uid_from_patient_id(
        patient_id + "SOP", base_uid
    )

    dicom.remove_private_tags()

    return dicom


def save_anonymized_dataset(dicom, file_path, input_dir, output_dir):
    """Save a DICOM dataset preserving the original directory structure."""

    relative_path = os.path.relpath(file_path, input_dir)
    output_path = os.path.join(output_dir, relative_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    dicom.save_as(output_path)
    return output_path


def anonymize_dicom_files(input_dir, output_dir, base_uid="1.2.826.0.1.3680043.9.7433"):
    """Anonymize all DICOM files found in *input_dir*.

    The function walks the input directory tree, anonymizes each dataset using
    :func:`anonymize_dataset` and saves the result to *output_dir* while
    preserving the directory layout.

    Parameters
    ----------
    input_dir : str
        Directory containing the original DICOM files.
    output_dir : str
        Directory to save anonymized DICOM files.
    base_uid : str, optional
        Base UID for reproducible UID generation.
    """

    dicom_files = get_dicom_files(input_dir)
    print(f"Found {len(dicom_files)} DICOM files to anonymize.")

    for file_path in dicom_files:
        try:
            dicom = pydicom.dcmread(file_path)
            patient_id = getattr(dicom, "PatientID", "default")
            anonymize_dataset(dicom, patient_id, base_uid)
            output_path = save_anonymized_dataset(dicom, file_path, input_dir, output_dir)
            print(f"Anonymized and saved: {output_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
