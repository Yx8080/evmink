#例如 {p:"bsc-20","op":"mint","tick":"bnbi","amt":"5000"}
class Tick:
    def __init__(self, data):
        self.p = data.get("p")
        self.op = data.get("op")
        self.tick = data.get("tick")
        self.amt = data.get("amt")