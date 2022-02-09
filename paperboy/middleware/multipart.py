"""Copied from https://github.com/yohanboniface/falcon-multipart due to conda-forge issues.

MIT License

Copyright (c) 2017 Yohan Boniface

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from io import BytesIO
import falcon
import cgi


class Parser(cgi.FieldStorage):
    pass


class MultipartMiddleware(object):
    def __init__(self, parser=None):
        self.parser = parser or Parser

    def parse(self, stream, environ):
        return self.parser(fp=stream, environ=environ)

    def parse_field(self, field):
        if isinstance(field, list):
            return [self.parse_field(subfield) for subfield in field]

        # When file name isn't ascii FieldStorage will not consider it.
        encoded = field.disposition_options.get("filename*")
        if encoded:
            # http://stackoverflow.com/a/93688
            encoding, filename = encoded.split("''")
            field.filename = filename
            # FieldStorage will decode the file content by itself when
            # file name is encoded, but we need to keep a consistent
            # API, so let's go back to bytes.
            # WARNING we assume file encoding will be same as filename
            # but there is no guaranty.
            field.file = BytesIO(field.file.read().encode(encoding))
        if getattr(field, "filename", False):
            return field
        # This is not a file, thus get flat value (not
        # FieldStorage instance).
        return field.value

    def process_request(self, req, resp, **kwargs):

        if "multipart/form-data" not in (req.content_type or ""):
            return

        # This must be done to avoid a bug in cgi.FieldStorage.
        req.env.setdefault("QUERY_STRING", "")

        # To avoid all stream consumption problem which occurs in falcon 1.0.0
        # or above.
        stream = req.stream.stream if hasattr(req.stream, "stream") else req.stream
        try:
            form = self.parse(stream=stream, environ=req.env)
        except ValueError as e:  # Invalid boundary?
            raise falcon.HTTPBadRequest("Error parsing file", str(e))

        for key in form:
            # TODO: put files in req.files instead when #418 get merged.
            req._params[key] = self.parse_field(form[key])
