"""
Minimal dependency to broken data-gathering consent from users. 

Libraries can depend on `consent_broker` to request whether a user agrees to data gathering. 

Frontends can depends on `consent_broker` to see whether some libraries are requesting consent, prompt users, and update
the consent database if possible.
"""

__version__ = "0.0.1"

import json


from collections import namedtuple
from pathlib import Path
from datetime import datetime, timedelta


class Broker:
    CONF = Path("~").expanduser() / ".consent_broker.json"

    def now():
        return datetime.now()

    def _load(self):
        if self.CONF.exists():
            return json.loads(self.CONF.read_text())
        return {}

    def _save(self, data):
        self.CONF.touch(exist_ok=True)
        self.CONF.write_text(json.dumps(data, indent=2))

    def request_consent_to_collect(self, library: str):
        """
        Does the user consent for the data to be collected ?

        Note that by default consent is valid only for 90 days.


        Parameters
        ----------
        library : str
            current library, we request consent for

        Return
        ------
        True|False|None:
            True if explict consent, False if explicit refusal.
            None if not set yet or expired.

        """

        data = self._load()
        this_lib = data.get(library, {})
        time = this_lib.get("timestamp", 0)
        then = datetime.fromtimestamp(time)
        _now = self.now()
        value = this_lib.get("value", None)
        if value is False:
            return False
        if then + timedelta(days=90) < _now:
            data.setdefault(library, {"timestamp": _now.timestamp()})
            self._save(data)
            return None

        return value

    def set_consent_to_collect(self, library, value):
        data = self._load()
        _now = self.now()
        data.setdefault(library, {})
        data[library]["value"] = value
        data[library]["timestamp"] = _now.timestamp()
        self._save(data)

    def need_consent(self):
        data = self._load()
        nc = []
        _now = self.now()
        for name, lib in data.items():
            val = lib.get("value", None)
            when = datetime.fromtimestamp(lib.get("timestamp", 0))
            if (val is None) or ((val is True) and (when + timedelta(days=90) < _now)):
                nc.append(name)
        return nc


broker = Broker()


set_consent_to_collect = broker.set_consent_to_collect
request_consent_to_collect = broker.request_consent_to_collect
need_consent = broker.need_consent
CONF = broker.CONF
