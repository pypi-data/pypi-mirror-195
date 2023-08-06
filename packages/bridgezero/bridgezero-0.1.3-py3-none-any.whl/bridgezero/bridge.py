# -*- coding: utf-8 -*-

class Bridge:
    """
        class that provides basic constants for bridge game
    """
    def getPlayersList(self):
        return ['N', 'E', 'S', 'W']

    def getPlayersCount(self):
        if not hasattr(self, 'PLAYERS_COUNT'):
            self.PLAYERS_COUNT = len(self.getPlayersList())
        return self.PLAYERS_COUNT


    def getCardColorsList(self):
        return ['S', 'H', 'D', 'C']

    def getCardValuesList(self):
        return ['A', 'K', 'Q', 'J', 'T'] + [str(x) for x in range(9,1,-1)]

    def getTotalCardsCount(self):
        return len(self.getCardColorsList()) * len(self.getCardValuesList())

    def getHandCardsCount(self):
        return  self.getTotalCardsCount() / self.getPlayersCount()


    def getBidColorsList(self):
        return ['C', 'D', 'H', 'S', 'NT']

    def getBidColorsCount(self):
        return len(self.getBidColorsList())

    def getBidValuesList(self):
        return [str(x) for x in range(1, 8)]

    def getBidValuesCount(self):
        return len(self.getBidValuesList())

    def getColorOrNtBidsList(self):
        bidsList = []
        for level in self.getBidValuesList():
            for color in self.getBidColorsList():
                bidsList.append(level + color)
        return bidsList

    def getOtherBidsList(self):
        return ["PASS", "DBL", "RDBL"]

    def getAllBidsList(self):
        return self.getColorOrNtBidsList() + self.getOtherBidsList()

    def getAllBidsCount(self):
        return len(self.getAllBidsList())


bridge = Bridge()

BRIDGE_PLAYERS_LIST = bridge.getPlayersList()
BRIDGE_PLAYERS_COUNT = bridge.getPlayersCount()

BRIDGE_CARD_COLORS_LIST = bridge.getCardColorsList()
BRIDGE_CARD_VALUES_LIST = bridge.getCardValuesList()
BRIDGE_CARD_VALUES_COUNT = len(BRIDGE_CARD_VALUES_LIST)
BRIDGE_TOTAL_CARDS_COUNT = bridge.getTotalCardsCount()
BRIDGE_HAND_CARD_COUNT = bridge.getHandCardsCount()

BRIDGE_BID_COLORS_LIST = bridge.getBidColorsList()
BRIDGE_BID_COLORS_COUNT = bridge.getBidColorsCount()
BRIDGE_BID_VALUES_LIST = bridge.getBidValuesList()
BRIDGE_BID_VALUES_COUNT = bridge.getBidValuesCount()

BRIDGE_COLOR_OR_NT_BIDS_LIST = bridge.getColorOrNtBidsList()
BRIDGE_OTHER_BIDS_LIST = bridge.getOtherBidsList()
BRIDGE_ALL_BIDS_LIST = bridge.getAllBidsList()
BRIDGE_ALL_BIDS_COUNT = bridge.getAllBidsCount()

BRIDGE_RANK_VALID_DEALS_COUNT = 1000  # a priori
BRIDGE_TABLE_RECOMMENDED_DEALS_COUNT = 200



BRIDGE_HCP_A = 4
BRIDGE_HCP_K = 3
BRIDGE_HCP_Q = 2
BRIDGE_HCP_J = 1



BRIDGE_TRAINING_SET_SIZE = 10000 # probably it will be increased (comment added, when it was 100)

BRIDGE_PENALTY_FOR_ILLEGAL_BID = 10000 # obsolete


# contract values

BRIDGE_BASE_TRICK_NUMBER_TO_TAKE = 6

BRIDGE_UNSUCCESSFUL_DBL_PENALTY = 50
BRIDGE_SUCCESSFUL_RDBL_BONUS = 100

BRIDGE_FIRST_TRICK_VALUE = {'C':20, 'D':20, 'H':30, 'S':30, 'NT':40}
BRIDGE_NEXT_TRICK_VALUE = {'C':20, 'D':20, 'H':30, 'S':30, 'NT':30}

BRIDGE_PART_GAME_BONUS = 50

BRIDGE_GAME_VALUE = 100 # points to make a game
BRIDGE_GAME_BONUS = {False: 300, True: 500}

BRIDGE_SMALL_SLAM_TRICKS = 12
BRIDGE_SMALL_SLAM_BONUS = {False: 500, True: 750}

BRIDGE_BIG_SLAM_TRICKS = 13
BRIDGE_BIG_SLAM_BONUS = {False: 1000, True: 1500}


BRIDGE_DOUBLED_OVERTRICKS_VALUE = {False: 100, True: 200}

BRIDGE_UNDERTRICK = {False: 50, True: 100}

BRIDGE_FIRST_UNDERTRICK_DBL = {False: 100, True: 200}
BRIDGE_FIRST_UNDERTRICK_RDBL = {False: 200, True: 400}

BRIDGE_NEXT_UNDERTRICK_DBL = {False: 200, True: 300}
BRIDGE_NEXT_UNDERTRICK_RDBL = {False: 400, True: 600}

BRIDGE_ADDITIONAL_FOURTH_UNDERTRICK_DBL = {False: 100, True: 200}





BRIDGE_MILTON_NV = {20:0, 21:50, 22:90, 23:130, 24:220, 25:300, 26:400, 27:430, 28:460, 29:490, 30:520, 31:700, 32:900, 33:990, 34:1250, 35:1400, 36:1500, 37:1500, 38:1500, 39:1500, 40:1500}
BRIDGE_MILTON_VU = {20:0, 21:50, 22:90, 23:130, 24:260, 25:400, 26:600, 27:630, 28:660, 29:690, 30:720, 31:1000, 32:1350, 33:1440, 34:1800, 35:2100, 36:2200, 37:2200, 38:2200, 39:2200, 40:2200}




UNDERTRICK_PENALTY_COEFFICIENT = 0.1