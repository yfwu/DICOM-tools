import os
import unittest
import tempfile
import pydicom
from anonymizer import generate_uid_from_patient_id, anonymize_dicom_files


class TestAnonymizer(unittest.TestCase):
    def test_generate_uid_consistent(self):
        uid1 = generate_uid_from_patient_id("patient1")
        uid2 = generate_uid_from_patient_id("patient1")
        self.assertEqual(uid1, uid2)

        custom_base = "1.2.3"
        uid3 = generate_uid_from_patient_id("patient1", base_uid=custom_base)
        uid4 = generate_uid_from_patient_id("patient1", base_uid=custom_base)
        self.assertEqual(uid3, uid4)

    def create_simple_dicom(self, path, patient_id="PID"):
        ds = pydicom.Dataset()
        ds.is_little_endian = True
        ds.is_implicit_VR = True
        ds.file_meta = pydicom.dataset.FileMetaDataset()
        ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
        ds.PatientID = patient_id
        ds.PatientName = "Test"
        ds.save_as(path)

    def test_anonymize_preserves_structure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = os.path.join(tmpdir, "input")
            subdir = os.path.join(input_dir, "inner")
            os.makedirs(subdir)
            dcm_path = os.path.join(subdir, "img.dcm")
            self.create_simple_dicom(dcm_path, patient_id="ABC")

            output_dir = os.path.join(tmpdir, "output")
            anonymize_dicom_files(input_dir, output_dir, base_uid="1.2.3")

            out_file = os.path.join(output_dir, "inner", "img.dcm")
            self.assertTrue(os.path.exists(out_file))
            ds = pydicom.dcmread(out_file)
            self.assertEqual(ds.PatientName, "Anonymous")
            self.assertTrue(ds.PatientID.startswith("1.2.3."))


if __name__ == "__main__":
    unittest.main()
