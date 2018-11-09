from traitlets import List, Int, Unicode, Bool, Instance, HasTraits, validate, TraitError
from .base import Base

_DOM_IMPLEMENTED = ('text', 'select', 'label', 'button', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span')
_FORM_IMPLEMENTED = ('file', 'text', 'select', 'label', 'submit', 'datetime', 'autocomplete', 'checkbox', 'textarea', 'json')


class FormEntry(HasTraits):
    name = Unicode(allow_none=False)
    type = Unicode(default_value='text')

    @validate('type')
    def _validate_type(self, proposal):
        if proposal['value'] not in _FORM_IMPLEMENTED:
            raise TraitError('Unrecognized type : {}'.format(proposal['value']))
        return proposal['value']

    value = Unicode(default_value='')
    label = Unicode(allow_none=True)
    placeholder = Unicode(allow_none=True)
    options = List(default_value=[])
    required = Bool(default_value=False)
    readonly = Bool(default_value=False)
    url = Unicode(allow_none=True)

    def to_json(self):
        ret = {}
        ret['name'] = self.name
        ret['type'] = self.type
        if self.value:
            ret['value'] = self.value
        if self.label:
            ret['label'] = self.label
        if self.placeholder:
            ret['placeholder'] = self.placeholder
        if self.options:
            ret['options'] = self.options
        if self.required:
            ret['required'] = self.required
        if self.readonly:
            ret['readonly'] = self.readonly
        if self.url:
            ret['url'] = self.url
        return ret


class DOMEntry(HasTraits):
    name = Unicode(allow_none=False)
    type = Unicode(default_value='p')

    @validate('type')
    def _validate_type(self, proposal):
        if proposal['value'] not in _DOM_IMPLEMENTED:
            raise TraitError('Unrecognized type : {}'.format(proposal['value']))
        return proposal['value']

    value = Unicode(default_value='')
    label = Unicode(allow_none=True)
    placeholder = Unicode(allow_none=True)
    options = List(default_value=[])
    required = Bool(default_value=False)
    readonly = Bool(default_value=False)

    def to_json(self):
        ret = {}
        ret['name'] = self.type
        ret['type'] = self.type
        if self.value:
            ret['value'] = self.value
        if self.label:
            ret['label'] = self.label
        if self.placeholder:
            ret['placeholder'] = self.placeholder
        if self.options:
            ret['options'] = self.options
        if self.required:
            ret['required'] = self.required
        if self.readonly:
            ret['readonly'] = self.readonly
        return ret

    @staticmethod
    def from_json(jsn):
        ret = DOMEntry()

        for k, v in jsn.items():
            ret.set_trait(k, v)
        return ret


class Response(HasTraits):
    entries = List()

    def to_json(self):
        ret = []
        for entry in self.entries:
            ret.append(entry.to_json())
        return ret


class ListResult(HasTraits):
    page = Int(default_value=1)
    pages = Int(default_value=1)
    count = Int(default_value=1)
    total = Int(default_value=1)
    results = List(trait=Instance(Base))

    def to_json(self):
        ret = {}
        ret['page'] = self.page
        ret['pages'] = self.pages
        ret['count'] = self.count
        ret['total'] = self.total
        ret['results'] = [r.to_json() for r in self.results]
        return ret
