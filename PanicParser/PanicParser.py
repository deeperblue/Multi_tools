#!/usr/bin/python
#coding=utf-8

import os
import sys
import getpass
import string
import codecs
import datetime
import time
import codecs
import subprocess
from sys import version_info

showLog=False
CALL_STACK_ADDR_PREFIX="addr:"
PANIC_ADDR_PREFIX="MCSRR0(Address): 0x"
DEBUG_ELF_PATH_DEFAULT="C:\zongmu\work\Panic_Z4\Debug_RAM\Panic_Z4.elf"

#ELF_PATH_DEFAULT="c:\zongmu\work\\radar\Radar_S32R274_TEF810X_Z4\Debug\Radar_S32R274_TEF810X_Z4.elf"
ELF_PATH_DEFAULT="C:\zongmu\work\PanicParser\Radar.elf"
#ELF_PATH_DEFAULT="c:\zongmu\work\\radar\Radar_S32R274_TEF810X_Z7_0\Debug\Radar_S32R274_TEF810X_Z7_0.elf"

STACK_TRACE_LIST=[]

def show_str(str):
    print("\033[1;31;40m %s \033[0m" %(str))


def show_err(str):
    print("\033[1;31;40m %s \033[0m" %(str))


def run_command(cmd, showLog=True):
    devNull = open(os.devnull, 'w')
    if showLog:
        show_str(cmd)
    try:
        #ret =subprocess.call(cmd, shell=True, stdout=devNull)
        ret=subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        pass
    return ret

def Parser_StackParse(elf_file_name, panic_str):
    for line in panic_str.splitlines():
        offset = line.find(CALL_STACK_ADDR_PREFIX)
        if offset != -1:
           start_idx = offset + len(CALL_STACK_ADDR_PREFIX)+1
           ret_code =run_command("powerpc-eabivle-addr2line.exe -f -e "+ elf_file_name + " 0x" + line[start_idx:start_idx+8])
           if version_info.major == 3:
            STACK_TRACE_LIST.append(str(ret_code, encoding="utf-8").replace("\r\n", "  "))
           else:
               STACK_TRACE_LIST.append(str(ret_code).replace("\r\n", "  "))


def Parser_PanicAddrParse(elf_file_name, panic_str):
    for line in panic_str.splitlines():
        offset = line.find(PANIC_ADDR_PREFIX)
        if offset != -1:
           start_idx = offset + len(PANIC_ADDR_PREFIX)
           print("%s" %(line[start_idx:start_idx+8]))
           ret_code=run_command("powerpc-eabivle-addr2line.exe -f -e "+ elf_file_name + " 0x" + line[start_idx:start_idx+8])
           if version_info.major == 3:
               STACK_TRACE_LIST.append(str(ret_code, encoding="utf-8").replace("\r\n", "  "))
           else:
               STACK_TRACE_LIST.append(str(ret_code).replace("\r\n", "  "))



def ParserDbgtext(filename):
    file_str=""
    f = codecs.open(filename, "r", "utf-8",  'replace')

    file = f.readlines()
    for line in file:
        file_str+=line.replace("\n", "").replace("...", "\r\n").replace("..", "\r\n")
    print("%s" %(file_str))
    f.close
    print("===========================")
    Parser_PanicAddrParse(DEBUG_ELF_PATH_DEFAULT, file_str)
    Parser_StackParse(DEBUG_ELF_PATH_DEFAULT, file_str)

def ParserNormaltext(filename):
    file_str=""
    f = codecs.open(filename, "r", "utf-8",  'replace')

    file = f.readlines()
    for line in file:
        Parser_PanicAddrParse(ELF_PATH_DEFAULT, line)
    for line in file:
        Parser_StackParse(ELF_PATH_DEFAULT, line)
    f.close
    print("===========================")
    print("CallStack Trace:")
    PREFIX = ""
    for line in STACK_TRACE_LIST:
        print("%s -> %s" %(PREFIX, line))
        PREFIX+=" "

def do_dumpdbg():
    ParserDbgtext("dbg_text.txt")

def do_dump():
    ParserNormaltext("dbg_text.txt")

def do_help():
    print(ACTIONS.keys())

ACTIONS = {
"dumpdbg":do_dumpdbg,
"dump":do_dump,
"help":do_help
}

#main
if __name__ == "__main__":
    if len(sys.argv) > 2:
        ACTIONS.get(sys.argv[1])()
    else:
        do_help()
    exit
