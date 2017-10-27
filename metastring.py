import re

from abstract_model import keys_list, BlockTypes, BlockTypeMismatchException
from specparser import HeaderTagBlock, ChangelogBlock, SectionBlock, ConditionBlock, MacroConditionBlock, MacroDefinitionBlock, CommentBlock

class KeyMetastring(object):
    def __init__(self):
        self._left_ws = ""
        self._right_ws = ""
        self._idx = -1

    def fromBlock(self, string, idx):
        if not isinstance(string, basestring):
            return self

        self._idx = idx
        if string == None:
            return self

        if string.isspace():
            self._right_ws = string
            return self

        self._left_ws = string[:len(string) - len(string.lstrip())]
        self._right_ws = string[len(string.rstrip()):]

        return self

    @staticmethod
    def cleanBlock(string):
        if string == None:
            return None

        if isinstance(string, basestring):
            return string.strip()

        return string

    def to_str(self):
        if self._idx == -1:
            return ""

        return "{}%{}{}".format(self._left_ws, self._idx, self._right_ws)

class HeaderTagMetastring(object):
    def __init__(self):
        self._type = BlockTypes.HeaderTagType
        self._key = None
        self._option = None
        self._content = None

    def fromBlockType(self, block):
        if block.block_type != BlockTypes.HeaderTagType:
            # TODO(jchaloup): replace the block type number with a string name
            raise BlockTypeMismatchException("Expected HeaderTagType, got {} instead".format(block.block_type))

        self._key = KeyMetastring().fromBlock(block.key, 0)
        self._option = KeyMetastring().fromBlock(block.option, 1)
        self._content = KeyMetastring().fromBlock(block.content, 2)

        return self

    def cleanBlockType(self, block):
        return HeaderTagBlock(
            KeyMetastring.cleanBlock(block.key),
            KeyMetastring.cleanBlock(block.content),
            KeyMetastring.cleanBlock(block.option)
        )

    def to_str(self):
        metastring = ""
        for ms in [self._key, self._option, self._content]:
            metastring += ms.to_str()
        return metastring

class SectionMetastring(object):
    def __init__(self):
        self._type = BlockTypes.SectionTagType
        self._keyword = None
        self._content = None
        self._parameters = None
        self._subname = None
        self._name = None
        self._section_type = ""

    def fromBlockType(self, block):
        if block.block_type != BlockTypes.SectionTagType:
            # TODO(jchaloup): replace the block type number with a string name
            raise BlockTypeMismatchException("Expected SectionTagType, got {} instead".format(block.block_type))

        self._keyword = KeyMetastring().fromBlock(block.keyword, 0)
        # Given the section keyword is not checked, its content can be basically anything.
        # Either string, array, dictionary. However, only the string content
        # can be metastringed and the current implemention of the metastring extraction
        # skips all non-string contents. So the section metastring gets extracted
        # before its non-string content is processed.
        self._name = KeyMetastring().fromBlock(block.name, 1)
        self._parameters = KeyMetastring().fromBlock(block.parameters, 2)
        self._subname = KeyMetastring().fromBlock(block.subname, 3)
        self._content = KeyMetastring().fromBlock(block.content, 4)
        self._section_type = block.keyword.strip()

        return self

    def cleanBlockType(self, block):
        return SectionBlock(
            KeyMetastring.cleanBlock(block.keyword),
            KeyMetastring.cleanBlock(block.parameters),
            KeyMetastring.cleanBlock(block.name),
            KeyMetastring.cleanBlock(block.subname),
            KeyMetastring.cleanBlock(block.content)
        )

    def to_str(self):
        metastring = ""
        for ms in [self._keyword, self._name, self._parameters, self._subname, self._content]:
            metastring += ms.to_str()
        # TODO(jchaloup): why do we need this?
        if self._section_type == "package":
            metastring += "%4"
        return metastring

class ConditionMetastring(object):
    def __init__(self):
        self._type = BlockTypes.ConditionType
        self._keyword = None
        self._expression = None
        self._content = None
        self._else_body = None
        self._end_keyword = None
        self._else_keyword = None

    def fromBlockType(self, block):
        if block.block_type != BlockTypes.ConditionType:
            # TODO(jchaloup): replace the block type number with a string name
            raise BlockTypeMismatchException("Expected ConditionType, got {} instead".format(block.block_type))

        self._keyword = KeyMetastring().fromBlock(block.keyword, 0)
        self._expression = KeyMetastring().fromBlock(block.expression, 1)
        self._content = KeyMetastring().fromBlock(block.content, 2)
        self._else_keyword = KeyMetastring().fromBlock(block.else_keyword, 3)
        self._else_body = KeyMetastring().fromBlock(block.else_body, 4)
        self._end_keyword = KeyMetastring().fromBlock(block.end_keyword, 5)

        return self

    def cleanBlockType(self, block):
        return ConditionBlock(
            KeyMetastring.cleanBlock(block.keyword),
            KeyMetastring.cleanBlock(block.expression),
            KeyMetastring.cleanBlock(block.content),
            KeyMetastring.cleanBlock(block.else_body),
            KeyMetastring.cleanBlock(block.end_keyword),
            KeyMetastring.cleanBlock(block.else_keyword)
        )

    def to_str(self):
        metastring = ""
        for ms in [self._keyword, self._expression, self._content, self._else_keyword, self._else_body, self._end_keyword]:
            metastring += ms.to_str()
        return metastring

