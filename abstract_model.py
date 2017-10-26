prettyprint_headervalue_position = 16
prettyprint_macroname_position = 20


class BlockTypes(object):

    HeaderTagType = 0
    SectionTagType = 1
    MacroDefinitionType = 2
    MacroConditionType = 3
    MacroUndefinitionType = 4
    CommentType = 5
    ConditionType = 6
    ChangelogTagType = 7



keys_list = [
    ['key', 'option', 'content'],
    ['keyword', 'name', 'parameters', 'subname', 'content'],
    ['keyword', 'name', 'options', 'body'],
    ['condition', 'name', 'content', 'ending'],
    ['keyword', 'name'],
    ['content'],
    ['keyword', 'expression', 'content', 'else_keyword', 'else_body', 'end_keyword'],
    ['author', 'date', 'mark', 'comment']
]

class RawSpecFile(object):

    def __init__(self):
        self.block_list = []
        self.metastring = ""
        self.beginning = ""
        self.end = ""

class SpecfileClass(object):

    def __init__(self):
        self.block_list = []
        self.metastring = ""
