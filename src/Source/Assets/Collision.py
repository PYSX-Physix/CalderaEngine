from PIL import Image

class CollisionObject():
    def __init__(self, mask_image_path):
        """
        mask_image_path: Path to an image file representing the object's collision mask.
        Non-transparent pixels are considered "solid" for collision.
        """
        self.mask_image = Image.open(mask_image_path).convert("L")  # Convert to grayscale
        self.mask = self.mask_image.point(lambda p: p > 0 and 1)  # 1 for solid, 0 for transparent
        self.width, self.height = self.mask.size

    def pixel_perfect_collides(self, other, offset=(0, 0)):
        """
        Checks for pixel-perfect collision with another CollisionObject.
        offset: (dx, dy) tuple representing the position of 'other' relative to self.
        """
        dx, dy = offset

        # Calculate overlap rectangle
        x1 = max(0, dx)
        y1 = max(0, dy)
        x2 = min(self.width, dx + other.width)
        y2 = min(self.height, dy + other.height)

        if x1 >= x2 or y1 >= y2:
            return False  # No overlap

        # Crop overlapping regions
        self_crop = self.mask.crop((x1, y1, x2, y2))
        other_crop = other.mask.crop((x1 - dx, y1 - dy, x2 - dx, y2 - dy))

        # Compare pixels
        self_pixels = self_crop.load()
        other_pixels = other_crop.load()
        for x in range(x2 - x1):
            for y in range(y2 - y1):
                if self_pixels[x, y] and other_pixels[x, y]:
                    return True  # Collision detected
        return False