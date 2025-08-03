class PlayerInput:
    """
    Handles player input state.
    Example usage:
        input = PlayerInput()
        input.update({'up': True, 'left': False})
        if input.is_pressed('up'):
            ...
    """
    def __init__(self):
        self.state = {}

    def update(self, input_dict):
        """
        Update the input state.
        input_dict: dict of {action: bool}, e.g., {'up': True, 'left': False}
        """
        self.state.update(input_dict)

    def is_pressed(self, action):
        """
        Returns True if the given action is pressed.
        """
        return self.state.get(action, False)

    def reset(self):
        """
        Resets all input states to False.
        """
        for key in self.state:
            self.state[key] = False