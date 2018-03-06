from __future__ import print_function
from abstract_model import BlockTypes, BlockTypeUnknown
from metastring import HeaderTagMetastring, SectionMetastring, ConditionMetastring, MacroConditionMetastring, MacroDefinitionMetastring, CommentMetastring, ChangelogMetastring, PackageMetastring, MMetastring, WhitespacesMetastring, UninterpretedMetastring
from specparser import MacroDefinitionBlock, CommentBlock, ConditionBlock, HeaderTagBlock, SectionBlock, PackageBlock, ChangelogBlock, MacroUndefinitionBlock, MacroConditionBlock, UninterpretedBlock

import json

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
    Uninterpreted = 13

class SpecModel(object):

    def __init__(self):
        self._metastrings = []

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
        self._predicates = []
        self._comments = []
        self._uninterpreted = []

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

    def addPredicate(self, data):
        idx = len(self._predicates)
        self._predicates.append(data)
        return idx

    def getPredicate(self, idx):
        return self._predicates[idx]

    def addComment(self, data):
        idx = len(self._comments)
        self._comments.append(data)
        return idx

    def getComment(self, idx):
        return self._comments[idx]

    def addUninterpreted(self, data):
        idx = len(self._uninterpreted)
        self._uninterpreted.append(data)
        return idx

    def getUninterpreted(self, idx):
        return self._uninterpreted[idx]

