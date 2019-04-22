
from .book import BookViewModel


class TradeInfo(object):
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self._parse(goods)

    def _parse(self, goods):
        self.total = len(goods)
        self.trades = [self._map_to_trade(single) for single in goods]

    @staticmethod
    def _map_to_trade(single):
        return dict(
            user_name=single.user.nickname,
            time=single.create_datetime.strftime('%Y-%m-%d') or '未知',
            id=single.id
        )


class MyTrades(object):
    def __init__(self, trades_of_min, trade_count_list):
        self.trades = []
        self._trades_of_min = trades_of_min
        self._trade_count_list = trade_count_list

        self.trades = self._parse()

    def _parse(self):
        temp_trades = []
        for trade in self._trades_of_min:
            my_trade = self._matching(trade)
            temp_trades.append(my_trade)
        return temp_trades

    def _matching(self, trade):
        count = 0
        for trade_count in self._trade_count_list:
            if trade.isbn == trade_count['isbn']:
                count = trade_count['count']
        r = {
            'wishes_count': count,
            'book': BookViewModel(trade.book),
            'id': trade.id
        }
        return r
