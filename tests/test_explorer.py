import os
import unittest
import tempfile
from explorer import get_dicom_files


class TestGetDicomFiles(unittest.TestCase):
    def test_get_dicom_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dcm1 = os.path.join(tmpdir, "a.dcm")
            with open(dcm1, "w") as f:
                f.write("test")
            sub = os.path.join(tmpdir, "sub")
            os.makedirs(sub)
            dcm2 = os.path.join(sub, "b.DCM")
            with open(dcm2, "w") as f:
                f.write("test")
            with open(os.path.join(tmpdir, "c.txt"), "w") as f:
                f.write("nope")

            found = get_dicom_files(tmpdir)
            self.assertEqual(
                set(map(os.path.normpath, found)),
                {os.path.normpath(dcm1), os.path.normpath(dcm2)},
            )


if __name__ == "__main__":
    unittest.main()
