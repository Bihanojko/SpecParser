from abstract_model import BlockTypes
from metastring import HeaderTagMetastring, SectionMetastring, ConditionMetastring, MacroConditionMetastring, MacroDefinitionMetastring, CommentMetastring, ChangelogMetastring

class SpecModel(object):
    def __init__(self):
        self._block_list = []

        self._beginning = ""
        self._metastrings = []
        self._end = ""

    def fromRawSpecfile(self, raw):
        self._beginning = raw.beginning
        self._end = raw.end
        self._block_list, self._metastrings = self._processBlockList(raw.block_list)

        return self

    def _processBlockList(self, block_list, predicate_list = []):
        processed_blocks = []
        generated_metastrings = []

        for single_block in block_list:

            if single_block.block_type == BlockTypes.HeaderTagType:
                generated_metastrings.append( HeaderTagMetastring().fromBlockType(single_block).to_str() )
                clean_block = HeaderTagMetastring().cleanBlockType(single_block)
                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.CommentType:
                generated_metastrings.append( CommentMetastring().fromBlockType(single_block).to_str() )
                clean_block = CommentMetastring().cleanBlockType(single_block)
                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.MacroDefinitionType:
                generated_metastrings.append( MacroDefinitionMetastring().fromBlockType(single_block).to_str() )
                clean_block = MacroDefinitionMetastring().cleanBlockType(single_block)
                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.SectionTagType:
                if single_block.keyword.strip() == "changelog":
                    generated_metastrings.append( ChangelogMetastring().fromBlockType(single_block).to_str() )
                    clean_block = ChangelogMetastring().cleanBlockType(single_block)
                    if predicate_list != []:
                        # TODO(jchaloup): register the AP in the conditioner table as well
                        clean_block.AP = predicate_list
                    processed_blocks.append(clean_block)
                    continue

                if single_block.keyword.strip() == "package":
                    clean_block = SectionMetastring().cleanBlockType(single_block)
                    generated_metastrings.append( SectionMetastring().fromBlockType(single_block).to_str() )

                    if single_block.content != []:
                        clean_block.content, metastring_children = self._processBlockList(single_block.content, predicate_list)
                        generated_metastrings.append(metastring_children)

                    if predicate_list != []:
                        # TODO(jchaloup): register the AP in the conditioner table as well
                        clean_block.AP = predicate_list
                    processed_blocks.append(clean_block)
                    continue

                generated_metastrings.append( SectionMetastring().fromBlockType(single_block).to_str() )
                clean_block = SectionMetastring().cleanBlockType(single_block)
                if predicate_list != []:
                    # TODO(jchaloup): register the AP in the conditioner table as well
                    clean_block.AP = predicate_list
                processed_blocks.append(clean_block)
                continue

            if single_block.block_type == BlockTypes.ConditionType:
                generated_metastrings.append( ConditionMetastring().fromBlockType(single_block).to_str() )
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
                generated_metastrings.append( MacroConditionMetastring().fromBlockType(single_block).to_str() )
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

    def _metastring_list_to_str(self, metastring_list):
        str = ""
        for item in metastring_list:
            if isinstance(item, list):
                str += self._metastring_list_to_str(item)
                continue
            str += "#" + item

        return str

    def metastrings_to_str(self):
        return self._beginning + self._metastring_list_to_str(self._metastrings) + self._end

    def model_to_json(self):
        return {
            "block_list": map(lambda l: l.to_json(), self._block_list),
            "metastring": self.metastrings_to_str(),
        }
