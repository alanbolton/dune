
class Troops :
    def __init__(self, round, owner, tokens, fedaykins):
        self.round_placed = round
        self.owner = owner
        self.tokens = tokens
        self.fedaykins = fedaykins
        self.peaceful = False
        if owner == 'Emperor' or owner == 'Fremen':
            self.include_fedaykins = True
        else:
            self.include_fedaykins = False

    def __str__(self):
        if False == self.peaceful:
            ret_str = 'tokens: {} fedaykins: {} placed in round: {} by {}\n'.format(self.tokens, \
                                                                                    self.fedaykins,\
                                                                                    self.round_placed,
                                                                                    self.owner)
        else:
            ret_str = 'tokens: {} fedaykins: {} placed in round: {} by {} who is peaceful\n'.format(self.tokens, \
                                                                                                    self.fedaykins,\
                                                                                                    self.round_placed,
                                                                                                    self.owner)

        return ret_str

    def troops_update(self, tokens, fedaykins):
        self.tokens = tokens
        self.fedaykins = fedaykins

    def troops_peaceful_set(self, im_peaceful):
        self.peaceful = im_peaceful

    def troops_get_total_number(self):
        return (self.tokens + self.fedaykins)

    def troops_get_num_of_tokens(self):
        return self.tokens

    def troops_get_num_of_fedaykins(self):
        return self.fedaykins

def beam_troops(reserve, round, owner, tokens, fedaykins):
    #cap the request to be the maximum number currently in reserves
    if tokens > reserve.tokens:
        tokens = reserve.tokens
    if fedaykins > reserve.fedaykins:
        fedaykins = reserve.fedaykins
    troops = Troops(round, owner, tokens, fedaykins)
    reserve.tokens -= tokens
    reserve.fedaykins -= fedaykins
    return troops