class MacroConditionMetastring(object):
    def __init__(self):
        self._type = BlockTypes.MacroConditionType
        self._condition = None
        self._name = None
        self._content = None
        self._ending = None

    def fromBlockType(self, block):
        if block.block_type != BlockTypes.MacroConditionType:
            # TODO(jchaloup): replace the block type number with a string name
            raise BlockTypeMismatchException("Expected MacroConditionType, got {} instead".format(block.block_type))

        self._condition = KeyMetastring().fromBlock(block.condition, 0)
        self._name = KeyMetastring().fromBlock(block.name, 1)
        self._content = KeyMetastring().fromBlock(block.content, 2)
        self._ending = KeyMetastring().fromBlock(block.ending, 3)

        return self

    def cleanBlockType(self, block):
        return MacroConditionBlock(
            KeyMetastring.cleanBlock(block.name),
            KeyMetastring.cleanBlock(block.condition),
            KeyMetastring.cleanBlock(block.content),
            KeyMetastring.cleanBlock(block.ending)
        )

    def to_str(self):
        metastring = ""
        for ms in [self._condition, self._name, self._content, self._ending]:
            metastring += ms.to_str()
        return metastring

class MacroDefinitionMetastring(object):
    def __init__(self):
        self._type = BlockTypes.MacroDefinitionType
        self._keyword = None
        self._name = None
        self._options = None
        self._body = None

    def fromBlockType(self, block):
        if block.block_type != BlockTypes.MacroDefinitionType:
            # TODO(jchaloup): replace the block type number with a string name
            raise BlockTypeMismatchException("Expected MacroDefinitionType, got {} instead".format(block.block_type))

        self._keyword = KeyMetastring().fromBlock(block.keyword, 0)
        self._name = KeyMetastring().fromBlock(block.name, 1)
        self._options = KeyMetastring().fromBlock(block.options, 2)
        self._body = KeyMetastring().fromBlock(block.body, 3)

        return self

    def cleanBlockType(self, block):
        return MacroDefinitionBlock(
            KeyMetastring.cleanBlock(block.name),
            KeyMetastring.cleanBlock(block.keyword),
            KeyMetastring.cleanBlock(block.options),
            KeyMetastring.cleanBlock(block.body)
        )

    def to_str(self):
        metastring = ""
        for ms in [self._keyword, self._name, self._options, self._body]:
            metastring += ms.to_str()
        return metastring

class CommentMetastring(object):
    def __init__(self):
        self._type = BlockTypes.CommentType
        self._content = None

    def fromBlockType(self, block):
        if block.block_type != BlockTypes.CommentType:
            # TODO(jchaloup): replace the block type number with a string name
            raise BlockTypeMismatchException("Expected CommentType, got {} instead".format(block.block_type))

        self._content = KeyMetastring().fromBlock(block.content, 0)

        return self

    def cleanBlockType(self, block):
        return CommentBlock(
            KeyMetastring.cleanBlock(block.content),
        )

    def to_str(self):
        metastring = ""
        for ms in [self._content]:
            metastring += ms.to_str()
        return metastring

class ChangelogMetastring(object):
    def __init__(self):
        self._type = BlockTypes.ChangelogTagType
        self._keyword = None
        self._content = []

    def fromBlockType(self, block):
        if block.block_type != BlockTypes.SectionTagType:
            # TODO(jchaloup): replace the block type number with a string name
            raise BlockTypeMismatchException("Expected ChangelogTagType, got {} instead".format(block.block_type))

        if not isinstance(block.content, list):
            raise TypeError("Expected Changelog content to be a list, got {} instead".format(type(block.content)))

        self._keyword = KeyMetastring().fromBlock(block.keyword, 0)
        for item in block.content:
            self._content.append( KeyMetastring().fromBlock(item, 4) )

        return self

    def cleanBlockType(self, block):
        content = []
        for item in block.content:
            content.append(KeyMetastring.cleanBlock(item))

        return ChangelogBlock(
            KeyMetastring.cleanBlock(block.keyword),
            KeyMetastring.cleanBlock(content)
        )

    def to_str(self):
        metastring = ""
        for ms in [self._keyword] + self._content:
            metastring += ms.to_str()
        return metastring


