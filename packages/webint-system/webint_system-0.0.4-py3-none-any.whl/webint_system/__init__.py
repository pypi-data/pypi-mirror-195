"""
Manage code on your website.

- Supports [PEP 503 -- Simple Repository API][0] managing Python packages.

[0]: https://www.python.org/dev/peps/pep-0503/

"""

# TODO PEP 592 -- Adding "Yank" Support to the Simple API
# TODO PEP 658 -- Serve Distribution Metadata in the Simple Repository API

import importlib.metadata
import pathlib
import re
import shutil
import subprocess
import time

import pkg_resources
import semver
import web
import webagt

app = web.application(__name__, prefix="system")

code_dir = pathlib.Path.home() / "code"
meta_dir = code_dir / "meta"
working_dir = code_dir / "working"


def update_system(package):
    print(
        subprocess.run(
            ["/home/gaea/runinenv", "/home/gaea/app", "pip", "install", "-U", package],
            capture_output=True,
        )
    )


def get_versions(package):
    """Return the latest version if currently installed `package` is out of date."""
    current_version = pkg_resources.get_distribution(package).version
    current_version = current_version.partition("a")[0]  # TODO FIXME strips alpha/beta
    update_available = False
    versions_rss = webagt.get(
        f"https://pypi.org/rss/project/{package}/releases.xml"
    ).xml
    latest_version = [
        child.getchildren()[0].text
        for child in versions_rss.getchildren()[0].getchildren()
        if child.tag == "item"
    ][0]
    if semver.compare(current_version, latest_version) == -1:
        update_available = latest_version
    return current_version, update_available


@app.wrap
def set_working_dir(handler, main_app):
    web.tx.host.working_dir = working_dir
    yield


@app.control("")
class System:
    """The system that runs your website."""

    def get(self):
        """"""
        ip_address = subprocess.check_output(["hostname", "-I"]).split()[0].decode()
        addresses = []
        webint_metadata = importlib.metadata.metadata("webint")
        webint_versions = get_versions("webint")
        return app.view.index(
            ip_address,
            addresses,
            web.tx.app.cfg,
            web.tx.app,
            web.get_apps(),
            webint_metadata,
            webint_versions,
        )


@app.control("addresses")
class Addresses:
    """System addresses."""

    def post(self):
        """"""
        return "addresses have been updated"


@app.control("settings")
class Settings:
    """System settings."""

    def post(self):
        """"""
        form = web.form("key", "value")
        web.tx.app.update_config(form.key, form.value)
        return "settings have been updated"


@app.control("software")
class Software:
    """System software."""

    def post(self):
        """"""
        web.enqueue(update_system, "canopy")  # TODO FIXME
        return "software update has been started"


@app.control("robots.txt", prefixed=False)
class RobotsTXT:
    """A robots.txt file."""

    def get(self):
        """Return a robots.txt file."""
        all_bots = ["User-agent: *"]
        for project in web.application("webint_code").model.get_projects():
            all_bots.append(f"Disallow: /code/{project}/releases/")
        return "\n".join(all_bots)
