class myDecorator(object):

    def __init__(self, f):
        self.f = f

    def __call__(self):
        print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        self.f()
        print "-----------------------------------"

@myDecorator
def aFunction():
    print "My original function."

aFunction()
