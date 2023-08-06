class Serializable():
    def __init__(self):
        self.id = hex(id(self))

    def serialize(self):
        return None

    def deserialize(self, data, hashmap={}, restore_id=True):
        if restore_id:
            self.id = data['id']
        hashmap[data['id']] = self
