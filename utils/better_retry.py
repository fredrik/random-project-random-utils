#!/usr/bin/env python

# Copyright 2012 by Jeff Laughlin Consulting LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import itertools


def better_retry(max_tries=None, start_delay=1, backoff=2,
                 exceptions=(Exception,), hook=None):
    """Function decorator implementing retrying logic.

    max_tries: Maximum number of times to retry before raising exception;
               defaults to None (Keep retrying indefinitely)
    start_delay: Sleep this many seconds * backoff * try number after failure
    backoff: Multiply delay by this factor after each failure
    exceptions: A tuple of exception classes; default (Exception,)
    hook: A function with the signature hook(try_count, exception, delay);

    The decorator will call the function up to max_tries times if it raises
    an exception.

    By default it catches instances of the Exception class and subclasses.
    This will recover after all but the most fatal errors. You may specify a
    custom tuple of exception classes with the 'exceptions' argument; the
    function will only be retried if it raises one of the specified
    exceptions.

    Additionally you may specify a hook function which will be called prior
    to retrying with the current try count the exception instance and the
    delay length in seconds. This is primarily intended to give the
    opportunity to log the failure. Hook is not called after failure if no
    retries remain.
    """
    def dec(func):
        def f2(*args, **kwargs):
            delay = start_delay
            for try_count in itertools.count(1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if max_tries is None or try_count < max_tries:
                        if hook:
                            hook(try_count, e, delay)
                        time.sleep(delay)
                        delay = delay * backoff
                    else:
                        raise
        return f2
    return dec
