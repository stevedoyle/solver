class A(object):
    def setv(self):
        print('A:setv')

    def run(self):
        self.setv()

class B(A):
    def setv(self):
        print('B:setv')

b = B()
b.run()
