import requests

"""
    Data format per card:
    All cards:
        name - name of the card
        color - color to which card belongs
        type  - hero, item, creep, spell, improvement
        icon - to be displayed next to name
        image - URL of a big image representing whole card
        rarity - self explanatory ;)
    Hero:
        stats - dict with following keys holding integer values:
            attack
            armor
            health
        spell - hero's signature spell, represented by dict with following keys
            name - spell's name
            image - URL of spell's image
        abilities - list hero's abilities, represented by entries (dicts) with following keys
            name - ability's name
            image - URL of ability's image
            description - string with description
        illustrator - name of the art creator
"""


class CardDataUnifierArticraft:

    @classmethod
    def unify_card_data(cls, data: list, limit: int = 5) -> list:
        cards = list()

        for item in data:
            if len(cards) == limit:
                break
            cards.append(cls.unify_card(item))

        return cards

    @classmethod
    def unify_card(cls, card_data: dict) -> dict:
        card = dict()

        card['stats'] = dict()
        card['spell'] = dict()
        card['abilities'] = list()

        card['type'] = cls.get_type(card_data)
        card['rarity'] = cls.get_rarity(card_data['rarity'])

        card['name'] = card_data['name']
        card['color'] = card_data['colour']

        if card['color'] == 'item':
            card['color'] = 'dark_gold'

        card['icon'] = card_data['images']['icon']
        card['image'] = card_data['images']['cardArt']

        if 'stats' in card_data:
            card['stats'] = {
                'attack': card_data['stats']['attack'],
                'armor': card_data['stats']['armour'],
                'health': card_data['stats']['health']
            }

        if card['type'] == 'spell':
            card['spell'] = {
                'name': card_data['name'],
                'image': card_data['images']['card']
            }
        elif card['type'] == 'hero':
            card['spell'] = {
                'name': 'To be implemented',
                'image': ''
            }

        if 'abilities' in card_data:
            card['abilities'] = cls.get_abilities(card_data['abilities'])

        card['illustrator'] = card_data['artist']['name']

        return card

    @classmethod
    def get_type(cls, card_data: dict) -> str:
        if card_data['type'] == 'main':
            return card_data['subType']
        else:
            return card_data['type']

    @classmethod
    def get_abilities(cls, items: list) -> list:
        abilities = list()

        for item in items:
            ability = {
                'type': item['type'],
                'name': item['name'],
                'description': item['description'],
                'image': item['image']
            }
            abilities.append(ability)

        return abilities

    @classmethod
    def get_rarity(cls, rarity: int) -> str:
        if rarity == 0:
            return 'no_rarity'
        elif rarity == 1:
            return 'common'
        elif rarity == 2:
            return 'rare'
        else:
            return 'very_rare'
        pass


class CardDataProviderMock:

    @classmethod
    def get_data(cls, partial_name: str = ''):
        mocked_card_data = list()
        mocked_card_data.append(dict())
        mocked_card_data[0]['name'] = 'Mocked Axe'
        mocked_card_data[0]['color'] = 'red'
        mocked_card_data[0]['type'] = 'hero'
        mocked_card_data[0]['icon'] = 'https://steamcdn-a.akamaihd.net/apps/583950/icons/set01/10020.023febd622949d771d9f6a4322efc339ced8c560.png'
        mocked_card_data[0]['image'] = 'https://steamcdn-a.akamaihd.net/apps/583950/icons/set01/10020_large_english.2eabe3c2871aa2ebc94e78033faae2374457292e.png'
        mocked_card_data[0]['rarity'] = 'rare'
        mocked_card_data[0]['stats'] = {'attack': 7, 'armor': 2, 'health': 11}
        mocked_card_data[0]['spell'] = {'name': "Berserker's Call", 'image': 'URL_TO_SPELL'}
        mocked_card_data[0]['abilities'] = [{'name': 'Multicast', 'image': 'URL_TO_ABILITY', 'description': 'After you play a blue spell, there is a 25% chance to put a base copy of that card in to your hand.'}]
        mocked_card_data[0]['illustrator'] = 'Tyler Jacobson'

        return mocked_card_data


class CardDataProviderArticraft:

    @classmethod
    def get_data(cls, partial_name: str, limit: int = 5) -> list:
        r = requests.get('https://api.articraft.io/api/cards/search?search=' + partial_name)
        r.raise_for_status()

        return CardDataUnifierArticraft.unify_card_data(r.json(), limit)
