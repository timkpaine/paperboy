"""Copied from https://github.com/lwcolton/falcon-cors due to conda-forge issues.


                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "{}"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright {yyyy} {name of copyright owner}

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import logging
import re
from falcon import HTTP_METHODS


def get_default_logger(level=None):
    logger = logging.getLogger("falcon_cors")
    logger.setLevel(logging.INFO)
    logger.propogate = False
    if not logger.handlers:
        handler = logging.StreamHandler()
        logger.addHandler(handler)
    return logger


class CORSMiddleware:
    """This is the middleware that applies a CORS object to requests.
    Args:
        cors (CORS, required): An instance of :py:class:`~falcon.cors.CORS`.
        default_enabled (bool, optional): Whether CORS processing should
            take place for every resource.  Default ``True``.
    """

    def __init__(self, cors, default_enabled=True):
        self.cors = cors
        self.default_enabled = default_enabled

    def process_resource(self, req, resp, resource, *args):
        if not getattr(resource, "cors_enabled", self.default_enabled):
            return
        cors = getattr(resource, "cors", self.cors)
        cors.process(req, resp, resource)


class CORS(object):
    """
    Initialize a CORS object, passing in configuration options.
    All of the configuration settings are optional, however if none
    of them are specified the default configuration will simply
    deny all CORS requests.  You can pass this to
    :py:class:`~falcon.api.API` for a global configuration.
    After enabling globally, you can override the settings for a
    particular resource by setting the 'cors' attribute on it to
    an instance of this class.
    Args:
        logger(:py:meth:`logging.Logger`, optional):
            Specifies the logger to use.  A basic logger and StreamHandler
            will be configure for you if none is provided.
        allow_all_origins(bool, optional): Specifies whether CORS
            should allow requests from all origins.  Default is ``False``.
        allow_origins_list(list, optional): A list of
            origins that are allowed to make CORS requests.  Default is empty.
        allow_origins_regex(str, optional): A string containing
            a Python regular expression that matches origins which
            are allowed to make CORS requests.  Default is ``None``.
        allow_all_headers(bool, optional):  If ``True``, when the server is
            responding to a preflight request it will approve any headers
            requested by the client via the Access-Control-Request-Headers
            header, setting each requested header in the
            value of the Access-Control-Allow-Headers header in the response.
            Default is ``False``.
        allow_headers_list(list, optional): A list of headers which are
            allowed values for the Access-Control-Allow-Headers header
            in response to a preflight request.  When the server is
            responding to a preflight request, it will check each header
            requested by the client in the Access-Control-Request-Headers
            header to see if it exists in this list.  If it does, it
            will be included in the Access-Control-Allow-Headers header
            in the response to the preflight request.
            Default is empty.
        allow_headers_regex(str, optional): A string containing a Python
            regular expression that matches headers that should be
            allowed in response to a preflight request.  If this is set,
            when a preflight request is received by the server, it will
            try to match each header requested by the client via the
            Access-Control-Request-Headers header of the request.  If
            the requested header is matched by this regex, it will be
            included in the value of the Access-Control-Allow-Headers
            header of the response.
        expose_headers_list(list, optional): A list of headers that
            should be sent as values to the Access-Control-Expose-Headers
            header in response to simple or actual requests.
        allow_all_methods(bool, optional): Specifies whether all methods
            are allowed via CORS requests.  Default is ``False``.
        allow_methods_list(list, optional): A list of methods which are
            allowed via CORS requests. These should be values from
            ``falcon.HTTP_METHODS``, which are strings like 'GET' and 'PATCH'.
            Default is empty.
        allow_credentials_all_origins(bool, optional): Where or not the
            Access-Control-Allow-Credentials should be set to True
            and set on all responses.  Default is ``False``.
        allow_credentials_origins_list(list, optional): A list of
            origins for which the Access-Control-Allow-Credentials
            header should be set to True and included with all
            responses.  Default is empty.
        allow_credentials_origins_regex(string, optional): A string
            containing a Python regular expression matching origins
            for which the Access-Control-Allow-Credentials header
            should be set to True and included in all responses.
            Default is ``None``.
        max_age(int, optional): If set to an integer, this value
            will be used as the value of the Access-Control-Max-Age
            header in response to preflight requests.  This is
            in seconds the maximum amount of time a client may cache
            responses to preflight requests.
            Default is ``None`` (no header sent).
    Note:
        The arguments above are inclusie, meaning a header, origin, or method
        will only be disallowed if it doesn't match ANY specification.
        First the allow_all directive is checked, then the list directive,
        then the regex directive if applicable, then list by method if applicable,
        and lastly regex by method if applicable.  For instance, this means if
        you specify 'Auth-Key' in allow_headers_list, it will be allowed for all
        methods regardless of the values in header_list_By_method.
    Note:
        Headers are converted to lower-case for you.
        Methods are converted to upper-case for you.
        Take note of this if you are writing regular expressions.
    Note:
        The allow_headers_* settings relate to the Access-Control-Allow-Headers
        header which is only sent in response to pre-flight requests.
        This is different from the Access-Control-Expose-Headers header which
        is set via the expose_headers_list setting and is sent only in response
        to basic or actual requests.
    Warning:
        Exercise caution when using the regex enabled settings.  It is very
        easy to misunderstand Python regex syntax and accidentally
        introduce an unintentionally allowed origin or other vulnerability
        into your application.
    """

    def __init__(self, **cors_config):
        default_cors_config = {
            "logger": get_default_logger(),
            "log_level": None,
            "allow_all_origins": False,
            "allow_origins_list": [],
            "allow_origins_regex": None,
            "allow_all_headers": False,
            "allow_headers_list": [],
            "allow_headers_regex": None,
            "expose_headers_list": [],
            "allow_all_methods": False,
            "allow_methods_list": [],
            "allow_credentials_all_origins": False,
            "allow_credentials_origins_list": [],
            "allow_credentials_origins_regex": None,
            "max_age": None,
        }
        for cors_setting, setting_value in default_cors_config.items():
            cors_config.setdefault(cors_setting, setting_value)

        unknown_settings = list(
            set(cors_config.keys()) - set(default_cors_config.keys())
        )
        if unknown_settings:
            raise ValueError("Unknown CORS settings: {0}".format(unknown_settings))

        self.logger = cors_config["logger"]
        if cors_config["log_level"] is not None:
            level = logging.getLevelName(cors_config["log_level"])
            self.logger.setLevel(level)

        unknown_methods = list(
            set(cors_config["allow_methods_list"]) - set(HTTP_METHODS)
        )
        if unknown_methods:
            raise ValueError(
                "Unknown methods specified for "
                "allow_methods_list: {0}".format(unknown_methods)
            )

        self._compile_keys(
            cors_config,
            [
                "allow_origins_regex",
                "allow_headers_regex",
                "allow_credentials_origins_regex",
            ],
        )

        cors_config["allow_methods_list"] = [
            method.upper() for method in cors_config["allow_methods_list"]
        ]

        for header_list_key in ["allow_headers_list", "expose_headers_list"]:
            cors_config[header_list_key] = [
                header.lower() for header in cors_config[header_list_key]
            ]

        # We need to detect if we support credentials, if we do
        # we cannot set Access-Control-Allow-Origin to *
        self.supports_credentials = False
        for credentials_key in [
            "allow_credentials_all_origins",
            "allow_credentials_origins_list",
            "allow_credentials_origins_regex",
        ]:
            if cors_config[credentials_key]:
                self.supports_credentials = True
        self.logger.debug("supports_credentials: {0}".format(self.supports_credentials))

        # Detect if we need to send 'Vary: Origin' header
        # This needs to be set if any decisions about which headers to send
        # are being made based on the Origin header the client sends
        self.origins_vary = False
        if cors_config["allow_all_origins"]:
            for vary_origin_config_key in [
                "allow_credentials_origins_list",
                "allow_credentials_origins_regex",
            ]:
                if cors_config[vary_origin_config_key]:
                    self.origins_vary = True

        self.logger.debug("origins_vary {0}".format(self.origins_vary))

        self._cors_config = cors_config

    def _compile_keys(self, settings_dict, keys):
        for key in keys:
            if settings_dict[key] is not None:
                settings_dict[key] = re.compile(settings_dict[key])

    @property
    def middleware(self):
        """A property which returns a CORSMiddleware instance"""
        return CORSMiddleware(self)

    def process(self, req, resp, resource):
        # Comments in this section will refer to sections of the W3C
        # specification for CORS, most notably 6.1.X and 6.2.X which are
        # list of steps a server should take when responding to CORS
        # requests   http://www.w3.org/TR/cors/# resource-processing-model
        # According to the spec, it is OK for steps to take place out of
        # order, as long as the end result is indistinguishable from the
        # reference algorithm specified in the W3C document.  (Section 2)
        # For efficiency and code structure, some steps may take place
        # out of order, although we try our best to stick to the order
        # of steps specified in Section 6.1 and 6.2

        # We must always set 'Vary: Origin' even if the Origin header is not set,
        # Otherwise cache servers in front of the app (e.g. varnish) will cache
        # this response
        if self.origins_vary:
            self._set_vary_origin(resp)

        origin = req.get_header("origin")
        # 6.1.1
        # 6.2.1
        if not origin:
            self.logger.debug("Aborting response due to no origin header")
            return

        # 6.1.2
        # 6.1.3 (Access-Control-Allow-Origin)
        # 6.2.2
        # 6.2.7 (Access-Control-Allow-Origin)
        if not self._process_origin(req, resp, origin):
            self.logger.info("Aborting response due to origin not allowed")
            return

        # Basic or actual request
        if req.method != "OPTIONS":
            self.logger.debug("Processing basic or actual request")
            # 6.1.3 (Access-Control-Allow-Credentials)
            self._process_credentials(req, resp, origin)

            # 6.1.4
            self._process_expose_headers(req, resp)
        # Preflight request
        else:
            self.logger.debug("Processing preflight request")
            request_method = req.get_header("access-control-request-method")
            # 6.2.3
            if not request_method:
                self.logger.info(
                    "Aborting response due to no access-control-request-method header"
                )
                return

            # 6.2.4
            requested_header_list = self._get_requested_headers(req)

            # 6.2.5
            # 6.2.9
            if not self._process_methods(req, resp, resource):
                self.logger.info("Aborting response due to unallowed method")
                return

            # 6.2.6
            # 6.2.10
            if not self._process_allow_headers(req, resp, requested_header_list):
                self.logger.info("Aborting response due to unallowed headers")
                return

            # 6.2.7 (Access-Control-Allow-Credentials)
            self._process_credentials(req, resp, origin)

            # 6.2.8
            self._process_max_age(req, resp)

    def _process_origin(self, req, resp, origin):
        """Inspects the request and adds the Access-Control-Allow-Origin
        header if the requested origin is allowed.
        Returns:
            ``True`` if the header was added and the requested origin
            is allowed, ``False`` if the origin is not allowed and the
            header has not been added.
        """
        if self._cors_config["allow_all_origins"]:
            if self.supports_credentials:
                self._set_allow_origin(resp, origin)
            else:
                self._set_allow_origin(resp, "*")
            return True

        if origin in self._cors_config["allow_origins_list"]:
            self._set_allow_origin(resp, origin)
            return True

        regex = self._cors_config["allow_origins_regex"]
        if regex is not None:
            if regex.match(origin):
                self._set_allow_origin(resp, origin)
                return True

        return False

    def _process_allow_headers(self, req, resp, requested_headers):
        """Adds the Access-Control-Allow-Headers header to the response,
        using the cors settings to determine which headers are allowed.
        Returns:
            True if all the headers the client requested are allowed.
            False if some or none of the headers the client requested are allowed.
        """
        if not requested_headers:
            return True
        elif self._cors_config["allow_all_headers"]:
            self._set_allowed_headers(resp, requested_headers)
            return True

        approved_headers = []
        for header in requested_headers:
            if header.lower() in self._cors_config["allow_headers_list"]:
                approved_headers.append(header)
            elif self._cors_config.get("allow_headers_regex"):
                if self._cors_config["allow_headers_regex"].match(header):
                    approved_headers.append(header)

        if len(approved_headers) == len(requested_headers):
            self._set_allowed_headers(resp, approved_headers)
            return True

        return False

    def _process_methods(self, req, resp, resource):
        """Adds the Access-Control-Allow-Methods header to the response,
        using the cors settings to determine which methods are allowed.
        """
        requested_method = self._get_requested_method(req)
        if not requested_method:
            return False

        if self._cors_config["allow_all_methods"]:
            allowed_methods = self._get_resource_methods(resource)
            self._set_allowed_methods(resp, allowed_methods)
            if requested_method in allowed_methods:
                return True
        elif requested_method in self._cors_config["allow_methods_list"]:
            resource_methods = self._get_resource_methods(resource)
            # Only list methods as allowed if they exist
            # on the resource AND are in the allowed_methods_list
            allowed_methods = [
                method
                for method in resource_methods
                if method in self._cors_config["allow_methods_list"]
            ]
            self._set_allowed_methods(resp, allowed_methods)
            if requested_method in allowed_methods:
                return True

        return False

    def _get_resource_methods(self, resource):
        allowed_methods = []
        for method in HTTP_METHODS:
            if hasattr(resource, "on_" + method.lower()) or resource is None:
                allowed_methods.append(method)
        return allowed_methods

    def _process_credentials(self, req, resp, origin):
        """Adds the Access-Control-Allow-Credentials to the response
        if the cors settings indicates it should be set.
        """
        if self._cors_config["allow_credentials_all_origins"]:
            self._set_allow_credentials(resp)
            return True

        if origin in self._cors_config["allow_credentials_origins_list"]:
            self._set_allow_credentials(resp)
            return True

        credentials_regex = self._cors_config["allow_credentials_origins_regex"]
        if credentials_regex:
            if credentials_regex.match(origin):
                self._set_allow_credentials(resp)
                return True

        return False

    def _process_expose_headers(self, req, resp):
        for header in self._cors_config["expose_headers_list"]:
            resp.append_header("access-control-expose-headers", header)

    def _process_max_age(self, req, resp):
        if self._cors_config["max_age"]:
            resp.set_header("access-control-max-age", self._cors_config["max_age"])

    def _get_requested_headers(self, req):
        headers = []
        raw_header = req.get_header("access-control-request-headers")
        if raw_header is None:
            return headers
        for requested_header in raw_header.split(","):
            requested_header = requested_header.strip()
            if requested_header:
                headers.append(requested_header)
        return headers

    def _get_requested_method(self, req):
        return req.get_header("access-control-request-method")

    def _set_allow_origin(self, resp, allowed_origin):
        resp.set_header("access-control-allow-origin", allowed_origin)

    def _set_allowed_headers(self, resp, allowed_header_list):
        for allowed_header in allowed_header_list:
            resp.append_header("access-control-allow-headers", allowed_header)

    def _set_allowed_methods(self, resp, allowed_methods):
        for method in allowed_methods:
            resp.append_header("access-control-allow-methods", method)

    def _set_allow_credentials(self, resp):
        resp.set_header("access-control-allow-credentials", "true")

    def _set_vary_origin(self, resp):
        resp.append_header("vary", "origin")
