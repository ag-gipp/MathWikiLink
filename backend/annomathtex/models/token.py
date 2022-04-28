from abc import ABCMeta, abstractmethod
import json


class Token(object, metaclass=ABCMeta):
    def __init__(
                 self,
                 unique_id,
                 type,
                 highlight,
                 content,
                 endline,
                 math_env = None
                 ):
        """
        Each word/identifier/formula/emptyline in a document is a token. A token must be one of those 4.
        Punctuation are excluded.

        :param unique_id: uuid.uuid1 object, converted to a string. Needed in template for rendering.
        :param type: String, "Word", "Identifier", "Formula", or "Endline". Needed for correct template rendering.
        :param highlight: String, color, that the Token should be highlighted in. None if no highlight desired.
        :param content: String, The Word/Identifier itself.
        :param endline: Boolean, needed for page rendering, true if token ends the line.
        """
        self.unique_id = str(unique_id)
        self.type = type
        self.highlight = highlight
        self.content = content
        self.endline = endline
        self.math_env = math_env

        self.json_content = json.dumps({'content': content})
        self.json_math_env = json.dumps({'math_env': math_env})


