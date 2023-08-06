import hashlib

class Cell():
    def __init__(self, value) -> None:
        h = hashlib.new('sha256')
        h.update(str(value).encode())
        self.sha256 = h.hexdigest()
        self.value = value