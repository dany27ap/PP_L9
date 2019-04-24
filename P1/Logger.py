import os

class Log:
    instanta = None
    name = None

    def __init__(self, fname):
        if not Log.instanta:
            Log.name = os.path.dirname(os.path.realpath(__file__)) + '\\' + fname
            print('Log : [' + Log.name + ']')
            Log.instanta = self
            if os.path.isfile(Log.name):
                os.remove(Log.name)
        else:
            raise Exception('Singleton class')

    def write(self, line):
        f = open(self.name, "a+")
        try:
            f.write(line)
            f.write("\n")
        finally:
            f.close()
    @staticmethod
    def get_instanta():
        if not Log.instanta:
            return Log()
        return Log.instanta
