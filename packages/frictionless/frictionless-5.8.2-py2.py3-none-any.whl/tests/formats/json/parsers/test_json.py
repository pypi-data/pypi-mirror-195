import json
import pytest
from frictionless import Resource, formats, resources


BASEURL = "https://raw.githubusercontent.com/frictionlessdata/frictionless-py/master/%s"


# Read


def test_json_parser():
    with resources.TableResource(path="data/table.json") as resource:
        assert resource.header == ["id", "name"]
        assert resource.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


def test_json_parser_keyed():
    with resources.TableResource(path="data/table.keyed.json") as resource:
        assert resource.dialect.to_descriptor() == {"json": {"keyed": True}}
        assert resource.header == ["id", "name"]
        assert resource.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


def test_json_parser_keyed_with_keys_provided():
    control = formats.JsonControl(keys=["name", "id"])
    with resources.TableResource(
        path="data/table.keyed.json", control=control
    ) as resource:
        assert resource.dialect.to_descriptor() == {
            "json": {"keyed": True, "keys": ["name", "id"]}
        }
        assert resource.header == ["name", "id"]
        assert resource.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


def test_json_parser_from_buffer():
    source = '[["id", "name"], [1, "english"], [2, "中国人"]]'.encode("utf-8")
    with resources.TableResource(source, format="json") as resource:
        assert resource.header == ["id", "name"]
        assert resource.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


def test_json_parser_from_buffer_keyed():
    source = '[{"id": 1, "name": "english" }, {"id": 2, "name": "中国人" }]'.encode("utf-8")
    with resources.TableResource(source, format="json") as resource:
        assert resource.dialect.to_descriptor() == {"json": {"keyed": True}}
        assert resource.header == ["id", "name"]
        assert resource.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


@pytest.mark.vcr
def test_json_parser_from_remote():
    with resources.TableResource(path=BASEURL % "data/table.json") as resource:
        assert resource.header == ["id", "name"]
        assert resource.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


@pytest.mark.vcr
def test_json_parser_from_remote_keyed():
    with resources.TableResource(path=BASEURL % "data/table.keyed.json") as resource:
        assert resource.dialect.to_descriptor() == {"json": {"keyed": True}}
        assert resource.header == ["id", "name"]
        assert resource.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


# Write


def test_json_parser_write(tmpdir):
    source = Resource("data/table.csv")
    target = resources.TableResource(path=str(tmpdir.join("table.json")))
    target = source.write(target)
    assert target.normpath
    with open(target.normpath) as file:
        assert json.load(file) == [
            ["id", "name"],
            [1, "english"],
            [2, "中国人"],
        ]


def test_json_parser_write_decimal(tmpdir):
    control = formats.JsonControl(keyed=True)
    source = Resource([["id", "name"], [1.5, "english"], [2.5, "german"]])
    target = resources.TableResource(path=str(tmpdir.join("table.json")), control=control)
    target = source.write(target)
    assert target.normpath
    with open(target.normpath) as file:
        assert json.load(file) == [
            {"id": "1.5", "name": "english"},
            {"id": "2.5", "name": "german"},
        ]


def test_json_parser_write_keyed(tmpdir):
    control = formats.JsonControl(keyed=True)
    source = Resource("data/table.csv")
    target = resources.TableResource(path=str(tmpdir.join("table.json")), control=control)
    target = source.write(target)
    assert target.normpath
    with open(target.normpath) as file:
        assert json.load(file) == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]
