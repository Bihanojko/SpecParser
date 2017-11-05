from __future__ import print_function
import json
from abstract_model import RawSpecFile, BlockTypes, SectionContextException, SectionKeywordUnknown

class Block(object):

    def _filter(self, data):
        return {k:v for k,v in data.items() if v != None and v != []}

class HeaderTagBlock(Block):
    def __init__(self, key, content, option=None):
        self.block_type = BlockTypes.HeaderTagType
        self.key = key
        self.option = option
        self.content = content
        self.AP = None

    def to_json(self):
        return self._filter({
          "AP": self.AP,
          "block_type": self.block_type,
          "key": self.key,
          "option": self.option,
          "content": self.content,
        })

class SectionBlock(Block):
    def __init__(self, keyword, parameters, name, subname, content):
        self.block_type = BlockTypes.SectionTagType
        self.keyword = keyword
        self.content = content
        self.parameters = parameters
        self.subname = subname
        self.name = name
        self.AP = None

    def to_json(self):
        return self._filter({
          "AP": self.AP,
          "block_type": self.block_type,
          "keyword": self.keyword,
          # TODO(jchaloup): Make sure the content of a general section is always a string
          "content": self.content if isinstance(self.content, basestring) else map(lambda l: l.to_json(), self.content),
          "parameters": self.parameters,
          "subname": self.subname,
          "name": self.name
        })

class PackageBlock(Block):
    def __init__(self, keyword, parameters, subname, content):
        self.block_type = BlockTypes.PackageTagType
        self.keyword = keyword
        self.content = content
        self.parameters = parameters
        self.subname = subname
        self.AP = None

    def to_json(self):
        return self._filter({
          "AP": self.AP,
          "block_type": self.block_type,
          "keyword": self.keyword,
          "content": map(lambda l: l.to_json(), self.content),
          "parameters": self.parameters,
          "subname": self.subname
        })

class ChangelogBlock(Block):
    def __init__(self, keyword, content):
        self.block_type = BlockTypes.ChangelogTagType
        self.keyword = keyword
        self.content = content
        self.AP = None

    def to_json(self):
        return self._filter({
          "AP": self.AP,
          "block_type": self.block_type,
          "keyword": self.keyword,
          "content": self.content
        })

class MacroDefinitionBlock(Block):
    def __init__(self, name, keyword, options, body):
        self.block_type = BlockTypes.MacroDefinitionType
        self.name = name
        self.keyword = keyword
        self.options = options
        self.body = body
        self.AP = None

    def to_json(self):
        return self._filter({
          "AP": self.AP,
          "block_type": self.block_type,
          "name": self.name,
          "keyword": self.keyword,
          "options": self.options,
          "body": self.body,
        })

class MacroUndefinitionBlock(Block):
    def __init__(self, name, keyword):
        self.block_type = BlockTypes.MacroUndefinitionType
        self.name = name
        self.keyword = keyword
        self.AP = None

    def to_json(self):
        return self._filter({
          "AP": self.AP,
          "block_type": self.block_type,
          "name": self.name,
          "keyword": self.keyword
        })

class MacroConditionBlock(Block):
    def __init__(self, name, condition, content, ending = None):
        self.block_type = BlockTypes.MacroConditionType
        self.name = name
        self.condition = condition
        self.content = content
        self.ending = ending
        self.AP = None

    def to_json(self):
        return self._filter({
          "AP": self.AP,
          "block_type": self.block_type,
          "name": self.name,
          "condition": self.condition,
          "content": map(lambda l: l.to_json(), self.content),
          "ending": self.ending,
        })

class CommentBlock(Block):
    def __init__(self, content):
        self.block_type = BlockTypes.CommentType
        self.content = content
        self.AP = None

    def to_json(self):
        return self._filter({
          "AP": self.AP,
          "block_type": self.block_type,
          "content": self.content,
        })

class WhitespacesBlock(Block):
    def __init__(self, content):
        self.block_type = BlockTypes.Whitespaces
        self.content = content
        self.AP = None

    def to_json(self):
        return self._filter({
          "AP": self.AP,
          "block_type": self.block_type,
          "content": self.content,
        })

class UninterpretedBlock(Block):
    def __init__(self, content):
        self.block_type = BlockTypes.Uninterpreted
        self.content = content
        self.AP = None

    def to_json(self):
        return self._filter({
          "AP": self.AP,
          "block_type": self.block_type,
          "content": self.content,
        })

