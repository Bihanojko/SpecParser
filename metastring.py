import re

from abstract_model import keys_list, BlockTypes, BlockTypeMismatchException
from specparser import HeaderTagBlock, ChangelogBlock, SectionBlock, ConditionBlock, MacroConditionBlock, MacroDefinitionBlock, CommentBlock, PackageBlock

class KeyMetastring(object):
    def __init__(self):
        self._left_ws = ""
        self._right_ws = ""
        self._idx = -1
        self._is_none = False

    def fromBlock(self, string, idx):
        if string == None:
            self._is_none = True
            return self

        if not isinstance(string, basestring):
            return self

        self._idx = idx

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

    def format(self, value):
        if self._is_none:
            return ""
        return "{}{}{}".format(self._left_ws, value, self._right_ws)

class BaseMetastring(object):
    def __init__(self):
        self._block_idx = None
        self._model_type = -1
        self._block_idx = None

    def setBlockIdx(self, model_type, idx = 0):
        self._model_type = model_type
        self._block_idx = idx

    def blockIdx(self):
        return self._block_idx

    def modelType(self):
        return self._model_type

    def to_str(self):
        metastring = "#"
        if self._block_idx != None:
            metastring += "{}:{}:".format(self._model_type, self._block_idx)

        for key in self._order:
            if isinstance(self.__dict__["_{}".format(key)], list):
                for item in self.__dict__["_{}".format(key)]:
                    metastring += item.to_str()
                continue
            metastring += self.__dict__["_{}".format(key)].to_str()
        return metastring

    def to_json(self):
        data = {"type": self._model_type, "idx": self._block_idx}
        for key in self._order:
            if isinstance(self.__dict__["_{}".format(key)], list):
                data[key] = []
                for item in self.__dict__["_{}".format(key)]:
                    if isinstance(item, KeyMetastring):
                        data[key].append(item.to_str())
                    else:
                        data[key].append(item.to_json())
                continue
            data[key] = self.__dict__["_{}".format(key)].to_str()
        return data

    def format(self, spec_model):
        return ""

class HeaderTagMetastring(BaseMetastring):
    def __init__(self, key, option, content):
        BaseMetastring.__init__(self)
        self._type = BlockTypes.HeaderTagType
        self._key = KeyMetastring().fromBlock(key, 0)
        self._option = KeyMetastring().fromBlock(option, 1)
        self._content = KeyMetastring().fromBlock(content, 2)

        self._order = ["key", "option", "content"]

    @staticmethod
    def cleanBlockType(block):
        return HeaderTagBlock(
            KeyMetastring.cleanBlock(block.key),
            KeyMetastring.cleanBlock(block.content),
            KeyMetastring.cleanBlock(block.option)
        )

    def format(self, specmodel):
        tag = specmodel.getTag(self._block_idx)
        if tag.option == None:
            return "{}:{}".format(self._key.format(tag.key), self._content.format(tag.content))
        else:
            return "{}({}):{}".format(self._key.format(tag.key), self._option.format(tag.option), self._content.format(tag.content))

class SectionMetastring(BaseMetastring):
    def __init__(self, keyword, parameters, name, subname, content):
        BaseMetastring.__init__(self)
        self._type = BlockTypes.SectionTagType
        self._keyword = KeyMetastring().fromBlock(keyword, 0)
        self._content = KeyMetastring().fromBlock(content, 4)
        self._parameters = KeyMetastring().fromBlock(parameters, 2)
        self._subname = KeyMetastring().fromBlock(subname, 3)
        self._name = KeyMetastring().fromBlock(name, 1)

        self._order = ["keyword", "name", "parameters", "subname", "content"]

    @staticmethod
    def cleanBlockType(block):
        return SectionBlock(
            KeyMetastring.cleanBlock(block.keyword),
            KeyMetastring.cleanBlock(block.parameters),
            KeyMetastring.cleanBlock(block.name),
            KeyMetastring.cleanBlock(block.subname),
            KeyMetastring.cleanBlock(block.content)
        )

class PackageMetastring(BaseMetastring):
    def __init__(self, keyword, parameters, subname):
        BaseMetastring.__init__(self)
        self._type = BlockTypes.SectionTagType
        self._keyword = KeyMetastring().fromBlock(keyword, 0)
        self._content = []
        self._parameters = KeyMetastring().fromBlock(parameters, 1)
        self._subname = KeyMetastring().fromBlock(subname, 2)

        self._order = ["keyword", "parameters", "subname", "content"]

    def setContentMetastring(self, metastring):
        self._content = metastring

    def getContentMetastring(self):
        return self._content

    @staticmethod
    def cleanBlockType(block):
        return PackageBlock(
            KeyMetastring.cleanBlock(block.keyword),
            KeyMetastring.cleanBlock(block.parameters),
            KeyMetastring.cleanBlock(block.subname),
            block.content
        )

    def format(self, specmodel):
        package = specmodel.getPackage(self._block_idx)
        body = []
        for item in self._content:
            print item

        exit(1)
        #return "{}{}{}{}{}{}".format(self._keyword.format("%if"), self._expression.format(condition), "".join(if_body), self._else_keyword.format("%else"), "".join(else_body), self._end_keyword.format("%endif"))

