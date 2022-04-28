from .parser import Parser
from TexSoup import TexSoup
import logging
import re
import warnings
import logging
warnings.filterwarnings("ignore")


logging.basicConfig(level=logging.INFO)
tex_parser_logger = logging.getLogger(__name__)

class TEXParser(Parser):
    """
    This class is a subclass of the abstract base class Parser. It is used to parse and process LaTeX files.
    """

    def decode(self, request_file):
        """
        TeX files are in bytes and have to be converted to string in utf-8.
        :param request_file: The file that the user selected.
        :return: The decoded file as a string.
        """

        #tex_parser_logger.info(request_file)


        bytes = request_file#.read()
        string = bytes.decode('utf-8')
        return string

    def extract_math_envs(self):
        """
        Extract the math environments that are contained in the file (e.g. within '$...$').
        :return: A list of the math environments as strings.
        """

        def handle_special_chars(math_env):
            """
            Mainly for FormulaSplitter() in latexformlaidentifiers.py, since it has trouble detecting certain
            characters. Make it easier by preprocessing the math environment first (e.g. 'S_i' becomes 'S_{i}').
            :param math_env: The math environment that is currently being processed.
            :return: A tuple of the old math environment and the new math environment (with special characters
                     handled). If the math environment contains no special characters, return a tuple of the math
                     environment x 2.

            """
            special_char = re.search(r'_(\w|\d)', math_env)
            if special_char:
                found_char = re.search(r'(?<=_)(\w|\d)', math_env).group()[0]
                found_char_with_brackets = '{' + found_char + '}'
                math_env_new = math_env.replace(found_char, found_char_with_brackets)
                return (math_env, math_env_new)
            return (math_env, math_env)

        tex_soup = TexSoup(self.file)
        equation = list(tex_soup.find_all('equation'))
        align = list(tex_soup.find_all('align'))
        dollar = list(tex_soup.find_all('$'))
        math_envs = equation + align + dollar
        math_envs = list(map(lambda m: str(m), math_envs))
        return math_envs