class ConditionBlock(Block):
    def __init__(self, keyword, expression, content, else_body, end_keyword, else_keyword):
        self.block_type = BlockTypes.ConditionType
        self.keyword = keyword
        self.expression = expression
        self.content = content
        self.else_body = else_body
        self.end_keyword = end_keyword
        # If else keyword is None, the else_body is ignored
        self.else_keyword = else_keyword
        self.AP = None

    def to_json(self):
        return self._filter({
          "AP": self.AP,
          "block_type": self.block_type,
          "keyword": self.keyword,
          "expression": self.expression,
          "content": map(lambda l: l.to_json(), self.content),
          "else_keyword": self.else_keyword,
          "else_body": map(lambda l: l.to_json(), self.else_body),
          "end_keyword": self.end_keyword,
        })

class RawConditionBlock(Block):
    def __init__(self, keyword, expression, content, else_body, end_keyword, else_keyword):
        self.block_type = BlockTypes.ConditionType
        self.keyword = keyword
        self.expression = expression
        self.content = content
        self.else_body = else_body
        self.end_keyword = end_keyword
        self.else_keyword = else_keyword

    def to_json(self):
        return self._filter({
          "block_type": self.block_type,
          "keyword": self.keyword,
          "expression": self.expression,
          "content": map(lambda l: l.to_json(), self.content),
          "else_keyword": self.else_keyword,
          "else_body": map(lambda l: l.to_json(), self.else_body),
          "end_keyword": self.end_keyword,
        })

class RawContextType:
  Unknown = 0
  Section = 1

class RawContext(Block):
  def __init__(self, type = RawContextType.Unknown):
    self.blocks = []
    self.type = type
    self.closed = False

  def to_json(self):
      return self._filter({
        "type": self.type,
        "closed": self.closed,
        "blocks": map(lambda l: l.to_json(), self.blocks),
      })

class RawText(Block):
  def __init__(self, text):
    self.block_type = BlockTypes.RawText
    self.text = text

  def to_json(self):
      return self._filter({
        "block_type": self.block_type,
        "text": self.text,
      })

class RawSection(Block):
  def __init__(self, kw, section):
    self.block_type = BlockTypes.RawSection
    self.section = section
    self.kw = kw

  def to_json(self):
      return self._filter({
        "block_type": self.block_type,
        "section": self.section,
        "kw": self.kw,
      })


# Begin -- grammar generated by Yapps

import sys, re
from yapps import runtime

