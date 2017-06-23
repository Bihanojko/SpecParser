from __future__ import print_function
import json

from abstract_model import BlockTypes, SpecfileClass
from specparser import parse_specfile






def remove_blocktype(single_block):
    
    # del single_block['block_type']
    return single_block


def json_to_specfile_class(json_containing_parsed_spec):
    
    global Specfile
    global previous_node_next_pointer
    global next_field

    for single_block in json_containing_parsed_spec:
        single_block['next'] = None

        # Header Tag
        if single_block['block_type'] == BlockTypes.HeaderTagType:
            Specfile.headerTags.append(remove_blocktype(single_block))
            next_field = Specfile.headerTags[-1]

        # Section Tag
        elif single_block['block_type'] == BlockTypes.SectionTagType:
            if 'package' not in single_block['keyword']:
                Specfile.sectionTags.append(remove_blocktype(single_block))
                next_field = Specfile.sectionTags[-1]
            else:
                content = single_block['content']
                del single_block['content']
                point_package_to_ptr = previous_node_next_pointer
                Specfile.sectionTags.append(remove_blocktype(single_block))
                if content != []:
                    tmp = {'next': None}
                    previous_node_next_pointer = tmp
                    json_to_specfile_class(content)
                    single_block['content'] = tmp['next']
                Specfile.conditions.append(remove_blocktype(single_block))
                next_field = Specfile.sectionTags[-1]
                previous_node_next_pointer = point_package_to_ptr

        # Macro Definition
        elif single_block['block_type'] == BlockTypes.MacroDefinitionType:
            Specfile.macroDefinitions.append(remove_blocktype(single_block))
            next_field = Specfile.macroDefinitions[-1]

        # Macro Condition
        elif single_block['block_type'] == BlockTypes.MacroConditionType:
            Specfile.macroConditions.append(remove_blocktype(single_block))
            next_field = Specfile.macroConditions[-1]
        
        # Macro Undefinition
        elif single_block['block_type'] == BlockTypes.MacroUndefinitionType:
            Specfile.macroUndefinitions.append(remove_blocktype(single_block))
            next_field = Specfile.macroUndefinitions[-1]

        # Commentary
        elif single_block['block_type'] == BlockTypes.CommentType:
            Specfile.comments.append(remove_blocktype(single_block))
            next_field = Specfile.comments[-1]
        
        # Condition
        elif single_block['block_type'] == BlockTypes.ConditionType:
            content = single_block['content']
            else_body = single_block['else_body']
            point_condition_to_ptr = previous_node_next_pointer
            if content != []:
                tmp = {'next': None}
                previous_node_next_pointer = tmp
                json_to_specfile_class(content)
                single_block['content'] = tmp['next']
            if else_body != []:
                tmp = {'next': None}
                previous_node_next_pointer = tmp
                json_to_specfile_class(else_body)
                single_block['else_body'] = tmp['next']                
            Specfile.conditions.append(remove_blocktype(single_block))
            next_field = Specfile.conditions[-1]
            previous_node_next_pointer = point_condition_to_ptr

        previous_node_next_pointer.update({'next': next_field})
        previous_node_next_pointer = next_field

Specfile = SpecfileClass('AbstractModel')
previous_node_next_pointer = None

def create_abstract_model(input_filepath):

    global previous_node_next_pointer

    json_containing_parsed_spec = json.loads(parse_specfile(input_filepath))
    Specfile.beginning = {'content': json_containing_parsed_spec['beginning'], 'next': None}

    next_field = None
    previous_node_next_pointer = Specfile.beginning

    json_to_specfile_class(json_containing_parsed_spec['block_list'])

    print(json.dumps(Specfile, default=lambda o: o.__dict__, sort_keys=True))
    # class_to_specfile(Specfile)

    return













# specfile class to specfile reconstruction - main
def class_to_specfile(intern_specfile):
    
    print(str(intern_specfile.beginning["content"]), end='')

    if intern_specfile.beginning["next"] != None:
        print_field(intern_specfile.beginning["next"])

    return


# specfile class to specfile reconstruction - subprocedure
def print_field(intern_field):

    if intern_field != None:
        if intern_field["block_type"] == BlockTypes.HeaderTagType:
            print(str(intern_field["key"]) + ":" + str(intern_field["content"]), end='')

        elif intern_field["block_type"] == BlockTypes.SectionTagType:
            print("%" + str(intern_field["keyword"]), end='')

            if "changelog" in intern_field["keyword"]:
                for single_log in intern_field["content"]:
                    print(str(single_log), end='')
            # elif "package" in intern_field["keyword"]: # TODO
            else:
                print(str(intern_field["content"]), end='')

        elif intern_field["block_type"] == BlockTypes.CommentType:
            print(str(intern_field["content"]), end='')

        elif intern_field["block_type"] == BlockTypes.MacroDefinitionType:
            print("%" + str(intern_field["keyword"]) + str(intern_field["name"]) + str(intern_field["options"]) + str(intern_field["body"]), end='')

        elif intern_field["block_type"] == BlockTypes.MacroConditionType:
            print("%" + str(intern_field["name"]) + str(intern_field["condition"]) + str(intern_field["content"]), end='')

        elif intern_field["block_type"] == BlockTypes.ConditionType:
            print("%" + str(intern_field["keyword"]) + str(intern_field["expression"]), end='')
            print_field(intern_field["content"])
            print("%endif\n\n", end='')         # TODO



        if intern_field["next"] != None:
            print_field(intern_field["next"])

    return
