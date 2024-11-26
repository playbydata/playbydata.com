
__all__ = ('BaseDataSourceClient',)


class BaseDataSourceClient(object):
    """"""
    def __str__(self):
        return self.__class__.__name__

    @property
    def client(self):
        raise NotImplementedError
