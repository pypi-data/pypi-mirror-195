import requests
import itertools
import collections
import re
import datetime
from chans import util
from chans.chans.base import Chan

class Ch4(Chan):
    boards = 'news', 'pol', 'b', 'sci', 'bant', 'trash'


    @classmethod
    def board_threads(cls, board):
        _ = requests.get(f'https://a.4cdn.org/{board}/catalog.json').json()
        _ = (x['threads'] for x in _)
        threads = itertools.chain.from_iterable(_)
        threads = list(threads)
        for thread in threads:
            thread['board'] = board
            id_ = thread['no']
            thread['id'] = id_
            thread['url'] = f"https://boards.4chan.org/{board}/thread/{id_}"
            thread = cls.mapper(thread)
        return threads
    
    @classmethod
    def mapper(cls, thread):
        now = datetime.datetime.now()
        thread['comment'] = thread.get('com')
        thread['title'] = thread.get('sub') or thread['comment'] or 'x' * 70
        thread['timestamp'] = thread['time']
        thread['lifetime_seconds'] = (now - datetime.datetime.fromtimestamp(thread['timestamp'])).total_seconds()
        thread['posts_count'] = thread['replies']
        thread['chan'] = '4ch'
        return thread
    
    @classmethod
    def viral_comments(cls, thread, top_k=None, min_replies=None):
        json_url = f"https://a.4cdn.org/{thread['board']}/thread/{thread['id']}.json"
        T = util.try_till_success(lambda: requests.get(json_url).json()['posts'], maxtrials=3)
        if not T: return []

        quotes = collections.Counter()

        for t in T:
            if com := t.get('com'):
                q = map(int, set(re.findall(r'(?<=href="#p)\d+(?=" class="quotelink")', com)))
                quotes.update(q)

        t0 = T[0]['no']
        most_quoted = {k: v for k, v in quotes.most_common(top_k + 1) if v >= min_replies}
        if t0 in most_quoted:
            del most_quoted[t0]

        for t in T:
            if (count := most_quoted.get(t['no'])) and (com := t.get('com')):
                yield util.html2text(com, newline=False), count
