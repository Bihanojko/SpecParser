# FROMFUTUREIMPORT
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

%%
parser SpecfileParser:

    # *? ... non-greedy match
    # ?= ... don't include the string after the ?= to the matched string
    # ^(?!mpeg).* ... match all strings not starting with mpeg prefix

    token END: "\s*$"
    token BEGINNING: r'\s*'
    token TAG_KEY: r'(?i)(NAME|VERSION|RELEASE|SUMMARY|LICENSE|URL|BUILDREQUIRES(\(\S+\))?|REQUIRES(\(\S+\))?|GROUP|BUILDROOT|EXCLUDEARCH|EXCLUSIVEARCH|CONFLICTS|BUILDARCH|PROVIDES|PRE|PREUN|POST|POSTUN)\s*|(SOURCE|PATCH)\d*\s*'
    token COLON: "\:"
    token TAG_VALUE: r'.*\s*'
    token COMMENT: r'\#.+\s*'
    token PERCENT_SIGN: '%'
    token DASH: r'\-'
    token PARAMETERS: r'\S+[ \t\r\f\v]*'
    token PARAMETER_VALUE: r'\S+[ \t\r\f\v]*'
    token NAME: r'(?!\-)\S+[ \t\r\f\v]*'
    token NEWLINE: r'\n'
    token MACRO_DEF_KEYWORD: r'(?i)%(define|global)\s*'
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
    token CONDITION_BEG_KEYWORD: r'(?i)%(if|ifarch|ifos|ifnarch|ifnos)\s*'
    token CONDITION_ELSE_KEYWORD: r'(?i)%else\s*'
    token CONDITION_EXPRESSION: r'.*[^\n]*'
    token CONDITION_BODY: r'(?!(endif|if|else))[\W\w]*?(?=%(else|endif|if))'
    token CONDITION_END_KEYWORD: r'(?i)%endif'
    token SECTION_KEY: r'(?i)(DESCRIPTION|PREP|PREUN|PRE|POSTUN|POST|FILES)[ \t\r\f\v]*'
    token SECTION_KEY_NOPARSE_WITH_OPTS: r'(?i)%(DESCRIPTION|PREUN|PRE|POSTUN|POST|FILES)[ \t\r\f\v]*'
    token SECTION_KEY_NOPARSE_PURE: r'(?i)%(PREP|BUILD|CHECK|INSTALL|CLEAN)[ \t\r\f\v]*'
    token SECTION_CONTENT: r'(?i)(?!(NAME|VERSION|RELEASE|SUMMARY|LICENSE|URL|SOURCE|PATCH|BUILDREQUIRES|REQUIRES|GROUP|BUILDROOT|EXCLUDEARCH|EXCLUSIVEARCH|CONFLICTS|BUILDARCH|PROVIDES)\:|%(DESCRIPTION|BUILD|CHECK|INSTALL|FILES|PACKAGE|CHANGELOG|PRE|PREUN|POST|POSTUN)|%(define|global|undefine)|%(if|ifarch|ifos|ifnarch|ifnos|else|endif))[\w\W]+?(?=(NAME|VERSION|RELEASE|SUMMARY|LICENSE|URL|SOURCE|PATCH|BUILDREQUIRES|REQUIRES|GROUP|BUILDROOT|EXCLUDEARCH|EXCLUSIVEARCH|CONFLICTS|BUILDARCH|PROVIDES)\:|%(DESCRIPTION|PREP|BUILD|CHECK|INSTALL|FILES|PACKAGE|CHANGELOG|PRE|PREUN|POST|POSTUN)|%(define|global|undefine)|%(if|ifarch|ifos|ifnarch|ifnos|else|endif)|%\{!\?|%\{\?|$)\s*'
    token SECTION_CONTENT_NOPARSE: r'(?i)(?!(NAME|VERSION|RELEASE|SUMMARY|LICENSE|URL|SOURCE|PATCH|BUILDREQUIRES|REQUIRES|GROUP|BUILDROOT|EXCLUDEARCH|EXCLUSIVEARCH|CONFLICTS|BUILDARCH|PROVIDES)\:|%(DESCRIPTION|BUILD|CHECK|INSTALL|FILES|PACKAGE|CHANGELOG|PRE|PREUN|POST|POSTUN))[\w\W]+?(?=(NAME|VERSION|RELEASE|SUMMARY|LICENSE|URL|SOURCE|PATCH|BUILDREQUIRES|REQUIRES|GROUP|BUILDROOT|EXCLUDEARCH|EXCLUSIVEARCH|CONFLICTS|BUILDARCH|PROVIDES)\:|%(DESCRIPTION|PREP|BUILD|CHECK|INSTALL|FILES|PACKAGE|CHANGELOG|PRE|PREUN|POST|POSTUN)|$)\s*'
    token CHANGELOG_KEYWORD: r'(?i)%CHANGELOG\s*'
    token SINGLE_LOG: r'\*[\W\w]*?(?=\*|$)'

    token PACKAGE_KW:     r'%(?i)package[ \t\r\f\v]*'
    token DESCRIPTION_KW: r'%(?i)description[ \t\r\f\v]*'
    token PREP_KW:        r'%(?i)prep[ \t\r\f\v]*'
    token BUILD_KW:       r'%(?i)build[ \t\r\f\v]*'

    token SECTION_CONTENT_BLOCK: r'(?i)[^%#]*(?=%(PACKAGE|DESCRIPTION|PREP|BUILD|INSTALL|CHECK|PRE|PREUN|POST|POSTUN|FILES|IF|ELSE|ENDIF)|$)'
    token TEXT_LINE: r'(?i)([^%#]|%{)[\W\w]*?(?=[\n](#|%(package|description|prep|build|install|check|pre|preun|endif|if|else|patch)))\s*'
    token ALL: r'(?i)[\W\w]*$'

    token SETUP_LINE: r'(?i)%setup[^\n]*\n'
    token PATCH_LINE: r'(?i)%patch[^\n]*\s*'

    token PACKAGE_CONTENT: '(?i)[\W\w]*?(?=%(PACKAGE|PREP|BUILD|INSTALL|CHECK|PRE|PREUN|POST|POSTUN|FILES)|$)\s*'

    token SECTION_KW:         r'(?i)\n%(DESCRIPTION|PACKAGE|PREP|BUILD|CHECK|INSTALL|FILES|CHANGELOG|PRE|PREUN|POST|POSTUN)'
    token SECTION_CONTENT:    r'(?i)(?!\n%(DESCRIPTION|PACKAGE|PREP|BUILD|CHECK|INSTALL|FILES|CHANGELOG|PRE|PREUN|POST|POSTUN))[\w\W]+?(?=\n%(DESCRIPTION|PACKAGE|PREP|BUILD|CHECK|INSTALL|FILES|CHANGELOG|PRE|PREUN|POST|POSTUN)|$)'

    #####################################################################################################
    #####################################################################################################
    ### First, parse the spec file only with respect to if[arch|narch|os|nos]-[else-]endif conditions ###
    #####################################################################################################
    #####################################################################################################
    token NON_COND_TEXT:      r'(?i)[\W\w]*?(?=%(endif|if|else)|$)\s*'
    token ALMOST_ANYTHING:    r'(?!%(endif|if|else))[\W\w]*'


    rule spec:         (
                          NON_COND_TEXT {{ self._rawSpecFile.beginning = NON_COND_TEXT; }}
                       )?
                       (
                          cond_spec       {{ self._rawSpecFile.block_list.append(cond_spec) }}
                          NON_COND_TEXT   {{ if NON_COND_TEXT != "": self._rawSpecFile.block_list.append(RawText(NON_COND_TEXT)) }}
                       )*
                       (
                           ALMOST_ANYTHING {{ self._rawSpecFile.end = ALMOST_ANYTHING; }}
                       )?

    rule cond_body:    {{ items = [] }}
                       (
                       NON_COND_TEXT  {{ items.append(RawText(NON_COND_TEXT)) }}
                       | cond_spec {{ items.append(cond_spec) }}
                       )*
                       {{ return items }}

    rule cond_spec:    {{ if_body = [] }}
                       {{ else_body = [] }}
                       {{ else_kw = "" }}
                       CONDITION_BEG_KEYWORD CONDITION_EXPRESSION cond_body {{ if_body = cond_body }}
                       (
                            CONDITION_ELSE_KEYWORD cond_body  {{ else_kw = CONDITION_ELSE_KEYWORD; else_body = cond_body }}
                       )?
                       CONDITION_END_KEYWORD
                       {{ return RawConditionBlock(CONDITION_BEG_KEYWORD, CONDITION_EXPRESSION, if_body, else_body, CONDITION_END_KEYWORD, else_kw) }}

    #####################################################################################################
    #####################################################################################################
    ### Parse condition-free section pieces of a specfile ###############################################
    #####################################################################################################
    #####################################################################################################
    rule sections_list:   {{ items = [] }}
                          (
                          SECTION_CONTENT {{ items.append(RawText(SECTION_CONTENT)) }}
                          | SECTION_KW SECTION_CONTENT
                            {{ items.append(RawSection(SECTION_KW.strip(), "{}{}".format(SECTION_KW,SECTION_CONTENT))) }}
                          )*
                          END
                          {{ if len(items) > 0 and items[-1].block_type == BlockTypes.RawText: items[-1].text += END }}
                          {{ else: items.append(RawText(END)) }}
                          {{ self._rawSpecFile.block_list = items }}

    #####################################################################################################
    #####################################################################################################
    ### Parse individual sections of a specfile #########################################################
    #####################################################################################################
    #####################################################################################################
    rule main_section:    {{ items = [] }}
                          (
                            BEGINNING         {{ if BEGINNING != "": items.append(WhitespacesBlock(BEGINNING)); }}
                          )?
                          (
                            macro_definition  {{ items.append(macro_definition) }}
                            | commentary      {{ items.append(commentary) }}
                            | tag             {{ items.append(tag) }}
                          )*
                          (
                            END               {{ if END != "": items.append(WhitespacesBlock(END)) }}
                          )
                          {{ self._rawSpecFile.block_list = items }}

    rule macro_definition:  MACRO_DEF_KEYWORD MACRO_NAME MACRO_OPTIONS? MACRO_BODY
                            {{ if 'MACRO_OPTIONS' in locals(): options = MACRO_OPTIONS }}
                            {{ else: options = None }}
                            {{ return MacroDefinitionBlock(MACRO_NAME, MACRO_DEF_KEYWORD, options, MACRO_BODY) }}


    rule tag:   TAG_KEY COLON TAG_VALUE
                {{ if TAG_KEY.find('(') == -1: key = TAG_KEY; option = None }}
                {{ else: key = TAG_KEY[:TAG_KEY.find('(')]; option = TAG_KEY[TAG_KEY.find('(')+1:-1] }}
                {{ return HeaderTagBlock(key, TAG_VALUE, option) }}

    rule commentary:  COMMENT   {{ return CommentBlock(COMMENT) }}

    rule uninterpreted_section_content:  ALL {{ return UninterpretedBlock(ALL) }}

    rule uninterpreted_section_body: uninterpreted_section_content {{ self._rawSpecFile.block_list = [uninterpreted_section_content] }}

    rule uninterpreted_section_with_opts: {{ self._rawSpecFile.block_list = [] }}
                                          (
                                            BEGINNING   {{ if BEGINNING != "": self._rawSpecFile.block_list.append(WhitespacesBlock(BEGINNING)) }}
                                          )?
                                          SECTION_KEY_NOPARSE_WITH_OPTS NAME? {{ parameters = [] }}
                                          (
                                            DASH PARAMETERS {{ pvalue = None }}
                                            (
                                              PARAMETER_VALUE {{ pvalue = PARAMETER_VALUE }}
                                            )?
                                            {{ parameters.append({"key": PARAMETERS, "value": pvalue}) }}
                                          )*
                                          NEWLINE uninterpreted_section_content
                                          {{ if 'NAME' in locals(): subname = NAME + NEWLINE }}
                                          {{ else: subname = NEWLINE }}
                                          {{ self._rawSpecFile.block_list.append(SectionBlock(SECTION_KEY_NOPARSE_WITH_OPTS, parameters, None, subname, [uninterpreted_section_content])) }}

    rule uninterpreted_section:    {{ self._rawSpecFile.block_list = []; }}
                          (
                            BEGINNING   {{ if BEGINNING != "": self._rawSpecFile.block_list.append(WhitespacesBlock(BEGINNING)) }}
                          )?
                          SECTION_KEY_NOPARSE_PURE NEWLINE uninterpreted_section_content
                          {{ self._rawSpecFile.block_list.append(SectionBlock(SECTION_KEY_NOPARSE_PURE, None, None, None, [uninterpreted_section_content])) }}

    rule package_section_content:   {{ package_body = [] }}
                                    (
                                      BEGINNING         {{ if BEGINNING != "": package_body.append(WhitespacesBlock(BEGINNING)) }}
                                    )?
                                    (
                                      tag                     {{ package_body.append(tag) }}
                                      #| macro_definition      {{ package_body.append(macro_definition) }}
                                      | COMMENT               {{ package_body.append(CommentBlock(COMMENT)) }}
                                    )*
                                    (
                                      END               {{ if END != "": package_body.append(WhitespacesBlock(END)) }}
                                    )
                                    {{ return package_body }}

    rule package_section_body: package_section_content {{ self._rawSpecFile.block_list = package_section_content }}

    rule package_section:   {{ self._rawSpecFile.block_list = [] }}
                            (
                              BEGINNING         {{ if BEGINNING != "": self._rawSpecFile.block_list.append(WhitespacesBlock(BEGINNING)) }}
                            )?
                            PACKAGE_KW (DASH PARAMETERS)? NAME? NEWLINE
                            {{ parameters = None }}
                            {{ name = None }}
                            {{ if 'NAME' in locals(): subname = NAME + NEWLINE }}
                            {{ else: subname = NEWLINE }}
                            {{ if 'PARAMETERS' in locals(): parameters = PARAMETERS }}
                            package_section_content
                            {{ self._rawSpecFile.block_list.append(PackageBlock(PACKAGE_KW, parameters, subname, package_section_content)) }}

    rule changelog:     SINGLE_LOG   {{ return SINGLE_LOG }}

    rule changelog_section:     {{ content = [] }}
                                {{ self._rawSpecFile.block_list = [] }}
                                (
                                  BEGINNING         {{ if BEGINNING != "": self._rawSpecFile.block_list.append(WhitespacesBlock(BEGINNING)) }}
                                )?
                                CHANGELOG_KEYWORD (
                                    changelog                               {{ content.append(changelog) }}
                                )*
                                {{ self._rawSpecFile.block_list.append(ChangelogBlock(CHANGELOG_KEYWORD, content)) }}
                                (
                                  END               {{ if END != "": self._rawSpecFile.block_list.append(WhitespacesBlock(END)) }}
                                )










    rule macro_condition:   EXCLAMATION_MARK? QUESTION_MARK MACRO_NAME COLON MACRO_CONDITION_BODY
                                                                        {{ if 'EXCLAMATION_MARK' in locals(): condition = EXCLAMATION_MARK + QUESTION_MARK }}
                                                                        {{ else: condition = QUESTION_MARK }}
                                                                        {{ _, rawSpecFile = parseByRule('spec_file', MACRO_CONDITION_BODY) }}
                                                                        {{ return MacroConditionBlock(MACRO_NAME, condition, rawSpecFile.block_list) }}

    rule macro_undefine:    MACRO_UNDEF_KEYWORD MACRO_NAME              {{ return MacroUndefinitionBlock(MACRO_UNDEF_KEYWORD, MACRO_NAME) }}


%%

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
