#
# completion.py for Completion in /home/jean.walrave/projects/epitech/autoCompletion_2016/sources
#
# Made by Jean Walrave
# Login	 <jean.walrave@epitech.net>
#
# Started on	Sun Jul	10 09:43:07 2017 Jean Walrave
# Last update	Sun Jul	10 09:43:07 2017 Jean Walrave
#

import sys

from match import Match
from address import Address


ABORT = 'ABORT'
ERR_MSG_UNKNOWN_ADDRESS = 'Unknown address'

def eprint(*args, **kwargs):
    print (*args, file=sys.stderr, **kwargs)

class Completion(object):
    class State(object):
        (UNKNOWN, CITY_COMPLETION, STREET_NAME_COMPLETION, FINISHED) = range(4)

    def __init__(self, addresses_dictionnary):
        self.addresses_dictionnary = addresses_dictionnary

    @staticmethod
    def quit_unknown_address():
        eprint(ERR_MSG_UNKNOWN_ADDRESS)

        sys.exit(84)

    @staticmethod
    def autocomplete_search(dictionnary, search):
        if not dictionnary:
            return (search, False)

        csearch = search
        cletter = None
        while cletter is not False:
            for w in dictionnary:
                if not cletter and len(w) > len(csearch):
                    cletter = w[len(csearch)]
                elif len(w) <= len(csearch) or w[len(csearch)] != cletter:
                    cletter = False
                    break

            if cletter is not False:
                csearch += cletter
                cletter = None

        return (csearch, True if search != csearch else False)

    def do_city_completion(self, addresses, search):
        if hasattr(Completion.do_city_completion, 'choices'):
            choices = Completion.do_city_completion.choices

            if search[-1].isnumeric() and int(search[-1]) in range(1, len(choices) + 1):
                choice = choices[int(search[-1]) - 1]

                for address in list([address for address in addresses if address.city.lower() != choice.lower()]):
                    addresses.remove(address)

                return (Completion.State.STREET_NAME_COMPLETION)
            elif not search[-1].isnumeric():
                delattr(Completion.do_city_completion, 'choices')
            else:
                Address.city_choice_print(choices, search)

                return (search[:len(search) - 1])

        while True:
            results = {'matches': [], Match.Type.CITY: [], Match.Type.CITY_PART: {}, Match.Type.PARTIAL_CITY: []}

            for address in list(addresses):
                matchr = address.match_with_criteria(search, Match.Type.CITY)

                if matchr['state'] != Match.Type.UNKNOWN:
                    for match in matchr['match']:
                        results['matches'].append(match)

                    if matchr['state'] in (Match.Type.CITY, Match.Type.PARTIAL_CITY):
                        results[matchr['state']].append(address)
                    elif matchr['match'] in results[Match.Type.CITY_PART]:
                        results[Match.Type.CITY_PART][matchr['match']].append(address)
                    else:
                        results[Match.Type.CITY_PART][matchr['match']] = [address]
                elif address in addresses:
                    addresses.remove(address)

            if results['matches']:
                search, supdated = self.autocomplete_search(set(results['matches']), search)

                if supdated:
                    continue

            addresses_have_same_city = len(set([address.city.lower() for address in addresses])) == 1

            if not addresses or len(addresses) == 1:
                break
            elif (results[Match.Type.CITY] and (results[Match.Type.CITY_PART] or results[Match.Type.PARTIAL_CITY])) or results[Match.Type.CITY_PART] and not addresses_have_same_city:
                choices = Address.sort_cities_by_alphabetical_order(Address.extract_cities([address for address in addresses if address.match_state in (Match.Type.CITY, Match.Type.CITY_PART)], full_city=True))
                Completion.do_city_completion.choices = choices

                Address.city_choice_print(choices, search)
            elif results[Match.Type.CITY] or addresses_have_same_city:
                return (Completion.State.STREET_NAME_COMPLETION)
            else:
                if not search:
                    Address.city_matching_print(Address.sort_cities_by_recurrence(Address.extract_cities(addresses, size=1)))
                else:
                    Address.city_matching_print(Address.sort_cities_by_recurrence(results['matches']), size=len(search))

            return (search)

    def do_street_name_completion(self, addresses, city, search):
        if hasattr(Completion.do_street_name_completion, 'choices'):
            choices = Completion.do_street_name_completion.choices

            if search[-1].isnumeric() and int(search[-1]) in range(1, len(choices) + 1):
                choice = choices[int(search[-1]) - 1]

                for address in list([address for address in addresses if str(address).lower() != choice.lower()]):
                    addresses.remove(address)

                return (Completion.State.FINISHED)
            elif not search[-1].isnumeric():
                delattr(Completion.do_street_name_completion, 'choices')
            else:
                Address.street_name_choice_print(choices, search)

                return (search[:len(search) - 1])
        while True:
            results = {'matches': [], Match.Type.STREET_NAME: [], Match.Type.STREET_NAME_PART: {}, Match.Type.PARTIAL_STREET_NAME: []}

            for address in list(addresses):
                matchr = address.match_with_criteria(search, Match.Type.STREET_NAME)

                if matchr['state'] != Match.Type.UNKNOWN:
                    for match in matchr['match']:
                        results['matches'].append(match)

                    if matchr['state'] in (Match.Type.STREET_NAME, Match.Type.PARTIAL_STREET_NAME):
                        results[matchr['state']].append(address)
                    elif matchr['match'] in results[Match.Type.STREET_NAME_PART]:
                        results[Match.Type.STREET_NAME_PART][matchr['match']].append(address)
                    else:
                        results[Match.Type.STREET_NAME_PART][matchr['match']] = [address]
                elif address in addresses:
                    addresses.remove(address)

            if results['matches']:
                search, supdated = self.autocomplete_search(set(results['matches']), search)

                if supdated:
                    continue

            all_addresses_have_same_stname = len(set([address.street_name.lower() for address in addresses])) == 1

            if not addresses or len(addresses) == 1:
                break
            elif (results[Match.Type.STREET_NAME] and (results[Match.Type.STREET_NAME_PART] or results[Match.Type.PARTIAL_STREET_NAME])) or results[Match.Type.STREET_NAME_PART] or all_addresses_have_same_stname:
                addresses = Address.sort_addresses_by_alphanumeric_order([address for address in addresses if address.match_state in (Match.Type.STREET_NAME, Match.Type.STREET_NAME_PART)])
                Completion.do_street_name_completion.choices = addresses

                Address.street_name_choice_print(addresses, search)
            elif results[Match.Type.STREET_NAME] and not all_addresses_have_same_stname:
                return (Completion.State.FINISHED)
            else:
                if not search:
                    Address.street_name_matching_print(city, Address.sort_cities_by_recurrence(Address.extract_street_names(addresses, size=1)))
                else:
                    Address.street_name_matching_print(city, Address.sort_cities_by_recurrence(results['matches']), size=len(search))

            return (search)


    def do_completion(self):
        def _rprint(address):
            print ('=> %s' % str(address))

        addresses = self.addresses_dictionnary

        if len(addresses) == 1:
            return (_rprint(addresses[0]))

        states = [Completion.State.CITY_COMPLETION]
        city = None
        search = ''

        k = -1
        while True:
            k += 1

            input = '' if not k else sys.stdin.readline().rstrip('\n')

            if input == ABORT:
                break
            else:
                for ch in list(input):
                    search += ch

                while True:
                    completion = None

                    if states[-1] == Completion.State.CITY_COMPLETION:
                        completion = self.do_city_completion(addresses, search)
                    elif states[-1] == Completion.State.STREET_NAME_COMPLETION:
                        completion = self.do_street_name_completion(addresses, city, search)

                    if len(addresses) == 1:
                        return (_rprint(addresses[0]))
                    elif not addresses:
                        Completion.quit_unknown_address()

                    if isinstance(completion, int):
                        city = addresses[0].city
                        search = ''

                        states.append(completion)

                        continue
                    elif isinstance(completion, str):
                        search = completion

                    break
