import datetime
import itertools
import re
import html
import time
import humanize

from chans import chans


def html2text(htm, newline=False):
    ret = html.unescape(htm)
    ret = ret.translate({8209: ord('-'), 8220: ord('"'), 8221: ord('"'), 160: ord(' '),})
    ret = re.sub(r"\s", " ", ret, flags = re.MULTILINE)
    if newline:
        ret = re.sub("<br>|<br />|</p>|</div>|</h\d>", '\n', ret, flags = re.IGNORECASE)
    else:
        ret = re.sub("<br>|<br />|</p>|</div>|</h\d>", ' ', ret, flags = re.IGNORECASE)
    ret = re.sub('<.*?>', ' ', ret, flags=re.DOTALL)
    ret = re.sub(r"  +", " ", ret)
    return ret


def try_till_success(f, maxtrials=None):
    it = itertools.count()
    if maxtrials: it = itertools.islice(it, maxtrials)
    for trial in it:
        try:
            out = f()
        except:
            print(f'{trial} failed, sleep 2 seconds and retry...')
            time.sleep(2)
        else:
            return out


def get_threads():
    threads = try_till_success(lambda: list(itertools.chain(
        chans.Ch2.boards_threads(),
        chans.Ch4.boards_threads(),
    )))
    return threads or []
    # for trial in itertools.count():
    #     try:
    #         threads = list(itertools.chain(
    #             boards_threads(_4ch.board_threads, _4ch.boards),
    #             boards_threads(_2ch.board_threads, _2ch.boards),
    #         ))
    #     except:
    #         print(f'bad JSON, trial {trial}, sleep 2 seconds and retry...')
    #         time.sleep(2)
    #     else:
    #         return threads


def color(v):
    if   v <   5: c = 236
    elif v <  10: c = 237
    elif v <  15: c = 238
    elif v <  20: c = 239
    elif v <  25: c = 240
    elif v <  30: c = 241
    elif v <  35: c = 242
    elif v <  40: c = 243
    elif v <  45: c = 244
    elif v <  50: c = 245
    elif v <  55: c = 246
    elif v <  60: c = 247
    elif v <  65: c = 248
    elif v <  70: c = 249
    elif v <  75: c = 250
    elif v <  80: c = 251
    elif v <  85: c = 252
    elif v <  90: c = 253
    elif v <  95: c = 254
    elif v < 100: c = 255
    elif v < 200: c = 82  # green
    elif v < 300: c = 87  # blue
    elif v < 400: c = 226 # yellow
    elif v < 500: c = 208 # orange
    elif v>= 500: c = 196 # red
    return c

class color_string:
    BLACK     = lambda s: '\033[30m' + str(s) + '\033[0m'
    RED       = lambda s: '\033[31m' + str(s) + '\033[0m'
    GREEN     = lambda s: '\033[32m' + str(s) + '\033[0m'
    YELLOW    = lambda s: '\033[33m' + str(s) + '\033[0m'
    BLUE      = lambda s: '\033[34m' + str(s) + '\033[0m'
    MAGENTA   = lambda s: '\033[35m' + str(s) + '\033[0m'
    CYAN      = lambda s: '\033[36m' + str(s) + '\033[0m'
    WHITE     = lambda s: '\033[37m' + str(s) + '\033[0m'
    UNDERLINE = lambda s: '\033[4m'  + str(s) + '\033[0m'


def color_i(s, i):
    return f"\x1b[38;5;{i}m{s}\033[0m"


def to_local_time(dt: datetime.datetime, timezone: datetime.timezone):
    if dt.tzinfo is not None:
        raise ValueError('pass timezone as separate argument')
    dt = dt.replace(tzinfo=timezone)
    return datetime.datetime.fromtimestamp(dt.timestamp())


def format_time(
    t: datetime.datetime | int,
    absolute: bool = False,
    pad: bool = False,
    timezone: datetime.timezone | None = None,
) -> str:
    if isinstance(t, int):
        t = datetime.datetime.fromtimestamp(t)
    if timezone is not None:
        t = to_local_time(t, timezone)
    if absolute or (datetime.datetime.utcnow() - t).days > 30:  # noqa: PLR2004
        return t.strftime('%Y %b %d %H:%M')
    t = datetime.datetime.fromtimestamp(t.timestamp())
    out = humanize.naturaltime(t)
    if pad:
        out = out.rjust(17)
    return out
