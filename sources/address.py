#
# address.py for Address in /home/jean.walrave/projects/epitech/autoCompletion_2016/sources
#
# Made by Jean Walrave
# Login	 <jean.walrave@epitech.net>
#
# Started on	Mon Jul	10 08:27:17 2017 Jean Walrave
# Last update	Mon Jul	10 08:27:17 2017 Jean Walrave
#

import re
import collections

from match import Match


class Holder(object):
    def __init__(self):
        self.value = None

    def set(self, value):
        self.value = value

        return (value)

    def get(self):
        return (self.value)


class Address(object):
    def __init__(self, address):
        self.match_state = Match.Type.UNKNOWN

        for k, v in Address.split_address(address).items():
            setattr(self, '_' + k if k in ('city', 'street_name') else k, v)

    @property
    def city(self):
        return (self._city.replace('\'', '').replace('-', ''))

    @property
    def street_name(self):
        return (self._street_name.replace('\'', '').replace('-', ''))

    def match_with_criteria(self, criteria, match_state):
        criteria = criteria.lower()
        holder = Holder()
        match = {'state': Match.Type.UNKNOWN, 'match': None}

        if match_state == Match.Type.CITY:
            if holder.set(Match.match_full(self.city, criteria)):
                match['state'] = Match.Type.CITY
            elif holder.set(Match.match_part(self.city, criteria)):
                match['state'] = Match.Type.CITY_PART
            elif holder.set(Match.match_partial(self.city, criteria)):
                match['state'] = Match.Type.PARTIAL_CITY
        elif match_state == Match.Type.STREET_NAME:
            if holder.set(Match.match_full(self.street_name, criteria)):
                match['state'] = Match.Type.STREET_NAME
            elif holder.set(Match.match_part(self.street_name, criteria)):
                match['state'] = Match.Type.STREET_NAME_PART
            elif holder.set(Match.match_partial(self.street_name, criteria)):
                match['state'] = Match.Type.PARTIAL_STREET_NAME

        match['match'] = holder.get()

        if self.match_state != match['state']:
            self.match_state = match['state']

        return (match)

    def __str__(self):
        return ('{_city:s}, {number:s} {street_type:s} {_street_name:s}').format(**self.__dict__)

    def __repr__(self):
        return ('<(Address) city: {_city:s}, number: {number:s}, street type: {street_type:s}, street name: {_street_name:s}>').format(**self.__dict__)

    @staticmethod
    def split_address(address):
        r = re.match(r"(?P<city>[\w '-]+)(,|) (?P<number>\d+) (?P<street_type>\w+) (?P<street_name>[\w '-]+)", address)

        return (None if not r else r.groupdict())

    @staticmethod
    def is_valid_address(address):
        r = Address.split_address(address)
        street_types = [u'allée', 'avenue', 'boulevard', 'chemin', 'impasse', 'place', 'quai', 'rue', 'square']

        return (False if not r or r['street_type'].lower() not in street_types else True)

    @staticmethod
    def extract_cities(addresses, size=1, full_city=False):
        excities = []
        for address in addresses:
            if not full_city:
                for city in address.city.split():
                    excities.append(city[:size].lower())
            else:
                excities.append(address.city)

        return (excities)

    @staticmethod
    def extract_street_names(addresses, size=1, full_address=False):
        exsnames = []
        for address in addresses:
            if not full_address:
                for street_name in address.street_name.split():
                    exsnames.append(street_name[:size].lower())
            else:
                exsnames.append(str(address))

        return (exsnames)

    @staticmethod
    def sort_cities_by_alphabetical_order(cities):
        cities.sort(key=lambda city: city.lower())

        return (sorted(set(cities), key=cities.index))

    @staticmethod
    def sort_addresses_by_alphanumeric_order(addresses):
        addresses = sorted(addresses, key=lambda address: (address.street_name.lower(), address.street_type.lower(), int(address.number)))

        return (addresses)

    @staticmethod
    def sort_cities_by_recurrence(cities):
        ccities = collections.Counter(cities)
        cities.sort(key=lambda city: (-ccities[city], city.lower()))

        return (sorted(set(cities), key=cities.index))

    @staticmethod
    def city_matching_print(cities, size=0, limit=5):
        print (' '.join('{%s}' % (city.upper() if size is None else city[:size].upper() + city[size].lower()) for k, city in enumerate(cities) if not limit or k < limit))

    @staticmethod
    def street_name_matching_print(city, street_names, size=0, limit=5):
        print (' '.join('{%s, %s}' % (city.upper(), street_name.uper() if size is None else street_name[:size].upper() + street_name[size].lower()) for k, street_name in enumerate(street_names) if not limit or k < limit))

    @staticmethod
    def city_choice_print(cities, search):
        print (' '.join('{%d : %s}' % (k + 1, city.lower().replace(search.lower(), search.upper(), 1)) for k, city in enumerate(cities)))

    @staticmethod
    def street_name_choice_print(addresses, search):
        def get_common_words(addresses):
            faddresses = [str(address).lower().replace(', ', ' ').split() for address in addresses]
            cwords = set(faddresses[0])

            for fwords in faddresses[1:]:
                cwords = cwords.intersection(set(fwords))

            return (cwords)

        if len(addresses) > 1:
            common_words = list(get_common_words(addresses))

            for k, _ in enumerate(addresses):
                addresses[k] = str(addresses[k]).lower()

                for word in common_words:
                    addresses[k] = addresses[k].replace(word.lower(), word.upper())
        else:
            addresses[0] = str(addresses[0]).lower().replace(addresses[0].city.lower(), addresses[0].city.upper()).replace(search.lower(), search.upper())

        print (' '.join('{%d : %s}' % (k + 1, address) for k, address in enumerate(addresses)))
