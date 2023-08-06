import requests
import datetime
import collections
import re
from chans import util

from chans.chans.base import Chan


class Ch2(Chan):
    boards = 'news', 'po', 'b'

    @classmethod
    def board_threads(cls, board):
        threads = requests.get(f'https://2ch.hk/{board}/catalog.json').json()['threads']
        for thread in threads:
            thread['board'] = board
            id_ = thread['num']
            thread['id'] = id_
            thread['url'] = f"https://2ch.hk/{board}/res/{id_}.html"
            thread = cls.mapper(thread)
        return threads

    @classmethod
    def mapper(cls, thread):
        now = datetime.datetime.now()
        # thread['comment'] =
        # thread['title'] = thread['subject']
        thread['title'] = util.html2text(thread['subject'])
        # title = html.escape(title)
        # title       = util.html2text(title)
        # thread['title'] = thread['comment']#[:100]
        thread['lifetime_seconds'] = (now - datetime.datetime.fromtimestamp(thread['timestamp'])).total_seconds()
        thread['chan'] = '2ch'
        return thread

    @classmethod
    def viral_comments(cls, thread, top_k=None, min_replies=None):
        json_url = f"https://2ch.hk/{thread['board']}/res/{thread['id']}.json"
        T = util.try_till_success(lambda: requests.get(json_url).json()['threads'][0]['posts'], maxtrials=3)
        if not T: return []

        quotes = collections.Counter()

        for t in T:
            com = t['comment']
            q = map(int, set(re.findall(r'(?<=#)\d+(?=" class="post-reply-link")', com)))
            quotes.update(q)

        t0 = T[0]['num']
        most_quoted = {k: v for k, v in quotes.most_common(top_k + 1) if v >= min_replies}
        if t0 in most_quoted:
            del most_quoted[t0]

        for t in T:
            if count := most_quoted.get(t['num']):
                yield util.html2text(t['comment'], newline=False), count
