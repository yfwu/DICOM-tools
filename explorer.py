"""Helper utilities for discovering DICOM files on disk."""

import os


def get_dicom_files(input_dir):
    """Collect paths to DICOM files under ``input_dir``.

    The search is recursive and any file ending with ``.dcm`` or ``.DCM`` is
    considered a DICOM file.

    Parameters
    ----------
    input_dir : str
        Directory to search for DICOM files.

    Returns
    -------
    list of str
        List of file paths to discovered DICOM files.
    """
    dicom_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".dcm") or file.endswith("DCM"):
                # Check for DICOM file extension
                dicom_files.append(os.path.join(root, file))
    return dicom_files
