class UID(str):
    pass

SecondaryCaptureImageStorage = UID("1.2.840.10008.5.1.4.1.1.7")
ImplicitVRLittleEndian = UID("1.2.840.10008.1.2")
ExplicitVRLittleEndian = UID("1.2.840.10008.1.2.1")
PYDICOM_IMPLEMENTATION_UID = UID("1.2.826.0.1.3680043.8.498.1")

def generate_uid():
    import uuid
    return UID(f"2.25.{uuid.uuid4().int}")
