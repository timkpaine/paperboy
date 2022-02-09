import base64
import emails
from bs4 import BeautifulSoup
from datetime import datetime
from jupyterlab_email.attachments import CUSTOM_TAG
from six import iteritems
from .base import BaseOutput


def make_email(name, data, from_, type="email", subject="", header="", footer=""):
    """Helper method to convert jupyter notebook into an email

    Args:
        path (str): path to notebook
        model (str): notebook itself (in case deployment strips outputs or
                     notebook not available except through ContentsManager)
        from_ (str): address to send the email from
        type (str): type to convert notebook to
        template (str): template to use when converting notebook
        code (boolean): include input cells in notebook
        subject (str): subject of email
        header (str): html header to inject
        footer (str): html footer to inject
        also_attach (str): also attach pdf/html/both
        postprocessor (function): run postprocessor on soup
    Returns:
        emails.html: HTML Email to send
    """
    if type == "email":
        type_to = "html"
    elif type == "html attachment":
        type_to = "html"
    elif type == "pdf attachment":
        type_to = "pdf"
    else:
        raise Exception("Type not recognized")

    if type == "email":
        soup = BeautifulSoup(data, "html.parser")

        # strip markdown links
        for item in soup.findAll("a", {"class": "anchor-link"}):
            item.decompose()

        # strip matplotlib base outs
        for item in soup.find_all(
            "div", class_="output_text output_subarea output_execute_result"
        ):
            for c in item.contents:
                if "&lt;matplotlib" in str(c):
                    item.decompose()

        # remove dataframe table borders
        for item in soup.findAll("table", {"border": 1}):
            item["border"] = 0
            item["cellspacing"] = 0
            item["cellpadding"] = 0

        # extract imgs for outlook
        imgs = soup.find_all("img")
        imgs_to_attach = {}

        # attach main part
        for i, img in enumerate(imgs):
            if not img.get("localdata"):
                continue
            imgs_to_attach[
                img.get("cell_id") + "_" + str(i) + ".png"
            ] = base64.b64decode(img.get("localdata"))
            img["src"] = "cid:" + img.get("cell_id") + "_" + str(i) + ".png"
            # encoders.encode_base64(part)
            del img["localdata"]

        attaches = soup.find_all(CUSTOM_TAG)
        att_to_attach = {}

        # attach custom attachments
        for i, att in enumerate(attaches):
            if not att.get("localdata"):
                continue
            filename = att.get("filename")
            if (
                filename.endswith(".png")
                or filename.endswith(".xls")
                or filename.endswith(".xlsx")
                or filename.endswith(".pdf")
            ):
                att_to_attach[filename] = base64.b64decode(att.get("localdata"))
            else:
                att_to_attach[filename] = att.get("localdata")
            att.decompose()

        # attach header/footer
        if header or footer:
            head = soup.find("div", {"class": "header"})
            foot = soup.find("div", {"class": "footer"})
            head.append(BeautifulSoup(header, "html.parser"))
            foot.append(BeautifulSoup(footer, "html.parser"))

        # assemble email soup
        soup = str(soup)
        message = emails.html(
            charset="utf-8", subject=subject, html=soup, mail_from=from_
        )

        for img, data in iteritems(imgs_to_attach):
            message.attach(filename=img, content_disposition="inline", data=data)

        for att, data in iteritems(att_to_attach):
            message.attach(filename=att, content_disposition="inline", data=data)

        return message

    message = emails.html(
        subject=subject,
        html="<html>Attachment: %s.%s</html>" % (name, type_to),
        mail_from=from_,
    )
    message.attach(filename=name + "." + type_to, data=data)
    return message


def email(message, to, username, password, domain, host, port):
    """Email a given message using smtp server details
    Args:
        to (str): who to send notebook to
        username (str): email account username
        password (str): email account password
        domain (str): email account provider
        host (str): smtp host
        port (str): smtp port
    """
    r = message.send(
        to=to,
        smtp={
            "host": host,
            "port": port,
            "ssl": True,
            "user": username,
            "password": password,
        },
    )
    if r.status_code != 250:
        print(r)
        raise Exception("Email exception! Check username and password")
    return r


class EmailOutput(BaseOutput):
    """Email output type"""

    def __init__(self, config, *args, **kwargs):
        self.config = config

    def write(self, report, output, *args, **kwargs):
        """write a given notebook as an email"""
        task_id = kwargs.get("task_id", "")

        name = task_id + "_" + datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        msg = make_email(
            name,
            output,
            from_=self.config.from_,
            type=report["meta"]["output"],
            subject=name,
            header=self.config.header,
            footer=self.config.footer,
        )
        email(
            msg,
            self.config.to,
            self.config.username,
            self.config.password,
            self.config.domain,
            self.config.host,
            self.config.port,
        )