class SpecfileParserScanner(runtime.Scanner):
    patterns = [
        ('END', re.compile('\\s*$')),
        ('BEGINNING', re.compile('\\s*')),
        ('TAG_KEY', re.compile('(?i)(NAME|VERSION|RELEASE|SUMMARY|LICENSE|URL|BUILDREQUIRES(\\(\\S+\\))?|REQUIRES(\\(\\S+\\))?|GROUP|BUILDROOT|EXCLUDEARCH|EXCLUSIVEARCH|CONFLICTS|BUILDARCH|PROVIDES|PRE|PREUN|POST|POSTUN)\\s*|(SOURCE|PATCH)\\d*\\s*')),
        ('COLON', re.compile('\\:')),
        ('TAG_VALUE', re.compile('.*\\s*')),
        ('COMMENT', re.compile('\\#.+\\s*')),
        ('PERCENT_SIGN', re.compile('%')),
        ('DASH', re.compile('\\-')),
        ('PARAMETERS', re.compile('\\S+[ \\t\\r\\f\\v]*')),
        ('PARAMETER_VALUE', re.compile('\\S+[ \\t\\r\\f\\v]*')),
        ('NAME', re.compile('(?!\\-)\\S+[ \\t\\r\\f\\v]*')),
        ('NEWLINE', re.compile('\\n')),
        ('MACRO_DEF_KEYWORD', re.compile('(?i)%(define|global)\\s*')),
        ('MACRO_UNDEF_KEYWORD', re.compile('(?i)undefine\\s*')),
        ('MACRO_NAME', re.compile('\\S+?(?=[\\(|\\:|\\s])\\s*')),
        ('MACRO_OPTIONS', re.compile('\\(.*?\\)\\s*')),
        ('MACRO_BODY', re.compile('(?!\\().*\\s*')),
        ('MACRO_CONDITION_BODY', re.compile('(?!\\().*(?=\\}\\s*)')),
        ('LEFT_PARENTHESIS', re.compile('\\{')),
        ('RIGHT_PARENTHESIS', re.compile('\\}')),
        ('EXCLAMATION_MARK', re.compile('\\!')),
        ('QUESTION_MARK', re.compile('\\?')),
        ('WHITESPACE', re.compile('[ \\t\\n\\r\\f\\v]*')),
        ('CONDITION_BEG_KEYWORD', re.compile('(?i)%(if|ifarch|ifos|ifnarch|ifnos)\\s*')),
        ('CONDITION_ELSE_KEYWORD', re.compile('(?i)%else\\s*')),
        ('CONDITION_EXPRESSION', re.compile('.*[^\\n]*')),
        ('CONDITION_BODY', re.compile('(?!(endif|if|else))[\\W\\w]*?(?=%(else|endif|if))')),
        ('CONDITION_END_KEYWORD', re.compile('(?i)%endif')),
        ('SECTION_KEY', re.compile('(?i)(DESCRIPTION|PREP|PREUN|PRE|POSTUN|POST|FILES)[ \\t\\r\\f\\v]*')),
        ('SECTION_KEY_NOPARSE_WITH_OPTS', re.compile('(?i)%(DESCRIPTION|PREUN|PRE|POSTUN|POST|FILES)[ \\t\\r\\f\\v]*')),
        ('SECTION_KEY_NOPARSE_PURE', re.compile('(?i)%(PREP|BUILD|CHECK|INSTALL|CLEAN)[ \\t\\r\\f\\v]*')),
        ('SECTION_CONTENT', re.compile('(?i)(?!\\n%(DESCRIPTION|PACKAGE|PREP|BUILD|CHECK|INSTALL|FILES|CHANGELOG|PRE|PREUN|POST|POSTUN))[\\w\\W]+?(?=\\n%(DESCRIPTION|PACKAGE|PREP|BUILD|CHECK|INSTALL|FILES|CHANGELOG|PRE|PREUN|POST|POSTUN)|$)')),
        ('SECTION_CONTENT_NOPARSE', re.compile('(?i)(?!(NAME|VERSION|RELEASE|SUMMARY|LICENSE|URL|SOURCE|PATCH|BUILDREQUIRES|REQUIRES|GROUP|BUILDROOT|EXCLUDEARCH|EXCLUSIVEARCH|CONFLICTS|BUILDARCH|PROVIDES)\\:|%(DESCRIPTION|BUILD|CHECK|INSTALL|FILES|PACKAGE|CHANGELOG|PRE|PREUN|POST|POSTUN))[\\w\\W]+?(?=(NAME|VERSION|RELEASE|SUMMARY|LICENSE|URL|SOURCE|PATCH|BUILDREQUIRES|REQUIRES|GROUP|BUILDROOT|EXCLUDEARCH|EXCLUSIVEARCH|CONFLICTS|BUILDARCH|PROVIDES)\\:|%(DESCRIPTION|PREP|BUILD|CHECK|INSTALL|FILES|PACKAGE|CHANGELOG|PRE|PREUN|POST|POSTUN)|$)\\s*')),
        ('CHANGELOG_KEYWORD', re.compile('(?i)%CHANGELOG\\s*')),
        ('SINGLE_LOG', re.compile('\\*[\\W\\w]*?(?=\\*|$)')),
        ('PACKAGE_KW', re.compile('%(?i)package[ \\t\\r\\f\\v]*')),
        ('DESCRIPTION_KW', re.compile('%(?i)description[ \\t\\r\\f\\v]*')),
        ('PREP_KW', re.compile('%(?i)prep[ \\t\\r\\f\\v]*')),
        ('BUILD_KW', re.compile('%(?i)build[ \\t\\r\\f\\v]*')),
        ('SECTION_CONTENT_BLOCK', re.compile('(?i)[^%#]*(?=%(PACKAGE|DESCRIPTION|PREP|BUILD|INSTALL|CHECK|PRE|PREUN|POST|POSTUN|FILES|IF|ELSE|ENDIF)|$)')),
        ('TEXT_LINE', re.compile('(?i)([^%#]|%{)[\\W\\w]*?(?=[\\n](#|%(package|description|prep|build|install|check|pre|preun|endif|if|else|patch)))\\s*')),
        ('ALL', re.compile('(?i)[\\W\\w]*$')),
        ('SETUP_LINE', re.compile('(?i)%setup[^\\n]*\\n')),
        ('PATCH_LINE', re.compile('(?i)%patch[^\\n]*\\s*')),
        ('PACKAGE_CONTENT', re.compile('(?i)[\\W\\w]*?(?=%(PACKAGE|PREP|BUILD|INSTALL|CHECK|PRE|PREUN|POST|POSTUN|FILES)|$)\\s*')),
        ('SECTION_KW', re.compile('(?i)\\n%(DESCRIPTION|PACKAGE|PREP|BUILD|CHECK|INSTALL|FILES|CHANGELOG|PRE|PREUN|POST|POSTUN)')),
        ('SECTION_CONTENT', re.compile('(?i)(?!\\n%(DESCRIPTION|PACKAGE|PREP|BUILD|CHECK|INSTALL|FILES|CHANGELOG|PRE|PREUN|POST|POSTUN))[\\w\\W]+?(?=\\n%(DESCRIPTION|PACKAGE|PREP|BUILD|CHECK|INSTALL|FILES|CHANGELOG|PRE|PREUN|POST|POSTUN)|$)')),
        ('NON_COND_TEXT', re.compile('(?i)[\\W\\w]*?(?=%(endif|if|else)|$)\\s*')),
        ('ALMOST_ANYTHING', re.compile('(?!%(endif|if|else))[\\W\\w]*')),
    ]
    def __init__(self, str,*args,**kw):
        runtime.Scanner.__init__(self,None,{},str,*args,**kw)

