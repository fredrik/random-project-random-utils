import json
import requests
from requests_oauthlib import OAuth1

from django.conf import settings

from scores import logging


logger = logging.getLogger('utils.twitter')


class NotFoundException(Exception):
    pass


def screen_name_lookup(screen_names):
    """
    Takes an iterable of screen names,
    returns a dict of screen name to user id.

    Raises TwitterException if anything goes wrong.
    """
    url = 'https://api.twitter.com/1.1/users/lookup.json'
    screen_names = list(screen_names)
    oauth = OAuth1(
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET
    )
    response = requests.get(
        url,
        auth=oauth,
        params={"screen_name": screen_names}
    )

    if response.status_code == 404:
        raise NotFoundException('404')

    response.raise_for_status()

    users = json.loads(response.text)

    if not len(users) == len(screen_names):
        logger.warning(u"expected payload to have same length as input: %d v %d",
            len(users), len(screen_names)
        )

    lookup = {}

    for user in users:
        lookup[user.get(u'screen_name')] = user.get(u'id')

    return lookup


if __name__ == '__main__':
    from pprint import pprint
    screen_names = set(['mollerstrand', 'johtso', 'crowdscores'])
    pprint(screen_name_lookup(screen_names))
