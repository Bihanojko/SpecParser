from abstract_model import BlockTypes, BlockTypeUnknown
from metastring import HeaderTagMetastring, SectionMetastring, ConditionMetastring, MacroConditionMetastring, MacroDefinitionMetastring, CommentMetastring, ChangelogMetastring, PackageMetastring

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
        #self.to_spec()
        #exit(1)

        return self

    def _processBlockList(self, block_list, predicate_list = []):
        processed_blocks = []
        generated_metastrings = []

        for single_block in block_list:

            if single_block.block_type == BlockTypes.HeaderTagType:
                generated_metastrings.append( HeaderTagMetastring(single_block.key, single_block.content, single_block.option) )
                clean_block = HeaderTagMetastring.cleanBlockType(single_block)
                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.CommentType:
                generated_metastrings.append( CommentMetastring(single_block.content) )
                clean_block = CommentMetastring.cleanBlockType(single_block)
                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.MacroDefinitionType:
                metastring = MacroDefinitionMetastring(single_block.keyword, single_block.name, single_block.options, single_block.body)
                generated_metastrings.append( metastring )
                clean_block = MacroDefinitionMetastring.cleanBlockType(single_block)
                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.PackageTagType:
                clean_block = PackageMetastring.cleanBlockType(single_block)
                metastring = PackageMetastring(single_block.keyword, single_block.parameters, single_block.subname)

                if single_block.content != []:
                    clean_block.content, metastring_children = self._processBlockList(single_block.content, predicate_list)
                    metastring.setContentMetastring(metastring_children)

                generated_metastrings.append( metastring )

                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.ChangelogTagType:
                generated_metastrings.append( ChangelogMetastring(single_block.keyword, single_block.content) )
                clean_block = ChangelogMetastring.cleanBlockType(single_block)
                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.SectionTagType:
                generated_metastrings.append( SectionMetastring(single_block.keyword, single_block.parameters, single_block.name, single_block.subname, single_block.content) )
                clean_block = SectionMetastring.cleanBlockType(single_block)
                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.ConditionType:
                clean_block = ConditionMetastring.cleanBlockType(single_block)
                ms = ConditionMetastring(single_block.keyword, single_block.expression, single_block.end_keyword, single_block.else_keyword)

                if single_block.content != []:
                    clean_block.content, content_metastring_children = self._processBlockList(single_block.content, predicate_list + [[clean_block.expression, 1, clean_block.keyword]])
                    ms.setIfBodyMetastring(content_metastring_children)
                if single_block.else_body != []:
                    clean_block.else_body, else_body_metastring_children = self._processBlockList(single_block.else_body, predicate_list + [[clean_block.expression, 0, clean_block.keyword]])
                    ms.setElseBodyMetastring(else_body_metastring_children)

                generated_metastrings.append( ms )

                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.MacroConditionType:
                metastring = MacroConditionMetastring(single_block.condition, single_block.name, single_block.ending)
                clean_block = MacroConditionMetastring.cleanBlockType(single_block)

                if single_block.content != []:
                    if '!' in single_block.condition:
                        clean_block.content, metastring_children = self._processBlockList(single_block.content, predicate_list + [[clean_block.name, 0, None]])
                        metastring.setContentMetastring(metastring_children)
                    else:
                        clean_block.content, metastring_children = self._processBlockList(single_block.content, predicate_list + [[clean_block.name, 1, None]])
                        metastring.setContentMetastring(metastring_children)

                generated_metastrings.append( metastring )

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
                self._metadata_macros.append(block)
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.MacroConditionType:
                # TODO(jchaloup): Should it be under the macros or under its own category?
                metastrings[ms_idx].setBlockIdx(ModelTypes.Macros, len(self._metadata_macros))
                self._metadata_macros.append(block)
                if block.content != []:
                    self._toAbstractModel(metastrings[ms_idx].getContentMetastring(), block.content)
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.CommentType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Comment, len(self._comments_table))
                self._comments_table.append(block)
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.HeaderTagType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Tag, len(self._metadata_tags))
                self._metadata_tags.append(block)
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.ConditionType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Condition, len(self._conditioner_table))
                self._conditioner_table.append(block.expression)
                # TODO(jchaloup): distribute the APs properly
                if block.content != []:
                    self._toAbstractModel(metastrings[ms_idx].getIfBodyMetastring(), block.content)
                if block.else_body != []:
                    self._toAbstractModel(metastrings[ms_idx].getElseBodyMetastring(), block.else_body)
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.PackageTagType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Package, len(self._packages))
                self._packages.append(block)
                if block.content != []:
                    self._toAbstractModel(metastrings[ms_idx].getContentMetastring(), block.content)
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.ChangelogTagType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Changelog)
                self._changelog = block
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.SectionTagType:
                if block.keyword == "description":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Description, len(self._descriptions))
                    self._descriptions.append(block)
                    ms_idx += 1
                    continue
                if block.keyword == "files":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Files, len(self._files))
                    self._files.append(block)
                    ms_idx += 1
                    continue
                if block.keyword == "prep":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Prep)
                    self._prep = block
                    ms_idx += 1
                    continue
                if block.keyword == "build":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Build)
                    self._build = block
                    ms_idx += 1
                    continue
                if block.keyword == "install":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Install)
                    self._install = block
                    ms_idx += 1
                    continue
                if block.keyword == "check":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Check)
                    self._check = block
                    ms_idx += 1
                    continue

                metastrings[ms_idx].setBlockIdx(ModelTypes.OtherSection, len(self._other_sections))
                self._other_sections.append(block)
                ms_idx += 1
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
            data.append(item.to_json())
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

    def _generate_spec(self, metastrings):
        for metastring in metastrings:
            if metastring.modelType() == ModelTypes.Condition:
                expression = self._conditioner_table[metastring.blockIdx()]
                print metastring
                print metastring.blockIdx()

                #self._generate_spec

                print metastring.hasElseBody()

            exit(1)

    def to_spec(self):
        self._generate_spec(self._metastrings)
