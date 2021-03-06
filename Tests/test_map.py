import sys

import pytest
from PIL import Image

from .helper import is_win32

try:
    import numpy
except ImportError:
    numpy = None

pytestmark = pytest.mark.skipif(is_win32(), reason="Win32 does not call map_buffer")


def test_overflow():
    # There is the potential to overflow comparisons in map.c
    # if there are > SIZE_MAX bytes in the image or if
    # the file encodes an offset that makes
    # (offset + size(bytes)) > SIZE_MAX

    # Note that this image triggers the decompression bomb warning:
    max_pixels = Image.MAX_IMAGE_PIXELS
    Image.MAX_IMAGE_PIXELS = None

    # This image hits the offset test.
    with Image.open("Tests/images/l2rgb_read.bmp") as im:
        with pytest.raises((ValueError, MemoryError, IOError)):
            im.load()

    Image.MAX_IMAGE_PIXELS = max_pixels


@pytest.mark.skipif(sys.maxsize <= 2 ** 32, reason="Requires 64-bit system")
@pytest.mark.skipif(numpy is None, reason="NumPy is not installed")
def test_ysize():
    # Should not raise 'Integer overflow in ysize'
    arr = numpy.zeros((46341, 46341), dtype=numpy.uint8)
    Image.fromarray(arr)
