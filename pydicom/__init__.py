import pickle
import uuid
import sys

class Dataset(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object.__setattr__(self, 'is_little_endian', True)
        object.__setattr__(self, 'is_implicit_VR', True)
        object.__setattr__(self, 'file_meta', None)

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name in {'is_little_endian', 'is_implicit_VR', 'file_meta'}:
            object.__setattr__(self, name, value)
        else:
            self[name] = value

    def save_as(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    def remove_private_tags(self):
        pass

class FileMetaDataset(Dataset):
    pass

class _UIDModule:
    ImplicitVRLittleEndian = '1.2.840.10008.1.2'
    @staticmethod
    def generate_uid():
        return '2.25.' + str(uuid.uuid4().int)

uid = _UIDModule()

dataset = sys.modules[__name__]

def dcmread(path):
    with open(path, 'rb') as f:
        return pickle.load(f)
