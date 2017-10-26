class GoSpecModel(object):
    """Class containing GoSpecModel initialization"""

    def __init__(self):
        """Initialize GoSpecModel sections as empty field."""
        self.metadata = []
        self.main_unit = []
        self.unit_list = []
        self.history = {}
        self.comments = []
        self.metastring = ""
