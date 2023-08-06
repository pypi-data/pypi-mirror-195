# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2023)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import datetime as dttm
import logging as lggg
import platform as pltf
import sys as sstm
import time
from pathlib import Path as path_t
from typing import Any, Callable, ClassVar, Dict, Union

from rich.color import Color as color_t
from rich.console import Console as console_t
from rich.style import Style as style_t
from rich.text import Text as text_t

try:
    from psutil import Process as process_t

    _PROCESS = process_t()
    _GIGA_SCALING = 1.0 / (1024**3)

    def UsedMemoryInGb() -> float:
        """"""
        return round(_GIGA_SCALING * _PROCESS.memory_info().rss, 1)

except ModuleNotFoundError:
    _PROCESS = None

    def UsedMemoryInGb() -> float:
        """"""
        return 0.0


# This module is certainly imported early. Therefore, the current time should be close enough to the real start time.
_START_TIME = time.time()


_MESSAGE_FORMAT = (
    "%(asctime)s[%(levelname)s]\t- "
    "%(message)s @ "
    "%(module)s:%(funcName)s:%(lineno)d"
)
_DATE_FORMAT = "%Y-%m-%d@%H:%M:%S"

_SYSTEM_DETAILS = (
    "node",
    "machine",
    "processor",
    "architecture",
    #
    "system",
    "release",
    "version",
    "platform",
    #
    "python_implementation",
    "python_version",
    "python_revision",
    "python_branch",
    "python_compiler",
    "python_build",
)
_SYSTEM_DETAILS = {_dtl.capitalize(): getattr(pltf, _dtl)() for _dtl in _SYSTEM_DETAILS}
_MAX_DETAIL_NAME_LENGTH = max(map(len, _SYSTEM_DETAILS.keys()))


# TODO: might be simpler/better to use filters (https://devdocs.io/python~3.10/howto/logging-cookbook#context-info) or a
#     logging.LoggerAdapter
class _handler_extension:
    formatter: lggg.Formatter = None
    show_memory_usage: bool = False

    def __init__(self) -> None:
        """"""
        self.formatter = lggg.Formatter(fmt=_MESSAGE_FORMAT, datefmt=_DATE_FORMAT)


class console_handler_t(lggg.Handler, _handler_extension):
    _LEVEL_COLOR: ClassVar[Dict[int, Union[str, style_t]]] = {
        lggg.DEBUG: "orchid",
        lggg.INFO: "white",
        lggg.WARNING: "yellow",
        lggg.ERROR: "orange3",
        lggg.CRITICAL: "red",
    }
    _GRAY_STYLE: ClassVar[style_t] = style_t(color=color_t.from_rgb(150, 150, 150))
    _ACTUAL: ClassVar[str] = r" Actual=[^.]+\."
    _EXPECTED: ClassVar[str] = r" Expected([!<>]=|: )[^.]+\."

    console: console_t = None

    def __init__(self, /, *, level=lggg.NOTSET) -> None:
        """"""
        lggg.Handler.__init__(self, level=level)
        _handler_extension.__init__(self)

        self.setFormatter(self.formatter)
        self.console = console_t(
            record=True, force_terminal=True, width=1000, tab_size=5
        )

    def emit(self, record: lggg.LogRecord, /) -> None:
        """"""
        cls = self.__class__

        formatted = self.formatter.format(record)
        if self.show_memory_usage:
            memory_usage = f" :{UsedMemoryInGb()}Gb"
        else:
            memory_usage = ""
        if "\n" in formatted:
            lines = formatted.splitlines()
            highlighted = text_t(lines[0])
            highlighted.append(f" +{ElapsedTime()}{memory_usage}\n", style="green")
            highlighted.append("    " + "\n    ".join(lines[1:]))
        else:
            highlighted = text_t(formatted)
            highlighted.append(f" +{ElapsedTime()}{memory_usage}", style="green")

        highlighted.stylize("dodger_blue2", end=19)
        highlighted.highlight_words(
            (f"[{record.levelname}]",), style=cls._LEVEL_COLOR[record.levelno]
        )
        highlighted.highlight_regex(
            f"@ {record.module}:{record.funcName}:{record.lineno}",
            style=cls._GRAY_STYLE,
        )
        highlighted.highlight_regex(cls._ACTUAL, style="red")
        highlighted.highlight_regex(cls._EXPECTED, style="green")

        self.console.print(highlighted)


