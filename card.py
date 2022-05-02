class Card:
    def __init__(self, name, suit) -> None:
        self.name_value = name
        self.name = f'{name if isinstance(name, int) else name[0]}{suit[0]}'
        self.suit = suit
        self.full_name = f'{name} of {suit}'
        
        