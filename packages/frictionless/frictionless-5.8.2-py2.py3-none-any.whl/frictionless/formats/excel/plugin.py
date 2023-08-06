from __future__ import annotations
from ...system import Plugin
from ...resource import Resource
from .adapter import ExcelAdapter
from .control import ExcelControl
from .parsers import XlsxParser, XlsParser


class ExcelPlugin(Plugin):
    """Plugin for Excel"""

    # Hooks

    def create_adapter(self, source, *, control=None):
        if isinstance(source, str):
            resource = Resource(path=source)
            if resource.format == "xlsx":
                control = control or ExcelControl()
                return ExcelAdapter(control, resource=resource)  # type: ignore

    def create_parser(self, resource):
        if resource.format == "xlsx":
            return XlsxParser(resource)
        elif resource.format == "xls":
            return XlsParser(resource)

    def detect_resource(self, resource: Resource):
        if resource.format in ["xlsx", "xls"]:
            resource.datatype = resource.datatype or "table"
            resource.mediatype = resource.mediatype or "application/vnd.ms-excel"

    def select_control_class(self, type):
        if type == "excel":
            return ExcelControl
