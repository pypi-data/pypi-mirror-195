import abc
import operator
import pipe21 as P


class Chan(abc.ABC):
    
    @classmethod
    @abc.abstractmethod
    def board_threads(cls, board):
        pass
    
    @classmethod
    @abc.abstractmethod
    def mapper(cls, thread):
        pass

    @classmethod
    @abc.abstractmethod
    def viral_comments(cls, thread, top_k, min_replies):
        pass

    @classmethod
    def boards_threads(cls, sortby='posts_count', reverse=True):
        return (
            cls.boards
            | P.FlatMap(cls.board_threads)
            | P.Filter(lambda x: x['lifetime_seconds'] < 60 * 60 * 24 * 1.5) # last number is days
            # | P.Filter(lambda x: x['posts_count'] > 20)
            | P.Sorted(key = operator.itemgetter(sortby), reverse = True)
            | P.Pipe(list)
        )
