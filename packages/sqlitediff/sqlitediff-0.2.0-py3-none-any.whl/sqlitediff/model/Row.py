import hashlib

class Row():
    def __init__(self, row) -> None:
        h = hashlib.new('sha256')
        h.update(str(row).encode())
        self.sha256 = h.hexdigest()
        self.values = row