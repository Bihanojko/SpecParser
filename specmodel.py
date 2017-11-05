from abstract_model import BlockTypes, BlockTypeUnknown
from metastring import HeaderTagMetastring, SectionMetastring, ConditionMetastring, MacroConditionMetastring, MacroDefinitionMetastring, CommentMetastring, ChangelogMetastring, PackageMetastring, MMetastring

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
        self._beginning = ""
        self._metastrings = []
        self._end = ""

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
        self._conditions = []
        self._comments = []

    def addTag(self, data):
        idx = len(self._metadata_tags)
        self._metadata_tags.append(data)
        return idx

    def getTag(self, idx):
        return self._metadata_tags[idx]

    def addMacro(self, data):
        idx = len(self._metadata_macros)
        self._metadata_macros.append(data)
        return idx

    def getMacro(self, idx):
        return self._metadata_macros[idx]

    def addPackage(self, data):
        idx = len(self._packages)
        self._packages.append(data)
        return idx

    def getPackage(self, idx):
        return self._packages[idx]

    def addDescription(self, data):
        idx = len(self._descriptions)
        self._descriptions.append(data)
        return idx

    def getDescription(self, idx):
        return self._descriptions[idx]

    def addFiles(self, data):
        idx = len(self._files)
        self._files.append(data)
        return idx

    def getFiles(self, idx):
        return self._files[idx]

    def setPrep(self, data):
        self._prep = data

    def getPrep(self):
        return self._prep

    def setBuild(self, data):
        self._build = data

    def getBuild(self):
        return self._build

    def setInstall(self, data):
        self._install = data

    def getInstall(self):
        return self._install

    def setCheck(self, data):
        self._check = data

    def getCheck(self):
        return self._check

    def setChangelog(self, data):
        self._changelog = data

    def getChangelog(self):
        return self._changelog

    def addSection(self, data):
        idx = len(self._other_sections)
        self._other_sections.append(data)
        return idx

    def getSection(self, idx):
        return self._other_sections[idx]

    def addCondition(self, data):
        idx = len(self._conditions)
        self._conditions.append(data)
        return idx

    def getCondition(self, idx):
        return self._conditions[idx]

    def addComment(self, data):
        idx = len(self._comments)
        self._comments.append(data)
        return idx

    def getComment(self, idx):
        return self._comments[idx]

class SpecModelGenerator(object):
    def __init__(self):
        # metastring extraction from a raw specfile
        self._block_list = []
        self._beginning = ""
        self._metastrings = []
        self._end = ""
        # abstract specfile modeling
        self._spec_model = SpecModel()

    def fromRawSpecfile(self, raw):
        self._beginning = raw.beginning
        self._end = raw.end
        self._block_list, self._metastrings = self._processBlockList(raw.block_list)
        self._toAbstractModel(self._metastrings, self._block_list)
        #print (self.metastrings_to_json())
        MMetastring(self._metastrings).format(self._spec_model)
        #self.to_spec()
        exit(1)

        return self

    def _processBlockList(self, block_list, predicate_list = []):
        processed_blocks = []
        generated_metastrings = []

        for single_block in block_list:

            if single_block.block_type == BlockTypes.HeaderTagType:
                generated_metastrings.append( HeaderTagMetastring(single_block.key, single_block.option, single_block.content) )
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
                print(single_block.content)
                if single_block.content != []:
                    clean_block.content, metastring_children = self._processBlockList(single_block.content, predicate_list)
                    print(clean_block.content)
                    exit(1)
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
                metastrings[ms_idx].setBlockIdx(ModelTypes.Macros, self._spec_model.addMacro(block))
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.MacroConditionType:
                # TODO(jchaloup): Should it be under the macros or under its own category?
                metastrings[ms_idx].setBlockIdx(ModelTypes.Macros, self._spec_model.addMacro(block))
                if block.content != []:
                    self._toAbstractModel(metastrings[ms_idx].getContentMetastring(), block.content)
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.CommentType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Comment, self._spec_model.addComment(block))
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.HeaderTagType:
                idx = self._spec_model.addTag(block)
                metastrings[ms_idx].setBlockIdx(ModelTypes.Tag, idx)
                metastrings[ms_idx].format(self._spec_model)
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.ConditionType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Condition, self._spec_model.addCondition(block.expression))
                # TODO(jchaloup): distribute the APs properly
                if block.content != []:
                    self._toAbstractModel(metastrings[ms_idx].getIfBodyMetastring(), block.content)
                if block.else_body != []:
                    self._toAbstractModel(metastrings[ms_idx].getElseBodyMetastring(), block.else_body)
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.PackageTagType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Package, self._spec_model.addPackage(block))
                if block.content != []:
                    self._toAbstractModel(metastrings[ms_idx].getContentMetastring(), block.content)
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.ChangelogTagType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Changelog)
                self._spec_model.setChangelog(block)
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.SectionTagType:
                if block.keyword == "description":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Description, self._spec_model.addDescription(block))
                    ms_idx += 1
                    continue
                if block.keyword == "files":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Files, self._spec_model.addFiles(block))
                    ms_idx += 1
                    continue
                if block.keyword == "prep":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Prep)
                    self._spec_model.setPrep(block)
                    ms_idx += 1
                    continue
                if block.keyword == "build":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Build)
                    self._spec_model.setBuild(block)
                    ms_idx += 1
                    continue
                if block.keyword == "install":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Install)
                    self._spec_model.setInstall(block)
                    ms_idx += 1
                    continue
                if block.keyword == "check":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Check)
                    self._spec_model.setCheck(block)
                    ms_idx += 1
                    continue

                metastrings[ms_idx].setBlockIdx(ModelTypes.OtherSection, self._spec_model.addSection(block))
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
                expression = self._conditions[metastring.blockIdx()]
                print metastring
                print metastring.blockIdx()

                #self._generate_spec

                print metastring.hasElseBody()

            exit(1)

    def to_spec(self):
        self._generate_spec(self._metastrings)