class Metastring(object):
    """Class containing metastring creation and manipulation operations."""

    def __init__(self):
        pass



    @staticmethod
    def get_whitespace(current_string, order):
        """Trim whitespace characters from both sides of current_string and form a metastring of the input string.

        Example:
            current_string = ' 0%{?fedora}\n'
            order = 1
            return: ' %1\n'"""
        if not isinstance(current_string, basestring):
            return ''

        if current_string.isspace():
            return '%' + str(order) + current_string

        metastring = current_string[:len(current_string) - len(current_string.lstrip())]
        metastring += '%' + str(order)
        metastring += current_string[len(current_string.rstrip()):]

        return metastring



    @staticmethod
    def create_metastring(single_block, block_type):
        """Create metastring for the given block single_block of type block_type.

        Example:
            single_block = {u'content': u'\t3.1.6\n', u'block_type': 0, u'option': None, u'key': u'Version'}
            block_type = 0
            return: '%0\t%2\n'"""
        metastring = ''

        for i, key in enumerate(keys_list[block_type]):

            if key in single_block:

                if isinstance(single_block[key], dict):
                    metastring += Metastring.create_metastring(single_block[key], single_block[key]['block_type'])

                    if 'keyword' in single_block and single_block['keyword'] == 'package':
                        metastring += '%' + str(i)

                else:
                    if isinstance(single_block[key], list):
                        if single_block[key] != []:
                            for j, record in enumerate(single_block[key]):
                                if isinstance(record, basestring):
                                    metastring += Metastring.get_whitespace(record, i)
                                    single_block[key][j] = record.strip()
                    else:
                        if single_block[key] is not None:
                            metastring += Metastring.get_whitespace(single_block[key], i)
                            single_block[key] = single_block[key].strip()

        return metastring



    @staticmethod
    def remove_block_ids(metastring):
        """Remove block type ids and sequence numbers from metastring.

        Example:
            metastring = '#00%0 %2\n#01%0 %2\n'
            return: '#%0 %2\n#%0 %2\n'"""
        return re.sub(r'#\d+%', '#%', metastring)



    @staticmethod
    def replace_field_number(metastring, prev_section_count, replacing):
        """In metastring, replace replacing[0] with '!' + replacing[1] + prev_section_count.

        Example:
            metastring = '#50%0\n \n#20%0 %1   %3\n#21%0 %1      %3 \n'
            prev_section_count = 8
            replacing = ['20', 0]
            return: '#50%0\n \n#!08%0 %1   %3\n#21%0 %1      %3 \n'"""
        to_be_replaced_list = re.findall(r'#' + str(replacing[0]) + '%', metastring)
        for replace_record in to_be_replaced_list:
            metastring = metastring.replace(replace_record, '#!' + str(replacing[1]) + str(prev_section_count) + '%')
        return metastring



    @staticmethod
    def change_metastring(metastring, index_old, index_new, unit_index):
        """In metastring, replace '!2' + index_old with '2<' + unit_index + '>' + index_new.

        Example:
            metastring = '#!20[55]%0        %2\n'
            index_old = 0
            index_new = 0
            unit_index = 1
            return: '#2<1>0[55]%0        %2\n'"""
        occurences = re.finditer(r'#!2' + str(index_old) + r'\[', metastring)
        for single_occurence in occurences:
            metastring = metastring.replace(single_occurence.group(), '#2<' + str(unit_index) + '>' + str(index_new) + '[')
        return metastring



    @staticmethod
    def check_for_conditions(metastring, section_pattern):
        """Get metastring of section preceding current section (with pattern section_pattern) and
        check if it is a conditional.

        Returns:
        Sequence number of condition if preceding section is '%if.*'
        -1 if preceding section is '%else'
        None in other cases"""
        prev_section_metastring = re.search(r'#[^#]*' + section_pattern, metastring)
        if prev_section_metastring is None:
            return None

        prev_section_metastring = prev_section_metastring.group()
        if prev_section_metastring[1] == '6' and prev_section_metastring[prev_section_metastring.find('%') + 1] == '0':
            return int(prev_section_metastring[2:prev_section_metastring.find('%')])
        elif (prev_section_metastring[1] == '6' and prev_section_metastring[prev_section_metastring.find('%') + 1] == '3') \
        or (prev_section_metastring[1] == '7' and prev_section_metastring[prev_section_metastring.find('%') + 1] == '0'):
            return -1

        return None
