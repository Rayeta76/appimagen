from pathlib import Path
from PIL import Image

class ThumbnailGenerator:
    def __init__(self, output_dir: str = "./thumbnails", size: int = 256) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.size = size

    def create_thumbnail(self, image_path: str) -> str:
        src = Path(image_path)
        dst = self.output_dir / f"{src.stem}.thumbnail{src.suffix}"
        with Image.open(src) as im:
            im.thumbnail((self.size, self.size))
            im.save(dst)
        return str(dst)
