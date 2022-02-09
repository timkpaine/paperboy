from six.moves.urllib_parse import urljoin
from datetime import datetime
from traitlets import HasTraits, Unicode, Int, Instance
from .forms import Response, FormEntry, DOMEntry
from .base import Base, _SERVICE_LEVELS, _PRIVACY_LEVELS


class NotebookMetadataConfig(HasTraits):
    """Paperboy configuration object representing a Notebook (metadata component)"""

    username = Unicode()
    userid = Unicode()

    notebook = Unicode()
    privacy = Unicode()
    level = Unicode()
    requirements = Unicode(allow_none=True, default_value="")
    dockerfile = Unicode(allow_none=True, default_value="")

    jobs = Int()
    reports = Int()

    created = Instance(datetime)
    modified = Instance(datetime)

    def to_json(self, include_notebook=False):
        """Convert NotebookMetadata to a JSON"""
        ret = {}
        ret["username"] = self.username
        # ret['userid'] = self.userid
        if include_notebook:
            ret["notebook"] = self.notebook
        ret["privacy"] = self.privacy
        ret["level"] = self.level
        ret["jobs"] = self.jobs
        ret["reports"] = self.reports
        ret["created"] = self.created.strftime("%m/%d/%Y %H:%M:%S")
        ret["modified"] = self.modified.strftime("%m/%d/%Y %H:%M:%S")
        return ret

    @staticmethod
    def from_json(jsn):
        """Create NotebookMetadata from a JSON"""
        ret = NotebookMetadataConfig()
        for k, v in jsn.items():
            if k in ("created", "modified"):
                ret.set_trait(k, datetime.strptime(v, "%m/%d/%Y %H:%M:%S"))
            else:
                ret.set_trait(k, v)
        return ret


class NotebookConfig(Base):
    """Paperboy configuration object representing a Notebook"""

    name = Unicode()
    id = Unicode()
    meta = Instance(NotebookMetadataConfig)

    def to_json(self, include_notebook=False):
        """Convert Notebook to a JSON"""
        ret = {}
        ret["name"] = self.name
        ret["id"] = self.id
        ret["meta"] = self.meta.to_json(include_notebook)
        return ret

    def form(self):
        """Generate Form template for client from a Notebook object"""
        f = Response()
        f.entries = [
            FormEntry(name="file", type="file", label="File", required=True),
            FormEntry(
                name="name",
                type="text",
                label="Name",
                placeholder="Name for Notebook...",
                required=True,
            ),
            FormEntry(
                name="privacy",
                type="select",
                label="Privacy",
                options=_PRIVACY_LEVELS,
                required=True,
            ),
            FormEntry(
                name="level",
                type="select",
                label="level",
                options=_SERVICE_LEVELS,
                required=True,
            ),
            FormEntry(name="build", type="label", label="Build options"),
            FormEntry(
                name="requirements",
                type="file",
                label="requirements.txt",
                required=False,
            ),
            FormEntry(
                name="dockerfile", type="file", label="Dockerfile", required=False
            ),
            FormEntry(
                name="submit",
                type="submit",
                value="save",
                url=urljoin(self.config.apiurl, "notebooks?action=save"),
            ),
        ]
        return f.to_json()

    @staticmethod
    def from_json(jsn, config):
        """Create Notebook from a JSON"""
        ret = NotebookConfig(config)
        ret.name = jsn.pop("name")
        ret.id = jsn.pop("id")

        if "meta" in jsn:
            ret.meta = NotebookMetadataConfig.from_json(jsn["meta"])
        else:
            ret.meta = NotebookMetadataConfig.from_json(jsn)

        return ret

    def edit(self):
        """Generate Edit template for client from a Notebook object"""
        f = Response()
        f.entries = [
            FormEntry(
                name="name",
                type="text",
                value=self.name,
                placeholder="Name for Job...",
                required=True,
            ),
            FormEntry(name="id", type="text", value=self.id, label="Id", hidden=True),
            FormEntry(
                name="privacy",
                type="select",
                value=self.meta.privacy,
                label="Visibility",
                options=_PRIVACY_LEVELS,
                required=True,
            ),
            FormEntry(
                name="level",
                type="select",
                value=self.meta.level,
                label="Level",
                options=_SERVICE_LEVELS,
                required=True,
            ),
            FormEntry(
                name="notebook",
                type="json",
                value=self.meta.notebook,
                placeholder="Notebook json...",
                required=True,
            ),
        ]

        f.entries.append(
            FormEntry(
                name="requirements",
                type="textarea",
                value=self.meta.requirements,
                label="requirements.txt",
                required=False,
            )
        )
        f.entries.append(
            FormEntry(
                name="dockerfile",
                type="textarea",
                value=self.meta.dockerfile,
                label="Dockerfile",
                required=False,
            )
        )

        f.entries.append(
            FormEntry(
                name="save",
                type="submit",
                value="save",
                url=urljoin(self.config.apiurl, "notebooks?action=save"),
            )
        )
        f.entries.append(
            FormEntry(
                name="delete",
                type="submit",
                value="delete",
                url=urljoin(self.config.apiurl, "notebooks?action=delete"),
            )
        )
        return f.to_json()

    def entry(self):
        """Generate ListTable entry for client from a Notebook object"""
        f = Response()
        f.entries = [
            DOMEntry(name="name", type="label", value=self.name, label="Name"),
            DOMEntry(name="id", type="label", value=self.id, label="Id", hidden=True),
            DOMEntry(
                name="visibility",
                type="label",
                value=self.meta.privacy,
                label="Visibility",
            ),
            DOMEntry(name="level", type="label", value=self.meta.level, label="Level"),
            DOMEntry(
                name="notebook",
                type="ipynb",
                value=self.meta.notebook,
                label="Notebook",
            ),
            DOMEntry(
                name="requirements",
                type="textfile",
                value=self.meta.requirements,
                label="requirements",
            ),
            DOMEntry(
                name="dockerfile",
                type="textfile",
                value=self.meta.dockerfile,
                label="Dockerfile",
            ),
            DOMEntry(
                name="jobs", type="label", value=str(self.meta.jobs), label="Jobs"
            ),
            DOMEntry(
                name="reports",
                type="label",
                value=str(self.meta.reports),
                label="Reports",
            ),
            DOMEntry(
                name="created",
                type="label",
                value=self.meta.created.strftime("%m/%d/%Y %H:%M:%S"),
                label="Created",
            ),
            DOMEntry(
                name="modified",
                type="label",
                value=self.meta.modified.strftime("%m/%d/%Y %H:%M:%S"),
                label="Modified",
            ),
            DOMEntry(
                name="delete",
                type="button",
                value="delete",
                label="delete",
                url=urljoin(self.config.apiurl, "notebooks?action=delete"),
            ),
        ]
        return f.to_json()

    def store(self):
        """Generate response modal for client when saving a Notebook object"""
        ret = Response()
        ret.entries = [
            DOMEntry(type="p", value="Success!"),
            DOMEntry(
                type="p", value="Successfully stored notebook: {}".format(self.name)
            ),
        ]
        return ret.to_json()
