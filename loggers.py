class Logger():
    def info(self, msg, **kwargs):
        pass

    def warning(self, msg, **kwargs):
        pass

    def error(self, msg, **kwargs):
        pass

class StdLogger(Logger):
    def info(self, msg, **kwargs):
        print(msg, **kwargs)

    def warning(self, msg, **kwargs):
        print(msg, **kwargs)

    def error(self, msg, **kwargs):
        print(msg, **kwargs)
