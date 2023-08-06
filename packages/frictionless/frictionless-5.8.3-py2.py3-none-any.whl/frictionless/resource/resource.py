from __future__ import annotations
import json
import attrs
import warnings
import builtins
from pathlib import Path
from collections.abc import Mapping
from typing import TYPE_CHECKING, Optional, Union, List, Any, ClassVar, Dict
from ..exception import FrictionlessException
from ..table import Header, Lookup, Row
from ..dialect import Dialect, Control
from .stats import ResourceStats
from ..platform import platform
from ..detector import Detector
from ..metadata import Metadata
from ..schema import Schema
from ..system import system
from .. import settings
from .. import helpers
from .. import errors
from .. import fields
from . import methods


if TYPE_CHECKING:
    from ..checklist import Checklist
    from ..pipeline import Pipeline
    from ..package import Package
    from ..table import IRowStream
    from ..system import Loader, Parser
    from ..interfaces import IDescriptor, IBuffer, ISample, IFragment
    from ..interfaces import ILabels, IByteStream, ITextStream, ICellStream
    from ..interfaces import IFilterFunction, IProcessFunction
    from ..formats.sql import IOnRow, IOnProgress
    from ..interfaces import ICallbackFunction


@attrs.define(kw_only=True)
class Resource(Metadata):
    """Resource representation.

    This class is one of the cornerstones of of Frictionless framework.
    It loads a data source, and allows you to stream its parsed contents.
    At the same time, it's a metadata class data description.

    ```python
    with Resource("data/table.csv") as resource:
        resource.header == ["id", "name"]
        resource.read_rows() == [
            {'id': 1, 'name': 'english'},
            {'id': 2, 'name': '中国人'},
        ]
    ```

    """

    source: Optional[Any] = attrs.field(default=None, kw_only=False)
    """
    # TODO: add docs
    """

    control: Optional[Control] = None
    """
    # TODO: add docs
    """

    name: str = ""
    """
    Resource name according to the specs.
    It should be a slugified name of the resource.
    """

    type: ClassVar[str]
    """
    Type of the resource
    """

    title: Optional[str] = None
    """
    Resource title according to the specs
    It should a human-oriented title of the resource.
    """

    description: Optional[str] = None
    """
    Resource description according to the specs
    It should a human-oriented description of the resource.
    """

    homepage: Optional[str] = None
    """
    A URL for the home on the web that is related to this package.
    For example, github repository or ckan dataset address.
    """

    profile: Optional[str] = None
    """
    A fully-qualified URL that points directly to a JSON Schema
    that can be used to validate the descriptor
    """

    licenses: List[dict] = attrs.field(factory=list)
    """
    The license(s) under which the resource is provided.
    If omitted it's considered the same as the package's licenses.
    """

    sources: List[dict] = attrs.field(factory=list)
    """
    The raw sources for this data resource.
    It MUST be an array of Source objects.
    Each Source object MUST have a title and
    MAY have path and/or email properties.
    """

    path: Optional[str] = None
    """
    Path to data source
    """

    data: Optional[Any] = None
    """
    Inline data source
    """

    scheme: Optional[str] = None
    """
    Scheme for loading the file (file, http, ...).
    If not set, it'll be inferred from `source`.
    """

    format: Optional[str] = None
    """
    File source's format (csv, xls, ...).
    If not set, it'll be inferred from `source`.
    """

    datatype: str = ""
    """
    Frictionless Framework specific data type as "table" or "schema"
    """

    mediatype: Optional[str] = None
    """
    Mediatype/mimetype of the resource e.g. “text/csv”,
    or “application/vnd.ms-excel”.  Mediatypes are maintained by the
    Internet Assigned Numbers Authority (IANA) in a media type registry.
    """

    compression: Optional[str] = None
    """
    Source file compression (zip, ...).
    If not set, it'll be inferred from `source`.
    """

    extrapaths: List[str] = attrs.field(factory=list)
    """
    List of paths to concatenate to the main path.
    It's used for multipart resources.
    """

    innerpath: Optional[str] = None
    """
    Path within the compressed file.
    It defaults to the first file in the archive (if the source is an archive).
    """

    encoding: Optional[str] = None
    """
    Source encoding.
    If not set, it'll be inferred from `source`.
    """

    hash: Optional[str] = None
    """
    # TODO: add docs
    """

    bytes: Optional[int] = None
    """
    # TODO: add docs
    """

    fields: Optional[int] = None
    """
    # TODO: add docs
    """

    rows: Optional[int] = None
    """
    # TODO: add docs
    """

    _dialect: Union[Dialect, str] = attrs.field(factory=Dialect, alias="dialect")
    """
    # TODO: add docs
    """

    _schema: Union[Schema, str] = attrs.field(factory=Schema, alias="schema")
    """
    # TODO: add docs
    """

    _basepath: Optional[str] = attrs.field(default=None, alias="basepath")
    """
    # TODO: add docs
    """

    detector: Detector = attrs.field(factory=Detector)
    """
    File/table detector.
    For more information, please check the Detector documentation.
    """

    package: Optional[Package] = None
    """
    Parental to this resource package.
    For more information, please check the Package documentation.
    """

    stats: ResourceStats = attrs.field(init=False)
    """
    # TODO: add docs
    """

    @classmethod
    def __create__(
        cls,
        source: Optional[Any] = None,
        *,
        control: Optional[Control] = None,
        **options,
    ):
        # Normalize
        if isinstance(source, Path):
            source = str(source)
        if isinstance(source, Mapping):
            source = {key: value for key, value in source.items()}

        # Control
        if control is not None:
            dialect = options.pop("dialect", None)
            if dialect is None:
                dialect = control.to_dialect()
            elif control not in dialect.controls:
                dialect.add_control(control)
            options["dialect"] = dialect
            if source is None:
                return cls(**options)

        # Source
        if source is not None:
            # Descriptor
            # TODO: deprecate in v6
            normsource = source
            package = options.get("package")
            basepath = options.get("basepath", package.basepath if package else None)
            if isinstance(normsource, str):
                normsource = helpers.normalize_path(normsource, basepath=basepath)
            metadata_type = Detector.detect_metadata_type(normsource)
            if metadata_type == "resource":
                return cls.from_descriptor(source, **options)

            # Path/data
            options["path" if isinstance(source, str) else "data"] = source
            return cls(**options)

        # Routing
        if cls is Resource:
            type = options.pop("type", None)
            if type:
                note = 'Argument "resource.type" is deprecated. Use "resources.TableResource"'
                warnings.warn(note, UserWarning)
            resource = platform.frictionless_resources.FileResource(**options)
            Class = system.select_resource_class(datatype=resource.datatype)
            resource = Class(**options)
            return resource

    def __attrs_post_init__(self):
        self.stats = ResourceStats()

        # State
        self.__loader: Optional[Loader] = None
        self.__parser: Optional[Parser] = None
        self.__buffer: Optional[IBuffer] = None
        self.__sample: Optional[ISample] = None
        self.__labels: Optional[ILabels] = None
        self.__fragment: Optional[IFragment] = None
        self.__header: Optional[Header] = None
        self.__lookup: Optional[Lookup] = None
        self.__row_stream: Optional[IRowStream] = None

        # Detect resource
        system.detect_resource(self)

        # TODO: remove this defined/not-defined logic?
        # Define default state
        self.add_defined("name")
        self.add_defined("scheme")
        self.add_defined("format")
        self.add_defined("compression")
        self.add_defined("mediatype")
        self.add_defined("dialect")
        self.add_defined("stats")

    # TODO: shall we guarantee here that it's at the beggining for the file?
    # TODO: maybe it's possible to do type narrowing here?
    def __enter__(self):
        if self.closed:
            self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    @property
    def paths(self) -> List[str]:
        """All paths of the resource"""
        paths = []
        if self.path is not None:
            paths.append(self.path)
        paths.extend(self.extrapaths)
        return paths

    @property
    def normpaths(self) -> List[str]:
        """Normalized paths of the resource"""
        normpaths = []
        for path in self.paths:
            normpaths.append(helpers.normalize_path(path, basepath=self.basepath))
        return normpaths

    @property
    def normpath(self) -> Optional[str]:
        """Normalized path of the resource or raise if not set"""
        if self.path:
            return helpers.normalize_path(self.path, basepath=self.basepath)

    # TODO: add asteriks for user/pass in url
    @property
    def place(self) -> str:
        """Stringified resource location"""
        if self.data is not None:
            return "<memory>"
        elif self.extrapaths:
            return f"{self.path} (multipart)"
        elif self.innerpath:
            return f"{self.path} -> {self.innerpath}"
        elif self.path:
            return self.path
        return ""

    @property
    def memory(self) -> bool:
        """Whether resource is not path based"""
        return self.data is not None

    @property
    def remote(self) -> bool:
        """Whether resource is remote"""
        return helpers.is_remote_path(self.basepath or self.path or "")

    @property
    def multipart(self) -> bool:
        """Whether resource is multipart"""
        return not self.memory and bool(self.extrapaths)

    @property
    def tabular(self) -> bool:
        """Whether resource is tabular"""
        return self.type == "table"

    @property
    def dialect(self) -> Dialect:
        if isinstance(self._dialect, str):
            self._dialect = Dialect.from_descriptor(self._dialect, basepath=self.basepath)
        return self._dialect

    @dialect.setter
    def dialect(self, value: Union[Dialect, str]):
        self._dialect = value

    @property
    def schema(self) -> Schema:
        if isinstance(self._schema, str):
            self._schema = Schema.from_descriptor(self._schema, basepath=self.basepath)
        return self._schema

    @schema.setter
    def schema(self, value: Union[Schema, str]):
        self._schema = value

    @property
    def basepath(self) -> Optional[str]:
        """
        A basepath of the resource
        The normpath of the resource is joined `basepath` and `/path`
        """
        if self._basepath:
            return self._basepath
        if self.package:
            return self.package.basepath

    @basepath.setter
    def basepath(self, value: Optional[str]):
        self._basepath = value

    @property
    def buffer(self) -> IBuffer:
        """File's bytes used as a sample

        These buffer bytes are used to infer characteristics of the
        source file (e.g. encoding, ...).
        """
        if self.__buffer is None:
            raise FrictionlessException("resource is not open or non binary")
        return self.__buffer

    @property
    def sample(self) -> ISample:
        """Table's lists used as sample.

        These sample rows are used to infer characteristics of the
        source file (e.g. schema, ...).

        Returns:
            list[]?: table sample
        """
        if self.__sample is None:
            raise FrictionlessException("resource is not open or non tabular")
        return self.__sample

    @property
    def labels(self) -> ILabels:
        """
        Returns:
            str[]?: table labels
        """
        if self.__labels is None:
            raise FrictionlessException("resource is not open or non tabular")
        return self.__labels

    @property
    def fragment(self) -> IFragment:
        """Table's lists used as fragment.

        These fragment rows are used internally to infer characteristics of the
        source file (e.g. schema, ...).

        Returns:
            list[]?: table fragment
        """
        if self.__fragment is None:
            raise FrictionlessException("resource is not open or non tabular")
        return self.__fragment

    @property
    def header(self) -> Header:
        """
        Returns:
            str[]?: table header
        """
        if self.__header is None:
            raise FrictionlessException("resource is not open or non tabular")
        return self.__header

    @property
    def lookup(self) -> Lookup:
        """
        Returns:
            str[]?: table lookup
        """
        if self.__lookup is None:
            raise FrictionlessException("resource is not open or non tabular")
        return self.__lookup

    @property
    def byte_stream(self) -> IByteStream:
        """Byte stream in form of a generator

        Yields:
            gen<bytes>?: byte stream
        """
        if self.closed:
            raise FrictionlessException("resource is not open or non binary")
        if not self.__loader:
            self.__loader = system.create_loader(self)
            self.__loader.open()
        return self.__loader.byte_stream

    @property
    def text_stream(self) -> ITextStream:
        """Text stream in form of a generator

        Yields:
            gen<str[]>?: text stream
        """
        if self.closed:
            raise FrictionlessException("resource is not open or non textual")
        if not self.__loader:
            self.__loader = system.create_loader(self)
            self.__loader.open()
        return self.__loader.text_stream

    @property
    def cell_stream(self) -> ICellStream:
        """Cell stream in form of a generator

        Yields:
            gen<any[][]>?: cell stream
        """
        if self.__parser is None:
            raise FrictionlessException("resource is not open or non tabular")
        return self.__parser.cell_stream

    @property
    def row_stream(self) -> IRowStream:
        """Row stream in form of a generator of Row objects

        Yields:
            gen<Row[]>?: row stream
        """
        if self.__row_stream is None:
            raise FrictionlessException("resource is not open or non tabular")
        return self.__row_stream

    # Infer

    # TODO: allow cherry-picking stats for adding to a descriptor
    def infer(self, *, stats: bool = False) -> None:
        """Infer metadata

        Parameters:
            stats: stream file completely and infer stats
        """
        if not self.closed:
            note = "Resource.infer canot be used on a open resource"
            raise FrictionlessException(errors.ResourceError(note=note))
        with self:
            if not stats:
                return
            stream = self.__row_stream or self.byte_stream
            helpers.pass_through(stream)
            self.hash = f"sha256:{self.stats.sha256}"
            self.bytes = self.stats.bytes
            if self.tabular:
                self.fields = self.stats.fields
                self.rows = self.stats.rows

    # Dereference

    def dereference(self):
        """Dereference underlaying metadata

        If some of underlaying metadata is provided as a string
        it will replace it by the metadata object
        """
        self.dialect.metadata_descriptor_path = None
        self.dialect.metadata_descriptor_initial = None
        self.schema.metadata_descriptor_path = None
        self.schema.metadata_descriptor_initial = None

    # Open/Close

    def open(self, *, as_file: bool = False):
        """Open the resource as "io.open" does"""
        self.close()
        try:
            # Table
            if self.type == "table" and not as_file:
                self.__prepare_parser()
                self.__prepare_buffer()
                self.__prepare_sample()
                self.__prepare_dialect()
                self.__prepare_labels()
                self.__prepare_fragment()
                self.__prepare_schema()
                self.__prepare_header()
                self.__prepare_lookup()
                self.__prepare_row_stream()

            # File
            elif self.scheme:
                self.__prepare_loader()
                self.__prepare_buffer()

        except Exception:
            self.close()
            raise
        return self

    def close(self) -> None:
        """Close the resource as "filelike.close" does"""
        if self.__parser:
            self.__parser.close()
            self.__parser = None
        if self.__loader:
            self.__loader.close()
            self.__loader = None

    @property
    def closed(self) -> bool:
        """Whether the table is closed

        Returns:
            bool: if closed
        """
        return self.__parser is None and self.__loader is None

    def __prepare_loader(self):
        self.__loader = system.create_loader(self)
        self.__loader.open()

    def __prepare_buffer(self):
        if self.__parser and self.__parser.requires_loader:
            self.__buffer = self.__parser.loader.buffer
        elif self.__loader:
            self.__buffer = self.__loader.buffer

    def __prepare_parser(self):
        self.__parser = system.create_parser(self)
        self.__parser.open()

    def __prepare_sample(self):
        if self.__parser:
            self.__sample = self.__parser.sample

    def __prepare_dialect(self):
        self.metadata_assigned.add("dialect")
        self.dialect = self.detector.detect_dialect(self.sample, dialect=self.dialect)

    def __prepare_labels(self):
        self.__labels = self.dialect.read_labels(self.sample)

    def __prepare_fragment(self):
        self.__fragment = self.dialect.read_fragment(self.sample)

    def __prepare_schema(self):
        self.metadata_assigned.add("schema")
        self.schema = self.detector.detect_schema(
            self.fragment,
            labels=self.labels,
            schema=self.schema,
            field_candidates=system.detect_field_candidates(),
        )
        self.stats.fields = len(self.schema.fields)

    def __prepare_header(self):
        # Create header
        self.__header = Header(
            self.__labels,
            fields=self.schema.fields,
            row_numbers=self.dialect.header_rows,
            ignore_case=not self.dialect.header_case,
        )

        # Handle errors
        if not self.header.valid:
            error = self.header.errors[0]
            if system.onerror == "warn":
                warnings.warn(error.message, UserWarning)
            elif system.onerror == "raise":
                raise FrictionlessException(error)

    def __prepare_lookup(self):
        self.__lookup = Lookup()
        for fk in self.schema.foreign_keys:
            # Prepare source
            source_name = fk["reference"]["resource"]
            source_key = tuple(fk["reference"]["fields"])
            if source_name != "" and not self.package:
                continue
            if source_name:
                if not self.package:
                    note = 'package is required for FK: "{fk}"'
                    raise FrictionlessException(errors.ResourceError(note=note))
                if not self.package.has_resource(source_name):
                    note = f'failed to handle a foreign key for resource "{self.name}" as resource "{source_name}" does not exist'
                    raise FrictionlessException(errors.ResourceError(note=note))
                source_res = self.package.get_resource(source_name)
            else:
                source_res = self.to_copy()
            if source_res.schema:
                source_res.schema.foreign_keys = []

            # Prepare lookup
            self.__lookup.setdefault(source_name, {})
            if source_key in self.__lookup[source_name]:
                continue
            self.__lookup[source_name][source_key] = set()
            if not source_res:
                continue
            with source_res:
                for row in source_res.row_stream:  # type: ignore
                    cells = tuple(row.get(field_name) for field_name in source_key)
                    if set(cells) == {None}:
                        continue
                    self.__lookup[source_name][source_key].add(cells)

    def __prepare_row_stream(self):
        # TODO: we need to rework this field_info / row code
        # During row streaming we crate a field info structure
        # This structure is optimized and detached version of schema.fields
        # We create all data structures in-advance to share them between rows

        # Create field info
        field_number = 0
        field_info = {"names": [], "objects": [], "mapping": {}}
        for field in self.schema.fields:
            field_number += 1
            field_info["names"].append(field.name)
            field_info["objects"].append(field.to_copy())
            field_info["mapping"][field.name] = (
                field,
                field_number,
                field.create_cell_reader(),
                field.create_cell_writer(),
            )

        # Create state
        memory_unique = {}
        memory_primary = {}
        foreign_groups = []
        is_integrity = bool(self.schema.primary_key)
        for field in self.schema.fields:
            if field.constraints.get("unique"):
                memory_unique[field.name] = {}
                is_integrity = True
        if self.__lookup:
            for fk in self.schema.foreign_keys:
                group = {}
                group["sourceName"] = fk["reference"]["resource"]
                group["sourceKey"] = tuple(fk["reference"]["fields"])
                group["targetKey"] = tuple(fk["fields"])
                foreign_groups.append(group)
                is_integrity = True

        # Create content stream
        enumerated_content_stream = self.dialect.read_enumerated_content_stream(
            self.cell_stream
        )

        # Create row stream
        def row_stream():
            self.stats.rows = 0
            for row_number, cells in enumerated_content_stream:
                self.stats.rows += 1

                # Create row
                row = Row(
                    cells,
                    field_info=field_info,
                    row_number=row_number,
                )

                # Unique Error
                if is_integrity and memory_unique:
                    for field_name in memory_unique.keys():
                        cell = row[field_name]
                        if cell is not None:
                            match = memory_unique[field_name].get(cell)
                            memory_unique[field_name][cell] = row.row_number
                            if match:
                                func = errors.UniqueError.from_row
                                note = "the same as in the row at position %s" % match
                                error = func(row, note=note, field_name=field_name)
                                row.errors.append(error)

                # Primary Key Error
                if is_integrity and self.schema.primary_key:
                    cells = tuple(row[name] for name in self.schema.primary_key)
                    if set(cells) == {None}:
                        note = 'cells composing the primary keys are all "None"'
                        error = errors.PrimaryKeyError.from_row(row, note=note)
                        row.errors.append(error)
                    else:
                        match = memory_primary.get(cells)
                        memory_primary[cells] = row.row_number
                        if match:
                            if match:
                                note = "the same as in the row at position %s" % match
                                error = errors.PrimaryKeyError.from_row(row, note=note)
                                row.errors.append(error)

                # Foreign Key Error
                if is_integrity and foreign_groups:
                    for group in foreign_groups:
                        group_lookup = self.lookup.get(group["sourceName"])
                        if group_lookup:
                            cells = tuple(row[name] for name in group["targetKey"])
                            if set(cells) == {None}:
                                continue
                            match = cells in group_lookup.get(group["sourceKey"], set())
                            if not match:
                                note = (
                                    'for "%s": values "%s" not found in the lookup table "%s" as "%s"'
                                    % (
                                        ", ".join(group["targetKey"]),
                                        ", ".join(str(d) for d in cells),
                                        group["sourceName"],
                                        ", ".join(group["sourceKey"]),
                                    )
                                )

                                error = errors.ForeignKeyError.from_row(
                                    row,
                                    note=note,
                                    field_names=list(group["targetKey"]),
                                    field_values=list(cells),
                                    reference_name=group["sourceName"],
                                    reference_field_names=list(group["sourceKey"]),
                                )
                                row.errors.append(error)

                # Handle errors
                if system.onerror != "ignore":
                    if not row.valid:
                        error = row.errors[0]
                        if system.onerror == "raise":
                            raise FrictionlessException(error)
                        warnings.warn(error.message, UserWarning)

                # Yield row
                yield row

        # Crreate row stream
        self.__row_stream = row_stream()

    # Read

    # TODO: open as a file?
    def read_bytes(self, *, size: Optional[int] = None) -> bytes:
        """Read bytes into memory

        Returns:
            any[][]: resource bytes
        """
        if self.memory:
            return b""
        with helpers.ensure_open(self):
            # Without size we need to read chunk by chunk because read1 doesn't return
            # the full contents by default (just an arbitrary amount of bytes)
            # and we use read1 as it includes stats calculation (system.loader)
            if not size:
                buffer = b""
                while True:
                    chunk = self.byte_stream.read1()  # type: ignore
                    buffer += chunk
                    if not chunk:
                        break
                return buffer
            return self.byte_stream.read1(size)  # type: ignore

    def read_text(self, *, size: Optional[int] = None) -> str:
        """Read text into memory

        Returns:
            str: resource text
        """
        if self.memory:
            return ""
        with helpers.ensure_open(self):
            return self.text_stream.read(size)  # type: ignore

    # TODO: support yaml?
    def read_data(self, *, size: Optional[int] = None) -> Any:
        """Read data into memory

        Returns:
            any: resource data
        """
        if self.data is not None:
            return self.data
        with helpers.ensure_open(self):
            text = self.read_text(size=size)
            data = json.loads(text)
            return data

    def read_cells(self, *, size: Optional[int] = None) -> List[List[Any]]:
        """Read lists into memory

        Returns:
            any[][]: table lists
        """
        with helpers.ensure_open(self):
            result = []
            for cells in self.cell_stream:
                result.append(cells)
                if size and len(result) >= size:
                    break
            return result

    def read_rows(self, *, size=None) -> List[Row]:
        """Read rows into memory

        Returns:
            Row[]: table rows
        """
        with helpers.ensure_open(self):
            rows = []
            for row in self.row_stream:
                rows.append(row)
                if size and len(rows) >= size:
                    break
            return rows

    # Write

    def write(
        self,
        target: Optional[Union[Resource, Any]] = None,
        *,
        control: Optional[Control] = None,
        **options,
    ) -> Resource:
        """Write this resource to the target resource

        Parameters:
            target (Resource|Any): target or target resource instance
            **options (dict): Resource constructor options
        """
        resource = target
        if not isinstance(resource, Resource):
            resource = Resource(target, control=control, **options)
        parser = system.create_parser(resource)
        parser.write_row_stream(self)
        return resource

    # Analyze

    def analyze(self, *, detailed=False) -> Dict:
        """Analyze the resource

        This feature is currently experimental, and its API may change
        without warning.

        Parameters:
            detailed? (bool): detailed analysis

        Returns:
            dict: resource analysis

        """
        return methods.analyze(self, detailed=detailed)

    # Describe

    @classmethod
    def describe(
        cls, source: Optional[Any] = None, *, stats: bool = False, **options
    ) -> Resource:
        """Describe the given source as a resource

        Parameters:
            source (any): data source
            stats? (bool): if `True` infer resource's stats
            **options (dict): Resource constructor options

        Returns:
            Resource: data resource

        """
        resource = cls.from_options(source, **options)
        resource.infer(stats=stats)
        return resource

    # Extract

    def extract(
        self,
        *,
        limit_rows: Optional[int] = None,
        process: Optional[IProcessFunction] = None,
        filter: Optional[IFilterFunction] = None,
        stream: bool = False,
    ):
        """Extract resource rows

        Parameters:
            process? (func): a row processor function
            filter? (bool): a row filter function
            stream? (bool): whether to stream data

        Returns:
            Row[]: an array/stream of rows

        """

        # Stream
        def read_row_stream():
            with self:
                row_count = 0
                for row in self.row_stream:  # type: ignore
                    row_count += 1
                    yield row
                    if limit_rows and limit_rows <= row_count:
                        break

        # Return
        data = read_row_stream()
        data = builtins.filter(filter, data) if filter else data
        data = (process(row) for row in data) if process else data
        return data if stream else list(data)

    # Index

    def index(
        self,
        database_url: str,
        *,
        table_name: str,
        fast: bool = False,
        qsv_path: Optional[str] = None,
        on_row: Optional[IOnRow] = None,
        on_progress: Optional[IOnProgress] = None,
        use_fallback: bool = False,
    ) -> None:
        """Index resource into a database"""
        indexer = platform.frictionless_formats.sql.SqlIndexer(
            resource=self,
            database_url=database_url,
            table_name=table_name,
            fast=fast,
            qsv_path=qsv_path,
            on_row=on_row,
            on_progress=on_progress,
            use_fallback=use_fallback,
        )
        indexer.index()

    # Validate

    def validate(
        self,
        checklist: Optional[Checklist] = None,
        *,
        limit_errors: int = settings.DEFAULT_LIMIT_ERRORS,
        limit_rows: Optional[int] = None,
        on_row: Optional[ICallbackFunction] = None,
    ):
        """Validate resource

        Parameters:
            checklist? (checklist): a Checklist object

        Returns:
            Report: validation report

        """
        return methods.validate(
            self,
            checklist,
            limit_errors=limit_errors,
            limit_rows=limit_rows,
            on_row=on_row,
        )

    # Transform

    def transform(self, pipeline: Optional[Pipeline] = None):
        """Transform resource

        Parameters:
            steps (Step[]): transform steps

        Returns:
            Resource: the transform result
        """
        return methods.transform(self, pipeline)

    # Convert

    def to_copy(self, **options):
        """Create a copy from the resource"""
        return super().to_copy(
            data=self.data,
            basepath=self.basepath,
            detector=self.detector,
            package=self.package,
            **options,
        )

    def to_view(self, type="look", **options):
        """Create a view from the resource

        See PETL's docs for more information:
        https://platform.petl.readthedocs.io/en/stable/util.html#visualising-tables

        Parameters:
            type (look|lookall|see|display|displayall): view's type
            **options (dict): options to be passed to PETL

        Returns
            str: resource's view
        """
        assert type in ["look", "lookall", "see", "display", "displayall"]
        view = str(getattr(self.to_petl(normalize=True), type)(**options))
        return view

    def to_snap(self, *, json=False):
        """Create a snapshot from the resource

        Parameters:
            json (bool): make data types compatible with JSON format

        Returns
            list: resource's data
        """
        snap = []
        with helpers.ensure_open(self):
            snap.append(self.header.to_list())
            for row in self.row_stream:
                snap.append(row.to_list(json=json))
        return snap

    def to_inline(self, *, dialect=None):
        """Helper to export resource as an inline data"""
        dialect = dialect or Dialect()
        target = self.write(Resource(format="inline", dialect=dialect))  # type: ignore
        return target.data

    def to_pandas(self, *, dialect=None):
        """Helper to export resource as an Pandas dataframe"""
        dialect = dialect or Dialect()
        target = self.write(Resource(format="pandas", dialect=dialect))  # type: ignore
        return target.data

    @staticmethod
    def from_petl(view, **options):
        """Create a resource from PETL view"""
        return Resource(data=view, **options)

    def to_petl(self, normalize=False):
        """Export resource as a PETL table"""
        resource = self.to_copy()

        # Define view
        class ResourceView(platform.petl.Table):
            def __iter__(self):
                with resource:
                    if normalize:
                        yield resource.schema.field_names
                        yield from (row.to_list() for row in resource.row_stream)
                        return
                    if not resource.header.missing:
                        yield resource.header.labels
                    yield from (row.cells for row in resource.row_stream)

        return ResourceView()

    # Metadata

    metadata_type = "resource"
    metadata_Error = errors.ResourceError
    metadata_profile = {
        "type": "object",
        "required": ["name"],  # TODO: add "type" in v6
        "properties": {
            "name": {"type": "string", "pattern": settings.NAME_PATTERN},
            "type": {"type": "string", "pattern": settings.TYPE_PATTERN},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "homepage": {"type": "string"},
            "profile": {"type": "string"},
            "licenses": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "path": {"type": "string"},
                        "title": {"type": "string"},
                    },
                },
            },
            "sources": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "path": {"type": "string"},
                        "email": {"type": "string"},
                    },
                },
            },
            "path": {"type": "string"},
            "data": {"type": ["object", "array"]},
            "scheme": {"type": "string"},
            "format": {"type": "string"},
            "mediatype": {"type": "string"},
            "compression": {"type": "string"},
            "extrapaths": {"type": "array", "item": {"type": "string"}},
            "innerpath": {"type": "string"},
            "encoding": {"type": "string"},
            "hash": {"type": "string"},
            "bytes": {"type": "integer"},
            "fields": {"type": "integer"},
            "rows": {"type": "integer"},
            "dialect": {"type": ["object", "string"]},
            "schema": {"type": ["object", "string"]},
        },
    }

    @classmethod
    def metadata_select_class(cls, type):
        return system.select_resource_class(type)

    @classmethod
    def metadata_select_property_class(cls, name):
        if name == "dialect":
            return Dialect
        elif name == "schema":
            return Schema

    @classmethod
    def metadata_transform(cls, descriptor):
        super().metadata_transform(descriptor)

        # Url (standards/v0)
        url = descriptor.pop("url", None)
        path = descriptor.get("path")
        data = descriptor.get("data")
        if not path and (data is None) and url:
            descriptor.setdefault("path", url)

        # Path (standards/v1)
        path = descriptor.get("path")
        if path and isinstance(path, list):
            descriptor["path"] = path[0]
            descriptor["extrapaths"] = path[1:]

        # Profile (standards/v1)
        profile = descriptor.pop("profile", None)
        if profile:
            if profile == "tabular-data-resource":
                descriptor["type"] = "table"
            elif profile not in ["data-resource"]:
                descriptor["profile"] = profile

        # Profiles (framework/v5)
        profiles = descriptor.pop("profiles", None)
        if isinstance(profiles, list) and profiles:
            if isinstance(profiles[0], str):
                descriptor["profile"] = profiles[0]

        # Bytes (standards/v1)
        bytes = descriptor.pop("bytes", None)
        if bytes:
            descriptor.setdefault("stats", {})
            descriptor["stats"]["bytes"] = bytes

        # Hash (framework/v4)
        hashing = descriptor.get("hashing", None)
        stats = descriptor.get("stats", None)
        if hashing and stats:
            hash = stats.pop("hash", None)
            if hash:
                descriptor[hashing] = hash
            note = 'Resource "stats.hash" is deprecated in favor of "stats.sha256/md5"'
            note += "(it will be removed in the next major version)"
            warnings.warn(note, UserWarning)

        # Hash (standards/v1)
        hash = descriptor.get("hash", None)
        if hash:
            algo, hash = helpers.parse_resource_hash_v1(hash)
            if algo in ["md5", "sha256"]:
                descriptor.pop("hash")
                descriptor.setdefault("stats", {})
                descriptor["stats"][algo] = hash

        # Stats (framework/v5)
        stats = descriptor.pop("stats", None)
        if stats and isinstance(stats, dict):
            md5 = stats.pop("md5", None)
            sha256 = stats.pop("sha256", None)
            if sha256:
                descriptor["hash"] = f"sha256:{sha256}"
            elif md5:
                descriptor["hash"] = md5
            for name in ["bytes", "fields", "rows"]:
                value = stats.get(name)
                if value:
                    descriptor[name] = value

        # Compression (framework/v4)
        compression = descriptor.get("compression")
        if compression == "no":
            descriptor.pop("compression")
            note = 'Resource "compression=no" is deprecated in favor not set value'
            note += "(it will be removed in the next major version)"
            warnings.warn(note, UserWarning)

        # Layout (framework/v4)
        layout = descriptor.pop("layout", None)
        if layout:
            descriptor.setdefault("dialect", {})
            descriptor["dialect"].update(layout)
            note = 'Resource "layout" is deprecated in favor of "dialect"'
            note += "(it will be removed in the next major version)"
            warnings.warn(note, UserWarning)

    @classmethod
    def metadata_validate(cls, descriptor: IDescriptor):
        metadata_errors = list(super().metadata_validate(descriptor))
        if metadata_errors:
            yield from metadata_errors
            return

        # Security
        if not system.trusted:
            keys = ["path", "extrapaths", "profile", "dialect", "schema"]
            for key in keys:
                value = descriptor.get(key)
                items = value if isinstance(value, list) else [value]
                for item in items:
                    if item and isinstance(item, str) and not helpers.is_safe_path(item):
                        yield errors.ResourceError(note=f'path "{item}" is not safe')
                        return

        # Required
        path = descriptor.get("path")
        data = descriptor.get("data")
        if path is None and data is None:
            note = 'one of the properties "path" or "data" is required'
            yield errors.ResourceError(note=note)

        # Path/Data
        if path is not None and data is not None:
            note = 'properties "path" and "data" is mutually exclusive'
            yield errors.ResourceError(note=note)

        # Contributors/Sources
        for name in ["contributors", "sources"]:
            for item in descriptor.get(name, []):
                if item.get("email"):
                    field = fields.StringField(name="email", format="email")
                    _, note = field.read_cell(item.get("email"))
                    if note:
                        note = f'property "{name}[].email" is not valid "email"'
                        yield errors.ResourceError(note=note)

        # Profile
        profile = descriptor.get("profile")
        if profile and profile not in ["data-resource", "tabular-data-resource"]:
            yield from Metadata.metadata_validate(
                descriptor,
                profile=profile,
                error_class=cls.metadata_Error,
            )

        # Misleading
        for name in ["missingValues"]:
            if name in descriptor:
                note = f'"{name}" should be set as "schema.{name}"'
                yield errors.ResourceError(note=note)

    @classmethod
    def metadata_import(cls, descriptor: IDescriptor, **options):
        return super().metadata_import(
            descriptor=descriptor,
            with_basepath=True,
            **options,
        )

    def metadata_export(self):
        descriptor = super().metadata_export()

        # Data
        data = descriptor.get("data")
        types = (str, bool, int, float, list, dict)
        if data is not None and not isinstance(data, types):
            descriptor["data"] = []

        # Path (standards/v1)
        if system.standards == "v1":
            path = descriptor.get("path")
            extrapaths = descriptor.pop("extrapaths", None)
            if extrapaths:
                descriptor["path"] = []
                if path:
                    descriptor["path"].append(path)
                descriptor["path"].extend(extrapaths)

        # Profile (standards/v1)
        if system.standards == "v1":
            type = descriptor.pop("type", None)
            profiles = descriptor.pop("profiles", None)
            descriptor["profile"] = "data-resource"
            if type == "table":
                descriptor["profile"] = "tabular-data-resource"
            elif profiles:
                descriptor["profile"] = profiles[0]

        # Stats (standards/v1)
        if system.standards == "v1":
            stats = descriptor.pop("stats", None)
            if stats:
                sha256 = stats.get("sha256")
                md5 = stats.get("md5")
                bytes = stats.get("bytes")
                if sha256 is not None:
                    descriptor["hash"] = f"sha256:{sha256}"
                if md5 is not None:
                    descriptor["hash"] = md5
                if bytes is not None:
                    descriptor["bytes"] = bytes

        return descriptor
