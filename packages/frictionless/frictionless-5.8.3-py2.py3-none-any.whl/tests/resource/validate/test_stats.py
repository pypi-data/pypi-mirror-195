import pytest
from frictionless import Resource, platform


# General


@pytest.mark.skipif(platform.type == "windows", reason="Fix on Windows")
def test_resource_validate_stats_hash():
    hash = "sha256:a1fd6c5ff3494f697874deeb07f69f8667e903dd94a7bc062dd57550cea26da8"
    resource = Resource("data/table.csv", hash=hash)
    report = resource.validate()
    assert report.task.valid


@pytest.mark.skipif(platform.type == "windows", reason="Fix on Windows")
def test_resource_validate_stats_hash_invalid():
    hash = "6c2c61dd9b0e9c6876139a449ed87933"
    resource = Resource("data/table.csv", hash="bad")
    report = resource.validate()
    assert report.flatten(["type", "note"]) == [
        [
            "hash-count",
            'expected is "bad" and actual is "%s"' % hash,
        ],
    ]


@pytest.mark.skipif(platform.type == "windows", reason="Fix on Windows")
def test_resource_validate_stats_bytes():
    resource = Resource("data/table.csv", bytes=30)
    report = resource.validate()
    assert report.task.valid


@pytest.mark.skipif(platform.type == "windows", reason="Fix on Windows")
def test_resource_validate_stats_bytes_invalid():
    resource = Resource("data/table.csv", bytes=40)
    report = resource.validate()
    assert report.task.error.to_descriptor().get("rowNumber") is None
    assert report.task.error.to_descriptor().get("fieldNumber") is None
    assert report.flatten(["type", "note"]) == [
        ["byte-count", 'expected is "40" and actual is "30"'],
    ]


@pytest.mark.skipif(platform.type == "windows", reason="Fix on Windows")
def test_resource_validate_stats_rows():
    resource = Resource("data/table.csv", rows=2)
    report = resource.validate()
    assert report.task.valid


@pytest.mark.skipif(platform.type == "windows", reason="Fix on Windows")
def test_resource_validate_stats_rows_invalid():
    resource = Resource("data/table.csv", rows=3)
    report = resource.validate()
    assert report.task.error.to_descriptor().get("rowNumber") is None
    assert report.task.error.to_descriptor().get("fieldNumber") is None
    assert report.flatten(["type", "note"]) == [
        ["row-count", 'expected is "3" and actual is "2"'],
    ]


def test_resource_validate_stats_not_supported_hash_algorithm():
    resource = Resource.from_descriptor(
        {
            "name": "name",
            "path": "data/table.csv",
            "hash": "sha1:db6ea2f8ff72a9e13e1d70c28ed1c6b42af3bb0e",
        }
    )
    report = resource.validate()
    assert report.task.warnings == ["hash is ignored; supported algorithms: md5/sha256"]
