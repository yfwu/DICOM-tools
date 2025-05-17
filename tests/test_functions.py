import os
import sys
import tempfile
import unittest

# Ensure project root is on sys.path for direct test execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from anonymizer import generate_uid_from_patient_id, anonymize_dicom_files
from explorer import get_dicom_files
from pydicom import FileDataset, FileMetaDataset
from pydicom.uid import (
    ExplicitVRLittleEndian,
    PYDICOM_IMPLEMENTATION_UID,
    SecondaryCaptureImageStorage,
)


def create_dummy_dicom(path, patient_id="TEST"):
    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = SecondaryCaptureImageStorage
    file_meta.MediaStorageSOPInstanceUID = generate_uid_from_patient_id(patient_id)
    file_meta.ImplementationClassUID = PYDICOM_IMPLEMENTATION_UID
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    ds = FileDataset(str(path), {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.PatientID = patient_id
    ds.is_little_endian = True
    ds.is_implicit_VR = False
    ds.save_as(str(path))


class TestDICOMTools(unittest.TestCase):
    def test_generate_uid_consistency(self):
        uid1 = generate_uid_from_patient_id("patient")
        uid2 = generate_uid_from_patient_id("patient")
        self.assertEqual(uid1, uid2)
        uid3 = generate_uid_from_patient_id("other")
        self.assertNotEqual(uid1, uid3)

    def test_get_dicom_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            d1 = os.path.join(tmpdir, "p1")
            d2 = os.path.join(tmpdir, "p2", "nested")
            os.makedirs(d1)
            os.makedirs(d2)
            create_dummy_dicom(os.path.join(d1, "a.dcm"))
            create_dummy_dicom(os.path.join(d2, "b.DCM"))
            with open(os.path.join(d1, "other.txt"), "w") as f:
                f.write("data")
            found = get_dicom_files(tmpdir)
            expected = {
                os.path.join(d1, "a.dcm"),
                os.path.join(d2, "b.DCM"),
            }
            self.assertEqual(set(found), expected)

    def test_anonymize_dicom_files_structure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = os.path.join(tmpdir, "input")
            output_dir = os.path.join(tmpdir, "output")
            os.makedirs(os.path.join(input_dir, "p1"))
            os.makedirs(os.path.join(input_dir, "p2", "nested"))
            create_dummy_dicom(os.path.join(input_dir, "p1", "a.dcm"), "P1")
            create_dummy_dicom(os.path.join(input_dir, "p2", "nested", "b.dcm"), "P2")

            anonymize_dicom_files(input_dir, output_dir)

            self.assertTrue(os.path.exists(os.path.join(output_dir, "p1", "a.dcm")))
            self.assertTrue(
                os.path.exists(os.path.join(output_dir, "p2", "nested", "b.dcm"))
            )
            found = []
            for root, _, files in os.walk(output_dir):
                for f in files:
                    if f.endswith(".dcm"):
                        found.append(os.path.join(root, f))
            self.assertEqual(len(found), 2)


if __name__ == "__main__":
    unittest.main()
