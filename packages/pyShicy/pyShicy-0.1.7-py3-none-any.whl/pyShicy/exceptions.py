"""
Exceptions which can be raised by py-Shicy Itself.
"""


class pyShicyError(Exception):
    ...


class PyrogramMissingError(ImportError):
    ...


class TelethonMissingError(ImportError):
    ...


class DependencyMissingError(ImportError):
    ...


class RunningAsFunctionLibError(pyShicyError):
    ...


class SpamFailed(Exception):
    ...


class DownloadFailed(Exception):
    ...


class DelAllFailed(Exception):
    ...


class FFmpegReturnCodeError(Exception):
    ...
