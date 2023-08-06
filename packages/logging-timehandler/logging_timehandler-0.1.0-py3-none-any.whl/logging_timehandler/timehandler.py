import os
import re
import time
import pathlib
import logging

class TimeHandler(logging.FileHandler):
    def __init__(self, format, mode: str = "a", encoding: str = None, delay: bool = False, errors: str = None, retain: int = 5) -> None:
        self.retain = retain
        self.last_logpath = None
        self.log_format = pathlib.Path(format)
        self.log_root = self.get_logroot()
        self.log_pattern = re.sub('%\w', '.*', str(self.log_format.name))
        logging.FileHandler.__init__(self, format, mode, encoding, delay)
    def is_log_file(self, path: pathlib.Path) -> bool:
        return re.match(self.log_pattern, str(path)) is not None
    def get_logroot(self) -> pathlib.Path:
        last_part = None
        for part in self.log_format.parts:
            if '%' in part:
                return last_part
            if last_part is None:
                last_part = pathlib.Path(part)
            else:
                last_part = last_part.joinpath(part)
        return self.log_format.parent
    def get_logpath(self):
        return pathlib.Path(time.strftime(str(self.log_format), time.localtime()))
    def get_logfiles(self):
        logfiles = []
        for root, dirs, files in os.walk(self.log_root):
            for file in files:
                path = pathlib.Path(root).joinpath(file).absolute()
                if self.is_log_file(path):
                    logfiles.append(path)
        logfiles.sort()
        return logfiles
    def _open(self):
        logpath = self.get_logpath()
        self.last_logpath = logpath
        if not logpath.parent.exists():
            os.makedirs(logpath.parent)
        logfiles = self.get_logfiles()
        if not logpath.exists():
            logfiles = self.get_logfiles()
            for logfile in logfiles[:max(len(logfiles) - self.retain + 1, 0)]:
                os.remove(logpath.parent.joinpath(logfile))
        return open(logpath, self.mode, encoding=self.encoding)
    def emit(self, record) -> None:
        if self.last_logpath != self.get_logpath():
            self.stream = self._open()
        return super().emit(record)