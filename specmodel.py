from abstract_model import BlockTypes
from metastring import HeaderTagMetastring, SectionMetastring, ConditionMetastring, MacroConditionMetastring, MacroDefinitionMetastring, CommentMetastring, ChangelogMetastring

# Condition-free layout of a specfile 2.0
#
# Metadata:
# - Tags: []
# - Macros: []
# Packages: []
# Descriptions: []
# Files: []
# Prep: {}
# Install: {}
# Changelog: {}
# OtherSections: {}
#
# Integration of Conditions:
# - register each condition expression in a conditioner table
# - have metastrings of conditions refer to the conditioner table
# - propagation of contidion is managed on a level of the layout (above)
#   each block conditions refer corresponding condition expression on the conditioner table
# - the conditioner table also counts the number of allocation of a condition (used during macro evaluations)
#
# Conditioner table
# - if-condition (used to construct AP of a block)
# - if-condition (used to construct AP of a block)
# - !if-condition (artificial condition?)
class ModelTypes:
    Tag = 0
    Macros = 1
    Package = 2
    Description = 3
    Files = 4
    OtherSection = 5
    Comment = 6
    Condition = 7
    Prep = 8
    Build = 9
    Install = 10
    Check = 11
    Changelog = 12

class SpecModel(object):
    def __init__(self):
        # metastring extraction from a raw specfile
        self._block_list = []
        self._beginning = ""
        self._metastrings = []
        self._end = ""
        # abstract specfile modeling
        self._metadata_tags = []
        self._metadata_macros = []
        self._packages = []
        self._descriptions = []
        self._files = []
        self._prep = {}
        self._build = {}
        self._install = {}
        self._check = {}
        self._changelog = {}
        self._other_sections = []
        self._conditioner_table = []
        self._comments_table = []

    def fromRawSpecfile(self, raw):
        self._beginning = raw.beginning
        self._end = raw.end
        self._block_list, self._metastrings = self._processBlockList(raw.block_list)

        self._toAbstractModel(self._metastrings, self._block_list)
        #import json
        #print(json.dumps(self.metastrings_to_json()))
        #exit(1)

        return self

    def _processBlockList(self, block_list, predicate_list = []):
        processed_blocks = []
        generated_metastrings = []

        for single_block in block_list:

            if single_block.block_type == BlockTypes.HeaderTagType:
                generated_metastrings.append( HeaderTagMetastring().fromBlockType(single_block) )
                clean_block = HeaderTagMetastring().cleanBlockType(single_block)
                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.CommentType:
                generated_metastrings.append( CommentMetastring().fromBlockType(single_block) )
                clean_block = CommentMetastring().cleanBlockType(single_block)
                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.MacroDefinitionType:
                generated_metastrings.append( MacroDefinitionMetastring().fromBlockType(single_block) )
                clean_block = MacroDefinitionMetastring().cleanBlockType(single_block)
                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.SectionTagType:
                if single_block.keyword.strip() == "changelog":
                    generated_metastrings.append( ChangelogMetastring().fromBlockType(single_block) )
                    clean_block = ChangelogMetastring().cleanBlockType(single_block)
                    if predicate_list != []:
                        # TODO(jchaloup): register the AP in the conditioner table as well
                        clean_block.AP = predicate_list
                    processed_blocks.append(clean_block)
                    continue

                if single_block.keyword.strip() == "package":
                    clean_block = SectionMetastring().cleanBlockType(single_block)
                    generated_metastrings.append( SectionMetastring().fromBlockType(single_block) )

                    if single_block.content != []:
                        clean_block.content, metastring_children = self._processBlockList(single_block.content, predicate_list)
                        generated_metastrings.append(metastring_children)

                    if predicate_list != []:
                        # TODO(jchaloup): register the AP in the conditioner table as well
                        clean_block.AP = predicate_list
                    processed_blocks.append(clean_block)
                    continue

                generated_metastrings.append( SectionMetastring().fromBlockType(single_block) )
                clean_block = SectionMetastring().cleanBlockType(single_block)
                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.ConditionType:
                generated_metastrings.append( ConditionMetastring().fromBlockType(single_block) )
                clean_block = ConditionMetastring().cleanBlockType(single_block)

                if single_block.content != []:
                    clean_block.content, content_metastring_children = self._processBlockList(single_block.content, predicate_list + [[clean_block.expression, 1, clean_block.keyword]])
                    generated_metastrings.append(content_metastring_children)
                if single_block.else_body != []:
                    clean_block.else_body, else_body_metastring_children = self._processBlockList(single_block.else_body, predicate_list + [[clean_block.expression, 0, clean_block.keyword]])
                    generated_metastrings.append(else_body_metastring_children)

                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.MacroConditionType:
                generated_metastrings.append( MacroConditionMetastring().fromBlockType(single_block) )
                clean_block = MacroConditionMetastring().cleanBlockType(single_block)

                if single_block.content != []:
                    if '!' in single_block.condition:
                        clean_block.content, metastring_children = self._processBlockList(single_block.content, predicate_list + [[clean_block.name, 0, None]])
                    else:
                        clean_block.content, metastring_children = self._processBlockList(single_block.content, predicate_list + [[clean_block.name, 1, None]])

                    generated_metastrings.append(metastring_children)

                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            raise BlockTypeUnknown("Block type {} unknown".format(single_block.block_type))

        return processed_blocks, generated_metastrings

    def _toAbstractModel(self, metastrings, block_list):

        ms_idx = 0
        for i, block in enumerate(block_list):
            if block.block_type == BlockTypes.MacroDefinitionType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Macros, len(self._metadata_macros))
                #print repr(metastrings[ms_idx].to_str()), block, len(self._metadata_macros)
                self._metadata_macros.append(block)
                ms_idx = ms_idx + 1
                continue

            if block.block_type == BlockTypes.MacroConditionType:
                # TODO(jchaloup): Should it be under the macros or under its own category?
                metastrings[ms_idx].setBlockIdx(ModelTypes.Macros, len(self._metadata_macros))
                #print repr(metastrings[ms_idx].to_str()), metastrings[ms_idx], block, len(self._metadata_macros)
                self._metadata_macros.append(block)
                ms_idx = ms_idx + 1
                if block.content != []:
                    self._toAbstractModel(metastrings[ms_idx], block.content)
                    ms_idx = ms_idx + 1
                continue

            if block.block_type == BlockTypes.CommentType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Comment, len(self._comments_table))
                #print repr(metastrings[ms_idx].to_str()), block, len(self._comments_table)
                self._comments_table.append(block)
                ms_idx = ms_idx + 1
                continue

            if block.block_type == BlockTypes.HeaderTagType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Tag, len(self._metadata_tags))
                #print repr(metastrings[ms_idx].to_str()), block, len(self._metadata_tags)
                self._metadata_tags.append(block)
                ms_idx = ms_idx + 1
                continue

            if block.block_type == BlockTypes.ConditionType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Condition, len(self._conditioner_table))
                #print repr(metastrings[ms_idx].to_str()), block, len(self._conditioner_table)
                self._conditioner_table.append(block.expression)
                ms_idx = ms_idx + 1
                # TODO(jchaloup): distribute the APs properly
                if block.content != []:
                    self._toAbstractModel(metastrings[ms_idx], block.content)
                    ms_idx = ms_idx + 1
                if block.else_body != []:
                    self._toAbstractModel(metastrings[ms_idx], block.else_body)
                    ms_idx = ms_idx + 1
                continue

            if block.block_type == BlockTypes.SectionTagType:
                if block.keyword == "description":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Description, len(self._descriptions))
                    #print repr(metastrings[ms_idx].to_str()), block, len(self._descriptions)
                    self._descriptions.append(block)
                    ms_idx = ms_idx + 1
                    continue
                if block.keyword == "package":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Package, len(self._packages))
                    #print repr(metastrings[ms_idx].to_str()), block, len(self._packages)
                    self._packages.append(block)
                    ms_idx = ms_idx + 1
                    if block.content != []:
                        self._toAbstractModel(metastrings[ms_idx], block.content)
                        ms_idx = ms_idx + 1
                    continue
                if block.keyword == "files":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Files, len(self._files))
                    #print repr(metastrings[ms_idx].to_str()), block, len(self._files)
                    self._files.append(block)
                    ms_idx = ms_idx + 1
                    continue
                if block.keyword == "prep":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Prep)
                    #print repr(metastrings[ms_idx].to_str()), block, 0
                    self._prep = block
                    ms_idx = ms_idx + 1
                    continue
                if block.keyword == "build":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Build)
                    #print repr(metastrings[ms_idx].to_str()), block, 0
                    self._build = block
                    ms_idx = ms_idx + 1
                    continue
                if block.keyword == "install":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Install)
                    #print repr(metastrings[ms_idx].to_str()), block, 0
                    self._install = block
                    ms_idx = ms_idx + 1
                    continue
                if block.keyword == "check":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Check)
                    #print repr(metastrings[ms_idx].to_str()), block, 0
                    self._check = block
                    ms_idx = ms_idx + 1
                    continue
                if block.keyword == "changelog":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Changelog)
                    #print repr(metastrings[ms_idx].to_str()), block, 0
                    self._changelog = block
                    ms_idx = ms_idx + 1
                    continue

                #print block.keyword
                metastrings[ms_idx].setBlockIdx(ModelTypes.OtherSection, len(self._other_sections))
                #print repr(metastrings[ms_idx].to_str()), block, len(self._other_sections)
                self._other_sections.append(block)
                ms_idx = ms_idx + 1
                continue

            raise BlockTypeUnknown("Block type {} unknown".format(block.block_type))

        return self

    def _metastring_list_to_str(self, metastring_list):
        str = ""
        for item in metastring_list:
            if isinstance(item, list):
                str += self._metastring_list_to_str(item)
                continue
            str += item.to_str()

        return str

    def _metastring_list_to_json(self, metastring_list):
        data = []
        for item in metastring_list:
            if isinstance(item, list):
                data.append(self._metastring_list_to_json(item))
                continue
            data.append(item.to_str())
        return data

    def metastrings_to_json(self):
        return self._metastring_list_to_json(self._metastrings)

    def metastrings_to_str(self):
        return self._beginning + self._metastring_list_to_str(self._metastrings) + self._end

    def model_to_json(self):
        return {
            "block_list": map(lambda l: l.to_json(), self._block_list),
            "metastring": self.metastrings_to_str(),
        }
