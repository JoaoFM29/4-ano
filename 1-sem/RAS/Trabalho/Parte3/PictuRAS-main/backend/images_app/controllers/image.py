from typing import Optional, List
from models.image import Image, ImageFile, ImageChunk


def list_images() -> List[Image]:
    return Image.objects()


def find_by_id(image_id: str) -> Optional[Image]:
    return Image.objects.get(id=image_id)


def find_info_by_id(image_id: str) -> Optional[ImageFile]:
    image = Image.objects.get(id=image_id)
    return ImageFile.objects.get(id=image.image._id)


def find_chunks_by_id(image_id) -> Optional[List[ImageChunk]]:
    image = Image.objects.get(id=image_id)
    return ImageChunk.objects.filter(files_id=image.image._id).order_by('n')


def list_project_images(project_id: str) -> Optional[List[Image]]:
    return Image.objects.filter(project=project_id)


def insert_image(image: Image) -> Optional[Image]:
    image.save()
    return image


def update_image(image_id: str, new_image: Image) -> Optional[Image]:
    image = Image.objects.get(id=image_id)
    image_file = ImageFile.objects.get(id=image.image._id)
    image_chunks = ImageChunk.objects.filter(files_id=image.image._id).order_by('n')

    image.project = new_image.project
    image.image = new_image.image

    image.save()
    image_file.delete()

    for chunk in image_chunks:
        chunk.delete()

    return image


def delete_image(image_id: str) -> Optional[Image]:
    image = Image.objects.get(id=image_id)
    image.delete()
    return image