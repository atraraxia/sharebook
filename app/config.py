from flask_script import Option
from flask_script import Server
from flask_script.commands import ShowUrls

__all__ = ['SubServer', 'SubShowUrls']


class SubServer(Server):
    help = description = 'Runs the Flask development server i.e. app.run()'

    def __init__(self, sub_app, host='127.0.0.1', port=5000, use_debugger=None,
                 use_reloader=None, threaded=False, processes=1,
                 passthrough_errors=False, **options):
        super(SubServer, self).__init__(host,
                                        port,
                                        use_debugger,
                                        use_reloader,
                                        threaded,
                                        processes,
                                        passthrough_errors,
                                        **options)
        self.sub_app = sub_app

    def get_options(self):
        options = super(SubServer, self).get_options()

        result = [Option('-s', '--sub',
                         dest='sub',
                         default=self.sub_app)]

        return result + [item for item in options]

    def __call__(self, app, sub, host, port, use_debugger, use_reloader,
                 threaded, processes, passthrough_errors):
        super(SubServer, self).__call__(sub, host, port, use_debugger,
                                        use_reloader, threaded, processes,
                                        passthrough_errors)


class SubShowUrls(ShowUrls):
    def __init__(self, sub, order='rule'):
        super(SubShowUrls, self).__init__(order=order)
        self.sub = sub

    def run(self, url, order):
        current_app = self.sub
        from werkzeug.exceptions import NotFound, MethodNotAllowed

        rows = []
        column_length = 0
        column_headers = ('Rule', 'Endpoint', 'Arguments')

        if url:
            try:
                rule, arguments = current_app.url_map \
                    .bind('localhost') \
                    .match(url, return_rule=True)
                rows.append((rule.rule, rule.endpoint, arguments))
                column_length = 3
            except (NotFound, MethodNotAllowed) as e:
                rows.append(("<%s>" % e, None, None))
                column_length = 1
        else:
            rules = sorted(current_app.url_map.iter_rules(),
                           key=lambda rule: getattr(rule, order))
            for rule in rules:
                rows.append((rule.rule, rule.endpoint, None))
            column_length = 2

        str_template = ''
        table_width = 0

        if column_length >= 1:
            max_rule_length = max(len(r[0]) for r in rows)
            max_rule_length = max_rule_length if max_rule_length > 4 else 4
            str_template += '%-' + str(max_rule_length) + 's'
            table_width += max_rule_length

        if column_length >= 2:
            max_endpoint_length = max(len(str(r[1])) for r in rows)
            # max_endpoint_length = max(rows, key=len)
            max_endpoint_length = max_endpoint_length \
                if max_endpoint_length > 8 else 8
            str_template += '  %-' + str(max_endpoint_length) + 's'
            table_width += 2 + max_endpoint_length

        if column_length >= 3:
            max_arguments_length = max(len(str(r[2])) for r in rows)
            max_arguments_length = max_arguments_length \
                if max_arguments_length > 9 else 9
            str_template += '  %-' + str(max_arguments_length) + 's'
            table_width += 2 + max_arguments_length

        print(str_template % (column_headers[:column_length]))
        print('-' * table_width)

        for row in rows:
            print(str_template % row[:column_length])