from pathlib import Path

class Florence2ImageTagger:
    """Wrapper to invoke the local Florence 2 checkpoint."""

    def __init__(self, model_dir: str = "./florence") -> None:
        self.model_dir = Path(model_dir)
        # In a real implementation this would load the model.

    def process(self, image_path: str):
        """Generate title, description and tags for an image.

        This demo just creates placeholder data based on the file name.
        """
        fname = Path(image_path).stem
        title = fname.replace(" ", "_")[:20]
        description = f"Descripción generada automáticamente para {fname}."
        tags = ["etiqueta1", "etiqueta2"]
        return title, description, tags