class ConditionMetastring(BaseMetastring):
    def __init__(self, keyword, expression, end_keyword, else_keyword = None):
        BaseMetastring.__init__(self)
        self._type = BlockTypes.ConditionType
        self._keyword = KeyMetastring().fromBlock(keyword, 0)
        self._expression = KeyMetastring().fromBlock(expression, 1)
        self._content = []
        self._else_body = []
        self._end_keyword = KeyMetastring().fromBlock(end_keyword, 5)
        self._else_keyword = KeyMetastring().fromBlock(else_keyword, 3)

        self._order = ["keyword", "expression", "content", "else_keyword", "else_body", "end_keyword"]

    def setIfBodyMetastring(self, body):
        self._content = body

    def getIfBodyMetastring(self):
        return self._content

    def setElseBodyMetastring(self, body):
        self._else_body = body

    def getElseBodyMetastring(self):
        return self._else_body

    @staticmethod
    def cleanBlockType(block):
        return ConditionBlock(
            KeyMetastring.cleanBlock(block.keyword),
            KeyMetastring.cleanBlock(block.expression),
            block.content,
            block.else_body,
            KeyMetastring.cleanBlock(block.end_keyword),
            KeyMetastring.cleanBlock(block.else_keyword)
        )

    def format(self, specmodel):
        condition = specmodel.getCondition(self._block_idx)
        if_body = []
        for item in self._content:
            if_body.append(item.format(specmodel))

        else_body = []
        for item in self._else_body:
            else_body.append(item.format(specmodel))

        return "{}{}{}{}{}{}".format(self._keyword.format("%if"), self._expression.format(condition), "".join(if_body), self._else_keyword.format("%else"), "".join(else_body), self._end_keyword.format("%endif"))

class MacroConditionMetastring(BaseMetastring):
    def __init__(self, condition, name, ending):
        BaseMetastring.__init__(self)
        self._type = BlockTypes.MacroConditionType
        self._condition = KeyMetastring().fromBlock(condition, 0)
        self._name = KeyMetastring().fromBlock(name, 1)
        self._content = []
        self._ending = KeyMetastring().fromBlock(ending, 3)

        self._order = ["condition", "name", "content", "ending"]

    def setContentMetastring(self, metastring):
        self._content = metastring

    def getContentMetastring(self):
        return self._content

    @staticmethod
    def cleanBlockType(block):
        return MacroConditionBlock(
            KeyMetastring.cleanBlock(block.name),
            KeyMetastring.cleanBlock(block.condition),
            KeyMetastring.cleanBlock(block.content),
            KeyMetastring.cleanBlock(block.ending)
        )

    def format(self, specmodel):
        macro = specmodel.getMacro(self._block_idx)
        metastrings = []
        for item in self._content:
            metastrings.append(item.format(specmodel))
        return "{{{}{}{}}}".format(self._condition.format(macro.condition), self._name.format(macro.name), "".join(metastrings), self._ending.format(macro.ending))

class MacroDefinitionMetastring(BaseMetastring):
    def __init__(self, keyword, name, options, body):
        BaseMetastring.__init__(self)
        self._type = BlockTypes.MacroDefinitionType
        self._keyword = KeyMetastring().fromBlock(keyword, 0)
        self._name = KeyMetastring().fromBlock(name, 1)
        self._options = KeyMetastring().fromBlock(options, 2)
        self._body = KeyMetastring().fromBlock(body, 3)

        self._order = ["keyword", "name", "options", "body"]

    @staticmethod
    def cleanBlockType(block):
        return MacroDefinitionBlock(
            KeyMetastring.cleanBlock(block.name),
            KeyMetastring.cleanBlock(block.keyword),
            KeyMetastring.cleanBlock(block.options),
            KeyMetastring.cleanBlock(block.body)
        )

    def format(self, specmodel):
        macro = specmodel.getMacro(self._block_idx)
        if macro.options == None:
            return "{}{}{}".format(self._keyword.format(macro.keyword), self._name.format(macro.name), self._body.format(macro.body))
        else:
            return "{}{}({}){}".format(self._keyword.format(macro.keyword), self._name.format(macro.name), self._options.format(macro.options), self._body.format(macro.body))

class CommentMetastring(BaseMetastring):
    def __init__(self, content):
        BaseMetastring.__init__(self)
        self._type = BlockTypes.CommentType
        self._content = KeyMetastring().fromBlock(content, 0)

        self._order = ["content"]

    @staticmethod
    def cleanBlockType(block):
        return CommentBlock(
            KeyMetastring.cleanBlock(block.content),
        )

    def format(self, specmodel):
        comment = specmodel.getComment(self._block_idx)
        return self._content.format(comment.content)

class ChangelogMetastring(BaseMetastring):
    def __init__(self, keyword, content):
        BaseMetastring.__init__(self)
        self._type = BlockTypes.SectionTagType
        self._keyword = KeyMetastring().fromBlock(keyword, 0)
        self._content = []
        for item in content:
            self._content.append( KeyMetastring().fromBlock(item, 4) )

        self._order = ["keyword", "content"]

    @staticmethod
    def cleanBlockType(block):
        content = []
        for item in block.content:
            content.append(KeyMetastring.cleanBlock(item))

        return ChangelogBlock(
            KeyMetastring.cleanBlock(block.keyword),
            KeyMetastring.cleanBlock(content)
        )

class MMetastring(object):
    def __init__(self, metastrings):
        self._metastrings = metastrings

    def format(self, spec_model):
        for metastring in self._metastrings:
            print repr(metastring.format(spec_model))

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
