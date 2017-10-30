# FROMFUTUREIMPORT
import json
from abstract_model import RawSpecFile, BlockTypes

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

%%
parser SpecfileParser:

    token END: "\s*$"
    token BEGINNING: r'\s*'
    token TAG_KEY: r'(?i)(NAME|VERSION|RELEASE|SUMMARY|LICENSE|URL|BUILDREQUIRES(\(\S+\))?|REQUIRES(\(\S+\))?|GROUP|BUILDROOT|EXCLUDEARCH|EXCLUSIVEARCH|CONFLICTS|BUILDARCH|PROVIDES|PRE|PREUN|POST|POSTUN)\s*|(SOURCE|PATCH)\d*\s*'
    token COLON: "\:"
    token TAG_VALUE: r'.*\s*'
    token COMMENT: r'\#.+\s*'
    token PERCENT_SIGN: '%'
    token DASH: r'\-'
    token PARAMETERS: r'\S+[ \t\r\f\v]*'
    token NAME: r'(?!\-)\S+[ \t\r\f\v]*'
    token NEWLINE: r'\n'
    token MACRO_DEF_KEYWORD: r'(?i)(define|global)\s*'
    token MACRO_UNDEF_KEYWORD: r'(?i)undefine\s*'
    token MACRO_NAME: r'\S+?(?=[\(|\:|\s])\s*'
    token MACRO_OPTIONS: r'\(.*?\)\s*'
    token MACRO_BODY: r'(?!\().*\s*'
    token MACRO_CONDITION_BODY: r'(?!\().*(?=\}\s*)'
    token LEFT_PARENTHESIS: r'\{'
    token RIGHT_PARENTHESIS: r'\}'
    token EXCLAMATION_MARK: r'\!'
    token QUESTION_MARK: r'\?'
    token WHITESPACE: r'[ \t\n\r\f\v]*'
    token CONDITION_BEG_KEYWORD: r'(?i)(if|ifarch|ifos|ifnarch|ifnos)\s*'
    token CONDITION_ELSE_KEYWORD: r'(?i)else\s*'
    token CONDITION_EXPRESSION: r'.*\s*'
    token CONDITION_BODY: r'(?!(endif|if|else))[\W\w]*?(?=%(else|endif|if))'
    token CONDITION_END_KEYWORD: r'(?i)endif\s*'
    token SECTION_KEY: r'(?i)(DESCRIPTION|PREP|PREUN|PRE|POSTUN|POST|FILES)[ \t\r\f\v]*'
    token SECTION_KEY_NOPARSE: r'(?i)(BUILD|CHECK|INSTALL|CLEAN)[ \t\r\f\v]*'
    token SECTION_CONTENT: r'(?i)(?!(NAME|VERSION|RELEASE|SUMMARY|LICENSE|URL|SOURCE|PATCH|BUILDREQUIRES|REQUIRES|GROUP|BUILDROOT|EXCLUDEARCH|EXCLUSIVEARCH|CONFLICTS|BUILDARCH|PROVIDES)\:|%(DESCRIPTION|BUILD|CHECK|INSTALL|FILES|PACKAGE|CHANGELOG|PRE|PREUN|POST|POSTUN)|%(define|global|undefine)|%(if|ifarch|ifos|ifnarch|ifnos|else|endif))[\w\W]+?(?=(NAME|VERSION|RELEASE|SUMMARY|LICENSE|URL|SOURCE|PATCH|BUILDREQUIRES|REQUIRES|GROUP|BUILDROOT|EXCLUDEARCH|EXCLUSIVEARCH|CONFLICTS|BUILDARCH|PROVIDES)\:|%(DESCRIPTION|PREP|BUILD|CHECK|INSTALL|FILES|PACKAGE|CHANGELOG|PRE|PREUN|POST|POSTUN)|%(define|global|undefine)|%(if|ifarch|ifos|ifnarch|ifnos|else|endif)|%\{!\?|%\{\?|$)\s*'
    token SECTION_CONTENT_NOPARSE: r'(?i)(?!(NAME|VERSION|RELEASE|SUMMARY|LICENSE|URL|SOURCE|PATCH|BUILDREQUIRES|REQUIRES|GROUP|BUILDROOT|EXCLUDEARCH|EXCLUSIVEARCH|CONFLICTS|BUILDARCH|PROVIDES)\:|%(DESCRIPTION|BUILD|CHECK|INSTALL|FILES|PACKAGE|CHANGELOG|PRE|PREUN|POST|POSTUN))[\w\W]+?(?=(NAME|VERSION|RELEASE|SUMMARY|LICENSE|URL|SOURCE|PATCH|BUILDREQUIRES|REQUIRES|GROUP|BUILDROOT|EXCLUDEARCH|EXCLUSIVEARCH|CONFLICTS|BUILDARCH|PROVIDES)\:|%(DESCRIPTION|PREP|BUILD|CHECK|INSTALL|FILES|PACKAGE|CHANGELOG|PRE|PREUN|POST|POSTUN)|$)\s*'
    token CHANGELOG_KEYWORD: r'(?i)CHANGELOG\s*'
    token SINGLE_LOG: r'\*[\W\w]*?(?=\*|$)'
    token PACKAGE_KEYWORD: r'(?i)PACKAGE[ \t\r\f\v]*'
    token PACKAGE_CONTENT: '(?i)[\W\w]*?(?=%(PACKAGE|PREP|BUILD|INSTALL|CHECK|PRE|PREUN|POST|POSTUN|FILES)|$)\s*'


    rule goal:         begin spec_file END              {{ self._rawSpecFile.end = END }}


    rule begin:        BEGINNING                        {{ self._rawSpecFile.beginning = BEGINNING }}


    rule spec_file:    header rest?


    rule header:       tag*



    rule tag:          header_tag                       {{ self._rawSpecFile.block_list.append(header_tag) }}
                    |  commentary                       {{ self._rawSpecFile.block_list.append(commentary) }}
                    |  PERCENT_SIGN keyword



    rule header_tag:   TAG_KEY COLON TAG_VALUE          {{ if TAG_KEY.find('(') == -1: key = TAG_KEY; option = None }}
                                                        {{ else: key = TAG_KEY[:TAG_KEY.find('(')]; option = TAG_KEY[TAG_KEY.find('(')+1:-1] }}
                                                        {{ return HeaderTagBlock(key, TAG_VALUE, option) }}



    rule rest:      PERCENT_SIGN keyword
                    |  commentary                       {{ self._rawSpecFile.block_list.append(commentary) }}



    rule keyword:      section                          {{ self._rawSpecFile.block_list.append(section) }}
                    |  macro_definition                 {{ self._rawSpecFile.block_list.append(macro_definition) }}
                    |  macro_undefine                   {{ self._rawSpecFile.block_list.append(macro_undefine) }}
                    |  condition_definition             {{ self._rawSpecFile.block_list.append(condition_definition) }}
                    |  LEFT_PARENTHESIS macro_condition RIGHT_PARENTHESIS WHITESPACE
                                                        {{ macro_condition.ending = WHITESPACE }}
                                                        {{ self._rawSpecFile.block_list.append(macro_condition) }}



    rule macro_definition: MACRO_DEF_KEYWORD MACRO_NAME MACRO_OPTIONS? MACRO_BODY
                                                                        {{ if 'MACRO_OPTIONS' in locals(): options = MACRO_OPTIONS }}
                                                                        {{ else: options = None }}
                                                                        {{ return MacroDefinitionBlock(MACRO_NAME, MACRO_DEF_KEYWORD, options, MACRO_BODY) }}


    rule macro_condition:   EXCLAMATION_MARK? QUESTION_MARK MACRO_NAME COLON MACRO_CONDITION_BODY
                                                                        {{ if 'EXCLAMATION_MARK' in locals(): condition = EXCLAMATION_MARK + QUESTION_MARK }}
                                                                        {{ else: condition = QUESTION_MARK }}
                                                                        {{ _, rawSpecFile = parseByRule('spec_file', MACRO_CONDITION_BODY) }}
                                                                        {{ return MacroConditionBlock(MACRO_NAME, condition, rawSpecFile.block_list) }}


    rule commentary:  COMMENT                                           {{ return CommentBlock(COMMENT) }}




    rule changelog:     SINGLE_LOG                                      {{ return SINGLE_LOG }}



    rule condition_definition:  CONDITION_BEG_KEYWORD CONDITION_EXPRESSION CONDITION_BODY PERCENT_SIGN
                                        {{ block_content = [] }}
                                        {{ _, rawSpecFile = parseByRule('spec_file', CONDITION_BODY) }}
                                        {{ block_content = rawSpecFile.block_list }}
                                        {{ block_else_body = [] }}
                        ((condition_definition
                                        {{ if block_content[-1].block_type == BlockTypes.SectionTagType and 'package' in block_content[-1].keyword and condition_definition not in block_content[-1].content: block_content[-1].content.append(condition_definition) }}
                                        {{ elif condition_definition not in block_content: block_content.append(condition_definition) }}
                        | body          {{ _, rawSpecFile = parseByRule('spec_file', body) }}
                                        {{ if block_content[-1].block_type == BlockTypes.SectionTagType and 'package' in block_content[-1].keyword: block_content[-1].content += rawSpecFile.block_list }}
                                        {{ else: block_content += rawSpecFile.block_list }}
                        ) PERCENT_SIGN?)*
                        (CONDITION_ELSE_KEYWORD condition_else_body PERCENT_SIGN
                                        {{ if 'condition_else_body' in locals(): _, rawSpecFile = parseByRule('spec_file', condition_else_body); block_else_body += rawSpecFile.block_list; del condition_else_body }}
                        ((condition_else_inner | else_body)
                                        {{ if 'else_body' in locals(): _, rawSpecFile = parseByRule('spec_file', else_body); block_else_body += rawSpecFile.block_list; del else_body }}
                                        {{ if 'condition_else_inner' in locals() and condition_else_inner not in block_else_body: block_else_body.append(condition_else_inner); del condition_else_inner }}
                        PERCENT_SIGN?)*)?
                        CONDITION_END_KEYWORD
                                        {{ if 'CONDITION_ELSE_KEYWORD' in locals(): block_else_keyword = CONDITION_ELSE_KEYWORD }}
                                        {{ else: block_else_keyword = None }}
                                        {{ return ConditionBlock(CONDITION_BEG_KEYWORD, CONDITION_EXPRESSION, block_content, block_else_body, CONDITION_END_KEYWORD, block_else_keyword) }}



    rule condition_else_body:       CONDITION_BODY                      {{ return CONDITION_BODY }}



    rule condition_else_inner:      condition_definition                {{ return condition_definition }}



    rule else_body:                 CONDITION_BODY                      {{ return CONDITION_BODY }}



    rule body:                      CONDITION_BODY                      {{ return CONDITION_BODY }}



    rule section:           SECTION_KEY option? (DASH PARAMETERS)? NAME? NEWLINE SECTION_CONTENT
                                                                        {{ parameters = None }}
                                                                        {{ subname = None }}
                                                                        {{ name = None }}
                                                                        {{ if 'PARAMETERS' in locals(): parameters = PARAMETERS }}
                                                                        {{ if 'NAME' in locals(): subname = NAME }}
                                                                        {{ if 'option' in locals(): name = option }}
                                                                        {{ return SectionBlock(SECTION_KEY, parameters, name, subname, NEWLINE + SECTION_CONTENT) }}
                        |   SECTION_KEY_NOPARSE option?  (DASH PARAMETERS)? NAME? NEWLINE SECTION_CONTENT_NOPARSE
                                                                        {{ parameters = None }}
                                                                        {{ subname = None }}
                                                                        {{ name = None }}
                                                                        {{ if 'PARAMETERS' in locals(): parameters = PARAMETERS }}
                                                                        {{ if 'NAME' in locals(): subname = NAME }}
                                                                        {{ if 'option' in locals(): name = option }}
                                                                        {{ return SectionBlock(SECTION_KEY_NOPARSE, parameters, name, subname, NEWLINE + SECTION_CONTENT_NOPARSE) }}
                        |   PACKAGE_KEYWORD (DASH PARAMETERS)? NAME? NEWLINE PACKAGE_CONTENT
                                                                        {{ parameters = None }}
                                                                        {{ name = None }}
                                                                        {{ if 'NAME' in locals(): subname = NAME + NEWLINE }}
                                                                        {{ else: subname = NEWLINE }}
                                                                        {{ if 'PARAMETERS' in locals(): parameters = PARAMETERS }}
                                                                        {{ _, rawSpecFile = parseByRule('spec_file', PACKAGE_CONTENT) }}
                                                                        {{ return PackageBlock(PACKAGE_KEYWORD, parameters, subname, rawSpecFile.block_list) }}
                        |                                               {{ content = [] }}
                            CHANGELOG_KEYWORD (
                                changelog                               {{ content.append(changelog) }}
                            )*
                                                                        {{ return ChangelogBlock(CHANGELOG_KEYWORD, content) }}



    rule option:            NAME                                        {{ return NAME }}



    rule macro_undefine:    MACRO_UNDEF_KEYWORD MACRO_NAME              {{ return MacroUndefinitionBlock(MACRO_UNDEF_KEYWORD, MACRO_NAME) }}


%%

def parseByRule(goal, text):
    P = SpecfileParser(SpecfileParserScanner(text))
    P._rawSpecFile = RawSpecFile()
    e = runtime.wrap_error_reporter(P, goal)
    return e, P._rawSpecFile

class RawSpecFileParser(object):

  def __init__(self, specfile):
    self._specfile = specfile
    self._rawSpecfile = None

  def parse(self):
     _, self._rawSpecfile = parseByRule("goal", self._specfile)
     return self

  def json(self):
     return json.loads(json.dumps(self._rawSpecfile, default=lambda o: o.__dict__, sort_keys=True))

  def raw(self):
    return self._rawSpecfile
