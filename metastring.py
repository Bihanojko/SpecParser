import re

from abstract_model import keys_list



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
