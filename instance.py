import HLD as bts


class SharedInstance():
    instance = None


def shared_HLD_instance():
    """ This method will initialize ``SharedInstance.instance`` and return it.
        The purpose of this method is to have offer single default
        HLD instance that can be reused by multiple classes.
    """
    if not SharedInstance.instance:
        clear_cache()
        SharedInstance.instance = bts.HLD()
    return SharedInstance.instance


def set_shared_HLD_instance(HLD_instance):
    """ This method allows us to override default HLD instance for all users of
        ``SharedInstance.instance``.

        :param HLD.HLD.HLD HLD_instance: HLD instance
    """
    clear_cache()
    SharedInstance.instance = HLD_instance


def clear_cache():
    """ Clear Caches
    """
    from .blockchainobject import BlockchainObject
    BlockchainObject.clear_cache()
