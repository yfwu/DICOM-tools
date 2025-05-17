"""Minimal stub of pydicom for testing purposes."""

import pickle
import uuid


class Dataset(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):
        self[name] = value

    def save_as(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    def remove_private_tags(self):
        pass


class FileDataset(Dataset):
    def __init__(self, filename, data=None, file_meta=None, preamble=None):
        super().__init__()
        if data:
            self.update(data)
        self.file_meta = file_meta
        self.filename = filename


class FileMetaDataset(Dataset):
    pass


def dcmread(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


class UID(str):
    pass


class _UIDModule:
    SecondaryCaptureImageStorage = UID("1.2.840.10008.5.1.4.1.1.7")
    ImplicitVRLittleEndian = UID("1.2.840.10008.1.2")
    ExplicitVRLittleEndian = UID("1.2.840.10008.1.2.1")
    PYDICOM_IMPLEMENTATION_UID = UID("1.2.826.0.1.3680043.8.498.1")

    def generate_uid(self):
        return UID(f"2.25.{uuid.uuid4().int}")


uid = _UIDModule()

from . import uid
