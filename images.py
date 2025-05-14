from PIL import Image, ImageTk


def resize(image_path: str, width: int, height: int):
    image = Image.open(image_path)
    resized_image = image.resize((width, height), Image.LANCZOS)
    photo_image = ImageTk.PhotoImage(resized_image)
    return photo_image
