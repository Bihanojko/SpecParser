from __future__ import print_function
import json
import io
from copy import deepcopy
import sys

from abstract_model import SpecfileClass, BlockTypes, keys_list
from abstract_model import prettyprint_headervalue_position, prettyprint_macroname_position
from specparser import RawSpecFileParser
# from metastring import Metastring
from specmodel import SpecModelGenerator



class ModelMethods(object):
    """Class containing methods manipulating the specfile model"""


    def __init__(self):
        self.specfile = SpecfileClass()
        self._metastring_list = []


    @staticmethod
    def open_file(input_filepath):

        if input_filepath is None:
            input_filepath = raw_input("Enter path to a specfile or json file: ")

        try:
            input_file = io.open(input_filepath, mode='r', encoding="utf-8")
            input_data = input_file.read()
            input_file.close()
            return input_data
        except IOError:
            print('ERROR: Cannot open input file ' + input_filepath + '!')
            sys.exit(3)


    def create_abstract_model(self, input_filepath):

        inputfile_content = self.open_file(input_filepath)
        try:
            json_containing_parsed_spec = json.loads(inputfile_content)
            return SpecModelGenerator().fromJsonInput(json_containing_parsed_spec)
        except ValueError, _:
            parser = RawSpecFileParser(inputfile_content).parse()
            json_containing_parsed_spec = parser.json()
            raw = parser.raw()
            return SpecModelGenerator().fromRawSpecfile(raw)

        # TODO load model from input json
        # if 'metastring' in json_containing_parsed_spec and json_containing_parsed_spec['metastring'] != '':
        #     self.specfile.block_list = json_containing_parsed_spec['block_list']
        #     self.specfile.metastring = json_containing_parsed_spec['metastring']
        # else:
        #     return SpecModelGenerator().fromRawSpecfile(raw)
        #     data = spec_model.model_to_json()
        #     self.specfile.metastring = data["metastring"]
        #     self.specfile.block_list = json.loads(json.dumps(data["block_list"], sort_keys=True))


    @staticmethod
    def print_indentation(indentation):

        for _ in range(indentation):
            print(' ', end='')



    def pretty_print_block(self, intern_field, block_type, indentation):

        self.print_indentation(indentation)

        if block_type == BlockTypes.HeaderTagType:
            print(intern_field['key'], end='')
            length = len(intern_field['key']) + 1

            if 'option' in intern_field and intern_field['option'] is not None:
                print('(' + intern_field['option'] + ')', end='')
                length += 2 + len(intern_field['option'])

            print(':', end='')

            if length >= prettyprint_headervalue_position:
                length = prettyprint_headervalue_position - 2
            for _ in range(prettyprint_headervalue_position - length):
                print(' ', end='')

            print(intern_field['content'] + '\n', end='')

        elif block_type == BlockTypes.SectionTagType:
            print('%' + intern_field['keyword'], end='')
            if 'name' in intern_field and intern_field['name'] is not None:
                print(' ' + intern_field['name'], end='')
            if 'parameters' in intern_field and intern_field['parameters'] is not None:
                print(' -' + intern_field['parameters'], end='')
            if 'subname' in intern_field and intern_field['subname'] is not None:
                print(' ' + intern_field['subname'], end='')
            if not isinstance(intern_field['content'], list):
                print('\n' + intern_field['content'] + '\n\n', end='')
            else:
                for record in intern_field['content']:
                    print('\n' + str(record) + '\n', end='')

        elif block_type == BlockTypes.MacroDefinitionType:
            print('%' + intern_field['keyword'], end='')
            length = len(intern_field['keyword']) + 1

            if 'name' in intern_field and intern_field['name'] is not None:
                print(' ' + intern_field['name'], end='')
                length += len(intern_field['name']) + 1
            if 'options' in intern_field and intern_field['options'] is not None:
                print(' -' + intern_field['options'], end='')
                length += len(intern_field['options']) + 1

            if length >= prettyprint_macroname_position:
                length = prettyprint_macroname_position - 1
            for _ in range(prettyprint_macroname_position - length):
                print(' ', end='')

            print(intern_field['body'] + '\n', end='')

        elif block_type == BlockTypes.MacroConditionType:
            print('{' + intern_field['condition'], end='')
            if 'name' in intern_field and intern_field['name'] is not None:
                print(' ' + intern_field['name'] + ':', end='')
            self.print_pretty_field(intern_field['content'], 0)
            print('}\n', end='')

        elif block_type == BlockTypes.MacroUndefinitionType:
            print('%' + intern_field['keyword'], end='')
            if 'name' in intern_field and intern_field['name'] is not None:
                print(' ' + intern_field['name'] + '\n', end='')

        elif block_type == BlockTypes.CommentType:
            print(intern_field['content'] + '\n', end='')

        elif block_type == BlockTypes.ConditionType:
            print('%' + intern_field['keyword'] + ' ', end='')
            print(intern_field['expression'] + '\n\n', end='')
            if 'content' in intern_field and intern_field['content'] is not None:
                self.print_pretty_field(intern_field['content'], indentation + 2)
            if 'else_keyword' in intern_field and intern_field['else_keyword'] is not None:
                self.print_indentation(indentation)
                print('%' + intern_field['else_keyword'] + '\n', end='')
            if 'else_body' in intern_field and intern_field['else_body'] is not None:
                self.print_pretty_field(intern_field['else_body'], indentation + 2)
            self.print_indentation(indentation)
            print('%' + intern_field['end_keyword'] + '\n\n', end='')


    def print_pretty_field(self, block_list, indentation):

        if block_list is None:
            return

        for block_type in [5, 2, 0, 1, 3, 4, 6]:
            printed = False

            for intern_field in block_list:
                if intern_field != None and intern_field['block_type'] == block_type:
                    self.pretty_print_block(intern_field, block_type, indentation)
                    printed = True

            if printed and block_type != 6:
                print('\n', end='')


    # specfile class to specfile reconstruction - main
    def class_to_specfile(self, intern_specfile, pretty): # TODO pretty print

        if not pretty:
            if intern_specfile.block_list != []:
                self._metastring_list = self.specfile.metastring.split('#')
                print(self._metastring_list[0], end='')
                self._metastring_list = self._metastring_list[1:]
                self.print_field(intern_specfile.block_list)

        else:
            if intern_specfile.block_list != []:
                self.print_pretty_field(intern_specfile.block_list, 0)


    # specfile class to specfile reconstruction - subprocedure
    def print_field(self, block_list):

        if block_list is None:
            return

        for intern_field in block_list:
            if intern_field is not None and self._metastring_list != []:
                metastring_block_list = self._metastring_list[0].split('%')
                self._metastring_list = self._metastring_list[1:]
                print(metastring_block_list[0], end='')

                if intern_field['block_type'] == BlockTypes.HeaderTagType:
                    for metastring in metastring_block_list[1:]:
                        if int(metastring[0]) == 1:
                            print('(', end='')

                        print(intern_field[keys_list[intern_field['block_type']][int(metastring[0])]], end='')

                        if int(metastring[0]) == 0 and ('option' not in intern_field or intern_field['option'] is None):
                            print(':', end='')
                        elif int(metastring[0]) == 1:
                            print('):', end='')

                        print(metastring[1:], end='')

                elif intern_field['block_type'] == BlockTypes.SectionTagType:
                    counter = 0

                    for metastring in metastring_block_list[1:]:
                        if int(metastring[0]) == 0:
                            print('%', end='')
                        elif int(metastring[0]) == 2:
                            print('-', end='')
                        elif int(metastring[0]) == 4 and 'keyword' in intern_field and intern_field['keyword'] == 'package':
                            self.print_field(intern_field['content'])
                            break

                        if isinstance(intern_field[keys_list[intern_field['block_type']][int(metastring[0])]], list):
                            print(intern_field[keys_list[intern_field['block_type']][int(metastring[0])]][counter], end='')
                            counter += 1

                        else:
                            print(intern_field[keys_list[intern_field['block_type']][int(metastring[0])]], end='')
                        print(metastring[1:], end='')

                elif intern_field['block_type'] == BlockTypes.MacroDefinitionType:
                    for metastring in metastring_block_list[1:]:
                        if int(metastring[0]) == 0:
                            print('%', end='')

                        print(intern_field[keys_list[intern_field['block_type']][int(metastring[0])]], end='')
                        print(metastring[1:], end='')

                elif intern_field['block_type'] == BlockTypes.MacroConditionType:
                    for metastring in metastring_block_list[1:]:
                        if int(metastring[0]) == 0:
                            print('%{', end='')
                        elif int(metastring[0]) == 1:
                            print(intern_field[keys_list[intern_field['block_type']][int(metastring[0])]], end='')
                            print(':', end='')
                            if 'content' in intern_field and intern_field['content'] != []:
                                self.print_field(intern_field['content'])
                        elif int(metastring[0]) == 3:
                            print('}', end='')

                        if int(metastring[0]) != 1:
                            print(intern_field[keys_list[intern_field['block_type']][int(metastring[0])]], end='')
                        print(metastring[1:], end='')

                elif intern_field['block_type'] == BlockTypes.MacroUndefinitionType:
                    for metastring in metastring_block_list[1:]:
                        if int(metastring[0]) == 0:
                            print('%', end='')

                        print(intern_field[keys_list[intern_field['block_type']][int(metastring[0])]], end='')
                        print(metastring[1:], end='')

                elif intern_field['block_type'] == BlockTypes.CommentType:
                    for metastring in metastring_block_list[1:]:
                        print(intern_field[keys_list[intern_field['block_type']][int(metastring[0])]], end='')
                        print(metastring[1:], end='')

                elif intern_field['block_type'] == BlockTypes.ConditionType:
                    for metastring in metastring_block_list[1:]:
                        if int(metastring[0]) in [0, 3, 5]:
                            print('%', end='')

                        print(intern_field[keys_list[intern_field['block_type']][int(metastring[0])]], end='')
                        print(metastring[1:], end='')

                        if int(metastring[0]) == 1:
                            self.print_field(intern_field['content'])

                        elif int(metastring[0]) == 3:
                            self.print_field(intern_field['else_body'])


    def reduce_inner_block(self, single_block):

        reduced_single_block = deepcopy(single_block)

        if isinstance(single_block, dict):
            for (attr, value), (_, reduced_value) in zip(single_block.iteritems(), reduced_single_block.iteritems()):
                if (value is None or not value) and value != 0:
                    reduced_single_block.pop(attr, None)
                elif (isinstance(value, dict) or isinstance(value, list)) and attr != 'AP':
                    for (index, single_record) in enumerate(value):
                        reduced_value[index] = self.reduce_inner_block(single_record)

        return reduced_single_block


    def remove_empty_fields(self, Specfile):

        reduced_Specfile = deepcopy(Specfile)

        # Specfile 1.0 abstract model
        if hasattr(Specfile, 'block_list'):
            for (single_block, reduced_single_block) in zip(Specfile.block_list, reduced_Specfile.block_list):
                for (attr, value), (_, reduced_value) in zip(single_block.iteritems(), reduced_single_block.iteritems()):
                    if value is None or value == []:
                        reduced_single_block.pop(attr, None)
                    elif isinstance(value, list):
                        for (index, single_record) in enumerate(value):
                            reduced_value[index] = self.reduce_inner_block(single_record)

        # Specfile 2.0 JSON representation
        elif isinstance(Specfile, dict):
            for key in Specfile.keys():
                if Specfile[key] is None or Specfile[key] == []:
                    reduced_Specfile.pop(key, None)

        # Specfile 2.0 abstract model
        else:
            for block_list in Specfile.__dict__.iteritems():
                if block_list[1] is None or block_list[1] == []:
                    delattr(reduced_Specfile, block_list[0])

        return reduced_Specfile


    def print_json_representation(self, Specfile_to_print, reduced):

        if reduced:
            print(json.dumps(self.remove_empty_fields(Specfile_to_print), default=lambda o: o.__dict__, sort_keys=True))
        else:
            print(json.dumps(Specfile_to_print, default=lambda o: o.__dict__, sort_keys=True))


    def process_config_file(self, Specfile, config_path):

        config_data = self.open_file(config_path)
        # TODO config form and make it work
