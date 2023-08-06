import bridgezero.bridge


def test1():
    assert bridgezero.bridge.BRIDGE_PLAYERS_LIST == ['N', 'E', 'S', 'W']


def test2():
    bridge = bridgezero.bridge.Bridge()
    assert bridge.getPlayersList() == ['N', 'E', 'S', 'W']
