# Installation
pip install [pnu-about](https://pypi.org/project/pnu-about/)

# ABOUT(1)

## NAME
about - show system information

## SYNOPSIS
**about**
[-a\|--all]
[-E\|--env\|--environment]
[-H\|--hw\|--hardware]
[-O\|--os\|--operating]
[-P\|--py\|--python]
[-S\|--sys\|--system]
[-U\|--user]
[-d\|--debug]
[-h\|--help\|-?]
[-v\|--version]
[--]

## DESCRIPTION
The **about** utility shows most of the system information available through the [Python Standard Library](https://docs.python.org/3/library/index.html).

## OPTIONS

Options | Use
------- | ---
-a\|--all|Same as -SUHOEP
-E\|--env\|--environment|Show information about the environment
-H\|--hw\|--hardware|Show information about the hardware
-O\|--os\|--operating|Show information about the Operating System
-P\|--py\|--python|Show information about Python
-S\|--sys\|--system|Show information about the system
-U\|--user|Show information about the user
-d\|--debug|Enable debug level messages
-h\|--help\|-?|Print usage and a short help message and exit
-v\|--version|Print version and exit
--|Options processing terminator

## EXIT STATUS
The about utility exits 0 on success, and >0 if an error occurs.

## SEE ALSO
[uname(1)](https://www.freebsd.org/cgi/man.cgi?query=uname), [sysctl(8)](https://www.freebsd.org/cgi/man.cgi?query=sysctl)

https://docs.python.org/3/library/index.html

## STANDARDS
The about command is not a standard [UNIX](https://en.wikipedia.org/wiki/Unix)/[POSIX](https://en.wikipedia.org/wiki/POSIX) command.

It tries to follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for [Python](https://www.python.org/) code.

## PORTABILITY
Tested OK under Windows.

## HISTORY
The about command was created as an example for the [PNU project](https://github.com/HubTou/PNU), testing many of the [standard Python functions](https://docs.python.org/3/library/index.html) for getting system information.

## LICENSE
This utility is available under the [3-clause BSD license](https://opensource.org/licenses/BSD-3-Clause).

## AUTHORS
[Hubert Tournier](https://github.com/HubTou)

