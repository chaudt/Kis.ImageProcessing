import logging
class Foo(object):
    def __init__(self) -> None:
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    def __getattribute__(self,name):
        attr = object.__getattribute__(self, name)
        if hasattr(attr, '__call__'):
            def newfunc(*args, **kwargs):
                print('before calling %s' %attr.__name__)
                logging.debug('before calling %s' %attr.__name__)
                result = attr(*args, **kwargs)
                print('done calling %s' %attr.__name__)
                logging.debug('done calling %s' %attr.__name__)
                return result
            return newfunc
        else:
            return attr
        

class Bar(Foo):
    def myFunc(self, data):
        print("myFunc: %s"% data)
        logging.debug("myFunc: %s"% data)



bar = Bar()
bar.myFunc(5)