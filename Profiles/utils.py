import uuid


def generate_uuid():
    code = str(uuid.uuid4()).replace('-', '').upper()[:12]
    return code

