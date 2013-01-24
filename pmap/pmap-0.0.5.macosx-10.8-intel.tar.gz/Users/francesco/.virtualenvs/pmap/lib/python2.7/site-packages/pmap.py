from threading import Thread, Event, activeCount

def mapper(f, arg, l, index, thread_terminated):
        l[index]= f(arg)
        thread_terminated.set()

def pmap(f, l, limit = None):
    """A parallel version of map, that preserves ordering.
    Example:
    >>> pmap(lambda x: x*x, [1,2,3])
    [1, 4, 9]
    >>> import time
    >>> t1 = time.clock()
    >>> null = pmap(lambda x: time.sleep(1), range(10), 3)
    >>> time.clock() - t1 > 0.001
    True
    """
    thread_terminated = Event()
    pool=[]
    res = range(len(l))
    for i in range(len(l)):
        t = Thread(target = mapper, args = (f, l[i], res, i,
                                            thread_terminated))
        pool.append(t)
        if limit and activeCount() > limit:
            thread_terminated.wait()
            thread_terminated.clear()

        t.start()
    map (lambda x:x.join(), pool)
    return res
