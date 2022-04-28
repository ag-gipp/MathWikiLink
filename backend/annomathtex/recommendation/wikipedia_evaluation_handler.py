import os
import json
import logging
from ..config import recommendations_limit
from ..settings.common import PROJECT_ROOT


logging.basicConfig(level=logging.INFO)
wikipedia_evaluation_list_handler_logger = logging.getLogger(__name__)

class WikipediaEvaluationListHandler:
    """
    This class reads the extracted list of Wikipedia identifiers and returns a dictionary of the results, with respect
    to the queried identifier. The queried identifier being an identifier clicked by the user through the frontend.
    """
    def __init__(self):
        self.identifier_dict = self.read_file()

    def read_file(self):
        """
        Read the file containing the previously extacted Wikipedia identifiers.
        :return: The read file as a string.
        """
        #path = os.getcwd() + '/annomathtex/recommendation/evaluation_files/wikipedia_list.json'
        path = os.path.join(PROJECT_ROOT, 'annomathtex', 'recommendation', 'evaluation_files', 'wikipedia_list.json')
        with open(path, 'r') as json_file:
            identifier_dict = json.load(json_file)
        return identifier_dict

    def check_identifiers(self, symbol):
        """
        Return the entries of the dictionary that match the symbol that was clicked by the user.
        :param symbol: The string of the symbol that was clicked by the user for annotation.
        :return: The corresponding matches from the dictionary of Wikipedia identifiers.
        """
        symbol = symbol if symbol in self.identifier_dict else '\\{}'.format(symbol)
        if symbol in self.identifier_dict:
            identifier_dict_symbol = self.identifier_dict[symbol]
            new_d = []
            found_descriptions = []
            for d in identifier_dict_symbol:
                if d['description'] not in found_descriptions:
                    item_dict = {
                        'name': d['description'].lower()
                    }
                    new_d.append(item_dict)
                    found_descriptions.append(d['description'])
            return new_d[:recommendations_limit]
        return []

