class SpecModel(object):
    """Class containing SpecModel initialization"""

    def __init__(self):
        """Initialize SpecModel sections as empty lists."""
        self.HeaderTags = []
        self.SectionTags = []
        self.MacroDefinitions = []
        self.MacroConditions = []
        self.MacroUndefinitions = []
        self.Comments = []
        self.Conditions = []
        self.metastring = ""
