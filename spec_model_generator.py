from __future__ import print_function
import re
from copy import deepcopy

from metastring import Metastring
from abstract_model import BlockTypes, SpecfileClass
from spec_model import SpecModel
# from go_spec_model_generator import GoSpecModelGenerator


class SpecModelGenerator(object):
    """Class containing SpecModel generation methods"""

    rawspecmodel_metastring_list = []
    specmodel = SpecModel()
    list_of_blocks = []


    def __init__(self):
        pass


    @classmethod
    def initialize_list_of_blocks(cls):
        """Initialize list_of_blocks as a list of as many empty lists
           as how many types of blocks there are."""
        number_of_blocktypes = len([a for a in dir(BlockTypes) if not a.startswith('__')])
        for _ in range(number_of_blocktypes):
            cls.list_of_blocks.append([])


    @staticmethod
    def get_files_block_pos(block_list, wanted_block):
        """Get index of 'files' section to which wanted_block belongs to."""
        count = 0
        for block in block_list:
            if 'keyword' in block and block['keyword'] == 'files':
                if wanted_block['files'] is None:
                    if (('name' in block and block['name'] is None) or 'name' not in block) and \
                    (('subname' in block and block['subname'] is None) or 'subname' not in block):
                        return count
                elif ('name' in block and block['name'] == wanted_block['files']) or \
                ('name' not in block and 'files' not in wanted_block):
                    return count
            count += 1
        return -1


    @classmethod
    def create_blocks_from_specfile(cls):
        """Initialize list_of_blocks with specmodel sections content."""
        cls.list_of_blocks = []

        cls.list_of_blocks.append(cls.specmodel.HeaderTags)
        cls.list_of_blocks.append(cls.specmodel.SectionTags)
        cls.list_of_blocks.append(cls.specmodel.MacroDefinitions)
        cls.list_of_blocks.append(cls.specmodel.MacroConditions)
        cls.list_of_blocks.append(cls.specmodel.MacroUndefinitions)
        cls.list_of_blocks.append(cls.specmodel.Comments)
        cls.list_of_blocks.append(cls.specmodel.Conditions)



    @classmethod
    def create_specmodel(cls, rawspecmodel):
        """Create specmodel by transforming rawspecmodel to specmodel."""
        cls.initialize_list_of_blocks()
        cls.rawspecmodel_metastring_list = rawspecmodel.metastring.split('#')
        cls.specmodel.metastring += cls.rawspecmodel_metastring_list[0]
        cls.rawspecmodel_metastring_list = cls.rawspecmodel_metastring_list[1:]
        cls.transform_rawspec_to_specmodel(rawspecmodel.block_list, None)

        return cls.specmodel


    @classmethod
    def transform_rawspec_to_specmodel(cls, rawspecmodel_block_list, package_name):
        """Transform rawspec to specmodel."""
        for block in rawspecmodel_block_list:
            if package_name is not None:
                block['package'] = package_name
            metastring1 = cls.rawspecmodel_metastring_list[0]
            cls.rawspecmodel_metastring_list = cls.rawspecmodel_metastring_list[1:]
            block_metastring_list = metastring1.split('%')
            sequence_number = len(SpecModelGenerator.list_of_blocks[block['block_type']])
            cls.specmodel.metastring += '#' + str(block['block_type']) + str(sequence_number)
            SpecModelGenerator.list_of_blocks[block['block_type']].append(block)

            if 'content' in block and block['block_type'] in [3]:
                cls.specmodel.metastring += metastring1[:metastring1.find('%3')]
                metastring1 = '#' + str(block['block_type']) + str(sequence_number) + metastring1[metastring1.find('%3'):]

                SpecModelGenerator.transform_rawspec_to_specmodel(block['content'], package_name)
                del block['content']

            elif 'content' in block and block['block_type'] in [6]:
                if not 'else_body' in block or block['else_body'] == []:
                    number_of_next_item = 5
                else:
                    number_of_next_item = 3

                cls.specmodel.metastring += metastring1[:metastring1.find('%' + str(number_of_next_item))]
                metastring1 = '#' + str(block['block_type']) + str(sequence_number) + metastring1[metastring1.find('%' + str(number_of_next_item)):]

                SpecModelGenerator.transform_rawspec_to_specmodel(block['content'], package_name)
                del block['content']

            if 'else_body' in block:
                if block['else_body'] != []:
                    cls.specmodel.metastring += metastring1[:metastring1.find('%5')]
                    metastring1 = '#' + str(block['block_type']) + str(sequence_number) + metastring1[metastring1.find('%5'):]

                    SpecModelGenerator.transform_rawspec_to_specmodel(block['else_body'], package_name)
                del block['else_body']

            if 'keyword' in block and block['keyword'] == 'package':
                cls.specmodel.metastring += metastring1[:metastring1.find('%4')]
                metastring1 = '#' + str(block['block_type']) + str(sequence_number) + metastring1[metastring1.find('%4'):]

                SpecModelGenerator.transform_rawspec_to_specmodel(block['content'], block['subname'])
                del block['content']

            elif 'keyword' in block and block['keyword'] == 'files':
                block['content'] = re.findall(r'.*\s*', block['content'])
                used_file_fields = 0
                metastring = ''
                to_be_removed = []
                first = False

                for idx, single_file in enumerate(block['content']):
                    if single_file == '':
                        to_be_removed.append(idx)
                    elif single_file[0] == '#':
                        metastring += '#5' + str(len(SpecModelGenerator.list_of_blocks[5]))
                        SpecModelGenerator.list_of_blocks[5].append({'block_type': 5, 'content': block['content'][idx], 'files': block['name'], 'position': idx})
                        metastring += Metastring.create_metastring(SpecModelGenerator.list_of_blocks[5][-1], SpecModelGenerator.list_of_blocks[5][-1]['block_type'])
                        to_be_removed.append(idx)
                        first = True
                    else:
                        if first:
                            metastring += '#' + str(block['block_type']) + str(sequence_number)
                            first = False
                        metastring += block['content'][idx][:len(block['content'][idx]) - len(block['content'][idx].lstrip())]
                        metastring += '%4' + str(used_file_fields)
                        metastring += block['content'][idx][len(block['content'][idx].rstrip()):]
                        block['content'][idx] = block['content'][idx][len(block['content'][idx]) - len(block['content'][idx].lstrip()):len(block['content'][idx].rstrip())]
                        used_file_fields += 1

                for record in reversed(to_be_removed):
                    del block['content'][record]

                metastring1 = metastring1.replace('%4', metastring)

            cls.specmodel.metastring += block_metastring_list[0] + metastring1
        SpecModelGenerator.add_blocks_to_specfile()
        return cls.specmodel


    @classmethod
    def add_blocks_to_specfile(cls):
        """Initialize specmodel with list_of_blocks content."""
        cls.specmodel.HeaderTags = cls.list_of_blocks[0]
        cls.specmodel.SectionTags = cls.list_of_blocks[1]
        cls.specmodel.MacroDefinitions = cls.list_of_blocks[2]
        cls.specmodel.MacroConditions = cls.list_of_blocks[3]
        cls.specmodel.MacroUndefinitions = cls.list_of_blocks[4]
        cls.specmodel.Comments = cls.list_of_blocks[5]
        cls.specmodel.Conditions = cls.list_of_blocks[6]


    @classmethod
    def transform_specmodel_to_rawspec(cls, specmodel):
        """Backwards transformation of specmodel to rawspec."""
        cls.create_blocks_from_specfile()
        cls.rawspecmodel = SpecfileClass()
        cls.rawspecmodel_metastring_list = cls.specmodel.metastring.split('#')
        cls.rawspecmodel.metastring = cls.rawspecmodel_metastring_list[0]
        cls.rawspecmodel_metastring_list = cls.rawspecmodel_metastring_list[1:]

        (cls.rawspecmodel.block_list, cls.rawspecmodel.metastring) = cls.process_blocks()
        cls.rawspecmodel.metastring = Metastring.remove_block_ids(cls.rawspecmodel.metastring)

        return cls.rawspecmodel



    @staticmethod
    def get_outer_block_pos(block_list, wanted_block):
        """Find index of wanted_block in block_list."""
        count = 0

        for block in block_list:
            if block == wanted_block:
                return count
            count += 1
        return -1



    @classmethod
    def process_blocks(cls):
        """According to metastring information, process blocks of specmodel and add them to block_list."""
        block_list = []
        metastring1 = ''

        for metastring2 in cls.rawspecmodel_metastring_list:
            processed_already = False

            if int(metastring2[0]) == 6 and int(metastring2[metastring2.find('%') + 1]) != 0:
                pos_of_next_field = metastring1.find('#', metastring1.find('#' + metastring2[:metastring2.find('%')]) + 1)
                metastring1 = metastring1[:pos_of_next_field] + metastring2[metastring2.find('%'):] + metastring1[pos_of_next_field:]
            elif int(metastring2[0]) == 1 and cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['keyword'] == 'package':
                if int(metastring2[metastring2.find('%') + 1]) == 0:
                    metastring1 += '#' + metastring2
                else:
                    pos_of_next_field = metastring1.find('#', metastring1.find('#' + metastring2[:metastring2.find('%')]) + 1)
                    metastring1 = metastring1[:pos_of_next_field] + metastring2[metastring2.find('%'):] + metastring1[pos_of_next_field:]
            elif int(metastring2[0]) == 3 and int(metastring2[metastring2.find('%') + 1]) != 0:
                pos_of_next_field = metastring1.find('#', metastring1.find('#' + metastring2[:metastring2.find('%')]) + 1)
                metastring1 = metastring1[:pos_of_next_field] + metastring2[metastring2.find('%'):] + metastring1[pos_of_next_field:]

                pos = cls.get_outer_block_pos(block_list, cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])])
                cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['content'] = [block_list[pos+1]]
                block_list = block_list[:pos] + block_list[pos + 2:]
            else:
                metastring1 += '#' + metastring2

            if 'package' in cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]:
                del cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['package']

            if int(metastring2[0]) == 1 and cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['keyword'] == 'package':
                if int(metastring2[metastring2.find('%') + 1]) == 4:
                    pos = cls.get_outer_block_pos(block_list, cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])])
                    cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['content'] = deepcopy(block_list[pos+1:])
                    block_list = block_list[:pos]

            elif int(metastring2[0]) == 1 and cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['keyword'] == 'files':
                merged_content = ''

                if isinstance(cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['content'], list):
                    last_field_id = len(cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['content']) - 1
                else:
                    last_field_id = 1 
                file_records = re.findall(r'%4[^%]*', metastring2)
                first_record = True
                original_files_line_id = 0
                files_line_id = 0
                processed_already = False
                subtract = 0

                for single_file in file_records:
                    files_line_id = int(re.match(r'\d+', single_file[2:]).group())
                    original_files_line_id = files_line_id

                    if first_record and files_line_id != 0:
                        subtract = files_line_id - 1
                        processed_already = True
                    files_line_id -= subtract

                    if first_record:
                        first_record = False

                    if len(cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['content']) - 1 >= files_line_id:
                        merged_content += cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['content'][files_line_id]

                    if files_line_id != last_field_id:
                        merged_content += single_file[len(str(original_files_line_id)) + 2:]
                    else:
                        metastring1 += single_file[len(str(original_files_line_id)) + 2:]

                    if files_line_id == 0:
                        metastring1 = metastring1.replace(single_file, '%4')
                    elif processed_already and files_line_id == last_field_id:
                        metastring1 = metastring1.replace(re.search(r'\s*#\d+' + single_file, metastring1).group(), '')
                    else:
                        metastring1 = metastring1.replace(single_file, '')

                if not processed_already:
                    del cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['content'][0:files_line_id]
                    cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['content'][0] = merged_content
                else:
                    del cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['content'][1:files_line_id + 1]
                    cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['content'][0] += merged_content

                if len(cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['content']) == 1:
                    cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['content'] = cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['content'][0]

            elif int(metastring2[0]) == 5 and 'files' in cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]:

                processed_already = True

                pos = cls.get_files_block_pos(block_list, cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])])
                if pos != -1:
                    comment_metastring = re.findall(r'\s*#5' + metastring2[1:metastring2.find('%')] + r'[^#]*', metastring1)[0]
                    pre_comment_whitespace = re.findall(r'[^#]*', comment_metastring)[0]
                    post_comment_whitespace = re.search(r'\s*$', comment_metastring).group()

                    # due to some unicode assignment failures
                    tmp = []
                    if isinstance(block_list[pos]['content'], list):
                        tmp.append(block_list[pos]['content'][0] + pre_comment_whitespace + cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['content'] + post_comment_whitespace)
                        tmp += block_list[pos]['content'][1:]
                    else:
                        tmp.append(block_list[pos]['content'] + pre_comment_whitespace + cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['content'])

                    del block_list[pos]['content']
                    block_list[pos]['content'] = tmp
                    if len(block_list[pos]['content']) == 1:
                        block_list[pos]['content'] = block_list[pos]['content'][0]
                        metastring1 = metastring1.replace(comment_metastring, post_comment_whitespace)
                    else:
                        metastring1 = metastring1.replace(comment_metastring, '')

            elif int(metastring2[0]) == 6:
                if int(metastring2[metastring2.find('%') + 1]) == 3 or (int(metastring2[metastring2.find('%') + 1]) == 5 and 'content' not in cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]):
                    pos = cls.get_outer_block_pos(block_list, cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])])
                    cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['content'] = block_list[pos+1:]
                    block_list = block_list[:pos]

                elif int(metastring2[metastring2.find('%') + 1]) == 5:
                    pos = cls.get_outer_block_pos(block_list, cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])])
                    cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])]['else_body'] = block_list[pos+1:]
                    block_list = block_list[:pos]

            if not processed_already:
                block_list.append(cls.list_of_blocks[int(metastring2[0])][int(metastring2[1:metastring2.find('%')])])

        return (block_list, metastring1)
