#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from subprocess import Popen, PIPE
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


def _decode_text(text):
    decoders = ["utf-8", "GBK"]
    for decoder in decoders:
        try:
            return text.decode(decoder)
        except UnicodeDecodeError:
            continue
    print("can't decode %s" % str(text))
    # Ignore not compatible characters
    return text.decode("utf-8", "ignore")


def _decode_stream(input_stream, output_stream, print_to_console = False):
    while True:
        line = input_stream.readline()
        if not line:
            break

        try:
            decoded_line = _decode_text(line)
            if print_to_console == True:
                # print(decoded_line, end="")
                sys.stdout.write(decoded_line)
        except Exception as e:
            raise e

        output_stream.write(decoded_line)


def run(command, cwd = None, print_to_console = False):
    if print_to_console == True:
        call_message = "\n----Running------\n> %s\n-----------------\n" % command
        print(call_message)

    if cwd == None:
        cwd = os.path.curdir
    
    try:
        proc = Popen(command, shell=True, stdout=PIPE,
                     stderr=PIPE, cwd=cwd)
    except Exception as e:
        raise Exception(
            "Error while executing '%s'\n\t%s" % (command, str(e)))
    
    stream_stdout = StringIO()
    stream_stderr = StringIO()
    _decode_stream(proc.stdout, stream_stdout, print_to_console)
    _decode_stream(proc.stderr, stream_stderr, print_to_console)

    proc.communicate()
    return_code = proc.returncode
    if return_code == 0:
        return (return_code, stream_stdout.getvalue())
    else:
        return (return_code, stream_stderr.getvalue())