class SpecfileParser(runtime.Parser):
    Context = runtime.Context
    def spec(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'spec', [])
        if self._peek('NON_COND_TEXT', 'ALMOST_ANYTHING', 'CONDITION_BEG_KEYWORD', context=_context) == 'NON_COND_TEXT':
            NON_COND_TEXT = self._scan('NON_COND_TEXT', context=_context)
            self._rawSpecFile.beginning = NON_COND_TEXT;
        while self._peek('ALMOST_ANYTHING', 'CONDITION_BEG_KEYWORD', context=_context) == 'CONDITION_BEG_KEYWORD':
            cond_spec = self.cond_spec(_context)
            self._rawSpecFile.block_list.append(cond_spec)
            NON_COND_TEXT = self._scan('NON_COND_TEXT', context=_context)
            if NON_COND_TEXT != "": self._rawSpecFile.block_list.append(RawText(NON_COND_TEXT))
        if 1:
            ALMOST_ANYTHING = self._scan('ALMOST_ANYTHING', context=_context)
            self._rawSpecFile.end = ALMOST_ANYTHING;

    def cond_body(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'cond_body', [])
        items = []
        while self._peek('NON_COND_TEXT', 'CONDITION_BEG_KEYWORD', 'CONDITION_ELSE_KEYWORD', 'CONDITION_END_KEYWORD', context=_context) in ['NON_COND_TEXT', 'CONDITION_BEG_KEYWORD']:
            _token = self._peek('NON_COND_TEXT', 'CONDITION_BEG_KEYWORD', context=_context)
            if _token == 'NON_COND_TEXT':
                NON_COND_TEXT = self._scan('NON_COND_TEXT', context=_context)
                items.append(RawText(NON_COND_TEXT))
            else: # == 'CONDITION_BEG_KEYWORD'
                cond_spec = self.cond_spec(_context)
                items.append(cond_spec)
        return items

    def cond_spec(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'cond_spec', [])
        if_body = []
        else_body = []
        else_kw = ""
        CONDITION_BEG_KEYWORD = self._scan('CONDITION_BEG_KEYWORD', context=_context)
        CONDITION_EXPRESSION = self._scan('CONDITION_EXPRESSION', context=_context)
        cond_body = self.cond_body(_context)
        if_body = cond_body
        if self._peek('CONDITION_ELSE_KEYWORD', 'CONDITION_END_KEYWORD', context=_context) == 'CONDITION_ELSE_KEYWORD':
            CONDITION_ELSE_KEYWORD = self._scan('CONDITION_ELSE_KEYWORD', context=_context)
            cond_body = self.cond_body(_context)
            else_kw = CONDITION_ELSE_KEYWORD; else_body = cond_body
        CONDITION_END_KEYWORD = self._scan('CONDITION_END_KEYWORD', context=_context)
        return RawConditionBlock(CONDITION_BEG_KEYWORD, CONDITION_EXPRESSION, if_body, else_body, CONDITION_END_KEYWORD, else_kw)

    def sections_list(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'sections_list', [])
        items = []
        while self._peek('END', 'SECTION_CONTENT', 'SECTION_KW', context=_context) != 'END':
            _token = self._peek('SECTION_CONTENT', 'SECTION_KW', context=_context)
            if _token == 'SECTION_CONTENT':
                SECTION_CONTENT = self._scan('SECTION_CONTENT', context=_context)
                items.append(RawText(SECTION_CONTENT))
            else: # == 'SECTION_KW'
                SECTION_KW = self._scan('SECTION_KW', context=_context)
                SECTION_CONTENT = self._scan('SECTION_CONTENT', context=_context)
                items.append(RawSection(SECTION_KW.strip(), "{}{}".format(SECTION_KW,SECTION_CONTENT)))
        END = self._scan('END', context=_context)
        if len(items) > 0 and items[-1].block_type == BlockTypes.RawText: items[-1].text += END
        else: items.append(RawText(END))
        self._rawSpecFile.block_list = items

    def main_section(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'main_section', [])
        items = []
        if self._peek('BEGINNING', 'END', 'MACRO_DEF_KEYWORD', 'COMMENT', 'TAG_KEY', context=_context) == 'BEGINNING':
            BEGINNING = self._scan('BEGINNING', context=_context)
            if BEGINNING != "": items.append(WhitespacesBlock(BEGINNING));
        while self._peek('END', 'MACRO_DEF_KEYWORD', 'COMMENT', 'TAG_KEY', context=_context) != 'END':
            _token = self._peek('MACRO_DEF_KEYWORD', 'COMMENT', 'TAG_KEY', context=_context)
            if _token == 'MACRO_DEF_KEYWORD':
                macro_definition = self.macro_definition(_context)
                items.append(macro_definition)
            elif _token == 'COMMENT':
                commentary = self.commentary(_context)
                items.append(commentary)
            else: # == 'TAG_KEY'
                tag = self.tag(_context)
                items.append(tag)
        END = self._scan('END', context=_context)
        if END != "": items.append(WhitespacesBlock(END))
        self._rawSpecFile.block_list = items

    def macro_definition(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'macro_definition', [])
        MACRO_DEF_KEYWORD = self._scan('MACRO_DEF_KEYWORD', context=_context)
        MACRO_NAME = self._scan('MACRO_NAME', context=_context)
        if self._peek('MACRO_OPTIONS', 'MACRO_BODY', context=_context) == 'MACRO_OPTIONS':
            MACRO_OPTIONS = self._scan('MACRO_OPTIONS', context=_context)
        MACRO_BODY = self._scan('MACRO_BODY', context=_context)
        if 'MACRO_OPTIONS' in locals(): options = MACRO_OPTIONS
        else: options = None
        return MacroDefinitionBlock(MACRO_NAME, MACRO_DEF_KEYWORD, options, MACRO_BODY)

    def tag(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'tag', [])
        TAG_KEY = self._scan('TAG_KEY', context=_context)
        COLON = self._scan('COLON', context=_context)
        TAG_VALUE = self._scan('TAG_VALUE', context=_context)
        if TAG_KEY.find('(') == -1: key = TAG_KEY; option = None
        else: key = TAG_KEY[:TAG_KEY.find('(')]; option = TAG_KEY[TAG_KEY.find('(')+1:-1]
        return HeaderTagBlock(key, TAG_VALUE, option)

    def commentary(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'commentary', [])
        COMMENT = self._scan('COMMENT', context=_context)
        return CommentBlock(COMMENT)

    def uninterpreted_section_content(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'uninterpreted_section_content', [])
        ALL = self._scan('ALL', context=_context)
        return UninterpretedBlock(ALL)

    def uninterpreted_section_body(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'uninterpreted_section_body', [])
        uninterpreted_section_content = self.uninterpreted_section_content(_context)
        self._rawSpecFile.block_list = [uninterpreted_section_content]

    def uninterpreted_section_with_opts(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'uninterpreted_section_with_opts', [])
        self._rawSpecFile.block_list = []
        if self._peek('BEGINNING', 'SECTION_KEY_NOPARSE_WITH_OPTS', context=_context) == 'BEGINNING':
            BEGINNING = self._scan('BEGINNING', context=_context)
            if BEGINNING != "": self._rawSpecFile.block_list.append(WhitespacesBlock(BEGINNING))
        SECTION_KEY_NOPARSE_WITH_OPTS = self._scan('SECTION_KEY_NOPARSE_WITH_OPTS', context=_context)
        if self._peek('NAME', 'DASH', 'NEWLINE', context=_context) == 'NAME':
            NAME = self._scan('NAME', context=_context)
        parameters = []
        while self._peek('NEWLINE', 'DASH', context=_context) == 'DASH':
            DASH = self._scan('DASH', context=_context)
            PARAMETERS = self._scan('PARAMETERS', context=_context)
            pvalue = None
            if self._peek('PARAMETER_VALUE', 'DASH', 'NEWLINE', context=_context) == 'PARAMETER_VALUE':
                PARAMETER_VALUE = self._scan('PARAMETER_VALUE', context=_context)
                pvalue = PARAMETER_VALUE
            parameters.append({"key": PARAMETERS, "value": pvalue})
        NEWLINE = self._scan('NEWLINE', context=_context)
        uninterpreted_section_content = self.uninterpreted_section_content(_context)
        if 'NAME' in locals(): subname = NAME + NEWLINE
        else: subname = NEWLINE
        self._rawSpecFile.block_list.append(SectionBlock(SECTION_KEY_NOPARSE_WITH_OPTS, parameters, None, subname, [uninterpreted_section_content]))

    def uninterpreted_section(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'uninterpreted_section', [])
        self._rawSpecFile.block_list = [];
        if self._peek('BEGINNING', 'SECTION_KEY_NOPARSE_PURE', context=_context) == 'BEGINNING':
            BEGINNING = self._scan('BEGINNING', context=_context)
            if BEGINNING != "": self._rawSpecFile.block_list.append(WhitespacesBlock(BEGINNING))
        SECTION_KEY_NOPARSE_PURE = self._scan('SECTION_KEY_NOPARSE_PURE', context=_context)
        NEWLINE = self._scan('NEWLINE', context=_context)
        uninterpreted_section_content = self.uninterpreted_section_content(_context)
        self._rawSpecFile.block_list.append(SectionBlock(SECTION_KEY_NOPARSE_PURE, None, None, None, [uninterpreted_section_content]))

    def package_section_content(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'package_section_content', [])
        package_body = []
        if self._peek('BEGINNING', 'TAG_KEY', 'COMMENT', 'END', context=_context) == 'BEGINNING':
            BEGINNING = self._scan('BEGINNING', context=_context)
            if BEGINNING != "": package_body.append(WhitespacesBlock(BEGINNING))
        while self._peek('END', 'TAG_KEY', 'COMMENT', context=_context) != 'END':
            _token = self._peek('TAG_KEY', 'COMMENT', context=_context)
            if _token == 'TAG_KEY':
                tag = self.tag(_context)
                package_body.append(tag)
            else: # == 'COMMENT'
                COMMENT = self._scan('COMMENT', context=_context)
                package_body.append(CommentBlock(COMMENT))
        END = self._scan('END', context=_context)
        if END != "": package_body.append(WhitespacesBlock(END))
        return package_body

    def package_section_body(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'package_section_body', [])
        package_section_content = self.package_section_content(_context)
        self._rawSpecFile.block_list = package_section_content

    def package_section(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'package_section', [])
        self._rawSpecFile.block_list = []
        if self._peek('BEGINNING', 'PACKAGE_KW', context=_context) == 'BEGINNING':
            BEGINNING = self._scan('BEGINNING', context=_context)
            if BEGINNING != "": self._rawSpecFile.block_list.append(WhitespacesBlock(BEGINNING))
        PACKAGE_KW = self._scan('PACKAGE_KW', context=_context)
        if self._peek('DASH', 'NAME', 'NEWLINE', context=_context) == 'DASH':
            DASH = self._scan('DASH', context=_context)
            PARAMETERS = self._scan('PARAMETERS', context=_context)
        if self._peek('NAME', 'NEWLINE', context=_context) == 'NAME':
            NAME = self._scan('NAME', context=_context)
        NEWLINE = self._scan('NEWLINE', context=_context)
        parameters = None
        name = None
        if 'NAME' in locals(): subname = NAME + NEWLINE
        else: subname = NEWLINE
        if 'PARAMETERS' in locals(): parameters = PARAMETERS
        package_section_content = self.package_section_content(_context)
        self._rawSpecFile.block_list.append(PackageBlock(PACKAGE_KW, parameters, subname, package_section_content))

    def changelog(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'changelog', [])
        SINGLE_LOG = self._scan('SINGLE_LOG', context=_context)
        return SINGLE_LOG

    def changelog_section(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'changelog_section', [])
        content = []
        self._rawSpecFile.block_list = []
        if self._peek('BEGINNING', 'CHANGELOG_KEYWORD', context=_context) == 'BEGINNING':
            BEGINNING = self._scan('BEGINNING', context=_context)
            if BEGINNING != "": self._rawSpecFile.block_list.append(WhitespacesBlock(BEGINNING))
        CHANGELOG_KEYWORD = self._scan('CHANGELOG_KEYWORD', context=_context)
        while self._peek('SINGLE_LOG', 'END', context=_context) == 'SINGLE_LOG':
            changelog = self.changelog(_context)
            content.append(changelog)
        self._rawSpecFile.block_list.append(ChangelogBlock(CHANGELOG_KEYWORD, content))
        END = self._scan('END', context=_context)
        if END != "": self._rawSpecFile.block_list.append(WhitespacesBlock(END))

    def macro_condition(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'macro_condition', [])
        if self._peek('EXCLAMATION_MARK', 'QUESTION_MARK', context=_context) == 'EXCLAMATION_MARK':
            EXCLAMATION_MARK = self._scan('EXCLAMATION_MARK', context=_context)
        QUESTION_MARK = self._scan('QUESTION_MARK', context=_context)
        MACRO_NAME = self._scan('MACRO_NAME', context=_context)
        COLON = self._scan('COLON', context=_context)
        MACRO_CONDITION_BODY = self._scan('MACRO_CONDITION_BODY', context=_context)
        if 'EXCLAMATION_MARK' in locals(): condition = EXCLAMATION_MARK + QUESTION_MARK
        else: condition = QUESTION_MARK
        _, rawSpecFile = parseByRule('spec_file', MACRO_CONDITION_BODY)
        return MacroConditionBlock(MACRO_NAME, condition, rawSpecFile.block_list)

    def macro_undefine(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'macro_undefine', [])
        MACRO_UNDEF_KEYWORD = self._scan('MACRO_UNDEF_KEYWORD', context=_context)
        MACRO_NAME = self._scan('MACRO_NAME', context=_context)
        return MacroUndefinitionBlock(MACRO_UNDEF_KEYWORD, MACRO_NAME)


