from six.moves.urllib_parse import urljoin
from datetime import datetime
from traitlets import HasTraits, Unicode, Int, Instance, validate, TraitError
from .forms import Response, FormEntry, DOMEntry
from .base import Base, _INTERVAL_TYPES, _OUTPUT_TYPES, _REPORT_TYPES, _SERVICE_LEVELS
from .notebook import NotebookConfig


class JobMetadataConfig(HasTraits):
    """Paperboy configuration object representing a Job (metadata component)"""

    notebook = Instance(NotebookConfig)
    username = Unicode()
    userid = Unicode()

    start_time = Instance(datetime)
    interval = Unicode()
    level = Unicode()

    @validate("interval")
    def _validate_interval(self, proposal):
        if proposal["value"] not in _INTERVAL_TYPES:
            raise TraitError("Unrecognized type : {}".format(proposal["value"]))
        return proposal["value"]

    reports = Int()
    created = Instance(datetime)
    modified = Instance(datetime)

    def to_json(self, include_notebook=False):
        """Convert JobMetadata to a JSON"""
        ret = {}
        ret["notebook"] = self.notebook.name
        if include_notebook:
            ret["notebook_text"] = self.notebook.meta.notebook
        # ret['notebookid'] = self.notebook.id
        ret["interval"] = self.interval
        ret["level"] = self.level
        ret["reports"] = self.reports
        ret["created"] = self.created.strftime("%m/%d/%Y %H:%M:%S")
        ret["modified"] = self.modified.strftime("%m/%d/%Y %H:%M:%S")
        return ret

    @staticmethod
    def from_json(jsn):
        """Create JobMetadata from a JSON"""
        ret = JobMetadataConfig()
        for k, v in jsn.items():
            if k in ("created", "modified"):
                ret.set_trait(k, datetime.strptime(v, "%m/%d/%Y %H:%M:%S"))
            else:
                ret.set_trait(k, v)
        return ret


class JobConfig(Base):
    """Paperboy configuration object representing a Job"""

    name = Unicode()
    id = Unicode()
    meta = Instance(JobMetadataConfig)

    def to_json(self, include_notebook=False):
        """Convert Job to a JSON"""
        ret = {}
        ret["name"] = self.name
        ret["id"] = self.id
        ret["meta"] = self.meta.to_json(include_notebook)
        return ret

    def form(self):
        """Generate Form template for client from a Job object"""
        f = Response()
        f.entries = [
            FormEntry(
                name="name",
                type="text",
                label="Name",
                value=self.name,
                placeholder="Name for Job...",
                required=True,
            ),
            FormEntry(
                name="notebook",
                type="autocomplete",
                label="Notebook",
                url=urljoin(self.config.apiurl, "autocomplete?type=notebooks&partial="),
                required=True,
            ),
            FormEntry(
                name="starttime",
                type="datetime",
                label="Start Time/Date",
                required=True,
            ),
            FormEntry(
                name="interval",
                type="select",
                label="Interval",
                options=_INTERVAL_TYPES,
                required=True,
            ),
            FormEntry(
                name="level",
                type="select",
                label="Level",
                options=_SERVICE_LEVELS,
                required=True,
            ),
            FormEntry(
                name="autogen",
                type="checkbox",
                label="Autogenerate reports",
                value="true",
                required=False,
            ),
            FormEntry(
                name="parameters_inline",
                type="textarea",
                label="Papermill params (.jsonl)",
                placeholder="Upload file or type here...",
                required=False,
            ),
            FormEntry(
                name="parameters",
                type="file",
                label="Papermill params (.jsonl)",
                required=False,
            ),
            FormEntry(name="options", type="label", label="Report options"),
            FormEntry(
                name="type",
                type="select",
                label="Type",
                options=_REPORT_TYPES,
                required=True,
            ),
            FormEntry(
                name="output",
                type="select",
                label="Output",
                options=_OUTPUT_TYPES,
                required=True,
            ),
            FormEntry(
                name="strip_code",
                type="select",
                label="Strip Code",
                options=["yes", "no"],
                required=True,
            ),
            FormEntry(
                name="submit",
                type="submit",
                value="save",
                url=urljoin(self.config.apiurl, "jobs?action=save"),
            ),
        ]
        return f.to_json()

    @staticmethod
    def from_json(jsn, config):
        """Create Job from a JSON"""
        ret = JobConfig(config)
        ret.name = jsn["name"]
        ret.id = jsn["id"]
        ret.meta = JobMetadataConfig.from_json(jsn["meta"])
        ret.meta.notebook = NotebookConfig(config)  # FIXME
        return ret

    def edit(self):
        """Generate Edit template for client from a Job object"""
        f = Response()
        f.entries = [
            FormEntry(
                name="name",
                type="text",
                value=self.name,
                label="Name",
                placeholder="Name for Job...",
                required=True,
            ),
            FormEntry(name="id", type="text", value=self.id, label="Id", hidden=True),
            FormEntry(
                name="notebook name",
                type="text",
                value=self.meta.notebook.name,
                label="Notebook",
                required=True,
                readonly=True,
            ),
            FormEntry(
                name="notebook",
                type="text",
                value=self.meta.notebook.id,
                required=True,
                readonly=True,
                hidden=True,
            ),
            FormEntry(
                name="starttime",
                value=self.meta.start_time.strftime("%Y-%m-%dT%H:%M"),
                type="datetime",
                label="Start Time/Date",
                required=True,
            ),
            FormEntry(
                name="interval",
                type="select",
                value=self.meta.interval,
                label="Interval",
                options=_INTERVAL_TYPES,
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
                name="reports", type="text", value=str(self.meta.reports), readonly=True
            ),
            FormEntry(
                name="save",
                type="submit",
                value="save",
                url=urljoin(self.config.apiurl, "jobs?action=save"),
            ),
            FormEntry(
                name="delete",
                type="submit",
                value="delete",
                url=urljoin(self.config.apiurl, "jobs?action=delete"),
            ),
        ]
        return f.to_json()

    def entry(self):
        """Generate ListTable entry for client from a Job object"""
        f = Response()
        f.entries = [
            DOMEntry(name="name", type="label", value=self.name, label="Name"),
            DOMEntry(name="id", type="label", value=self.id, label="Id", hidden=True),
            DOMEntry(
                name="notebook",
                type="label",
                value=self.meta.notebook.name,
                label="Notebook",
            ),
            DOMEntry(
                name="interval",
                type="label",
                value=self.meta.interval,
                label="Interval",
            ),
            DOMEntry(name="level", type="label", value=self.meta.level, label="Level"),
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
                url=urljoin(self.config.apiurl, "jobs?action=delete"),
            ),
        ]
        return f.to_json()

    def store(self):
        """Generate response modal for client when saving a Job object"""
        ret = Response()
        ret.entries = [
            DOMEntry(type="h2", value="Success!"),
            DOMEntry(
                type="p", value="Successfully configured job: {}".format(self.name)
            ),
            DOMEntry(type="p", value="Notebook: {}".format(self.meta.notebook.name)),
        ]
        if self.meta.reports:
            ret.entries.append(
                DOMEntry(type="p", value="Reports: {}".format(self.meta.reports))
            )
        return ret.to_json()
