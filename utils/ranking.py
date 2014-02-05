def rankify(things, attr):
    """
    Returns a generator of (thing, rank) for each thing in things.
    Assumes that things are sorted in decending order.
    """
    previous_thing = None
    previous_rank = None
    counter = 0
    for thing in things:
        counter += 1
        if not previous_thing or thing[attr] != previous_thing[attr]:
            rank = counter
            previous_rank = rank
        else:
            rank = previous_rank
        previous_thing = thing
        yield thing, rank
