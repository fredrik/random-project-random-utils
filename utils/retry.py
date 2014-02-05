import time

def retry(ExceptionToCheck, try_limit=4, start_delay=3, max_delay=None, backoff=2):
    """Retry calling the decorated function using an exponential backoff.

    modified version of: http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        excpetions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    """
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtry_limit = try_limit or float('inf')
            mdelay = start_delay
            max_delay_reached = False
            if max_delay:
                if mdelay >= max_delay:
                    max_delay_reached = True
            tries = 0
            try_one_last_time = True
            while tries < mtry_limit:
                try:
                    return f(*args, **kwargs)
                    try_one_last_time = False
                    break
                except ExceptionToCheck:
                    time.sleep(mdelay)
                    tries += 1
                    if not max_delay_reached:
                        mdelay *= backoff
                        if max_delay:
                            mdelay = min(mdelay, max_delay)
                        if mdelay == max_delay:
                            max_delay_reached = True
            if try_one_last_time:
                return f(*args, **kwargs)
            return
        return f_retry  # true decorator
    return deco_retry
