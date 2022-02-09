import gunicorn.app.base
from gunicorn.six import iteritems


class FalconGunicorn(gunicorn.app.base.BaseApplication):
    """Utility to deploy falcon.API on gunicorn"""

    def __init__(self, app, options=None):
        """Constructor
        Args:
            app (falcon.API): a routed falcon API
            options (dict): a set of options for gunicorn (e.g. workers, port, etc)
        """
        self.options = options or {}
        self.application = app
        super(FalconGunicorn, self).__init__()

    def load_config(self):
        config = dict(
            [
                (key, value)
                for key, value in iteritems(self.options)
                if key in self.cfg.settings and value is not None
            ]
        )
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
