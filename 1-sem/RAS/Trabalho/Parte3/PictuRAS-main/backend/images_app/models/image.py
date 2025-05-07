from mongoengine import Document, ImageField, StringField, IntField, LongField, ObjectIdField, DateTimeField, BinaryField # type: ignore


class ImageChunk(Document):

    meta = {'collection': 'images.chunks'}

    files_id = ObjectIdField(required=True)
    n = IntField(required=True)
    data = BinaryField(required=True)

    def to_json(self) -> dict:
        return {
            '_id': str(self.id),
            'files_id': str(self.files_id),
            'n': self.n,
            'data': self.data,
        }


class ImageFile(Document):

    meta = {'collection': 'images.files'}

    width = IntField(required=True)
    height = IntField(required=True)
    format = StringField(required=True)
    thumbnail_id = ObjectIdField()
    chunkSize = IntField()
    length = LongField()
    uploadDate = DateTimeField()

    def to_json(self) -> dict:
        return {
            '_id': str(self.id),
            'width': self.width,
            'height': self.height,
            'format': self.format,
            'chunkSize': self.chunkSize,
            'length': self.length,
            'uploadDate': str(self.uploadDate),
        }


class Image(Document):

    meta = {'collection': 'images'}

    project = ObjectIdField(required=True)
    image = ImageField(required=True)

    def to_json(self) -> dict:
        return {
            'id': str(self.id),
            'project': str(self.project),
            'image': str(self.image._id),
        }