def parse(rule, text):
    P = SpecfileParser(SpecfileParserScanner(text))
    return runtime.wrap_error_reporter(P, rule)

# End -- grammar generated by Yapps



def parseByRule(goal, text):
    P = SpecfileParser(SpecfileParserScanner(text))
    P._rawSpecFile = RawSpecFile()
    e = runtime.wrap_error_reporter(P, goal)
    return P._rawSpecFile

class RawSpecFileParser(object):

  def __init__(self, specfile):
    self._specfile = specfile
    self._rawSpecfile = None
    self.counter = 0

  def divide_sections(self, blocks, tab = 0):
    items = []
    for block in blocks:
      if block.block_type == BlockTypes.RawText:
        sections = parseByRule("sections_list", block.text)
        items += sections.block_list
      elif block.block_type == BlockTypes.ConditionType:
        items.append(
          # keyword, expression, content, else_body, end_keyword, else_keyword
          RawConditionBlock(
            block.keyword,
            block.expression,
            self.divide_sections(block.content, tab + 1),
            self.divide_sections(block.else_body, tab + 1),
            block.end_keyword,
            block.else_keyword
          )
        )
      else:
        raise BlockTypeUnknown("Unrecognized block type {}".format(block.block_type))
    return items

  def merge_contexts(self, sections):
    # Merge Section(Unknown)* into Section and Unknown+ into Unknown
    l = len(sections)
    i = 0
    while i < l:
      if i + 1 < l:
        if (sections[i].type in [RawContextType.Section, RawContextType.Unknown]) and sections[i+1].type == RawContextType.Unknown:
          # is the section closed?
          if sections[i].type == RawContextType.Section and sections[i].closed:
            # Unless the Unknown context consists only of a list of comments and/or whitespaces
            # TODO(jchaloup): run a simple parsing to verify so, in that case the Unknown can be appended to closed Section context
            raise SectionContextException("Closed Section context followed by an Unknown context")
          sections[i].blocks += sections[i+1].blocks
          del(sections[i+1])
          l -= 1
          continue
        i += 1
        continue
      # no more sections in the future
      break

    # Every Section in the list becomes closed now (end of a block is reached)
    for section in sections:
      if section.type == RawContextType.Section:
        section.closed = True

  def mark_sections(self, blocks, tab = 0):
    sections = []

    for item in blocks:
      if item.block_type == BlockTypes.RawText:
        if len(sections) == 0:
          sections.append(RawContext())

        sections[-1].blocks.append(item)
        continue

      if item.block_type == BlockTypes.RawSection:
        sections.append(RawContext(type=RawContextType.Section))
        sections[-1].blocks.append(item)
        continue

      if item.block_type != BlockTypes.ConditionType:
        raise BlockTypeUnknown("Unrecognized block type {}".format(item.block_type))

      ifsections = self.mark_sections(item.content, tab + 1)
      elsesections = self.mark_sections(item.else_body, tab + 1)

      # Expected context list: (Unknown)*(Section(Unknown)*)*
      # A section becomes closed when end of a block is reached
      # If a section is closed an followed by an Unknown => error (it means a section starts in %if block and does not end before %end)

      # Merge Section(Unknown)* into Section and Unknown+ into Unknown
      self.merge_contexts(ifsections)
      self.merge_contexts(elsesections)

      # A list of section conforms to (Unknown)?(Section)*
      if_context_unknown = True
      else_context_unknown = True
      for section in ifsections:
        if section.type != RawContextType.Unknown:
          if_context_unknown = False

      for section in elsesections:
        if section.type != RawContextType.Unknown:
          else_context_unknown = False

      # If one of the if/else blocks is of Unknown context and the other one has at least one Section context => error
      # Unless the Unknown context consists only of a list of comments/whitespaces
      # keyword, expression, content, else_body, end_keyword, else_keyword
      c = RawContext()
      c.blocks = [
        RawConditionBlock(
          item.keyword,
          item.expression,
          ifsections,
          elsesections,
          item.end_keyword,
          item.else_keyword
        )
      ]

      if if_context_unknown and else_context_unknown:
        c.type = RawContextType.Unknown
      else:
        c.type = RawContextType.Section
        c.closed = True

      sections.append(c)
    return sections

  def parse_section(self, rule, context, tab = 0):
    sections = [[]]
    for block in context.blocks:
      if block.block_type == BlockTypes.ConditionType:
        if_blocks = []
        for if_item in block.content:
          if_blocks += self.parse_section(rule, if_item, tab + 1)

        else_blocks = []
        for else_item in block.else_body:
          else_blocks += self.parse_section(rule, else_item, tab + 1)

        # keyword, expression, content, else_body, end_keyword, else_keyword
        sections[-1].append(ConditionBlock(
            block.keyword,
            block.expression,
            if_blocks,
            else_blocks,
            block.end_keyword,
            block.else_keyword
          )
        )
        continue

      if block.block_type == BlockTypes.RawText:
        data = parseByRule(rule, block.text)
        sections[-1] += data.block_list
        continue
      if block.block_type == BlockTypes.RawSection:
        if block.kw in ["%description", "%pre", "%post", "%preun", "%postun", "%files"]:
          data = parseByRule("uninterpreted_section_with_opts", block.section)
          rule = "uninterpreted_section_body"
        elif block.kw == "%package":
          data = parseByRule("package_section", block.section)
          rule = "package_section_body"
        elif block.kw in ["%prep", "%build", "%install", "%check"]:
          data = parseByRule("uninterpreted_section", block.section)
          rule = "uninterpreted_section_body"
        elif block.kw == "%changelog":
          data = parseByRule("changelog_section", block.section)
        else:
          raise SectionKeywordUnknown("Unknown block.kw: {}".format(block.kw))

        sections.append(data.block_list)
        continue

    # The first block processed was a RawSection
    if sections[0] == []:
      for section in sections[1:]:
        i = 0
        l = len(section)
        while i < l:
          if i + 1 < l:
            if section[i].block_type in [BlockTypes.SectionTagType, BlockTypes.PackageTagType]:
              section[i].content.append(section[i+1])
              del section[i+1]
              l -= 1
              continue
          i += 1
      return reduce(lambda x,y: x+y, sections)
    else:
      return sections[0]

  def parse(self):
     # Parse the conditions (to get a condition-free pieces of a specfile)
     self._rawSpecfile = parseByRule("spec", self._specfile)

     # Process condition-free pieces
     blocks = self.divide_sections(self._rawSpecfile.block_list)
     sections = self.mark_sections(blocks)
     self.merge_contexts(sections)

     # Here we end with Unknown(Section)* sequence
     # The first Unknown context corresponds to the main section
     # Run individual section parsers
     self._rawSpecfile = reduce(lambda x,y: x+y, map(lambda section: self.parse_section("main_section", section), sections))

     return self

  def printJson(self, data):
    if isinstance(data, list):
      items = []
      for item in data:
         items.append(self.printJson(item))
      return items
    if isinstance(data, basestring):
      return data
    return data.to_json()

  def json(self):
     return json.loads(json.dumps(self._rawSpecfile, default=lambda o: o.__dict__, sort_keys=True))

  def raw(self):
    return self._rawSpecfile
