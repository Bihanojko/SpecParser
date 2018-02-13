from __future__ import print_function
import re
from copy import deepcopy
import json


from abstract_model import BlockTypes, keys_list
from metastring import Metastring
from spec_model import SpecModel
from spec_model_generator import SpecModelGenerator
from go_spec_model import GoSpecModel


class GoSpecModelGenerator(object):
    """Class containing GoSpecModel generation methods"""

    gospecmodel = GoSpecModel()
    specmodelgenerator = SpecModelGenerator()
    Specfile2_from_GoSpec = SpecModel()
    ExcludeArch = []
    PredicateList = []


    def __init__(self):
        pass


    @classmethod
    def reduce_gospecmodel(cls):
        """Reduce GoSpecModel, e. g. delete unused fields."""
        reduced_gospecmodel = deepcopy(cls.gospecmodel)

        for (block_list, reduced_block_list) in zip(sorted(cls.gospecmodel.__dict__.iteritems()), sorted(reduced_gospecmodel.__dict__.iteritems())):
            if block_list[1] is None or block_list[1] == [[]] or block_list[1] == [] or block_list[1] == {} or block_list[1] == '':
                delattr(reduced_gospecmodel, block_list[0])
            elif isinstance(block_list[1], list):
                for (index, single_record) in reversed(list(enumerate(block_list[1]))):
                    if isinstance(single_record, list):
                        if single_record == []:
                            del reduced_block_list[1][index]
                        else:
                            to_be_removed = []
                            for (single_field_index, single_field) in enumerate(single_record):
                                if single_field['block_type'] == BlockTypes.HeaderTagType and re.match(r'(?i)requires', single_field['key']) is not None:
                                    reduced_block_list[1][index] = cls.append_dependency(reduced_block_list[1][index], 'runtime', single_field)
                                    to_be_removed.append([index, single_field_index])
                                elif single_field['block_type'] == BlockTypes.HeaderTagType and re.match(r'(?i)buildrequires', single_field['key']) is not None:
                                    cls.append_dependency(reduced_block_list[1][index], 'buildtime', single_field)
                                    to_be_removed.append([index, single_field_index])
                                elif single_field['block_type'] == BlockTypes.HeaderTagType and re.match(r'(?i)excludearch', single_field['key']) is not None:
                                    cls.append_dependency(reduced_block_list[1], 'excludearch', single_field)
                                    to_be_removed.append([index, single_field_index])
                                else:
                                    reduced_block_list[1][index][single_field_index] = cls.gospecmodel_to_print(single_field)
                                    
                            for record in reversed(sorted(to_be_removed)):
                                del reduced_block_list[1][record[0]][record[1]]
                                if reduced_block_list[1][record[0]] == []:
                                    del reduced_block_list[1][record[0]]
                    else:
                        if 'block_type' not in single_record:
                            for keyword in single_record:
                                if 'block_type' not in single_record[keyword]:
                                    for inner_keyword in single_record[keyword]:
                                        if single_record[keyword][inner_keyword] is not None:
                                            if 'block_type' in single_record[keyword][inner_keyword]:
                                                reduced_block_list[1][index][keyword][inner_keyword] = cls.gospecmodel_to_print(block_list[1][index][keyword][inner_keyword])

                        else:
                            if single_record['block_type'] == BlockTypes.HeaderTagType and re.match(r'(?i)requires', single_record['key']) is not None:
                                setattr(reduced_gospecmodel, reduced_block_list[0], cls.append_dependency(reduced_block_list[1], 'runtime', single_record))
                                del reduced_block_list[1][index]
                            elif single_record['block_type'] == BlockTypes.HeaderTagType and re.match(r'(?i)buildrequires', single_record['key']) is not None:
                                setattr(reduced_gospecmodel, reduced_block_list[0], cls.append_dependency(reduced_block_list[1], 'buildtime', single_record))
                                del reduced_block_list[1][index]
                            elif single_record['block_type'] == BlockTypes.HeaderTagType and re.match(r'(?i)excludearch', single_record['key']) is not None:
                                setattr(reduced_gospecmodel, reduced_block_list[0], cls.append_dependency(reduced_block_list[1], 'excludearch', single_record))
                                del reduced_block_list[1][index]
                            else:
                                reduced_block_list[1][index] = cls.gospecmodel_to_print(block_list[1][index])

            elif isinstance(block_list[1], dict):
                if block_list[1] != {}:
                    reduced_gospecmodel.history = cls.gospecmodel_to_print(block_list[1])

        return reduced_gospecmodel


    @staticmethod
    def append_dependency(current_unit, keyword, header_tag):
        """Append appropriate record from ExcludeArch, Requires or BuildRequires."""
        if current_unit == []:
            if keyword == 'excludearch':
                current_unit = {keyword:[header_tag['content']]}
            else:        
                current_unit = {keyword:{'dependencies':[{'name':header_tag['content']}]}}
        else:
            found = False
            for single_record in current_unit:
                if keyword in single_record:
                    found = True
                    if keyword == 'excludearch':
                        single_record[keyword].append(header_tag['content'])
                    else:
                        if 'dependencies' in single_record[keyword]:
                            single_record[keyword]['dependencies'].append({'name':header_tag['content']})
                        else:
                            single_record[keyword]['dependencies'] = [{'name':header_tag['content']}]

            if found is False:
                if keyword == 'excludearch':
                    current_unit.append({keyword:[header_tag['content']]})
                else:
                    current_unit.append({keyword:{'dependencies':[{'name':header_tag['content']}]}})

        return current_unit


    @classmethod
    def gospecmodel_to_print(cls, single_record):
        """Reduce GoSpecModel for printing - remove unnecessary information
        and transform all fields to a simpler representation."""
        predicate_list = []

        if 'AP' in single_record and single_record['AP'] != '':
            for single_predicate in single_record['AP']:
                single_condition = ''
                if single_predicate[2] != None:
                    single_condition += single_predicate[2] + ' '
                if single_predicate[1] == 0:
                    single_condition += 'NOT '
                predicate_list.append(single_condition + single_predicate[0])

        if single_record['block_type'] == BlockTypes.HeaderTagType:
            single_record = {single_record['key']:single_record['content']}

        elif single_record['block_type'] == BlockTypes.MacroDefinitionType:
            if 'name' in single_record and 'body' in single_record:
                single_record['name'] = '%' + single_record['name']
                single_record = {single_record['name']:single_record['body']}

        elif single_record['block_type'] == BlockTypes.SectionTagType:
            if 'keyword' in single_record and single_record['keyword'] == 'package':
                single_record = {'name':single_record['subname']}

            elif 'keyword' in single_record and 'content' in single_record:
                if single_record['keyword'] == 'changelog':
                    length = len(single_record['content']) - 1
                    for idx, single_log in enumerate(single_record['content']):
                        single_record[length - idx] = cls.parse_changelog(single_log)
                        Metastring.create_metastring(single_record[length - idx], BlockTypes.ChangelogTagType)
                        if 'keyword' in single_record:
                            del single_record['keyword']
                        if 'content' in single_record:
                            del single_record['content']
                    single_record['block_type'] = BlockTypes.ChangelogTagType
                    single_record = cls.gospecmodel_to_print(single_record)

                elif single_record['keyword'] == 'files':
                    parsed_record = {}
                    if 'subname' in single_record and single_record['subname'] is not None:
                        parsed_record.update({'meta':{'file':single_record['subname']}})
                    parsed_record.update({'list':single_record['content']})
                    single_record = {'files':parsed_record}

                else:
                    if single_record['content'] == '':
                        single_record['content'] = None
                    single_record = {single_record['keyword']:single_record['content']}

        elif single_record['block_type'] == BlockTypes.CommentType:
            single_record = single_record['content']

        elif single_record['block_type'] == BlockTypes.ChangelogTagType:
            del single_record['block_type']
            for record_index in single_record:
                for field in keys_list[BlockTypes.ChangelogTagType]:
                    if field in single_record[record_index] and single_record[record_index][field] == '':
                        single_record[record_index][field] = None

        if predicate_list != []:
            if isinstance(single_record, dict):
                single_record.update({'condition':predicate_list})
            elif isinstance(single_record, unicode):
                single_record = (single_record, {'condition':predicate_list})

        return single_record


    @staticmethod
    def parse_changelog(changelog):
        """Parse single changelog record into 4 given sections."""
        parsed_changelog = {}
        first_line = changelog[:changelog.find('\n')+1]

        parsed_changelog['comment'] = changelog[changelog.find('\n')+1:]
        parsed_changelog['date'] = first_line[first_line.find('*')+1:first_line.find('20')+4]
        parsed_changelog['mark'] = re.findall(r'\s+\-\s[\s\S]*', first_line)
        if parsed_changelog['mark'] == []:
            parsed_changelog['mark'] = re.findall(r'[\d\.\s-]*', first_line)
            if parsed_changelog['mark'] == []:
                parsed_changelog['mark'] = ''
            else:
                parsed_changelog['mark'] = parsed_changelog['mark'][-2]
        else:
            parsed_changelog['mark'] = parsed_changelog['mark'][0]

        parsed_changelog['author'] = first_line[first_line.find(parsed_changelog['date'])+(len(parsed_changelog['date'])):first_line.rfind(parsed_changelog['mark'])]

        return parsed_changelog


    @classmethod
    def process_unit_list(cls):
        """Transform a flat unit_list into a list of lists, where every list contains information
        about a single package."""
        used_unit_names = []

        for single_record in cls.gospecmodel.unit_list:
            for keyword in ['subname', 'name']:
                if keyword in single_record and single_record[keyword] != None:
                    if single_record[keyword] not in used_unit_names:
                        used_unit_names.append(single_record[keyword])

        if used_unit_names == []:
            return

        processed_unit_list = []
        for _ in range(len(used_unit_names) + 1):
            processed_unit_list.append([])

        for index, single_record in enumerate(cls.gospecmodel.unit_list):
            if 'subname' in single_record and single_record['subname'] != None:
                cls.gospecmodel.metastring = Metastring.change_metastring(cls.gospecmodel.metastring, index, len(processed_unit_list[used_unit_names.index(single_record['subname']) + 1]), used_unit_names.index(single_record['subname']) + 1)
                processed_unit_list[used_unit_names.index(single_record['subname']) + 1].append(single_record)
            elif 'name' in single_record and single_record['name'] != None:
                cls.gospecmodel.metastring = Metastring.change_metastring(cls.gospecmodel.metastring, index, len(processed_unit_list[used_unit_names.index(single_record['name']) + 1]), used_unit_names.index(single_record['name']) + 1)
                processed_unit_list[used_unit_names.index(single_record['name']) + 1].append(single_record)
            elif 'package' in single_record and single_record['package'] != None:
                cls.gospecmodel.metastring = Metastring.change_metastring(cls.gospecmodel.metastring, index, len(processed_unit_list[used_unit_names.index(single_record['package']) + 1]), used_unit_names.index(single_record['package']) + 1)
                processed_unit_list[used_unit_names.index(single_record['package']) + 1].append(single_record)
            elif single_record['block_type'] != BlockTypes.HeaderTagType:
                cls.gospecmodel.metastring = Metastring.change_metastring(cls.gospecmodel.metastring, index, len(processed_unit_list[0]), 0)
                processed_unit_list[0].append(single_record)

        cls.gospecmodel.unit_list = processed_unit_list

        return


    @classmethod
    def add_excludearch_tags(cls):
        """Append excludearch header tags information to gospec model."""
        if cls.gospecmodel.unit_list != []:
            for single_unit in cls.gospecmodel.unit_list:
                single_unit.append(cls.ExcludeArch[0:])
        else:
            for excludearch_tag in cls.ExcludeArch:
                cls.gospecmodel.main_unit = cls.gospecmodel.main_unit[:excludearch_tag[0]] + [excludearch_tag[1]] + cls.gospecmodel.main_unit[excludearch_tag[0]:]


    @classmethod
    def create_go_spec_model(cls, Specfile2_json_representation):
        """Transform specmodel into gospec model."""
        Specfile2 = json.loads(Specfile2_json_representation)
        cls.gospecmodel.metastring = Specfile2['metastring']

        prev_section_count = 0

        if 'HeaderTags' in Specfile2:
            for index, header_tag in enumerate(cls.specmodelgenerator.list_of_blocks[0]):
                if 'package' not in header_tag or header_tag['package'] == '':
                    if re.match(r'(?i)excludearch', header_tag['key']) is not None or \
                        re.match(r'(?i)requires', header_tag['key']) is not None or \
                        re.match(r'(?i)buildrequires', header_tag['key']) is not None:
                        cls.gospecmodel.main_unit.append(header_tag)
                        cls.gospecmodel.metastring = Metastring.replace_field_number(cls.gospecmodel.metastring, str(prev_section_count) + '[' + str(index) + ']', ['0' + str(index), 1])
                        prev_section_count += 1

                    elif 'AP' not in header_tag or header_tag['AP'] == '':
                        cls.gospecmodel.metadata.append(header_tag)

                        to_be_replaced_list = re.findall(r'#' + str('0' + str(index)) + '%', cls.gospecmodel.metastring)
                        for replace_record in to_be_replaced_list:
                            cls.gospecmodel.metastring = cls.gospecmodel.metastring.replace(replace_record, '#!' + str('0' + str(len(cls.gospecmodel.metadata) - 1) + '[' + str(index) + ']') + '%')
                else:
                    cls.gospecmodel.unit_list.append(header_tag)

                    to_be_replaced_list = re.findall(r'#' + str('0' + str(index)) + '%', cls.gospecmodel.metastring)
                    for replace_record in to_be_replaced_list:
                        cls.gospecmodel.metastring = cls.gospecmodel.metastring.replace(replace_record, '#!' + str('2' + str(len(cls.gospecmodel.unit_list) - 1) + '[' + str(index) + ']') + '%')

        if 'MacroDefinitions' in Specfile2:
            for index, macro_definition in enumerate(cls.specmodelgenerator.list_of_blocks[2]):
                cls.gospecmodel.metadata.append(macro_definition)
                cls.gospecmodel.metastring = Metastring.replace_field_number(cls.gospecmodel.metastring, len(cls.gospecmodel.metadata) - 1, ['2' + str(index), 0])

        if 'SectionTags' in Specfile2:
            for index, single_section in enumerate(Specfile2['SectionTags']):
                if single_section['keyword'] == 'changelog':
                    cls.gospecmodel.history = single_section
                    cls.gospecmodel.metastring = Metastring.replace_field_number(cls.gospecmodel.metastring, 0, ['1' + str(index), 3])

                elif single_section['keyword'] == 'package':
                    cls.gospecmodel.unit_list.append(single_section)

                    to_be_replaced_list = re.findall(r'#' + str('1' + str(index)) + '%', cls.gospecmodel.metastring)
                    for replace_record in to_be_replaced_list:
                        cls.gospecmodel.metastring = cls.gospecmodel.metastring.replace(replace_record, '#!' + str('2' + str(len(cls.gospecmodel.unit_list) - 1) + '[' + str(index) + ']') + '%')

                elif single_section['keyword'] == 'files' and 'name' in single_section and single_section['name'] != '' and single_section['name'] != None:
                    cls.gospecmodel.unit_list.append(single_section)

                    to_be_replaced_list = re.findall(r'#' + str('1' + str(index)) + '%', cls.gospecmodel.metastring)
                    for replace_record in to_be_replaced_list:
                        cls.gospecmodel.metastring = cls.gospecmodel.metastring.replace(replace_record, '#!' + str('2' + str(len(cls.gospecmodel.unit_list) - 1) + '[' + str(index) + ']') + '%')

                elif ('name' in single_section and single_section['name'] is not None) \
                or ('subname' in single_section and single_section['subname'] is not None
                and 'parameters' in single_section and 'n' in single_section['parameters']):
                    cls.gospecmodel.unit_list.append(single_section)

                    to_be_replaced_list = re.findall(r'#' + str('1' + str(index)) + '%', cls.gospecmodel.metastring)
                    for replace_record in to_be_replaced_list:
                        cls.gospecmodel.metastring = cls.gospecmodel.metastring.replace(replace_record, '#!' + str('2' + str(len(cls.gospecmodel.unit_list) - 1) + '[' + str(index) + ']') + '%')

                elif 'subname' in single_section and single_section['subname'] is not None:
                    cls.gospecmodel.main_unit.append(single_section)

                    to_be_replaced_list = re.findall(r'#' + str('1' + str(index)) + '%', cls.gospecmodel.metastring)
                    for replace_record in to_be_replaced_list:
                        cls.gospecmodel.metastring = cls.gospecmodel.metastring.replace(replace_record, '#!' + str('1' + str(len(cls.gospecmodel.main_unit) - 1) + '[' + str(index) + ']') + '%')

                elif 'AP' not in single_section or single_section['AP'] == '':
                    cls.gospecmodel.main_unit.append(single_section)
                    to_be_replaced_list = re.findall(r'#' + str('1' + str(index)) + '%', cls.gospecmodel.metastring)
                    for replace_record in to_be_replaced_list:
                        cls.gospecmodel.metastring = cls.gospecmodel.metastring.replace(replace_record, '#!' + str('1' + str(len(cls.gospecmodel.main_unit) - 1) + '[' + str(index) + ']') + '%')
                prev_section_count += 1

        if 'Comments' in Specfile2:
            for index in range(len(Specfile2['Comments'])):
                cls.gospecmodel.metastring = Metastring.replace_field_number(cls.gospecmodel.metastring, index, [str(5) + str(index), 4])
            prev_section_count += len(Specfile2['Comments'])
            cls.gospecmodel.comments = Specfile2['Comments']

        if 'MacroConditions' in Specfile2:
            for index in range(len(Specfile2['MacroConditions'])):
                cls.gospecmodel.metastring = Metastring.replace_field_number(cls.gospecmodel.metastring, index, [str(3) + str(index), str(7)])
        
        cls.process_unit_list()
        if cls.ExcludeArch != []:
            cls.add_excludearch_tags()
        cls.gospecmodel.metastring = cls.gospecmodel.metastring.replace('#!', '#')


    @classmethod
    def add_section_to_position(cls, position, section_record):
        """Append section_record to given position in SectionTags list."""
        if len(cls.Specfile2_from_GoSpec.SectionTags) > position:
            cls.Specfile2_from_GoSpec.SectionTags[position] = section_record
            return
        if len(cls.Specfile2_from_GoSpec.SectionTags) < position:
            for _ in range(position - len(cls.Specfile2_from_GoSpec.SectionTags)):
                cls.Specfile2_from_GoSpec.SectionTags.append('')
        cls.Specfile2_from_GoSpec.SectionTags.append(section_record)


    @classmethod
    def process_single_record(cls, metarecord, attribute, index, pos_in_unit):
        """Transform single record of GoSpecModel to its equivalent SpecModel representation."""
        if not isinstance(metarecord, list):
            if metarecord['block_type'] == 0:
                if attribute == 'metadata':
                    pattern = r'#0' + str(index) + '\[\d+\]'
                elif attribute == 'main_unit':
                    pattern = r'#1' + str(index) + '\[\d+\]'
                else:
                    pattern = r'#2<' + str(index) + '>' + str(pos_in_unit) + '\[\d+\]'
                
                condition_position = Metastring.check_for_conditions(cls.Specfile2_from_GoSpec.metastring, pattern)
                if condition_position != None and condition_position != -1:
                    cls.PredicateList[condition_position] = metarecord['AP']
                elif condition_position != None and condition_position == -1:
                    cls.PredicateList.append(metarecord['AP'])

                metastring_id = re.search(pattern, cls.Specfile2_from_GoSpec.metastring).group()
                former_field_id = int(metastring_id[metastring_id.find('[') + 1:-1])
                cls.Specfile2_from_GoSpec.HeaderTags = cls.Specfile2_from_GoSpec.HeaderTags[:former_field_id] + [metarecord] + cls.Specfile2_from_GoSpec.HeaderTags[former_field_id:]
                cls.Specfile2_from_GoSpec.metastring = cls.Specfile2_from_GoSpec.metastring.replace(metastring_id, '#!0' + str(former_field_id))

                if attribute == 'main_unit':
                    to_be_replaced = re.findall(r'#1\d+%', cls.Specfile2_from_GoSpec.metastring)
                    for single_replace in sorted(to_be_replaced):
                        cls.Specfile2_from_GoSpec.metastring = re.sub(single_replace, r'#1' + str(int(single_replace[2:-1]) - 1) + '%', cls.Specfile2_from_GoSpec.metastring)

            elif metarecord['block_type'] == 1:
                if ('keyword' in metarecord and metarecord['keyword'] == 'package') or ('package' in metarecord \
                and metarecord['package'] != None) or ('subname' in metarecord and metarecord['subname'] != None \
                and ('parameters' not in metarecord or 'n' in metarecord['parameters'])) \
                or ('name' in metarecord and metarecord['name'] != None):
                    condition_position = Metastring.check_for_conditions(cls.Specfile2_from_GoSpec.metastring, r'#2<' + str(index) + '>' + str(pos_in_unit) + '\[\d+\]')
                    if condition_position != None and condition_position != -1:
                        cls.PredicateList[condition_position] = metarecord['AP']
                    elif condition_position != None and condition_position == -1:
                        cls.PredicateList.append(metarecord['AP'])
                    package_section_id = re.search(r'#2<' + str(index) + '>' + str(pos_in_unit) + '\[\d+\]', cls.Specfile2_from_GoSpec.metastring).group()
                    former_field_id = int(package_section_id[package_section_id.find('[') + 1:-1])
                    cls.Specfile2_from_GoSpec.metastring = cls.Specfile2_from_GoSpec.metastring.replace(package_section_id, '#!1' + package_section_id[package_section_id.find('[') + 1:-1])
                    cls.add_section_to_position(former_field_id, metarecord)
                elif 'subname' in metarecord and metarecord['subname'] != None:
                    condition_position = Metastring.check_for_conditions(cls.Specfile2_from_GoSpec.metastring, r'#1' + str(index) + r'\[\d+\]')
                    if condition_position != None and condition_position != -1:
                        cls.PredicateList[condition_position] = metarecord['AP']
                    elif condition_position != None and condition_position == -1:
                        cls.PredicateList.append(metarecord['AP'])                
                    main_unit_section_id = re.search(r'#1' + str(index) + r'\[\d+\]', cls.Specfile2_from_GoSpec.metastring).group()
                    former_section_id = int(main_unit_section_id[main_unit_section_id.find('[') + 1:-1])
                    cls.Specfile2_from_GoSpec.metastring = cls.Specfile2_from_GoSpec.metastring.replace(main_unit_section_id, '#!1' + main_unit_section_id[main_unit_section_id.find('[') + 1:-1])
                    cls.add_section_to_position(former_section_id, metarecord)
                elif 'keyword' in metarecord and metarecord['keyword'] == 'changelog':
                    condition_position = Metastring.check_for_conditions(cls.Specfile2_from_GoSpec.metastring, '#30')
                    if condition_position != None and condition_position != -1:
                        cls.PredicateList[condition_position] = metarecord['AP']
                    elif condition_position != None and condition_position == -1:
                        cls.PredicateList.append(metarecord['AP'])                
                    cls.Specfile2_from_GoSpec.SectionTags.append(metarecord)
                    cls.Specfile2_from_GoSpec.metastring = cls.Specfile2_from_GoSpec.metastring.replace('#30', '#!1' + str(len(cls.Specfile2_from_GoSpec.SectionTags) - 1))
                else:
                    condition_position = Metastring.check_for_conditions(cls.Specfile2_from_GoSpec.metastring, r'#1' + str(index) + r'\[\d+\]')
                    if condition_position != None and condition_position != -1:
                        cls.PredicateList[condition_position] = metarecord['AP']
                    elif condition_position != None and condition_position == -1:
                        cls.PredicateList.append(metarecord['AP'])                
                    section_id = re.search(r'#1' + str(index) + r'\[\d+\]', cls.Specfile2_from_GoSpec.metastring).group()
                    former_section_id = int(section_id[section_id.find('[') + 1:-1])
                    cls.add_section_to_position(former_section_id, metarecord)
                    cls.Specfile2_from_GoSpec.metastring = cls.Specfile2_from_GoSpec.metastring.replace(section_id, '#!1' + section_id[section_id.find('[') + 1:-1])

            elif metarecord['block_type'] == 2:
                cls.Specfile2_from_GoSpec.MacroDefinitions.append(metarecord)
                index = len(cls.Specfile2_from_GoSpec.HeaderTags) + len(cls.Specfile2_from_GoSpec.MacroDefinitions) - 1
                condition_position = Metastring.check_for_conditions(cls.Specfile2_from_GoSpec.metastring, r'#0' + str(index))
                if condition_position != None and condition_position != -1:
                    cls.PredicateList[condition_position] = metarecord['AP']
                elif condition_position != None and condition_position == -1:
                    cls.PredicateList.append(metarecord['AP'])
                cls.Specfile2_from_GoSpec.metastring = re.sub(r'#0' + str(index), r'#!2' + str(index - len(cls.Specfile2_from_GoSpec.HeaderTags)), cls.Specfile2_from_GoSpec.metastring)
                    
            elif metarecord['block_type'] == 5:            
                condition_position = Metastring.check_for_conditions(cls.Specfile2_from_GoSpec.metastring, r'#5' + str(index))
                if condition_position != None and condition_position != -1:
                    cls.PredicateList[condition_position] = metarecord['AP']
                elif condition_position != None and condition_position == -1:
                    cls.PredicateList.append(metarecord['AP'])                
                cls.Specfile2_from_GoSpec.Comments.append(metarecord)

        else:
            for offset, unit_field in enumerate(metarecord):
                cls.process_single_record(unit_field, attribute, index, offset)



    @classmethod
    def get_existing_condition_position(cls, wanted_expression):
        """Get index of condition determined by wanted_expression."""
        for index, single_condition in enumerate(cls.Specfile2_from_GoSpec.Conditions):
            if single_condition['expression'] == wanted_expression:
                return index



    @classmethod
    def add_packages_to_conditions(cls):
        """Add package information to conditions which are part of a package section."""
        for section_index in range(len(cls.Specfile2_from_GoSpec.SectionTags)):
            section_index_metastring = cls.Specfile2_from_GoSpec.metastring[cls.Specfile2_from_GoSpec.metastring.find(r'#1' + str(section_index) + '%0'):cls.Specfile2_from_GoSpec.metastring.rfind(r'#1' + str(section_index) + '%4')]
            if section_index_metastring != '' and \
            cls.Specfile2_from_GoSpec.SectionTags[int(section_index_metastring[2:int(section_index_metastring.find('%'))])]['keyword'] == 'package':
                condition_records_list = re.findall(r'#6\d+\%0', section_index_metastring)
                for single_condition_record in condition_records_list:
                    cls.Specfile2_from_GoSpec.Conditions[int(single_condition_record[2:single_condition_record.find('%')])]['package'] = cls.Specfile2_from_GoSpec.SectionTags[int(section_index_metastring[2:int(section_index_metastring.find('%'))])]['subname']



    @classmethod
    def recreate_conditions(cls):
        """Based on the information gathered, recreate condition and macro condition sections."""
        used_conditions = []

        for single_predicate in cls.PredicateList:
            if single_predicate == '':
                break
            
            single_condition = {}

            if len(single_predicate) > 1:
                single_condition['AP'] = single_predicate[:-1]
                single_predicate = [single_predicate[-1]]

            if single_predicate[0][2] != None:
                if int(single_predicate[0][1]) == 0:
                    index = cls.get_existing_condition_position(single_predicate[0][0])
                    cls.Specfile2_from_GoSpec.Conditions[index]['else_keyword'] = 'else'
                else:
                    single_condition['block_type'] = BlockTypes.ConditionType
                    single_condition['else_keyword'] = None
                    single_condition['end_keyword'] = 'endif'
                    single_condition['keyword'] = single_predicate[0][2]
                    single_condition['expression'] = single_predicate[0][0]
                    cls.Specfile2_from_GoSpec.Conditions.append(single_condition)

            else:
                single_condition['block_type'] = BlockTypes.MacroConditionType
                single_condition['name'] = single_predicate[0][0]
                single_condition['ending'] = ''
                if (single_predicate[0][1]) == 0:
                    single_condition['condition'] = '!?'
                else:
                    single_condition['condition'] = '?'
                cls.Specfile2_from_GoSpec.MacroConditions.append(single_condition)
                cls.Specfile2_from_GoSpec.metastring = cls.Specfile2_from_GoSpec.metastring.replace('#7', '#3')

        cls.add_packages_to_conditions()


    @classmethod
    def init_PredicateList(cls):
        """Initialize PredicateList as a list of as many empty strings as there are condition 
        definitions."""
        condition_list = re.findall(r'#6[^%]*?%0', cls.gospecmodel['metastring'])
        for _ in condition_list:
            cls.PredicateList.append('')


    @classmethod
    def transform_gospec_to_specmodel(cls, go_specfile):
        """Transform GoSpecModel back to SpecModel."""
        cls.gospecmodel = json.loads(go_specfile)

        cls.init_PredicateList()
        cls.Specfile2_from_GoSpec.metastring = cls.gospecmodel['metastring']
        cls.Specfile2_from_GoSpec.metastring = cls.Specfile2_from_GoSpec.metastring.replace('#4', '#5')

        for attribute in ['metadata', 'main_unit', 'unit_list', 'history', 'comments']:
            if isinstance(cls.gospecmodel[attribute], list) and cls.gospecmodel[attribute] != []:
                for index, single_field in enumerate(cls.gospecmodel[attribute]):
                    cls.process_single_record(single_field, attribute, index, None)

            elif isinstance(cls.gospecmodel[attribute], dict) and cls.gospecmodel[attribute] != {}:
                cls.process_single_record(cls.gospecmodel[attribute], attribute, None, None)

        cls.Specfile2_from_GoSpec.metastring = cls.Specfile2_from_GoSpec.metastring.replace('#!', '#')
        cls.recreate_conditions()

        return json.dumps(cls.Specfile2_from_GoSpec, default=lambda o: o.__dict__, sort_keys=True)
