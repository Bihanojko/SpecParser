from __future__ import print_function

from metastring import SectionMetastring, ConditionMetastring, MacroConditionMetastring
from metastring import PackageMetastring, WhitespacesMetastring
from metastring import ModelTypes
# HeaderTagMetastring, WhitespacesMetastring, MacroDefinitionMetastring
# CommentMetastring, ChangelogMetastring, MMetastring, UninterpretedMetastring
# from copy import deepcopy
from abstract_model import BlockTypes
from specmodel import SpecModel



class SpecTransformationModel(SpecModel):

    def __init__(self, specModel):
        for key in specModel.__dict__:
            setattr(self, key, getattr(specModel, key))



class SpecModelTransformator(object):
    """Class containing SpecTransformator generation methods"""

    _metastring_rest = []

    def __init__(self, specModel):

        self.transformationModel = SpecTransformationModel(specModel)
        self._metastring_rest = self.transformationModel._metastrings
        self.createInnerRepresentation()



    def createInnerRepresentation(self):
        """Go through blocks and add metastring pointers to each of them."""

        while self._metastring_rest:
            self.addMetastringPointer(self._metastring_rest.pop(0))



    def addMetastringPointer(self, metastring):
        """Go through block and its subsections and add appropriate metastring pointers."""

        if isinstance(metastring, WhitespacesMetastring):
            return

        if isinstance(metastring, SectionMetastring) or \
        isinstance(metastring, MacroConditionMetastring) or \
        isinstance(metastring, PackageMetastring):
            self._metastring_rest += metastring.getContentMetastring()
        elif isinstance(metastring, ConditionMetastring):
            self._metastring_rest += metastring.getIfBodyMetastring()
            self._metastring_rest += metastring.getElseBodyMetastring()

        if metastring.modelType() == ModelTypes.Tag:
            setattr(self.transformationModel._metadata_tags[metastring.blockIdx()], '_metastring', metastring)
        elif metastring.modelType() == ModelTypes.Macros:
            setattr(self.transformationModel._metadata_macros[metastring.blockIdx()], '_metastring', metastring)
        elif metastring.modelType() == ModelTypes.Package:
            setattr(self.transformationModel._packages[metastring.blockIdx()], '_metastring', metastring)
        elif metastring.modelType() == ModelTypes.Description:
            setattr(self.transformationModel._descriptions[metastring.blockIdx()], '_metastring', metastring)
        elif metastring.modelType() == ModelTypes.Files:
            setattr(self.transformationModel._files[metastring.blockIdx()], '_metastring', metastring)
        elif metastring.modelType() == ModelTypes.OtherSection:
            setattr(self.transformationModel._other_sections[metastring.blockIdx()], '_metastring', metastring)
        elif metastring.modelType() == ModelTypes.Comment:
            setattr(self.transformationModel._comments[metastring.blockIdx()], '_metastring', metastring)
        elif metastring.modelType() == ModelTypes.Condition:
            setattr(self.transformationModel._conditions[metastring.blockIdx()], '_metastring', metastring)
        elif metastring.modelType() == ModelTypes.Prep:
            setattr(self.transformationModel._prep, 'metastring', metastring)
        elif metastring.modelType() == ModelTypes.Build:
            setattr(self.transformationModel._build, '_metastring', metastring)
        elif metastring.modelType() == ModelTypes.Install:
            setattr(self.transformationModel._install, '_metastring', metastring)
        elif metastring.modelType() == ModelTypes.Check:
            setattr(self.transformationModel._check, '_metastring', metastring)
        elif metastring.modelType() == ModelTypes.Changelog:
            setattr(self.transformationModel._changelog, '_metastring', metastring)
        elif metastring.modelType() == ModelTypes.Uninterpreted:
            setattr(self.transformationModel._uninterpreted[metastring.blockIdx()], '_metastring', metastring)



class RawSpecTransformator(object):
    """Class containing RawSpecTransformator generation methods"""

    _block_list = []
    _metastring = []
    _to_be_processed = []
    _metastring_rest = []



    def __init__(self, specModel):
        self._block_list = specModel.get_blocklist()
        self._metastring = specModel.get_metastring()
        self.createInnerRepresentation()



    def createInnerRepresentation(self):
        """Go through blocks and add metastring pointer to each of them."""

        for idx, single_block in enumerate(self._block_list):
            del self._to_be_processed[:]
            del self._metastring_rest[:]
            self._metastring_rest.append(self._metastring[idx])
            self.addMetastringPointer(single_block)



    def addMetastringPointer(self, block):
        """Go through block and its subsections and add appropriate metastring pointers."""

        if isinstance(self._metastring_rest[0], SectionMetastring) or \
        isinstance(self._metastring_rest[0], MacroConditionMetastring) or \
        isinstance(self._metastring_rest[0], PackageMetastring):
            self._metastring_rest += self._metastring_rest[0].getContentMetastring()
        elif isinstance(self._metastring_rest[0], ConditionMetastring):
            self._metastring_rest += self._metastring_rest[0].getIfBodyMetastring()
            self._metastring_rest += self._metastring_rest[0].getElseBodyMetastring()

        if not hasattr(block, 'content') or isinstance(block.content, str) or \
        isinstance(block.content, unicode) or \
        (hasattr(block, 'keyword') and block.keyword == '%changelog'):
            setattr(block, 'metastring', self._metastring_rest.pop(0))
        else:
            if hasattr(block, 'else_body') and isinstance(block.else_body, list):
                self._to_be_processed = block.else_body + self._to_be_processed
            if hasattr(block, 'content') and isinstance(block.content, list):
                self._to_be_processed = block.content + self._to_be_processed

            setattr(block, 'metastring', self._metastring_rest.pop(0))

        if self._to_be_processed:
            self.addMetastringPointer(self._to_be_processed.pop(0))
