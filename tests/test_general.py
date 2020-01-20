import os
from tempfile import NamedTemporaryFile
import locale

from opentargets_urlzsource import URLZSource


def test_file():
    with URLZSource('tests/general.txt').open() as source:
        content = source.readlines()
        assert content == ["Foo"]


def test_file_gz():
    with URLZSource('tests/general.txt.gz').open() as source:
        content = source.readlines()
        assert content == ["Foo"]


def test_file_zip():
    with URLZSource('tests/general.txt.zip').open() as source:
        content = source.readlines()
        assert content == ["Foo"]


def test_url():
    url = "https://raw.githubusercontent.com/opentargets/urlzsource/master/tests/general.txt"
    with URLZSource(url).open() as source:
        content = source.readlines()
        assert content == ["Foo"]


def test_file_url():
    with URLZSource('file://./tests/general.txt').open() as source:
        content = source.readlines()
        assert content == ["Foo"]


def test_different_platform_encoding():
    """Parse the input as UTF-8 regardless of platform encoding."""
    f = NamedTemporaryFile(suffix='.txt', delete=False)
    try:
        f.write(b"F\xc3\xb8o\n")
        f.close()
        old_encoding_func = locale.getpreferredencoding
        locale.getpreferredencoding = lambda: "latin_1"
        try:
            with URLZSource(f.name).open() as source:
                content = source.readline()
                assert content.encode("UTF-8") == b"F\xc3\xb8o\n"
        finally:
            locale.getpreferredencoding = old_encoding_func
    finally:
        os.remove(f.name)
