from items import Player, ZhangXuefeng


zhang = ZhangXuefeng()
you = Player()


def lead_distance(player=None, opponent=None):
    player = player or you
    opponent = opponent or zhang
    return int(player.distance - opponent.distance)


def win_lose(player=None, opponent=None):
    player = player or you
    opponent = opponent or zhang
    lead = lead_distance(player, opponent)

    if lead >= 3000 and opponent.portal:
        return True, "你居然杀到地狱来了？！"
    if lead >= 3000:
        return True, "不可能，绝对不可能！"
    if lead <= -3000 and opponent.portal:
        return False, "你都这样了，为什么不去报土木呢？"
    if lead <= -3000:
        return False, "我就说你跑不过我吧！"
    return None, ""
