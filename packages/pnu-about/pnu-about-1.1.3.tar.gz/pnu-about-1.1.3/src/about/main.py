#!/usr/bin/env python3
""" about - Show system information
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import getopt
import getpass
import locale
import logging
import os
import platform
import re
import shutil
import socket
import string
import sys
import sysconfig
import unicodedata

import libpnu

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: about - Show system information v1.1.3 (March 3, 2023) by Hubert Tournier $"

# Unix dependencies:
try:
    import pwd
    import grp
except ModuleNotFoundError:
    pass

# Optional dependency upon py-cpuinfo
# Use "pip install py-cpuinfo" to install
try:
    import cpuinfo
except ModuleNotFoundError:
    pass

# Default parameters. Can be superseded by command line options
parameters = {
    "Environment": False,
    "Hardware": False,
    "Operating System": False,
    "Python": False,
    "System": False,
    "User": False,
}


####################################################################################################
def _display_help():
    """ Displays usage and help """
    #pylint: disable=C0301
    print()
    print("usage: about [-d|--debug] [-h|--help|-?] [-v|--version] [-a|--all]")
    print("       [-E|--env|--environment] [-H|--hw|--hardware] [-O|--os|--operating]")
    print("       [-P|--py|--python] [-S|--sys|--system] [-U|--user] [--]")
    print("  ----------------------  ---------------------------------------------")
    print("  -a|--all                Same as -SUHOEP")
    print("  -E|--env|--environment  Show information about the environment")
    print("  -H|--hw|--hardware      Show information about the hardware")
    print("  -O|--os|--operating     Show information about the Operating System")
    print("  -P|--py|--python        Show information about Python")
    print("  -S|--sys|--system       Show information about the system")
    print("  -U|--user               Show information about the user")
    print("  -d|--debug              Enable debug mode")
    print("  -h|--help|-?            Print usage and this help message and exit")
    print("  -v|--version            Print version and exit")
    print("  --                      Options processing terminator")
    print()
    #pylint: enable=C0301


####################################################################################################
#pylint: disable=W0613
def _handle_interrupts(signal_number, current_stack_frame):
    """ Prevent SIGINT signals from displaying an ugly stack trace """
    print(" Interrupted!\n", file=sys.stderr)
    sys.exit(0)
#pylint: enable=W0613


####################################################################################################
def _process_command_line():
    """ Process command line """
    #pylint: disable=C0103, W0602
    global parameters
    #pylint: enable=C0103, W0602

    try:
        # option letters followed by : expect an argument
        # same for option strings followed by =
        options, remaining_arguments = getopt.getopt(
            sys.argv[1:],
            "adhvHOSEPU?",
            [
                "all",
                "debug",
                "env",
                "environment",
                "everything",
                "hardware",
                "help",
                "hw",
                "life",
                "operating",
                "os",
                "py",
                "python",
                "sys",
                "system",
                "universe",
                "user",
                "version",
            ],
        )
    except getopt.GetoptError as error:
        logging.critical("Syntax error: %s", error)
        _display_help()
        sys.exit(1)

    for option, _ in options:

        if option in ("-a", "--all"):
            parameters["Environment"] = True
            parameters["Hardware"] = True
            parameters["Operating System"] = True
            parameters["Python"] = True
            parameters["System"] = True
            parameters["User"] = True

        elif option in ("-E", "--env", "--environment"):
            parameters["Environment"] = True

        elif option in ("-H", "--hw", "--hardware"):
            parameters["Hardware"] = True

        elif option in ("-O", "--os", "--operating"):
            parameters["Operating System"] = True

        elif option in ("-P", "--py", "--python"):
            parameters["Python"] = True

        elif option in ("-S", "--sys", "--system"):
            parameters["System"] = True

        elif option in ("-U", "--user"):
            parameters["User"] = True

        elif option in ("--life", "--universe"):
            print("42!")
            sys.exit(42)

        elif option == "--everything":
            print("Mamma mia!")
            sys.exit(88)

        elif option in ("-d", "--debug"):
            logging.disable(logging.NOTSET)

        elif option in ("-h", "--help", "-?"):
            _display_help()
            sys.exit(0)

        elif option in ("-v", "--version"):
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

    logging.debug("_process_commandline(): parameters:")
    logging.debug(parameters)
    logging.debug("_process_commandline(): remaining_arguments:")
    logging.debug(remaining_arguments)

    return remaining_arguments


####################################################################################################
def printm(first_line, results):
    """ Multi-lines print """
    print(first_line + ":")
    print(">>>>>>>>>>")
    if isinstance(results, list):
        for line in results:
            print(line)
    elif isinstance(results, dict):
        for key, value in results.items():
            print(f"{key}={value}")
    else:
        print(results)
    print("<<<<<<<<<<")


####################################################################################################
# Possible values derived from https://hg.python.org/cpython/file/3.5/Lib/platform.py
def sys_type():
    """ Return (approximate) system type """
    operating_system_type = platform.system()
    if operating_system_type in (
        "FreeBSD",
        "NetBSD",
        "OpenBSD",
        "Linux",
        "Darwin",
        "MacOS X Server",
        "Solaris",
    ):
        return "Unix"

    return operating_system_type


####################################################################################################
def grep(filename, pattern):
    """ Search a string in a file """
    regexp = re.compile(pattern)
    results = []
    with open(filename, encoding="utf-8", errors="ignore") as file:
        lines = file.readlines()
        for line in lines:
            result = regexp.match(line)
            if result:
                results.append(line.strip())

    return results


####################################################################################################
def about_local_system():
    """ Show information about the local system """
    if parameters["System"]:
        print("[System]")
        if sys_type() == "Unix":
            print(f"os.uname().nodename={os.uname().nodename}")
        hostname = socket.gethostname()
        print(f"socket.gethostname()={hostname}")
        print(f"socket.getfqdn()={socket.getfqdn()}")
        print(f"socket.gethostbyname('{hostname}')={socket.gethostbyname(hostname)}")
        print(f"socket.gethostbyname_ex('{hostname}')={socket.gethostbyname_ex(hostname)}")
        print()

        print("[System/Network]")
        print(f"socket.if_nameindex()={socket.if_nameindex()}")
        print(f"socket.getdefaulttimeout()={socket.getdefaulttimeout()}")
        print(f"socket.has_dualstack_ipv6()={socket.has_dualstack_ipv6()}")
        print()


####################################################################################################
def about_user():
    """ Show information about the user """
    if parameters["User"]:
        print("[User]")
        user = getpass.getuser()
        print(f"getpass.getuser()={user}")
        print(f"os.getlogin()={os.getlogin()}")
        if sys_type() == "Unix":
            print(f'pwd.getpwnam("{user}")={pwd.getpwnam(user)}')
            print(f"os.getgroups()={os.getgroups()}")
            for group_id in os.getgroups():
                print(f"grp.getgrgid({group_id})={grp.getgrgid(group_id)}")
        elif sys_type() == "Windows":
            if "USERNAME" in os.environ:
                print(f"os.environ['USERNAME']={os.environ['USERNAME']}")
            if "USERPROFILE" in os.environ:
                print(f"os.environ['USERPROFILE']={os.environ['USERPROFILE']}")
            if "USERDOMAIN" in os.environ:
                print(f"os.environ['USERDOMAIN']={os.environ['USERDOMAIN']}")
            if "USERDOMAIN_ROAMINGPROFILE" in os.environ:
                print("os.environ['USERDOMAIN_ROAMINGPROFILE']"
                      + f"={os.environ['USERDOMAIN_ROAMINGPROFILE']}")
            if "HOME" in os.environ:
                print(f"os.environ['HOME']={os.environ['HOME']}")
            if "HOMEDRIVE" in os.environ:
                print(f"os.environ['HOMEDRIVE']={os.environ['HOMEDRIVE']}")
            if "HOMEPATH" in os.environ:
                print(f"os.environ['HOMEPATH']={os.environ['HOMEPATH']}")
        print()

        print("[User/Process]")
        if sys_type() == "Unix":
            print(f"os.getuid()={os.getuid()}")
            print(f"os.getgid()={os.getgid()}")
            print(f"os.geteuid()={os.geteuid()}")
            print(f"os.getegid()={os.getegid()}")
            print(f"os.getresuid()={os.getresuid()}")
            print(f"os.getresgid()={os.getresgid()}")
        print()

        print("[Process]")
        pid = os.getpid()
        print(f"os.getpid()={pid}")
        print(f"os.getppid()={os.getppid()}")
        if sys_type() == "Unix":
            print(f"os.getpgid({pid})={os.getpgid(pid)}")
            print(f"os.getpgrp()={os.getpgrp()}")
            print(f"os.getpriority(os.PRIO_PROCESS, 0)={os.getpriority(os.PRIO_PROCESS, 0)}")
            print(f"os.getpriority(os.PRIO_PGRP, 0)={os.getpriority(os.PRIO_PGRP, 0)}")
            print(f"os.getpriority(os.PRIO_USER, 0)={os.getpriority(os.PRIO_USER, 0)}")
        print()


####################################################################################################
def about_hardware():
    """ Show information about the hardware """
    if parameters["Hardware"]:
        print("[Hardware]")
        if sys_type() == "Unix":
            print(f"os.uname().machine={os.uname().machine}")
        print(f"platform.machine()={platform.machine()}")
        print(f"platform.processor()={platform.processor()}")
        print(f"os.cpu_count()={os.cpu_count()}")
        print(f"sys.byteorder={sys.byteorder}")
        if platform.system() == "FreeBSD":
            printm(
                "/var/run/dmesg.boot scan",
                grep("/var/run/dmesg.boot", "^(CPU: |FreeBSD/SMP: |real memory  =)"),
            )
        elif sys_type() == "Windows":
            if "NUMBER_OF_PROCESSORS" in os.environ:
                print(f"os.environ['NUMBER_OF_PROCESSORS']={os.environ['NUMBER_OF_PROCESSORS']}")
            if "PROCESSOR_ARCHITECTURE" in os.environ:
                print("os.environ['PROCESSOR_ARCHITECTURE']"
                      + f"={os.environ['PROCESSOR_ARCHITECTURE']}")
            if "PROCESSOR_IDENTIFIER" in os.environ:
                print(f"os.environ['PROCESSOR_IDENTIFIER']={os.environ['PROCESSOR_IDENTIFIER']}")
            if "PROCESSOR_LEVEL" in os.environ:
                print(f"os.environ['PROCESSOR_LEVEL']={os.environ['PROCESSOR_LEVEL']}")
            if "PROCESSOR_REVISION" in os.environ:
                print(f"os.environ['PROCESSOR_REVISION']={os.environ['PROCESSOR_REVISION']}")
        print()

        print("[Hardware/cpuinfo optional module]")
        try:
            for key, value in cpuinfo.get_cpu_info().items():
                print(f"{key}: {value}")
        except NameError:
            print("# For more detailed (and portable) CPU information do:")
            print("# pip install py-cpuinfo ; cpuinfo")
        print()

        print("[Hardware/Disk usage]")
        if sys_type() == "Unix":
            if os.path.exists("/etc/fstab"):
                with open("/etc/fstab", encoding="utf-8", errors="ignore") as file:
                    for line in file.readlines():
                        line = line.strip()
                        if not line.startswith("#"):
                            fields = line.split()
                            if fields[1] != "none":
                                print(f"File system={fields[0]}   Mount point={fields[1]}")
                                print(f"  shutil.disk_usage('{fields[1]}')"
                                      + f"={shutil.disk_usage(fields[1])}")
        elif sys_type() == "Windows":
            for letter in string.ascii_uppercase:
                drive = letter + ":\\"
                if os.path.exists(drive):
                    print(f"  shutil.disk_usage('{drive}')={shutil.disk_usage(drive)}")
        print()


####################################################################################################
def about_operating_system():
    """ Show information about the operating system """
    if parameters["Operating System"]:
        print("[Operating system]")
        print(f"os.name={os.name}")
        print(f"platform.system()={platform.system()}")
        print(f"platform.release()={platform.release()}")
        print(f"sys.platform={sys.platform}")
        print(f"sysconfig.get_platform()={sysconfig.get_platform()}")
        print(f"platform.platform()={platform.platform()}")
        print(f"platform.version()={platform.version()}")
        print(f"platform.uname()={platform.uname()}")
        if sys_type() == "Unix":
            print(f"os.uname().sysname={os.uname().sysname}")
            print(f"os.uname().release={os.uname().release}")
            print(f"os.uname().version={os.uname().version}")
        elif sys_type() == "Windows":
            print(f"sys.getwindowsversion()={sys.getwindowsversion()}")
            print(f"platform.win32_ver()={platform.win32_ver()}")
            print(f"platform.win32_edition()={platform.win32_edition()}")
            print(f"platform.win32_is_iot()={platform.win32_is_iot()}")
        print()

        if sys_type() == "Unix":
            print("[Operating system/Configuration]")
            for name in os.confstr_names:
                try:
                    print(f"os.confstr('{name}')={os.confstr(name)}")
                except OSError as error:
                    print(f"os.confstr('{name}')={'Error: ' + str(error)}")
            for name in os.sysconf_names:
                try:
                    print(f"os.sysconf('{name}')={os.sysconf(name)}")
                except OSError as error:
                    print(f"os.sysconf('{name}')={'Error: ' + str(error)}")
            print()

        print("[Operating system/Portability]")
        print(f"os.curdir={os.curdir}")
        print(f"os.pardir={os.pardir}")
        print(f"os.sep={os.sep}")
        print(f"os.altsep={os.altsep}")
        print(f"os.extsep={os.extsep}")
        print(f"os.pathsep={os.pathsep}")
        print(f"os.defpath={os.defpath}")
        print(f"os.devnull={os.devnull}")
        print(f"os.linesep={os.linesep}")


####################################################################################################
def about_environment():
    """ Show information about the environment """
    if parameters["Environment"]:
        print("[Environment]")
        print(f"os.getcwd()={os.getcwd()}")
        printm("dict(os.environ)", dict(os.environ))
        print(f"os.supports_bytes_environ={os.supports_bytes_environ}")
        print(f"shutil.get_terminal_size()={shutil.get_terminal_size()}")
        print(f"sys.prefix={sys.prefix}")
        if sys_type() == "Unix":
            print(f"os.getloadavg()={os.getloadavg()}")
        print()

        print("[Environment/Locale]")
        print(f"locale.getlocale()={locale.getlocale()}")
        printm("locale.localeconv()", locale.localeconv())
        print()

        print(f"locale.getlocale(locale.LC_CTYPE)={locale.getlocale(locale.LC_CTYPE)}")
        try:
            print(f"locale.getlocale(locale.CODESET)={locale.nl_langinfo(locale.CODESET)}")
        except:
           pass
        print(f"locale.getdefaultlocale()={locale.getdefaultlocale()}")
        print(f"locale.getpreferredencoding()={locale.getpreferredencoding()}")
        print(f"locale.getlocale(locale.LC_COLLATE)={locale.getlocale(locale.LC_COLLATE)}")
        try:
            print(f"locale.getlocale(locale.CHAR_MAX)={locale.getlocale(locale.CHAR_MAX)}")
        except:
            pass
        print()

        try:
            print(f"locale.getlocale(locale.LC_TIME)={locale.getlocale(locale.LC_TIME)}")
            print(f"locale.getlocale(locale.D_T_FMT)={locale.nl_langinfo(locale.D_T_FMT)}")
            print(f"locale.getlocale(locale.D_FMT)={locale.nl_langinfo(locale.D_FMT)}")
            print(f"locale.getlocale(locale.T_FMT)={locale.nl_langinfo(locale.T_FMT)}")
            print(f"locale.getlocale(locale.T_FMT_AMPM)={locale.nl_langinfo(locale.T_FMT_AMPM)}")
            print(f"locale.getlocale(locale.DAY_1)={locale.nl_langinfo(locale.DAY_1)}")
            print(f"locale.getlocale(locale.DAY_2)={locale.nl_langinfo(locale.DAY_2)}")
            print(f"locale.getlocale(locale.DAY_3)={locale.nl_langinfo(locale.DAY_3)}")
            print(f"locale.getlocale(locale.DAY_4)={locale.nl_langinfo(locale.DAY_4)}")
            print(f"locale.getlocale(locale.DAY_5)={locale.nl_langinfo(locale.DAY_5)}")
            print(f"locale.getlocale(locale.DAY_6)={locale.nl_langinfo(locale.DAY_6)}")
            print(f"locale.getlocale(locale.DAY_7)={locale.nl_langinfo(locale.DAY_7)}")
            print(f"locale.getlocale(locale.ABDAY_1)={locale.nl_langinfo(locale.ABDAY_1)}")
            print(f"locale.getlocale(locale.ABDAY_2)={locale.nl_langinfo(locale.ABDAY_2)}")
            print(f"locale.getlocale(locale.ABDAY_3)={locale.nl_langinfo(locale.ABDAY_3)}")
            print(f"locale.getlocale(locale.ABDAY_4)={locale.nl_langinfo(locale.ABDAY_4)}")
            print(f"locale.getlocale(locale.ABDAY_5)={locale.nl_langinfo(locale.ABDAY_5)}")
            print(f"locale.getlocale(locale.ABDAY_6)={locale.nl_langinfo(locale.ABDAY_6)}")
            print(f"locale.getlocale(locale.ABDAY_7)={locale.nl_langinfo(locale.ABDAY_7)}")
            print(f"locale.getlocale(locale.MON_1)={locale.nl_langinfo(locale.MON_1)}")
            print(f"locale.getlocale(locale.MON_2)={locale.nl_langinfo(locale.MON_2)}")
            print(f"locale.getlocale(locale.MON_3)={locale.nl_langinfo(locale.MON_3)}")
            print(f"locale.getlocale(locale.MON_4)={locale.nl_langinfo(locale.MON_4)}")
            print(f"locale.getlocale(locale.MON_5)={locale.nl_langinfo(locale.MON_5)}")
            print(f"locale.getlocale(locale.MON_6)={locale.nl_langinfo(locale.MON_6)}")
            print(f"locale.getlocale(locale.MON_7)={locale.nl_langinfo(locale.MON_7)}")
            print(f"locale.getlocale(locale.MON_8)={locale.nl_langinfo(locale.MON_8)}")
            print(f"locale.getlocale(locale.MON_9)={locale.nl_langinfo(locale.MON_9)}")
            print(f"locale.getlocale(locale.MON_10)={locale.nl_langinfo(locale.MON_10)}")
            print(f"locale.getlocale(locale.MON_11)={locale.nl_langinfo(locale.MON_11)}")
            print(f"locale.getlocale(locale.MON_12)={locale.nl_langinfo(locale.MON_12)}")
            print(f"locale.getlocale(locale.ABMON_1)={locale.nl_langinfo(locale.ABMON_1)}")
            print(f"locale.getlocale(locale.ABMON_2)={locale.nl_langinfo(locale.ABMON_2)}")
            print(f"locale.getlocale(locale.ABMON_3)={locale.nl_langinfo(locale.ABMON_3)}")
            print(f"locale.getlocale(locale.ABMON_4)={locale.nl_langinfo(locale.ABMON_4)}")
            print(f"locale.getlocale(locale.ABMON_5)={locale.nl_langinfo(locale.ABMON_5)}")
            print(f"locale.getlocale(locale.ABMON_6)={locale.nl_langinfo(locale.ABMON_6)}")
            print(f"locale.getlocale(locale.ABMON_7)={locale.nl_langinfo(locale.ABMON_7)}")
            print(f"locale.getlocale(locale.ABMON_8)={locale.nl_langinfo(locale.ABMON_8)}")
            print(f"locale.getlocale(locale.ABMON_9)={locale.nl_langinfo(locale.ABMON_9)}")
            print(f"locale.getlocale(locale.ABMON_10)={locale.nl_langinfo(locale.ABMON_10)}")
            print(f"locale.getlocale(locale.ABMON_11)={locale.nl_langinfo(locale.ABMON_11)}")
            print(f"locale.getlocale(locale.ABMON_12)={locale.nl_langinfo(locale.ABMON_12)}")
            print(f"locale.getlocale(locale.ERA)={locale.nl_langinfo(locale.ERA)}")
            print(f"locale.getlocale(locale.ERA_D_T_FMT)={locale.nl_langinfo(locale.ERA_D_T_FMT)}")
            print(f"locale.getlocale(locale.ERA_D_FMT)={locale.nl_langinfo(locale.ERA_D_FMT)}")
            print(f"locale.getlocale(locale.ERA_T_FMT)={locale.nl_langinfo(locale.ERA_T_FMT)}")
            print()

            print(f"locale.getlocale(locale.LC_MESSAGES)={locale.getlocale(locale.LC_MESSAGES)}")
            print(f"locale.getlocale(locale.YESEXPR)={locale.nl_langinfo(locale.YESEXPR)}")
            print(f"locale.getlocale(locale.NOEXPR)={locale.nl_langinfo(locale.NOEXPR)}")
            print()

            print(f"locale.getlocale(locale.LC_MONETARY)={locale.getlocale(locale.LC_MONETARY)}")
            print(f"locale.getlocale(locale.CRNCYSTR)={locale.nl_langinfo(locale.CRNCYSTR)}")
            print()

            print(f"locale.getlocale(locale.LC_NUMERIC)={locale.getlocale(locale.LC_NUMERIC)}")
            print(f"locale.getlocale(locale.RADIXCHAR)={locale.nl_langinfo(locale.RADIXCHAR)}")
            print(f"locale.getlocale(locale.THOUSEP)={locale.nl_langinfo(locale.THOUSEP)}")
            print(f"locale.getlocale(locale.ALT_DIGITS)={locale.nl_langinfo(locale.ALT_DIGITS)}")
            print()
        except:
            pass


####################################################################################################
def about_python():
    """ Show information about the python install """
    if parameters["Python"]:
        print("[Python]")
        print(f"sysconfig.get_python_version()={sysconfig.get_python_version()}")
        if sys_type() == "Windows":
            print(f"sys.winver={sys.winver}")
        printm("sys.version", sys.version)
        print(f"sys.version_info={sys.version_info}")
        print(f"sys.hexversion={sys.hexversion}")
        print(f"sys.implementation={sys.implementation}")
        print(f"platform.python_build()={platform.python_build()}")
        print(f"platform.python_branch()={platform.python_branch()}")
        print(f"platform.python_implementation()={platform.python_implementation()}")
        print(f"platform.python_revision()={platform.python_revision()}")
        print(f"platform.python_version()={platform.python_version()}")
        print(f"platform.python_version_tuple()={platform.python_version_tuple()}")
        printm("sys.copyright", sys.copyright)
        print()

        print("[Python/Config]")
        print(f"sys.base_prefix={sys.base_prefix}")
        print(f"sys.executable={sys.executable}")
        print(f"sys.flags={sys.flags}")
        printm("sys.builtin_module_names", sys.builtin_module_names)
        printm("sys.modules", sys.modules)
        print(f"fsys.path={sys.path}")
        python_version = platform.python_version_tuple()
        if python_version[0] == 3 and python_version[1] >= 9:
            printm("sys.platlibdir", sys.platlibdir)  # Python 3.9+
        print(f"sys.getrecursionlimit()={sys.getrecursionlimit()}")
        print(f"sys.getswitchinterval()={sys.getswitchinterval()}")
        print(f"sys.thread_info={sys.thread_info}")
        print(f"platform.python_compiler()={platform.python_compiler()}")
        if sys_type() == "Unix":
            print(f"platform.libc_ver()={platform.libc_ver()}")
        print(f"sys.api_version={sys.api_version}")
        print()

        print("[Python/Math]")
        print(f"sys.int_info={sys.int_info}")
        print(f"sys.maxsize={sys.maxsize}")
        print(f"sys.float_info={sys.float_info}")
        print()

        print("[Python/Unicode]")
        print(f"sys.getdefaultencoding()={sys.getdefaultencoding()}")
        print(f"sys.getfilesystemencoding()={sys.getfilesystemencoding()}")
        print(f"unicodedata.unidata_version={unicodedata.unidata_version}")
        print(f"sys.maxunicode={sys.maxunicode}")
        print()


####################################################################################################
def main():
    """ The program's entry point """
    program_name = os.path.basename(sys.argv[0])

    libpnu.initialize_debugging(program_name)
    libpnu.handle_interrupt_signals(_handle_interrupts)
    _process_command_line()

    if True not in parameters.values():
        logging.warning("Please select something to show:")
        _display_help()
        sys.exit(0)

    about_local_system()
    about_user()
    about_hardware()
    about_operating_system()
    about_environment()
    about_python()

    sys.exit(0)


if __name__ == "__main__":
    main()
