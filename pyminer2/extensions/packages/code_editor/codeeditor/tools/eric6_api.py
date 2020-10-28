#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2003 - 2020 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Eric6 API Generator.

This is the main Python script of the API generator. It is
this script that gets called via the API generation interface.
This script can be used via the commandline as well.
"""

import DocumentationTools
import Utilities
from DocumentationTools.APIGenerator import APIGenerator
import Utilities.ModuleParser
import fnmatch
import glob
import os
import sys

sys.path.insert(1, os.path.dirname(__file__))


# make ThirdParty package available as a packages repository
sys.path.insert(2, os.path.join(os.path.dirname(__file__),
                                "ThirdParty", "EditorConfig"))


Version = '20.8 (rev. 27cfb65c7324)'


def usage():
    """
    Function to print some usage information.

    It prints a reference of all commandline parameters that may
    be used and ends the application.
    """
    print("eric6_api")
    print()
    print("Copyright (c) 2004 - 2020 Detlev Offenbach"
          " <detlev@die-offenbachs.de>.")
    print()
    print("Usage:")
    print()
    print("  eric6_api [options] files...")
    print()
    print("where files can be either python modules, package")
    print("directories or ordinary directories.")
    print()
    print("Options:")
    print()
    print("  -b name or --base=name")
    print("        Use the given name as the name of the base package.")
    print("  -e eol-type or --eol=eol-type")
    print("        Use the given eol type to terminate lines.")
    print("        Valid values are 'cr', 'lf' and 'crlf'.")
    print("  --exclude-file=pattern")
    print("        Specify a filename pattern of files to be excluded.")
    print("        This option may be repeated multiple times.")
    print("  -h or --help")
    print("        Show this help and exit.")
    print("  -i or --ignore")
    print("        Ignore the set of builtin modules")
    print("  -l language or --language=language")
    print("        Generate an API file for the given programming language.")
    print("        Supported programming languages are:")
    for lang in sorted(
            DocumentationTools.supportedExtensionsDictForApis.keys()):
        print("            * {0}".format(lang))
    print("        The default is 'Python3'.")
    print("        This option may be repeated multiple times.")
    print("  -o filename or --output=filename")
    print("        Write the API information to the named file."
          " A '%L' placeholder")  # __IGNORE_WARNING_M601__
    print("        is replaced by the language of the API file"
          " (see --language).")
    print("  -p or --private")
    print("        Include private methods and functions.")
    print("  -R, -r or --recursive")
    print("        Perform a recursive search for source files.")
    print("  -t ext or --extension=ext")
    print("        Add the given extension to the list of file extensions.")
    print("        This option may be given multiple times.")
    print("  -V or --version")
    print("        Show version information and exit.")
    print("  -x directory or --exclude=directory")
    print("        Specify a directory basename to be excluded.")
    print("        This option may be repeated multiple times.")
    sys.exit(1)


def version():
    """
    Function to show the version information.
    """
    print(
        """eric6_api  {0}\n"""
        """\n"""
        """Eric6 API generator.\n"""
        """\n"""
        """Copyright (c) 2004 - 2020 Detlev Offenbach"""
        """ <detlev@die-offenbachs.de>\n"""
        """This is free software; see the LICENSE.GPL3 for copying"""
        """ conditions.\n"""
        """There is NO warranty; not even for MERCHANTABILITY or FITNESS"""
        """ FOR A\n"""
        """PARTICULAR PURPOSE.""".format(Version))
    sys.exit(1)


def main():
    """
    Main entry point into the application.
    """
    global supportedExtensions

    import getopt

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "b:e:hil:o:pRrt:Vx:",
            ["base=", "eol=", "exclude=", "exclude-file=", "extension=",
             "help", "ignore", "language=", "output=", "private", "recursive",
             "version", ])
    except getopt.error:
        usage()

    excludeDirs = [".svn", ".hg", ".git", ".ropeproject", ".eric6project",
                   "dist", "build", "doc", "docs"]
    excludePatterns = []
    outputFileName = ""
    recursive = False
    basePackage = ""
    includePrivate = False
    progLanguages = []
    extensions = []
    newline = None
    ignoreBuiltinModules = False

    for k, v in opts:
        if k in ["-o", "--output"]:
            outputFileName = v
        elif k in ["-R", "-r", "--recursive"]:
            recursive = True
        elif k in ["-x", "--exclude"]:
            excludeDirs.append(v)
        elif k == "--exclude-file":
            excludePatterns.append(v)
        elif k in ["-h", "--help"]:
            usage()
        elif k in ["-i", "--ignore"]:
            ignoreBuiltinModules = True
        elif k in ["-V", "--version"]:
            version()
        elif k in ["-t", "--extension"]:
            if not v.startswith("."):
                v = ".{0}".format(v)
            extensions.append(v)
        elif k in ["-b", "--base"]:
            basePackage = v
        elif k in ["-p", "--private"]:
            includePrivate = True
        elif k in ["-l", "--language"]:
            if v not in progLanguages:
                if v not in DocumentationTools.supportedExtensionsDictForApis:
                    sys.stderr.write(
                        "Wrong language given: {0}. Aborting\n".format(v))
                    sys.exit(1)
                else:
                    progLanguages.append(v)
        elif k in ["-e", "--eol"]:
            if v.lower() == "cr":
                newline = '\r'
            elif v.lower() == "lf":
                newline = '\n'
            elif v.lower() == "crlf":
                newline = '\r\n'

    if not args:
        usage()

    if outputFileName == "":
        sys.stderr.write("No output file given. Aborting\n")
        sys.exit(1)

    if len(progLanguages) == 0:
        progLanguages = ["Python3"]

    for progLanguage in sorted(progLanguages):
        basename = ""
        apis = []
        basesDict = {}

        supportedExtensions = (
            DocumentationTools.supportedExtensionsDictForApis[progLanguage]
        )
        supportedExtensions.extend(extensions)
        if "%L" in outputFileName:
            outputFile = outputFileName.replace("%L", progLanguage)
        else:
            if len(progLanguages) == 1:
                outputFile = outputFileName
            else:
                root, ext = os.path.splitext(outputFileName)
                outputFile = "{0}-{1}{2}".format(root, progLanguage.lower(),
                                                 ext)
        basesFile = os.path.splitext(outputFile)[0] + '.bas'

        for arg in args:
            if os.path.isdir(arg):
                if os.path.exists(os.path.join(
                        arg, Utilities.joinext("__init__", ".py"))):
                    basename = os.path.dirname(arg)
                    if arg == '.':
                        sys.stderr.write("The directory '.' is a package.\n")
                        sys.stderr.write(
                            "Please repeat the call giving its real name.\n")
                        sys.stderr.write("Ignoring the directory.\n")
                        continue
                else:
                    basename = arg
                if basename:
                    basename = "{0}{1}".format(basename, os.sep)

                if recursive and not os.path.islink(arg):
                    names = [arg] + Utilities.getDirs(arg, excludeDirs)
                else:
                    names = [arg]
            else:
                basename = ""
                names = [arg]

            for filename in sorted(names):
                inpackage = False
                if os.path.isdir(filename):
                    files = []
                    for ext in supportedExtensions:
                        files.extend(glob.glob(os.path.join(
                            filename, Utilities.joinext("*", ext))))
                        initFile = os.path.join(
                            filename, Utilities.joinext("__init__", ext))
                        if initFile in files:
                            inpackage = True
                            files.remove(initFile)
                            files.insert(0, initFile)
                        elif progLanguage != "Python3":
                            # assume package
                            inpackage = True
                else:
                    if (
                            Utilities.isWindowsPlatform() and
                            glob.has_magic(filename)
                    ):
                        files = glob.glob(filename)
                    else:
                        files = [filename]

                for file in files:
                    skipIt = False
                    for pattern in excludePatterns:
                        if fnmatch.fnmatch(os.path.basename(file), pattern):
                            skipIt = True
                            break
                    if skipIt:
                        continue

                    try:
                        module = Utilities.ModuleParser.readModule(
                            file,
                            basename=basename, inpackage=inpackage,
                            ignoreBuiltinModules=ignoreBuiltinModules)
                        apiGenerator = APIGenerator(module)
                        api = apiGenerator.genAPI(True, basePackage,
                                                  includePrivate)
                        bases = apiGenerator.genBases(includePrivate)
                    except IOError as v:
                        sys.stderr.write("{0} error: {1}\n".format(file, v[1]))
                        continue
                    except ImportError as v:
                        sys.stderr.write("{0} error: {1}\n".format(file, v))
                        continue

                    for apiEntry in api:
                        if apiEntry not in apis:
                            apis.append(apiEntry)
                    for basesEntry in bases:
                        if bases[basesEntry]:
                            basesDict[basesEntry] = bases[basesEntry][:]
                    sys.stdout.write("-- {0} -- {1} ok\n".format(
                        progLanguage, file))

        outdir = os.path.dirname(outputFile)
        if outdir and not os.path.exists(outdir):
            os.makedirs(outdir)
        try:
            out = open(outputFile, "w", encoding="utf-8", newline=newline)
            out.write("\n".join(sorted(apis)) + "\n")
            out.close()
        except IOError as v:
            sys.stderr.write("{0} error: {1}\n".format(outputFile, v[1]))
            sys.exit(3)
        # try:
        #     out = open(basesFile, "w", encoding="utf-8", newline=newline)
        #     for baseEntry in sorted(basesDict.keys()):
        #         out.write("{0} {1}\n".format(
        #             baseEntry, " ".join(sorted(basesDict[baseEntry]))))
        #     out.close()
        # except IOError as v:
        #     sys.stderr.write("{0} error: {1}\n".format(basesFile, v[1]))
        #     sys.exit(3)

    sys.stdout.write('\nDone.\n')
    sys.exit(0)


if __name__ == '__main__':
    main()

#
# eflag: noqa = M801
