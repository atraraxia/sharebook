
from app.helper.enums import PendingStatus


class DriftCollection(object):
    def __init__(self, drifts, current_user_id):
        self.data = []
        self._parse(drifts, current_user_id)

    def _parse(self, drifts, current_user_id):
        for drift in drifts:
            temp = DriftViewModel(drift, current_user_id)
            self.data.append(temp.data)


class DriftViewModel(object):
    def __init__(self, drift, current_user_id):
        self.data = {}
        self.data = self._parse(drift, current_user_id)

    @staticmethod
    def requester_or_gifter(drift, current_user_id):
        if drift.requester_id == current_user_id:
            you_are = 'requester'
            operator = drift.requester_nickname
        else:
            you_are = 'gifter'
            operator = drift.gifter_nickname
        return you_are, operator

    def _parse(self, drift, current_user_id):
        you_are, operator = self.requester_or_gifter(drift, current_user_id)
        pending_status = PendingStatus.pending_str(drift.pending, you_are)
        r = {
            'you_are': you_are,
            'operator': operator,
            'drift_id': drift.id,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_img': drift.book_img,
            'date': drift.create_datetime.strftime('%Y-%m-%d'),
            'message': drift.message,
            'address': drift.address,
            'recipient_name': drift.recipient_name,
            'mobile': drift.mobile,
            'status': drift.pending,
            'status_str': pending_status,
        }
        return r