class SpecModelGenerator(object):
    def __init__(self):
        # metastring extraction from a raw specfile
        self._block_list = []
        self._metastrings = []
        # abstract specfile modeling
        self._spec_model = SpecModel()

    def fromRawSpecfile(self, raw):
        self._block_list, self._metastrings = self._processBlockList(raw)
        self._toAbstractModel(self._metastrings, self._block_list)
        #MMetastring(self._metastrings).format(self._spec_model)
        self._spec_model._metastrings = self._metastrings
        print(self._spec_model._metastrings)
        exit(0)
        return self._spec_model
    
    def fromJsonInput(self, json_input):
        loaded_json = json.loads(json_input)
        for x in loaded_json:
            setattr(self._spec_model, x, loaded_json[x])
        self._recreateBlocks()
        self._recreateMetastringObjects()
        # print(self._spec_model._metastrings)
        # exit(0)
        return self._spec_model

    def _recreateBlocks(self):
        metadata_macros = self._spec_model._metadata_macros
        self._spec_model._metadata_macros = []
        for x in metadata_macros:
            self._spec_model._metadata_macros.append(MacroDefinitionBlock(x['name'], x['keyword'], x['options'], x['body']))

        comments = self._spec_model._comments
        self._spec_model._comments = []
        for x in comments:
            self._spec_model._comments.append(CommentBlock(x['content']))

        conditions = self._spec_model._conditions
        self._spec_model._conditions = []
        for x in conditions:
            self._spec_model._conditions.append(ConditionBlock(x['keyword'], x['expression'], x['content'], x['else_body'], x['end_keyword'], x['else_keyword']))

        metadata_tags = self._spec_model._metadata_tags
        self._spec_model._metadata_tags = []
        for x in metadata_tags:
            self._spec_model._metadata_tags.append(HeaderTagBlock(x['key'], x['content'], x['option']))

        packages = self._spec_model._packages
        self._spec_model._packages = []
        for x in packages:
            self._spec_model._packages.append(PackageBlock(x['keyword'], x['parameters'], x['subname'], x['content']))

        descriptions = self._spec_model._descriptions
        self._spec_model._descriptions = []
        for x in descriptions:
            self._spec_model._descriptions.append(SectionBlock(x['keyword'], x['parameters'], x['name'], x['subname'], x['content']))

        files = self._spec_model._files
        self._spec_model._files = []
        for x in files:
            self._spec_model._files.append(SectionBlock(x['keyword'], x['parameters'], x['name'], x['subname'], x['content']))

        other_sections = self._spec_model._other_sections
        self._spec_model._other_sections = []
        for x in other_sections:
            self._spec_model._other_sections.append(SectionBlock(x['keyword'], x['parameters'], x['name'], x['subname'], x['content']))

        uninterpreted = self._spec_model._uninterpreted
        self._spec_model._uninterpreted = []
        for x in uninterpreted:
            self._spec_model._uninterpreted.append(UninterpretedBlock(x['content']))

        if self._spec_model._prep != {}:
            prep = self._spec_model._prep
            self._spec_model._prep = SectionBlock(prep['keyword'], prep['parameters'], prep['name'], prep['subname'], prep['content'])

        if self._spec_model._build != {}:
            build = self._spec_model._build
            self._spec_model._build = SectionBlock(build['keyword'], build['parameters'], build['name'], build['subname'], build['content'])

        if self._spec_model._install != {}:
            install = self._spec_model._install
            self._spec_model._install = SectionBlock(install['keyword'], install['parameters'], install['name'], install['subname'], install['content'])

        if self._spec_model._check != {}:
            check = self._spec_model._check
            self._spec_model._check = SectionBlock(check['keyword'], check['parameters'], check['name'], check['subname'], check['content'])

        if self._spec_model._changelog != {}:
            changelog = self._spec_model._changelog
            self._spec_model._changelog = ChangelogBlock(changelog['keyword'], changelog['content'])

    def _recreateMetastringObjects(self):
        raw_metastrings = self._spec_model._metastrings
        self._spec_model._metastrings = []
        for single_object in raw_metastrings:
            self._spec_model._metastrings.append(self._formObject(single_object))

    # TODO
    def _formObject(self, single_object):
        # print(single_object)
        # return None
        if single_object['_type'] == BlockTypes.HeaderTagType:
            return HeaderTagMetastring(single_object['_key'], single_object['_option'], single_object['_content'])
        # TODO - problem with keyword stripping
        # elif single_object['_type'] == BlockTypes.SectionTagType:
        #     for attr in ["_keyword", "_name", "_parameters", "_subname"]:
        #         if attr not in single_object:
        #             single_object[attr] = None
        #     return SectionMetastring(single_object['_keyword'], single_object['_parameters'], single_object['_name'], single_object['_subname'])
        elif single_object['_type'] == BlockTypes.MacroDefinitionType:
            return MacroDefinitionMetastring(single_object['_keyword'], single_object['_name'], single_object['_options'], single_object['_body'])
        elif single_object['_type'] == BlockTypes.MacroConditionType:
            return MacroConditionMetastring(single_object['_condition'], single_object['_name'], single_object['_ending'])
        # elif single_object['_type'] == BlockTypes.MacroUndefinitionType:
        #     print("MacroUndefinitionType")
        elif single_object['_type'] == BlockTypes.CommentType:
            return CommentMetastring(single_object['_content'])
        elif single_object['_type'] == BlockTypes.ConditionType:
            return ConditionMetastring(single_object['_keyword'], single_object['_expression'], single_object['_end_keyword'], single_object['_else_keyword'])
        elif single_object['_type'] == BlockTypes.ChangelogTagType:
            return ChangelogMetastring(single_object['_keyword'], single_object['_content'])
        elif single_object['_type'] == BlockTypes.PackageTagType:
            return PackageMetastring(single_object['_keyword'], single_object['_parameters'], single_object['_subname'])
        elif single_object['_type'] == BlockTypes.Whitespaces:
            return WhitespacesMetastring(single_object['_content'])
        elif single_object['_type'] == BlockTypes.Uninterpreted:
            return UninterpretedMetastring(single_object['_content'])
        return None

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

            if single_block.block_type == BlockTypes.Whitespaces:
                generated_metastrings.append( WhitespacesMetastring(single_block.content) )
                clean_block = WhitespacesMetastring.cleanBlockType(single_block)
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.Uninterpreted:
                generated_metastrings.append( UninterpretedMetastring(single_block.content) )
                clean_block = UninterpretedMetastring.cleanBlockType(single_block)
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
                #print(single_block.content)
                if single_block.content != []:
                    clean_block.content, metastring_children = self._processBlockList(single_block.content, predicate_list)
                    #print(clean_block.content)
                    #exit(1)
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
                clean_block = SectionMetastring.cleanBlockType(single_block)
                metastring = SectionMetastring(single_block.keyword, single_block.parameters, single_block.name, single_block.subname)

                if single_block.content != []:
                    clean_block.content, metastring_children = self._processBlockList(single_block.content, predicate_list)
                    metastring.setContentMetastring(metastring_children)

                generated_metastrings.append( metastring )

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
        for _, block in enumerate(block_list):
            if block.block_type == BlockTypes.MacroDefinitionType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Macros, self._spec_model.addMacro(block))
                block.id = metastrings[ms_idx].blockIdx()
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.MacroConditionType:
                # TODO(jchaloup): Should it be under the macros or under its own category?
                metastrings[ms_idx].setBlockIdx(ModelTypes.Macros, self._spec_model.addMacro(block))
                if block.content != []:
                    self._toAbstractModel(metastrings[ms_idx].getContentMetastring(), block.content)
                block.id = metastrings[ms_idx].blockIdx()
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.CommentType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Comment, self._spec_model.addComment(block))
                block.id = metastrings[ms_idx].blockIdx()
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.Uninterpreted:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Uninterpreted, self._spec_model.addUninterpreted(block))
                block.id = metastrings[ms_idx].blockIdx()
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.Whitespaces:
                block.id = metastrings[ms_idx].blockIdx()
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.HeaderTagType:
                idx = self._spec_model.addTag(block)
                metastrings[ms_idx].setBlockIdx(ModelTypes.Tag, idx)
                metastrings[ms_idx].format(self._spec_model)
                block.id = metastrings[ms_idx].blockIdx()
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.ConditionType:
                idx = self._spec_model.addCondition(block)
                metastrings[ms_idx].setBlockIdx(ModelTypes.Condition, idx)
                # metastrings[ms_idx].format(self._spec_model)
                self._spec_model.addPredicate(self._spec_model._conditions[idx].expression)
                # TODO(jchaloup): distribute the APs properly
                if block.content != []:
                    self._toAbstractModel(metastrings[ms_idx].getIfBodyMetastring(), block.content)
                if block.else_body != []:
                    self._toAbstractModel(metastrings[ms_idx].getElseBodyMetastring(), block.else_body)
                block.id = metastrings[ms_idx].blockIdx()
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.PackageTagType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Package, self._spec_model.addPackage(block))
                if block.content != []:
                    self._toAbstractModel(metastrings[ms_idx].getContentMetastring(), block.content)
                block.id = metastrings[ms_idx].blockIdx()
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.ChangelogTagType:
                metastrings[ms_idx].setBlockIdx(ModelTypes.Changelog)
                self._spec_model.setChangelog(block)
                block.id = metastrings[ms_idx].blockIdx()
                ms_idx += 1
                continue

            if block.block_type == BlockTypes.SectionTagType:
                if block.keyword == "%description":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Description, self._spec_model.addDescription(block))
                    if block.content != []:
                        self._toAbstractModel(metastrings[ms_idx].getContentMetastring(), block.content)
                    block.id = metastrings[ms_idx].blockIdx()
                    ms_idx += 1
                    continue
                if block.keyword == "%files":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Files, self._spec_model.addFiles(block))
                    if block.content != []:
                        self._toAbstractModel(metastrings[ms_idx].getContentMetastring(), block.content)
                    block.id = metastrings[ms_idx].blockIdx()
                    ms_idx += 1
                    continue
                if block.keyword == "%prep":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Prep)
                    self._spec_model.setPrep(block)
                    if block.content != []:
                        self._toAbstractModel(metastrings[ms_idx].getContentMetastring(), block.content)
                    block.id = metastrings[ms_idx].blockIdx()
                    ms_idx += 1
                    continue
                if block.keyword == "%build":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Build)
                    self._spec_model.setBuild(block)
                    if block.content != []:
                        self._toAbstractModel(metastrings[ms_idx].getContentMetastring(), block.content)
                    block.id = metastrings[ms_idx].blockIdx()
                    ms_idx += 1
                    continue
                if block.keyword == "%install":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Install)
                    self._spec_model.setInstall(block)
                    if block.content != []:
                        self._toAbstractModel(metastrings[ms_idx].getContentMetastring(), block.content)
                    block.id = metastrings[ms_idx].blockIdx()
                    ms_idx += 1
                    continue
                if block.keyword == "%check":
                    metastrings[ms_idx].setBlockIdx(ModelTypes.Check)
                    self._spec_model.setCheck(block)
                    if block.content != []:
                        self._toAbstractModel(metastrings[ms_idx].getContentMetastring(), block.content)
                    block.id = metastrings[ms_idx].blockIdx()
                    ms_idx += 1
                    continue

                metastrings[ms_idx].setBlockIdx(ModelTypes.OtherSection, self._spec_model.addSection(block))
                if block.content != []:
                    self._toAbstractModel(metastrings[ms_idx].getContentMetastring(), block.content)
                block.id = metastrings[ms_idx].blockIdx()
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
        return self._metastring_list_to_str(self._metastrings)

    def model_to_json(self):
        return {
            "block_list": map(lambda l: l.to_json(), self._block_list),
            "metastring": self.metastrings_to_str(),
        }

    def _generate_spec(self, specModel):
        for metastring in specModel._metastrings:
            print(metastring.format(specModel), end = '')

    def to_spec(self, specModel):
        self._generate_spec(specModel)
