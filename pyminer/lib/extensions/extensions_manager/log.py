#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from utils import get_main_window


def log(text):
    """日志输出text"""
    # TODO (panhaoyu) 这个函数是否无用可删？
    get_main_window().slot_flush_console('info', 'Extension', 'Log:' + str(text))


def error(text):
    # TODO (panhaoyu) 这个函数是否无用可删？
    print("Error:", text)
    get_main_window().slot_flush_console(
        'error', 'Extension', 'Error:' + str(text))


def assert_(boolean, text):
    """
    boolean:bool
    text:str
    若bool为false,以异常级输出text
    """
    # TODO (panhaoyu) 这个函数是否无用可删？
    if not boolean:
        error(text)


class ColorHandler(logging.Handler):
    """部分关键词彩色，以及添加到日志控件中
    """

    Colors = {
        logging.DEBUG: 'black',
        logging.INFO: 'green',
        logging.WARNING: 'yellow',
        logging.ERROR: 'red',
        logging.CRITICAL: 'red'
    }

    def format(self, record):
        """
        Format the specified record.

        If a formatter is set, use it. Otherwise, use the default formatter
        for the module.
        """
        if self.formatter:
            fmt = self.formatter
        else:
            fmt = logging.Formatter()

        if fmt.usesTime():
            record.asctime = fmt.formatTime(record, fmt.datefmt)

        color = self.Colors.get(record.levelno, 'black')
        # record.asctime
        # record.name
        # record.module
        # record.funcName
        # record.lineno
        # record.levelname
        # record.message
        record.message = record.getMessage()

        s = fmt.formatMessage(record)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = fmt.formatException(record.exc_info)
        if record.exc_text:
            if not s.endswith('<br/>'):
                s += '<br/>'
            s += record.exc_text
        if record.stack_info:
            if not s.endswith('<br/>'):
                s += '<br/>'
            s += fmt.formatStack(record.stack_info)
        s = '<span style="color:{0};">{1}'.format(color, s.replace('\n', '<br/>').replace(' ', '&nbsp;'))
        return s

    def emit(self, record):
        """
        Emit a record.
        """
        try:
            msg = self.format(record)
            try:
                get_main_window().log_output_console.append(msg)
            except Exception:
                pass
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)