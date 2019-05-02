
from enum import Enum


class PendingStatus(Enum):
    Waiting = 1
    Success = 2
    Reject = 3
    Redraw = 4
    Connection=5

    @classmethod
    def pending_str(cls, status, key):
        key_map = {
            cls.Waiting: {
                'requester': '等待对方同意',
                'gifter': '等待你同意'
            },
            cls.Reject: {
                'requester': '对方已拒绝',
                'gifter': '你已拒绝'
            },
            cls.Redraw: {
                'requester': '你已撤销',
                'gifter': '对方已撤销'
            },
            cls.Success: {
                'requester': '对方已同意',
                'gifter': '你已同意'
            },
            cls.Connection:{
                'requester':"对方已收到书",
                'gifter':'交易完成'
            }

        }
        return key_map[status][key]
