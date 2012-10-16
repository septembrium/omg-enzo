# just a test
class TrainRide:
    def __init__(self, duration):
        self.duration = duration
        self.feet = 0
        self.tows = 0

    def get_on_train(self, people):
        self.feet = people * 2
        def calc_tows():
            tn = range(0,10)
            for i in tn:
                yield 1 # yeah silly
        for i in range(0, self.feet):
            for t in calc_tows():
                self.tows += t

    def puts(self):
        print("feet: " + str(self.feet) + " tows: " + str(self.tows))

class LovelyCouple:
    def __init__(self, him="alex", her="blanka", sparks=5):
       self.him = him
       self.her = her
       self.sparks = sparks

if __name__ == "__main__":
    # a test
    tr = TrainRide(20)
    tr.puts()
    tr.get_on_train(5)
    tr.puts()
    # another test
    lc = LovelyCouple(her="mariette", sparks=1000, him="eddy")
    print(lc.him)
    print(lc.her)
    print(lc.sparks)
