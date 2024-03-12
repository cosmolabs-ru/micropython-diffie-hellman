import uos as os
import ujson as json
from ucryptolib import aes
from uhashlib import sha256
import gc


class DH:
    def __init__(self):
        gc.enable()
        #  P is a 2048-bit (!) safe prime (!) number. Use this one only for testing.
        #  Pick another one from an online calculator for production.
        self.p = 798648912075407625469413199243939164006075016944961303497385979174101504011497028442037444353518892789312882960906842125095599956839938696136483536237476609650413012366432278138858858269510874808691510073356441844744727131172661425405965719311089605482684736989896013573688516061872298449955060294053001705161111352408072259518308331188074955713002948901650943418696683128598681085727768023333345987758696172634447979218316860264469176215587790614800391518787012602889495446751789071684366418760943229286289933546500211984903815614784638453890855497189485625927483154450843710380127870006003324558441924561286106334482964995273845870351970276888164938256885075264744405015957299515737781462821470515216743911207183407628582259737788953020166335103867210297857688087412955536642915583240746516996226829563959044348574106519091566339860037904743125813266822298306210417047951853224195427882291133411520990876170529998380871114401546874830898182896631896300752661167440554588096879682566935835936630838363019880123702547005338915258096304473222949897970414406640891088740201087471853135734607012252988471745129935350554424239794259543444814309146436789739972683800862225206784606248838269640371844365873610774533945800004975227253425859
        #  G is a generator. Pick your own, desirably not bigger than 10, otherwise your MCU may explode.
        self.g = 3
        self.public = 0
        self.secret = 0
        pass

    def load_keypair(self):
        ret = None
        try:
            f = open('dh.json', 'r')  # what if file doesnt exist?
        except:
            print('No DH file.')
            return ret
        else:
            try:
                d = json.loads(f.read())  # what if no JSON inside?
            except:
                print('DH: JSON parsing error.')
                return ret
            else:
                if 'public' in d:  # what if no valid data?
                    self.public = d['public']
                else:
                    return ret
                if 'secret' in d:
                    self.secret = d['secret']
                else:
                    return ret
                del d
                gc.collect()
            f.close()
        pass

    def save_keypair(self):
        if self.public == 0 or self.secret == 0:
            print("DH: SAVE: keypair is not inited. Nothing to save.")
            return
        f = open('dh.json', 'w')
        f.write(json.dumps({'public': self.public, 'secret': self.secret}))
        f.close()
        pass

    def make_keypair(self):
        self.generate_secret_key()
        self.make_public_key()

    def generate_secret_key(self):
        self.secret = int.from_bytes(os.urandom(16), 'big')
        pass

    def make_public_key(self):
        assert self.secret != 0
        self.public = pow(self.g, self.secret, self.p)
        pass

    def make_shared_secret(self, other_public: int):
        assert (self.secret != 0)
        assert (self.public != 0)
        return pow(other_public, self.secret, self.p)
        pass
