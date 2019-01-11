#
# match.py for Match in /home/jean.walrave/projects/epitech/autoCompletion_2016/sources
#
# Made by Jean Walrave
# Login	 <jean.walrave@epitech.net>
#
# Started on	Sun Jul	9 08:43:07 2017 Jean Walrave
# Last update	Sun Jul	9 08:43:07 2017 Jean Walrave
#

class Match(object):
    class Type(object):
        (UNKNOWN, PARTIAL_CITY, CITY_PART, CITY, PARTIAL_STREET_NAME, STREET_NAME_PART, STREET_NAME) = range(7)
        MATCH_NAME = ['UNKNOWN', 'PARTIAL_CITY', 'CITY_PART', 'CITY', 'PARTIAL_STREET_NAME', 'STREET_NAME_PART', 'STREET_NAME']

    @staticmethod
    def match_partial(str, criteria):
        partials = [x.lower() for x in str.split() if x.lower().startswith(criteria)]

        if any(partials):
            return ([partial[:len(criteria) + 1] for partial in partials])

        return (None)

    @staticmethod
    def match_part(str, criteria):
        parts = [x.lower() for x in str.split() if x.lower() == criteria]

        if any(parts):
            return (parts[0])

        return (None)

    @staticmethod
    def match_full(str, criteria):
        if str.lower() == criteria:
            return (str.lower())
