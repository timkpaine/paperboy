import os
import os.path
from traitlets import HasTraits, Unicode
from ..output import LocalOutput
from ..utils import class_to_name, name_to_class


class OutputConfig(HasTraits):
    """Base class for configuring output"""

    type = Unicode()
    pass


class LocalOutputConfig(OutputConfig):
    """Output report to local filesystem"""

    type = "local"
    dir = Unicode(default_value=os.path.expanduser("~/Downloads"))
    clazz = LocalOutput

    def to_json(self):
        ret = {}
        ret["type"] = self.type
        ret["dir"] = self.dir
        ret["clazz"] = class_to_name(self.clazz)
        ret["config"] = class_to_name(self.__class__)
        return ret

    @staticmethod
    def from_json(jsn):
        ret = LocalOutputConfig()
        ret.type = jsn.get("type")
        ret.dir = jsn.get("dir", ".")
        ret.clazz = name_to_class(jsn.get("clazz"))
        return ret
