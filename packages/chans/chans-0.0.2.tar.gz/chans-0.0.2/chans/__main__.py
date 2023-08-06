import time
import random
import difflib
import shutil
import pipe21 as P
from chans import util
from chans.util import color_string
from chans.util import color_i
from chans import chans
from chans import util


def main():
    while True:
        threads = (
            util.get_threads()
            | P.Filter(lambda thread: thread['lifetime_seconds'] < 60 * 60 * 1.5)
            | P.Pipe(list)
            | P.ApplyInplace(random.shuffle)
        )

        for i, thread in enumerate(threads, start=1):
            title = thread['title']
            title = util.html2text(title, newline=True)
            posts_count = thread['posts_count']
            sleep_time = round(-12 * 0.7 ** (0.03 * posts_count) + 12, 1)

            title_color = util.color(posts_count)
            derivative = int(posts_count/thread['lifetime_seconds'] * 1000)


            print('{:<14} {:<10} {} {:>10} {:>18} {:>10} {}'.format(
                color_string.YELLOW(f'{i}..{len(threads)}'),
                color_string.BLUE(f"{thread['board']:<4}"),
                posts_count and f'⬆ {derivative:<4}' or '',
                color_string.WHITE(f"{posts_count:>4} comments"),
                util.format_time(thread['timestamp']),
                color_string.CYAN(f'{sleep_time} sleep'),
                thread['url'],
            ))


            if comment := thread.get('comment'):
                comment = util.html2text(comment, newline=True)

                nospace_title   = [c for c in title   if not c.isspace()]
                nospace_comment = [c for c in comment if not c.isspace()]
                min_len = min(len(nospace_title), len(nospace_comment))

                ratio = difflib.SequenceMatcher(lambda x: x.isspace(), nospace_title[:min_len], nospace_comment[:min_len]).ratio()

                if ratio < 0.7:
                    print(color_i(title, title_color))
                print(color_i(comment[:500], title_color))
            else:
                print(color_i(title, title_color))

            t0 = time.time()
            for viral_comment, count in {'4ch': chans.Ch4, '2ch': chans.Ch2}[thread['chan']].viral_comments(thread, 3, min_replies=5):
                print(color_string.WHITE(f'[{count} replies]'), end=' ')
                print(color_i(viral_comment, title_color))

            print(color_i('─'*shutil.get_terminal_size().columns, 236))
            time.sleep(max(sleep_time - (time.time() - t0), 0))

if __name__ == '__main__':
    main()
