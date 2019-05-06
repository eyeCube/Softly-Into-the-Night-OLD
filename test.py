class I:
    a=0
    def __init__(self):
        self.a=self.get_a()
    def __hash__(self):
        return self.a
    def __eq__(self, other):
        return id(self) == id(other)
    def get_a(self):
        I.a += 1
        return I.a

i1=I()
i2=I()

r = {}
r.update({i1 : 'a'})
r.update({i2 : 'b'})

print(r)
for k,v in r.items():
    print(k,v)
