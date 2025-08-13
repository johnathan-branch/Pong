def singleton(cls):
    """
    This method is intended to be used as a class decorator for enforcing the decorated class to behave as a singleton.
    Init method is only invoked once, no matter how many times the instance is referenced.  
    """
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls.__new__(cls)  # manually create instance
            cls.__init__(instances[cls], *args, **kwargs)  # run init once
        return instances[cls]
    return get_instance