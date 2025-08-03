class Character:
    """
    Represents a game character with position and sprite.
    """
    def __init__(self, position=(0, 0), sprite=None):
        self.position = position  # (x, y) tuple
        self.sprite = sprite      # Can be a path to an image or an image object

    def move(self, dx, dy):
        """
        Move the character by (dx, dy).
        """
        x, y = self.position
        self.position = (x + dx, y + dy)