import re

from PySide2.QtCore import QCoreApplication, QByteArray


def dataString(size):
    """
    存储控件转换
    Module function to generate a formatted size string.

    @param size size to be formatted
    @type int
    @return formatted data string
    @rtype str
    """
    if size < 1024:
        return QCoreApplication.translate(
            "Globals", "{0:4.2f} Bytes").format(size)
    elif size < 1024 * 1024:
        size /= 1024
        return QCoreApplication.translate(
            "Globals", "{0:4.2f} KiB").format(size)
    elif size < 1024 * 1024 * 1024:
        size /= 1024 * 1024
        return QCoreApplication.translate(
            "Globals", "{0:4.2f} MiB").format(size)
    elif size < 1024 * 1024 * 1024 * 1024:
        size /= 1024 * 1024 * 1024
        return QCoreApplication.translate(
            "Globals", "{0:4.2f} GiB").format(size)
    else:
        size /= 1024 * 1024 * 1024 * 1024
        return QCoreApplication.translate(
            "Globals", "{0:4.2f} TiB").format(size)


###############################################################################
## functions for version handling
###############################################################################


def versionToTuple(version, length=3):
    """
    将版本号转换为元组
    Module function to convert a version string into a tuple.

    Note: A version string consists of non-negative decimals separated by "."
    optionally followed by a suffix. Suffix is everything after the last
    decimal.

    @param version version string
    @type str
    @param length desired length of the version tuple
    @type int
    @return version tuple without the suffix
    @rtype tuple of int
    """
    versionParts = []

    # step 1: extract suffix
    version = re.split(r"[^\d.]", version)[0]
    for part in version.split("."):
        try:
            versionParts.append(int(part.strip()))
        except ValueError:
            # skip non-integer parts
            pass
    versionParts.extend([0] * length)

    return tuple(versionParts[:length])


def strToQByteArray(txt):
    """
    Module function to convert a Python string into a QByteArray.

    @param txt Python string to be converted
    @type str, bytes, bytearray
    @return converted QByteArray
    @rtype QByteArray
    """
    if isinstance(txt, str):
        txt = txt.encode("utf-8")

    return QByteArray(txt)

# ###############################################################################
# ## functions for converting QSetting return types to valid types
# ###############################################################################
#
#
# def toBool(value):
#     """
#     Module function to convert a value to bool.
#
#     @param value value to be converted
#     @return converted data
#     """
#     if value in ["true", "1", "True"]:
#         return True
#     elif value in ["false", "0", "False"]:
#         return False
#     else:
#         return bool(value)
#
#
# def toList(value):
#     """
#     Module function to convert a value to a list.
#
#     @param value value to be converted
#     @return converted data
#     """
#     if value is None:
#         return []
#     elif not isinstance(value, list):
#         return [value]
#     else:
#         return value
#
#
def toByteArray(value):
    """
    Module function to convert a value to a byte array.

    @param value value to be converted
    @return converted data
    """
    if value is None:
        return QByteArray()
    else:
        return value


def toDict(value):
    """
    Module function to convert a value to a dictionary.

    @param value value to be converted
    @return converted data
    """
    if value is None:
        return {}
    else:
        return value