class file_handler_t(lggg.FileHandler, _handler_extension):
    def __init__(self, file: str, *args, **kwargs) -> None:
        """"""
        lggg.FileHandler.__init__(self, file, *args, **kwargs)
        _handler_extension.__init__(self)

        self.setFormatter(self.formatter)

    def emit(self, record: lggg.LogRecord, /) -> None:
        """"""
        formatted = self.formatter.format(record)
        if self.show_memory_usage:
            memory_usage = f" :{UsedMemoryInGb()}Gb"
        else:
            memory_usage = ""
        if "\n" in formatted:
            lines = formatted.splitlines()
            next_lines = "\n    ".join(lines[1:])
            message = f"{lines[0]} +{ElapsedTime()}{memory_usage}\n    {next_lines}"
        else:
            message = f"{formatted} +{ElapsedTime()}{memory_usage}"

        print(message, file=self.stream)
        self.stream.flush()


LOGGER = lggg.getLogger(name="color_w_rich")
LOGGER.setLevel(lggg.INFO)  # Minimum desired level
LOGGER.addHandler(console_handler_t())


def SetShowMemoryUsage(show_memory_usage: bool, /) -> None:
    """"""
    if show_memory_usage and (_PROCESS is None):
        LOGGER.warning('Cannot show memory usage: Package "psutil" not installed')
        return

    for handler in LOGGER.handlers:
        if hasattr(handler, "show_memory_usage"):
            handler.show_memory_usage = show_memory_usage


def AddFileHandler(file: Union[str, path_t], /) -> None:
    """"""
    if file.exists():
        raise ValueError(f"{file}: File already exists")

    LOGGER.addHandler(file_handler_t(file))


def SaveLOGasHTML(file: Union[str, path_t], /) -> None:
    """"""
    if file.exists():
        raise ValueError(f"{file}: File already exists")

    console = None
    found = False
    for handler in LOGGER.handlers:
        console = getattr(handler, "console", None)
        if found := isinstance(console, console_t):
            break
    if found:
        with open(file, "w") as accessor:
            accessor.write(console.export_html())

    raise ValueError("Cannot save logging record as HTML: Handler has no RICH console")


def WhereFunction(function: Any, /) -> str:
    """"""
    return f"{function.__module__}:{function.__name__}"


def WhereMethod(obj: Any, method: Callable, /) -> str:
    """
    method: Could be a str instead, which would require changing method.__name__ into getattr(cls, method). But if the
        method name changes while forgetting to change the string in the call to WhereMethod accordingly, then an
        exception would be raised here.
    """
    cls = obj.__class__

    return f"{cls.__module__}:{cls.__name__}:{method.__name__}"


def LogSystemDetails() -> None:
    """"""
    details = "\n".join(
        f"    {_key:>{_MAX_DETAIL_NAME_LENGTH}}: {_vle}"
        for _key, _vle in _SYSTEM_DETAILS.items()
    )

    modules = sstm.modules
    with_versions = []
    for name in modules.keys():
        if name.startswith("_") or ("." in name):
            continue

        module = modules[name]
        version = getattr(module, "__version__", None)
        if version is not None:
            with_versions.append(f"{name}={version}")
    modules = ", ".join(with_versions)

    LOGGER.info(
        f"SYSTEM DETAILS\n"
        f"{details}\n"
        f"    {'Python Modules':>{_MAX_DETAIL_NAME_LENGTH}}:\n"
        f"    {modules}"
    )


def TimeStamp() -> str:
    """"""
    return (
        dttm.datetime.now()
        .isoformat(timespec="milliseconds")
        .replace(".", "-")
        .replace(":", "-")
    )


def ElapsedTime() -> str:
    """"""
    output = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - _START_TIME))
    while output.startswith("00") and (" " in output):
        output = output.split(maxsplit=1)[-1]

    return output
