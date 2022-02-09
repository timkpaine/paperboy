import os
import os.path
from six.moves.urllib_parse import urljoin
from datetime import datetime
from traitlets import HasTraits, Unicode, Instance, Bool
from .forms import Response, FormEntry, DOMEntry
from .base import Base, _REPORT_TYPES, _OUTPUT_TYPES
from .notebook import NotebookConfig
from .job import JobConfig


TEMPLATE_BASEPATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "worker", "nbconvert_templates")
)


def _type_to_template(output, strip_code):
    """select correct nbconvert template for type"""
    if output in ("pdf", "html"):
        ret = output
        if output == "pdf":
            ret += ".tplx"
        else:
            ret += ".tpl"
        return ret
    elif output == "email":
        ret = "html_email"
        ret += ".tpl"
        return ret
    else:
        return ""


class ReportMetadataConfig(HasTraits):
    """Paperboy configuration object representing a Report (metadata component)"""

    notebook = Instance(NotebookConfig)
    job = Instance(JobConfig)

    username = Unicode()
    userid = Unicode()

    run = Instance(datetime)
    parameters = Unicode()
    type = Unicode()
    output = Unicode()
    strip_code = Bool()

    template = Unicode()

    run = Instance(datetime, allow_none=True)
    created = Instance(datetime)
    modified = Instance(datetime)

    def to_json(self, include_notebook=False):
        """Convert ReportMetadata to a JSON"""
        ret = {}
        ret = {}
        ret["notebook"] = self.notebook.name
        if include_notebook:
            ret["notebook_text"] = self.notebook.meta.notebook
        # ret['notebookid'] = self.notebook.id

        ret["job"] = self.job.name
        # ret['jobid'] = self.job.id

        ret["parameters"] = self.parameters
        ret["type"] = self.type
        ret["output"] = self.output
        ret["strip_code"] = self.strip_code

        ret["template"] = self.template or os.path.join(
            TEMPLATE_BASEPATH, _type_to_template(self.output, self.strip_code)
        )

        if self.run:
            ret["run"] = self.run.strftime("%m/%d/%Y %H:%M:%S")
        else:
            ret["run"] = "not run"
        ret["created"] = self.created.strftime("%m/%d/%Y %H:%M:%S")
        ret["modified"] = self.modified.strftime("%m/%d/%Y %H:%M:%S")

        return ret

    @staticmethod
    def from_json(jsn):
        """Create ReportMetadata from a JSON"""
        ret = ReportMetadataConfig()
        for k, v in jsn.items():
            if k in ("created", "modified", "run"):
                ret.set_trait(k, datetime.strptime(v, "%m/%d/%Y %H:%M:%S"))
            else:
                ret.set_trait(k, v)
        return ret


class ReportConfig(Base):
    """Paperboy configuration object representing a Report"""

    name = Unicode()
    id = Unicode()
    meta = Instance(ReportMetadataConfig)

    def to_json(self, include_notebook=False):
        """Convert Report to a JSON"""
        ret = {}
        ret["name"] = self.name
        ret["id"] = self.id
        ret["meta"] = self.meta.to_json(include_notebook)
        return ret

    def form(self):
        """Generate Form template for client from a Report object"""
        f = Response()
        f.entries = [
            FormEntry(
                name="name",
                type="text",
                label="Name",
                placeholder="Name for Report...",
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
                name="job",
                type="autocomplete",
                label="Job",
                url=urljoin(self.config.apiurl, "autocomplete?type=jobs&partial="),
                required=True,
            ),
            FormEntry(
                name="parameters",
                type="textarea",
                label="Parameters",
                placeholder="JSON Parameters...",
            ),
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
                name="code",
                type="select",
                label="Strip Code",
                options=["yes", "no"],
                required=True,
            ),
            FormEntry(name="template", type="text", label="Template", required=False),
            FormEntry(
                name="submit",
                type="submit",
                value="save",
                url=urljoin(self.config.apiurl, "reports?action=save"),
            ),
        ]
        return f.to_json()

    @staticmethod
    def from_json(jsn, config):
        """Create Report from a JSON"""
        ret = ReportConfig(config)
        ret.name = jsn["name"]
        ret.id = jsn["id"]
        ret.meta = ReportMetadataConfig.from_json(jsn["meta"])
        ret.meta.notebook = NotebookConfig(config)
        ret.meta.job = JobConfig(config)
        return ret

    def edit(self):
        """Generate Edit template for client from a Report object"""
        f = Response()
        f.entries = [
            FormEntry(
                name="name",
                type="text",
                value=self.name,
                label="Name",
                placeholder="Name for Report...",
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
                name="job name",
                type="text",
                value=self.meta.job.name,
                label="Job",
                required=True,
                readonly=True,
            ),
            FormEntry(
                name="job",
                type="text",
                value=self.meta.job.id,
                required=True,
                readonly=True,
                hidden=True,
            ),
            FormEntry(
                name="parameters",
                type="textarea",
                value=self.meta.parameters,
                label="Parameters",
                placeholder="JSON Parameters...",
            ),
            FormEntry(
                name="type",
                type="select",
                value=self.meta.type,
                label="Type",
                options=_REPORT_TYPES,
                required=True,
            ),
            FormEntry(
                name="output",
                type="select",
                value=self.meta.output,
                label="Output",
                options=_OUTPUT_TYPES,
                required=True,
            ),
            FormEntry(
                name="code",
                type="select",
                value="yes" if self.meta.strip_code else "no",
                label="Strip Code",
                options=["yes", "no"],
                required=True,
            ),
            FormEntry(
                name="save",
                type="submit",
                value="save",
                url=urljoin(self.config.apiurl, "reports?action=save"),
            ),
            FormEntry(
                name="delete",
                type="submit",
                value="delete",
                url=urljoin(self.config.apiurl, "reports?action=delete"),
            ),
        ]
        return f.to_json()

    def entry(self):
        """Generate ListTable entry for client from a Report object"""
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
            DOMEntry(name="job", type="label", value=self.meta.job.name, label="Job"),
            DOMEntry(
                name="parameters",
                type="json",
                value=self.meta.parameters,
                label="Parameters",
            ),
            DOMEntry(name="type", type="label", value=self.meta.type, label="Type"),
            DOMEntry(
                name="output", type="label", value=self.meta.output, label="Output"
            ),
            DOMEntry(
                name="strip_code",
                type="label",
                value=str(self.meta.strip_code),
                label="Strip Code",
            ),
            DOMEntry(
                name="template",
                type="label",
                value=self.meta.template,
                label="Template",
            ),
            # DOMEntry(type='label', value=self.meta.run, label='Run'),
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
                url=urljoin(self.config.apiurl, "reports?action=delete"),
            ),
        ]
        return f.to_json()

    def store(self):
        """Generate response modal for client when saving a Report object"""
        ret = Response()
        ret.entries = [
            DOMEntry(type="h2", value="Success!"),
            DOMEntry(
                type="p", value="Successfully configured report: {}!".format(self.name)
            ),
            DOMEntry(type="p", value="Notebook: {}".format(self.meta.notebook.name)),
            DOMEntry(type="p", value="Job: {}".format(self.meta.job.name)),
        ]
        return ret.to_json()
