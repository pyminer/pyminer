# -*- coding: utf-8 -*-

# Copyright (c) 2003 - 2020 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Parse a Python module file.

<b>BUGS</b> (from pyclbr.py)
<ul>
<li>Code that doesn't pass tabnanny or python -t will confuse it, unless
  you set the module TABWIDTH variable (default 8) to the correct tab width
  for the file.</li>
</ul>
"""

import os
import re
import sys
from functools import reduce

import Utilities
import importlib.machinery

__all__ = ["Module", "Class", "Function", "Attribute", "RbModule",
           "readModule", "getTypeFromTypeName"]

TABWIDTH = 4

SEARCH_ERROR = 0
PY_SOURCE = 1
PTL_SOURCE = 128
RB_SOURCE = 129

SUPPORTED_TYPES = [PY_SOURCE, PTL_SOURCE, RB_SOURCE]
TYPE_MAPPING = {
    "Python": PY_SOURCE,
    "Python3": PY_SOURCE,
    "MicroPython": PY_SOURCE,
    "Ruby": RB_SOURCE,
}


def getTypeFromTypeName(name):
    """
    Module function to determine the module type given the module type name.

    @param name module type name (string)
    @return module type or -1 for failure (integer)
    """
    if name in TYPE_MAPPING:
        return TYPE_MAPPING[name]
    else:
        return -1


_py_getnext = re.compile(
    r"""
    (?P<Comment>
        \# .*? $   # ignore everything in comments
    )

|   (?P<String>
        \""" (?P<StringContents1>
               [^"\\]* (?:
                            (?: \\. | "(?!"") )
                            [^"\\]*
                        )*
            )
        \"""

    |   """ (?P<StringContents2>
                [^'\\]* (?:
                            (?: \\. | '(?!'') )
                            [^'\\]*
                        )*
            )
        """

    |   " [^"\\\n]* (?: \\. [^"\\\n]*)* "

    |   ' [^'\\\n]* (?: \\. [^'\\\n]*)* '

    |   \#\#\# (?P<StringContents3>
                [^#\\]* (?:
                            (?: \\. | \#(?!\#\#) )
                            [^#\\]*
                        )*
            )
        \#\#\#
    )

|   (?P<Docstring>
        (?<= :) \s*
        [ru]? \""" (?P<DocstringContents1>
                [^"\\]* (?:
                            (?: \\. | "(?!"") )
                            [^"\\]*
                        )*
            )
        \"""

    |   (?<= :) \s*
        [ru]? """ (?P<DocstringContents2>
                [^'\\]* (?:
                            (?: \\. | '(?!'') )
                            [^'\\]*
                        )*
            )
        """

    |   (?<= :) \s*
        \#\#\# (?P<DocstringContents3>
                [^#\\]* (?:
                            (?: \\. | \#(?!\#\#) )
                            [^#\\]*
                        )*
            )
        \#\#\#
    )

|   (?P<MethodModifier>
        ^
        (?P<MethodModifierIndent> [ \t]* )
        (?P<MethodModifierType> @classmethod | @staticmethod )
    )

|   (?P<Method>
        (^ [ \t]* @ (?: PyQt[45] \. )? (?: QtCore \. )?
            (?: pyqtSignature | pyqtSlot )
            [ \t]* \(
                (?P<MethodPyQtSignature> [^)]* )
            \) \s*
        )?
        ^
        (?P<MethodIndent> [ \t]* )
        (?: async [ \t]+ )? def [ \t]+
        (?P<MethodName> \w+ )
        (?: [ \t]* \[ (?: plain | html ) \] )?
        [ \t]* \(
        (?P<MethodSignature> (?: [^)] | \)[ \t]*,? )*? )
        \) [ \t]*
        (?P<MethodReturnAnnotation> (?: -> [ \t]* [^:]+ )? )
        [ \t]* :
    )

|   (?P<Class>
        ^
        (?P<ClassIndent> [ \t]* )
        class [ \t]+
        (?P<ClassName> \w+ )
        [ \t]*
        (?P<ClassSupers> \( [^)]* \) )?
        [ \t]* :
    )

|   (?P<Attribute>
        ^
        (?P<AttributeIndent> [ \t]* )
        self [ \t]* \. [ \t]*
        (?P<AttributeName> \w+ )
        [ \t]* =
    )

|   (?P<Variable>
        ^
        (?P<VariableIndent> [ \t]* )
        (?P<VariableName> \w+ )
        [ \t]* = [ \t]* (?P<VariableSignal> (?:pyqtSignal)? )
    )

|   (?P<Main>
        ^
        if \s+ __name__ \s* == \s* [^:]+ : $
    )

|   (?P<Import>
        ^ [ \t]* (?: import | from [ \t]+ \. [ \t]+ import ) [ \t]+
        (?P<ImportList> (?: [^#;\\\n]* (?: \\\n )* )* )
    )

|   (?P<ImportFrom>
        ^ [ \t]* from [ \t]+
        (?P<ImportFromPath>
            \.* \w+
            (?:
                [ \t]* \. [ \t]* \w+
            )*
        )
        [ \t]+
        import [ \t]+
        (?P<ImportFromList>
            (?: \( \s* .*? \s* \) )
            |
            (?: [^#;\\\n]* (?: \\\n )* )* )
    )

|   (?P<ConditionalDefine>
        ^
        (?P<ConditionalDefineIndent> [ \t]* )
        (?: (?: if | elif ) [ \t]+ [^:]* | else [ \t]* ) :
        (?= \s* (?: async [ \t]+ )? def)
    )""",
    re.VERBOSE | re.DOTALL | re.MULTILINE).search

_rb_getnext = re.compile(
    r"""
    (?P<Docstring>
        =begin [ \t]+ edoc (?P<DocstringContents> .*? ) =end
    )

|   (?P<String>
        =begin .*? =end

    |   <<-? (?P<HereMarker1> [a-zA-Z0-9_]+? ) [ \t]* .*? (?P=HereMarker1)

    |   <<-? ['"] (?P<HereMarker2> .*? ) ['"] [ \t]* .*? (?P=HereMarker2)

    |   " [^"\\\n]* (?: \\. [^"\\\n]*)* "

    |   ' [^'\\\n]* (?: \\. [^'\\\n]*)* '
    )

|   (?P<Comment>
        ^
        [ \t]* \#+ .*? $
    )

|   (?P<Method>
        ^
        (?P<MethodIndent> [ \t]* )
        def [ \t]+
        (?:
            (?P<MethodName2> [a-zA-Z0-9_]+ (?: \. | :: )
            [a-zA-Z_] [a-zA-Z0-9_?!=]* )
        |
            (?P<MethodName> [a-zA-Z_] [a-zA-Z0-9_?!=]* )
        |
            (?P<MethodName3> [^( \t]{1,3} )
        )
        [ \t]*
        (?:
            \( (?P<MethodSignature> (?: [^)] | \)[ \t]*,? )*? ) \)
        )?
        [ \t]*
    )

|   (?P<Class>
        ^
        (?P<ClassIndent> [ \t]* )
        class
        (?:
            [ \t]+
            (?P<ClassName> [A-Z] [a-zA-Z0-9_]* )
            [ \t]*
            (?P<ClassSupers> < [ \t]* [A-Z] [a-zA-Z0-9_]* )?
        |
            [ \t]* << [ \t]*
            (?P<ClassName2> [a-zA-Z_] [a-zA-Z0-9_]* )
        )
        [ \t]*
    )

|   (?P<ClassIgnored>
        \(
        [ \t]*
        class
        .*?
        end
        [ \t]*
        \)
    )

|   (?P<Module>
        ^
        (?P<ModuleIndent> [ \t]* )
        module [ \t]+
        (?P<ModuleName> [A-Z] [a-zA-Z0-9_]* )
        [ \t]*
    )

|   (?P<AccessControl>
        ^
        (?P<AccessControlIndent> [ \t]* )
        (?:
            (?P<AccessControlType> private | public | protected ) [^_]
        |
            (?P<AccessControlType2>
            private_class_method | public_class_method )
        )
        \(?
        [ \t]*
        (?P<AccessControlList> (?: : [a-zA-Z0-9_]+ , \s* )*
        (?: : [a-zA-Z0-9_]+ )+ )?
        [ \t]*
        \)?
    )

|   (?P<Attribute>
        ^
        (?P<AttributeIndent> [ \t]* )
        (?P<AttributeName> (?: @ | @@ | [A-Z]) [a-zA-Z0-9_]* )
        [ \t]* =
    )

|   (?P<Attr>
        ^
        (?P<AttrIndent> [ \t]* )
        attr
        (?P<AttrType> (?: _accessor | _reader | _writer ) )?
        \(?
        [ \t]*
        (?P<AttrList> (?: : [a-zA-Z0-9_]+ , \s* )*
        (?: : [a-zA-Z0-9_]+ | true | false )+ )
        [ \t]*
        \)?
    )

|   (?P<Begin>
            ^
            [ \t]*
            (?: if | unless | case | while | until | for | begin ) \b [^_]
        |
            [ \t]* do [ \t]* (?: \| .*? \| )? [ \t]* $
    )

|   (?P<BeginEnd>
        \b (?: if ) \b [^_] .*? $
        |
        \b (?: if ) \b [^_] .*? end [ \t]* $
    )

|   (?P<End>
        [ \t]*
        (?:
            end [ \t]* $
        |
            end \b [^_]
        )
    )""",
    re.VERBOSE | re.DOTALL | re.MULTILINE).search

_hashsub = re.compile(r"""^([ \t]*)#[ \t]?""", re.MULTILINE).sub

_commentsub = re.compile(r"""#[^\n]*\n|#[^\n]*$""").sub

_modules = {}  # cache of modules we've seen


class VisibilityBase(object):
    """
    Class implementing the visibility aspect of all objects.
    """

    def isPrivate(self):
        """
        Public method to check, if the visibility is Private.

        @return flag indicating Private visibility (boolean)
        """
        return self.visibility == 0

    def isProtected(self):
        """
        Public method to check, if the visibility is Protected.

        @return flag indicating Protected visibility (boolean)
        """
        return self.visibility == 1

    def isPublic(self):
        """
        Public method to check, if the visibility is Public.

        @return flag indicating Public visibility (boolean)
        """
        return self.visibility == 2

    def setPrivate(self):
        """
        Public method to set the visibility to Private.
        """
        self.visibility = 0

    def setProtected(self):
        """
        Public method to set the visibility to Protected.
        """
        self.visibility = 1

    def setPublic(self):
        """
        Public method to set the visibility to Public.
        """
        self.visibility = 2


class Module(object):
    """
    Class to represent a Python module.
    """

    def __init__(self, name, file=None, moduleType=None):
        """
        Constructor

        @param name name of this module (string)
        @param file filename of file containing this module (string)
        @param moduleType type of this module
        """
        self.name = name
        self.file = file
        self.modules = {}
        self.modules_counts = {}
        self.classes = {}
        self.classes_counts = {}
        self.functions = {}
        self.functions_counts = {}
        self.description = ""
        self.globals = {}
        self.imports = []
        self.from_imports = {}
        self.package = '.'.join(name.split('.')[:-1])
        self.type = moduleType
        if moduleType in [PY_SOURCE, PTL_SOURCE]:
            self._getnext = _py_getnext
        elif moduleType == RB_SOURCE:
            self._getnext = _rb_getnext
        else:
            self._getnext = None

    def addClass(self, name, _class):
        """
        Public method to add information about a class.

        @param name name of class to be added (string)
        @param _class Class object to be added
        """
        if name in self.classes:
            self.classes_counts[name] += 1
            name = "{0}_{1:d}".format(name, self.classes_counts[name])
        else:
            self.classes_counts[name] = 0
        self.classes[name] = _class

    def addModule(self, name, module):
        """
        Public method to add information about a Ruby module.

        @param name name of module to be added (string)
        @param module Module object to be added
        """
        if name in self.modules:
            self.modules_counts[name] += 1
            name = "{0}_{1:d}".format(name, self.modules_counts[name])
        else:
            self.modules_counts[name] = 0
        self.modules[name] = module

    def addFunction(self, name, function):
        """
        Public method to add information about a function.

        @param name name of function to be added (string)
        @param function Function object to be added
        """
        if name in self.functions:
            self.functions_counts[name] += 1
            name = "{0}_{1:d}".format(name, self.functions_counts[name])
        else:
            self.functions_counts[name] = 0
        self.functions[name] = function

    def addGlobal(self, name, attr):
        """
        Public method to add information about global variables.

        @param name name of the global to add (string)
        @param attr Attribute object to be added
        """
        if name not in self.globals:
            self.globals[name] = attr
        else:
            self.globals[name].addAssignment(attr.lineno)

    def addDescription(self, description):
        """
        Public method to store the modules docstring.

        @param description the docstring to be stored (string)
        """
        self.description = description

    def scan(self, src):
        """
        Public method to scan the source text and retrieve the relevant
        information.

        @param src the source text to be scanned (string)
        """
        if self.type in [PY_SOURCE, PTL_SOURCE]:
            self.__py_scan(src)
        elif self.type == RB_SOURCE:
            self.__rb_scan(src)

    def __py_setVisibility(self, objectRef):
        """
        Private method to set the visibility of an object.

        @param objectRef reference to the object (Attribute, Class or Function)
        """
        if objectRef.name.startswith('__'):
            objectRef.setPrivate()
        elif objectRef.name.startswith('_'):
            objectRef.setProtected()
        else:
            objectRef.setPublic()

    def __py_scan(self, src):
        """
        Private method to scan the source text of a Python module and retrieve
        the relevant information.

        @param src the source text to be scanned (string)
        """
        lineno, last_lineno_pos = 1, 0
        lastGlobalEntry = None
        classstack = []  # stack of (class, indent) pairs
        conditionalsstack = []  # stack of indents of conditional defines
        deltastack = []
        deltaindent = 0
        deltaindentcalculated = 0
        i = 0
        modulelevel = True
        cur_obj = self
        modifierType = Function.General
        modifierIndent = -1
        while True:
            m = self._getnext(src, i)
            if not m:
                break
            start, i = m.span()

            if m.start("MethodModifier") >= 0:
                modifierIndent = _indent(m.group("MethodModifierIndent"))
                modifierType = m.group("MethodModifierType")

            elif m.start("Method") >= 0:
                # found a method definition or function
                thisindent = _indent(m.group("MethodIndent"))
                meth_name = m.group("MethodName")
                meth_sig = m.group("MethodSignature")
                meth_sig = meth_sig.replace('\\\n', '')
                meth_ret = m.group("MethodReturnAnnotation")
                meth_ret = meth_ret.replace('\\\n', '')
                if m.group("MethodPyQtSignature") is not None:
                    meth_pyqtSig = (
                        m.group("MethodPyQtSignature")
                        .replace('\\\n', '')
                        .split('result')[0]
                        .split('name')[0]
                        .strip("\"', \t")
                    )
                else:
                    meth_pyqtSig = None
                lineno = lineno + src.count('\n', last_lineno_pos, start)
                last_lineno_pos = start
                if modifierType and modifierIndent == thisindent:
                    if modifierType == "@staticmethod":
                        modifier = Function.Static
                    elif modifierType == "@classmethod":
                        modifier = Function.Class
                    else:
                        modifier = Function.General
                else:
                    modifier = Function.General
                # modify indentation level for conditional defines
                if conditionalsstack:
                    if thisindent > conditionalsstack[-1]:
                        if not deltaindentcalculated:
                            deltastack.append(
                                thisindent - conditionalsstack[-1])
                            deltaindent = reduce(
                                lambda x, y: x + y, deltastack)
                            deltaindentcalculated = 1
                        thisindent -= deltaindent
                    else:
                        while (
                                conditionalsstack and
                                conditionalsstack[-1] >= thisindent
                        ):
                            del conditionalsstack[-1]
                            if deltastack:
                                del deltastack[-1]
                        deltaindentcalculated = 0
                # close all classes indented at least as much
                while classstack and classstack[-1][1] >= thisindent:
                    if (
                            classstack[-1][0] is not None and
                            isinstance(classstack[-1][0], (Class, Function))
                    ):
                        # record the end line of this class or function
                        classstack[-1][0].setEndLine(lineno - 1)
                    del classstack[-1]
                if classstack:
                    csi = -1
                    while csi >= -len(classstack):
                        # nested defs are added to the class
                        cur_class = classstack[csi][0]
                        csi -= 1
                        if cur_class is None:
                            continue

                        if isinstance(cur_class, Class):
                            # it's a class method
                            f = Function(
                                None, meth_name, None, lineno,
                                meth_sig, meth_pyqtSig, modifierType=modifier,
                                annotation=meth_ret)
                            self.__py_setVisibility(f)
                            cur_class.addMethod(meth_name, f)
                            break
                    else:
                        # it's a nested function of a module function
                        f = Function(
                            self.name, meth_name, self.file, lineno,
                            meth_sig, meth_pyqtSig, modifierType=modifier,
                            annotation=meth_ret)
                        self.__py_setVisibility(f)
                        self.addFunction(meth_name, f)
                else:
                    # it's a module function
                    f = Function(self.name, meth_name, self.file, lineno,
                                 meth_sig, meth_pyqtSig, modifierType=modifier,
                                 annotation=meth_ret)
                    self.__py_setVisibility(f)
                    self.addFunction(meth_name, f)
                if not classstack:
                    if lastGlobalEntry:
                        lastGlobalEntry.setEndLine(lineno - 1)
                    lastGlobalEntry = f
                if cur_obj and isinstance(cur_obj, Function):
                    cur_obj.setEndLine(lineno - 1)
                cur_obj = f
                classstack.append((None, thisindent))  # Marker for nested fns

                # reset the modifier settings
                modifierType = Function.General
                modifierIndent = -1

            elif m.start("Docstring") >= 0:
                contents = m.group("DocstringContents3")
                if contents is not None:
                    contents = _hashsub(r"\1", contents)
                else:
                    if self.file.lower().endswith('.ptl'):
                        contents = ""
                    else:
                        contents = (
                            m.group("DocstringContents1") or
                            m.group("DocstringContents2")
                        )
                if cur_obj:
                    cur_obj.addDescription(contents)

            elif m.start("String") >= 0:
                if (
                        modulelevel and (
                        src[start - len('\r\n'):start] == '\r\n' or
                        src[start - len('\n'):start] == '\n' or
                        src[start - len('\r'):start] == '\r'
                        )
                ):
                    contents = m.group("StringContents3")
                    if contents is not None:
                        contents = _hashsub(r"\1", contents)
                    else:
                        if self.file.lower().endswith('.ptl'):
                            contents = ""
                        else:
                            contents = (
                                m.group("StringContents1") or
                                m.group("StringContents2")
                            )
                    if cur_obj:
                        cur_obj.addDescription(contents)

            elif m.start("Class") >= 0:
                # we found a class definition
                thisindent = _indent(m.group("ClassIndent"))
                lineno = lineno + src.count('\n', last_lineno_pos, start)
                last_lineno_pos = start
                # close all classes indented at least as much
                while classstack and classstack[-1][1] >= thisindent:
                    if (
                            classstack[-1][0] is not None and
                            isinstance(classstack[-1][0], (Class, Function))
                    ):
                        # record the end line of this class or function
                        classstack[-1][0].setEndLine(lineno - 1)
                    del classstack[-1]
                class_name = m.group("ClassName")
                inherit = m.group("ClassSupers")
                if inherit:
                    # the class inherits from other classes
                    inherit = inherit[1:-1].strip()
                    inherit = _commentsub('', inherit)
                    names = []
                    for n in inherit.split(','):
                        n = n.strip()
                        if n:
                            if n in self.classes:
                                # we know this super class
                                n = self.classes[n].name
                            else:
                                c = n.split('.')
                                if len(c) > 1:
                                    # super class is of the
                                    # form module.class:
                                    # look in module for class
                                    m = c[-2]
                                    c = c[-1]
                                    if m in _modules:
                                        m = _modules[m]
                                        n = m.name
                            names.append(n)
                    inherit = names
                # remember this class
                cur_class = Class(self.name, class_name, inherit,
                                  self.file, lineno)
                self.__py_setVisibility(cur_class)
                cur_obj = cur_class
                # add nested classes to the module
                self.addClass(class_name, cur_class)
                if not classstack:
                    if lastGlobalEntry:
                        lastGlobalEntry.setEndLine(lineno - 1)
                    lastGlobalEntry = cur_class
                classstack.append((cur_class, thisindent))

            elif m.start("Attribute") >= 0:
                lineno = lineno + src.count('\n', last_lineno_pos, start)
                last_lineno_pos = start
                index = -1
                while index >= -len(classstack):
                    if classstack[index][0] is not None:
                        attrName = m.group("AttributeName")
                        attr = Attribute(
                            self.name, attrName, self.file, lineno)
                        self.__py_setVisibility(attr)
                        classstack[index][0].addAttribute(attrName, attr)
                        break
                    else:
                        index -= 1

            elif m.start("Main") >= 0:
                # 'main' part of the script, reset class stack
                lineno = lineno + src.count('\n', last_lineno_pos, start)
                last_lineno_pos = start
                classstack = []

            elif m.start("Variable") >= 0:
                thisindent = _indent(m.group("VariableIndent"))
                variable_name = m.group("VariableName")
                isSignal = m.group("VariableSignal") != ""
                lineno = lineno + src.count('\n', last_lineno_pos, start)
                last_lineno_pos = start
                if thisindent == 0:
                    # global variable
                    attr = Attribute(
                        self.name, variable_name, self.file, lineno,
                        isSignal=isSignal)
                    self.__py_setVisibility(attr)
                    self.addGlobal(variable_name, attr)
                    if lastGlobalEntry:
                        lastGlobalEntry.setEndLine(lineno - 1)
                    lastGlobalEntry = None
                else:
                    index = -1
                    while index >= -len(classstack):
                        if classstack[index][1] >= thisindent:
                            index -= 1
                        else:
                            if (
                                    classstack[index][0] is not None and
                                    isinstance(classstack[index][0], Class)
                            ):
                                attr = Attribute(
                                    self.name, variable_name, self.file,
                                    lineno, isSignal=isSignal)
                                self.__py_setVisibility(attr)
                                classstack[index][0].addGlobal(
                                    variable_name, attr)
                            break

            elif m.start("Import") >= 0:
                ## import module
                names = [n.strip() for n in
                         "".join(m.group("ImportList").splitlines())
                         .replace("\\", "").split(',')]
                self.imports.extend(
                    [name for name in names
                     if name not in self.imports])

            elif m.start("ImportFrom") >= 0:
                ## from module import stuff
                mod = m.group("ImportFromPath")
                namesLines = (m.group("ImportFromList")
                              .replace("(", "").replace(")", "")
                              .replace("\\", "")
                              .strip().splitlines())
                namesLines = [line.split("#")[0].strip()
                              for line in namesLines]
                names = [n.strip() for n in
                         "".join(namesLines)
                         .split(',')]
                if mod not in self.from_imports:
                    self.from_imports[mod] = []
                self.from_imports[mod].extend(
                    [name for name in names
                     if name not in self.from_imports[mod]])

            elif m.start("ConditionalDefine") >= 0:
                # a conditional function/method definition
                thisindent = _indent(m.group("ConditionalDefineIndent"))
                while (
                        conditionalsstack and
                        conditionalsstack[-1] >= thisindent
                ):
                    del conditionalsstack[-1]
                    if deltastack:
                        del deltastack[-1]
                conditionalsstack.append(thisindent)
                deltaindentcalculated = 0

            elif m.start("Comment") >= 0:
                if modulelevel:
                    continue

            modulelevel = False

    def __rb_scan(self, src):
        """
        Private method to scan the source text of a Python module and retrieve
        the relevant information.

        @param src the source text to be scanned (string)
        """
        lineno, last_lineno_pos = 1, 0
        classstack = []  # stack of (class, indent) pairs
        acstack = []  # stack of (access control, indent) pairs
        indent = 0
        i = 0
        cur_obj = self
        lastGlobalEntry = None
        while True:
            m = self._getnext(src, i)
            if not m:
                break
            start, i = m.span()

            if m.start("Method") >= 0:
                # found a method definition or function
                thisindent = indent
                indent += 1
                meth_name = (
                    m.group("MethodName") or
                    m.group("MethodName2") or
                    m.group("MethodName3")
                )
                meth_sig = m.group("MethodSignature")
                meth_sig = meth_sig and meth_sig.replace('\\\n', '') or ''
                lineno = lineno + src.count('\n', last_lineno_pos, start)
                last_lineno_pos = start
                if meth_name.startswith('self.'):
                    meth_name = meth_name[5:]
                elif meth_name.startswith('self::'):
                    meth_name = meth_name[6:]
                # close all classes/modules indented at least as much
                while classstack and classstack[-1][1] >= thisindent:
                    if (
                            classstack[-1][0] is not None and
                            isinstance(classstack[-1][0],
                                       (Class, Function, RbModule))
                    ):
                        # record the end line of this class, function or module
                        classstack[-1][0].setEndLine(lineno - 1)
                    del classstack[-1]
                while acstack and acstack[-1][1] >= thisindent:
                    del acstack[-1]
                if classstack:
                    csi = -1
                    while csi >= -len(classstack):
                        # nested defs are added to the class
                        cur_class = classstack[csi][0]
                        csi -= 1
                        if cur_class is None:
                            continue

                        if (
                                isinstance(cur_class, Class) or
                                isinstance(cur_class, RbModule)
                        ):
                            # it's a class/module method
                            f = Function(None, meth_name,
                                         None, lineno, meth_sig)
                            cur_class.addMethod(meth_name, f)
                            break
                    else:
                        # it's a nested function of a module function
                        f = Function(
                            self.name, meth_name, self.file, lineno, meth_sig)
                        self.addFunction(meth_name, f)
                    # set access control
                    if acstack:
                        accesscontrol = acstack[-1][0]
                        if accesscontrol == "private":
                            f.setPrivate()
                        elif accesscontrol == "protected":
                            f.setProtected()
                        elif accesscontrol == "public":
                            f.setPublic()
                else:
                    # it's a function
                    f = Function(
                        self.name, meth_name, self.file, lineno, meth_sig)
                    self.addFunction(meth_name, f)
                if not classstack:
                    if lastGlobalEntry:
                        lastGlobalEntry.setEndLine(lineno - 1)
                    lastGlobalEntry = f
                if cur_obj and isinstance(cur_obj, Function):
                    cur_obj.setEndLine(lineno - 1)
                cur_obj = f
                classstack.append((None, thisindent))  # Marker for nested fns

            elif m.start("Docstring") >= 0:
                contents = m.group("DocstringContents")
                if contents is not None:
                    contents = _hashsub(r"\1", contents)
                if cur_obj:
                    cur_obj.addDescription(contents)

            elif m.start("String") >= 0:
                pass

            elif m.start("Comment") >= 0:
                pass

            elif m.start("ClassIgnored") >= 0:
                pass

            elif m.start("Class") >= 0:
                # we found a class definition
                thisindent = indent
                indent += 1
                lineno = lineno + src.count('\n', last_lineno_pos, start)
                last_lineno_pos = start
                # close all classes/modules indented at least as much
                while classstack and classstack[-1][1] >= thisindent:
                    if (
                            classstack[-1][0] is not None and
                            isinstance(classstack[-1][0],
                                       (Class, Function, RbModule))
                    ):
                        # record the end line of this class, function or module
                        classstack[-1][0].setEndLine(lineno - 1)
                    del classstack[-1]
                class_name = m.group("ClassName") or m.group("ClassName2")
                inherit = m.group("ClassSupers")
                if inherit:
                    # the class inherits from other classes
                    inherit = inherit[1:].strip()
                    inherit = [_commentsub('', inherit)]
                # remember this class
                cur_class = Class(self.name, class_name, inherit,
                                  self.file, lineno)
                # add nested classes to the file
                if classstack and isinstance(classstack[-1][0], RbModule):
                    parent_obj = classstack[-1][0]
                else:
                    parent_obj = self
                if class_name in parent_obj.classes:
                    cur_class = parent_obj.classes[class_name]
                elif (
                        classstack and
                        isinstance(classstack[-1][0], Class) and
                        class_name == "self"
                ):
                    cur_class = classstack[-1][0]
                else:
                    parent_obj.addClass(class_name, cur_class)
                if not classstack:
                    if lastGlobalEntry:
                        lastGlobalEntry.setEndLine(lineno - 1)
                    lastGlobalEntry = cur_class
                cur_obj = cur_class
                classstack.append((cur_class, thisindent))
                while acstack and acstack[-1][1] >= thisindent:
                    del acstack[-1]
                acstack.append(["public", thisindent])
                # default access control is 'public'

            elif m.start("Module") >= 0:
                # we found a module definition
                thisindent = indent
                indent += 1
                lineno = lineno + src.count('\n', last_lineno_pos, start)
                last_lineno_pos = start
                # close all classes/modules indented at least as much
                while classstack and classstack[-1][1] >= thisindent:
                    if (
                            classstack[-1][0] is not None and
                            isinstance(classstack[-1][0],
                                       (Class, Function, RbModule))
                    ):
                        # record the end line of this class, function or module
                        classstack[-1][0].setEndLine(lineno - 1)
                    del classstack[-1]
                module_name = m.group("ModuleName")
                # remember this class
                cur_class = RbModule(self.name, module_name,
                                     self.file, lineno)
                # add nested Ruby modules to the file
                if module_name in self.modules:
                    cur_class = self.modules[module_name]
                else:
                    self.addModule(module_name, cur_class)
                if not classstack:
                    if lastGlobalEntry:
                        lastGlobalEntry.setEndLine(lineno - 1)
                    lastGlobalEntry = cur_class
                cur_obj = cur_class
                classstack.append((cur_class, thisindent))
                while acstack and acstack[-1][1] >= thisindent:
                    del acstack[-1]
                acstack.append(["public", thisindent])
                # default access control is 'public'

            elif m.start("AccessControl") >= 0:
                aclist = m.group("AccessControlList")
                if aclist is None:
                    index = -1
                    while index >= -len(acstack):
                        if acstack[index][1] < indent:
                            actype = (
                                m.group("AccessControlType") or
                                m.group("AccessControlType2").split('_')[0]
                            )
                            acstack[index][0] = actype.lower()
                            break
                        else:
                            index -= 1
                else:
                    index = -1
                    while index >= -len(classstack):
                        if (
                                classstack[index][0] is not None and
                                not isinstance(classstack[index][0], Function) and
                                not classstack[index][1] >= indent
                        ):
                            parent = classstack[index][0]
                            actype = (
                                m.group("AccessControlType") or
                                m.group("AccessControlType2").split('_')[0]
                            )
                            actype = actype.lower()
                            for name in aclist.split(","):
                                # get rid of leading ':'
                                name = name.strip()[1:]
                                acmeth = parent.getMethod(name)
                                if acmeth is None:
                                    continue
                                if actype == "private":
                                    acmeth.setPrivate()
                                elif actype == "protected":
                                    acmeth.setProtected()
                                elif actype == "public":
                                    acmeth.setPublic()
                            break
                        else:
                            index -= 1

            elif m.start("Attribute") >= 0:
                lineno = lineno + src.count('\n', last_lineno_pos, start)
                last_lineno_pos = start
                index = -1
                while index >= -len(classstack):
                    if (
                            classstack[index][0] is not None and
                            not isinstance(classstack[index][0], Function) and
                            not classstack[index][1] >= indent
                    ):
                        attrName = m.group("AttributeName")
                        attr = Attribute(
                            self.name, attrName, self.file, lineno)
                        if attrName.startswith("@@") or attrName[0].isupper():
                            classstack[index][0].addGlobal(attrName, attr)
                        else:
                            classstack[index][0].addAttribute(attrName, attr)
                        break
                    else:
                        index -= 1
                else:
                    attrName = m.group("AttributeName")
                    if attrName[0] != "@":
                        attr = Attribute(
                            self.name, attrName, self.file, lineno)
                        self.addGlobal(attrName, attr)
                    if lastGlobalEntry:
                        lastGlobalEntry.setEndLine(lineno - 1)
                    lastGlobalEntry = None

            elif m.start("Attr") >= 0:
                lineno = lineno + src.count('\n', last_lineno_pos, start)
                last_lineno_pos = start
                index = -1
                while index >= -len(classstack):
                    if (
                            classstack[index][0] is not None and
                            not isinstance(classstack[index][0], Function) and
                            not classstack[index][1] >= indent
                    ):
                        parent = classstack[index][0]
                        if m.group("AttrType") is None:
                            nv = m.group("AttrList").split(",")
                            if not nv:
                                break
                            # get rid of leading ':'
                            name = nv[0].strip()[1:]
                            attr = (
                                parent.getAttribute("@" + name) or
                                parent.getAttribute("@@" + name) or
                                Attribute(
                                    self.name, "@" + name, self.file, lineno)
                            )
                            if len(nv) == 1 or nv[1].strip() == "false":
                                attr.setProtected()
                            elif nv[1].strip() == "true":
                                attr.setPublic()
                            parent.addAttribute(attr.name, attr)
                        else:
                            access = m.group("AttrType")
                            for name in m.group("AttrList").split(","):
                                # get rid of leading ':'
                                name = name.strip()[1:]
                                attr = (
                                    parent.getAttribute("@" + name) or
                                    parent.getAttribute("@@" + name) or
                                    Attribute(
                                        self.name, "@" + name, self.file,
                                        lineno)
                                )
                                if access == "_accessor":
                                    attr.setPublic()
                                elif (
                                        access == "_reader" or
                                        access == "_writer"
                                ):
                                    if attr.isPrivate():
                                        attr.setProtected()
                                    elif attr.isProtected():
                                        attr.setPublic()
                                parent.addAttribute(attr.name, attr)
                        break
                    else:
                        index -= 1

            elif m.start("Begin") >= 0:
                # a begin of a block we are not interested in
                indent += 1

            elif m.start("End") >= 0:
                # an end of a block
                indent -= 1
                if indent < 0:
                    # no negative indent allowed
                    if classstack:
                        # it's a class/module method
                        indent = classstack[-1][1]
                    else:
                        indent = 0

            elif m.start("BeginEnd") >= 0:
                pass

    def createHierarchy(self):
        """
        Public method to build the inheritance hierarchy for all classes of
        this module.

        @return A dictionary with inheritance hierarchies.
        """
        hierarchy = {}
        for cls in list(list(self.classes.keys())):
            self.assembleHierarchy(cls, self.classes, [cls], hierarchy)
        for mod in list(list(self.modules.keys())):
            self.assembleHierarchy(mod, self.modules, [mod], hierarchy)
        return hierarchy

    def assembleHierarchy(self, name, classes, path, result):
        """
        Public method to assemble the inheritance hierarchy.

        This method will traverse the class hierarchy, from a given class
        and build up a nested dictionary of super-classes. The result is
        intended to be inverted, i.e. the highest level are the super classes.

        This code is borrowed from Boa Constructor.

        @param name name of class to assemble hierarchy (string)
        @param classes A dictionary of classes to look in.
        @param path
        @param result The resultant hierarchy
        """
        rv = {}
        if name in classes:
            for cls in classes[name].super:
                if cls not in classes:
                    rv[cls] = {}
                    exhausted = path + [cls]
                    exhausted.reverse()
                    self.addPathToHierarchy(
                        exhausted, result, self.addPathToHierarchy)
                else:
                    rv[cls] = self.assembleHierarchy(
                        cls, classes, path + [cls], result)

        if len(rv) == 0:
            exhausted = path
            exhausted.reverse()
            self.addPathToHierarchy(exhausted, result, self.addPathToHierarchy)

    def addPathToHierarchy(self, path, result, fn):
        """
        Public method to put the exhausted path into the result dictionary.

        @param path the exhausted path of classes
        @param result the result dictionary
        @param fn function to call for classe that are already part of the
            result dictionary
        """
        if path[0] in list(list(result.keys())):
            if len(path) > 1:
                fn(path[1:], result[path[0]], fn)
        else:
            for part in path:
                result[part] = {}
                result = result[part]

    def getName(self):
        """
        Public method to retrieve the modules name.

        @return module name (string)
        """
        return self.name

    def getFileName(self):
        """
        Public method to retrieve the modules filename.

        @return module filename (string)
        """
        return self.file

    def getType(self):
        """
        Public method to get the type of the module's source.

        @return type of the modules's source (string)
        """
        if self.type in [PY_SOURCE, PTL_SOURCE]:
            moduleType = "Python3"
        elif self.type == RB_SOURCE:
            moduleType = "Ruby"
        else:
            moduleType = ""
        return moduleType


class Class(VisibilityBase):
    """
    Class to represent a Python class.
    """

    def __init__(self, module, name, superClasses, file, lineno):
        """
        Constructor

        @param module name of module containing this class (string)
        @param name name of the class (string)
        @param superClasses list of classnames this class is inherited from
                (list of strings)
        @param file name of file containing this class (string)
        @param lineno linenumber of the class definition (integer)
        """
        self.module = module
        self.name = name
        if superClasses is None:
            superClasses = []
        self.super = superClasses
        self.methods = {}
        self.attributes = {}
        self.globals = {}
        self.file = file
        self.lineno = lineno
        self.endlineno = -1  # marker for "not set"
        self.description = ""
        self.setPublic()

    def addMethod(self, name, function):
        """
        Public method to add information about a method.

        @param name name of method to be added (string)
        @param function Function object to be added
        """
        self.methods[name] = function

    def getMethod(self, name):
        """
        Public method to retrieve a method by name.

        @param name name of the method (string)
        @return the named method or None
        """
        try:
            return self.methods[name]
        except KeyError:
            return None

    def addAttribute(self, name, attr):
        """
        Public method to add information about attributes.

        @param name name of the attribute to add (string)
        @param attr Attribute object to be added
        """
        if name not in self.attributes:
            self.attributes[name] = attr
        else:
            self.attributes[name].addAssignment(attr.lineno)

    def getAttribute(self, name):
        """
        Public method to retrieve an attribute by name.

        @param name name of the attribute (string)
        @return the named attribute or None
        """
        try:
            return self.attributes[name]
        except KeyError:
            return None

    def addGlobal(self, name, attr):
        """
        Public method to add information about global (class) variables.

        @param name name of the global to add (string)
        @param attr Attribute object to be added
        """
        if name not in self.globals:
            self.globals[name] = attr
        else:
            self.globals[name].addAssignment(attr.lineno)

    def addDescription(self, description):
        """
        Public method to store the class docstring.

        @param description the docstring to be stored (string)
        """
        self.description = description

    def setEndLine(self, endLineNo):
        """
        Public method to record the number of the last line of a class.

        @param endLineNo number of the last line (integer)
        """
        self.endlineno = endLineNo


class RbModule(Class):
    """
    Class to represent a Ruby module.
    """

    def __init__(self, module, name, file, lineno):
        """
        Constructor

        @param module name of module containing this class (string)
        @param name name of the class (string)
        @param file name of file containing this class (string)
        @param lineno linenumber of the class definition (integer)
        """
        Class.__init__(self, module, name, None, file, lineno)
        self.classes = {}

    def addClass(self, name, _class):
        """
        Public method to add information about a class.

        @param name name of class to be added (string)
        @param _class Class object to be added
        """
        self.classes[name] = _class


class Function(VisibilityBase):
    """
    Class to represent a Python function or method.
    """
    General = 0
    Static = 1
    Class = 2

    def __init__(self, module, name, file, lineno, signature='',
                 pyqtSignature=None, modifierType=General, annotation=""):
        """
        Constructor

        @param module name of module containing this function (string)
        @param name name of the function (string)
        @param file name of file containing this function (string)
        @param lineno linenumber of the function definition (integer)
        @param signature the functions call signature (string)
        @param pyqtSignature the functions PyQt signature (string)
        @param modifierType type of the function
        @param annotation return annotation
        """
        self.module = module
        self.name = name
        self.file = file
        self.lineno = lineno
        self.endlineno = -1  # marker for "not set"
        signature = _commentsub('', signature)
        self.parameters = [e.strip() for e in signature.split(',')]
        self.description = ""
        self.pyqtSignature = pyqtSignature
        self.modifier = modifierType
        self.annotation = annotation
        self.setPublic()

    def addDescription(self, description):
        """
        Public method to store the functions docstring.

        @param description the docstring to be stored (string)
        """
        self.description = description

    def setEndLine(self, endLineNo):
        """
        Public method to record the number of the last line of a class.

        @param endLineNo number of the last line (integer)
        """
        self.endlineno = endLineNo


class Attribute(VisibilityBase):
    """
    Class to represent a Python function or method.
    """

    def __init__(self, module, name, file, lineno, isSignal=False):
        """
        Constructor

        @param module name of module containing this function (string)
        @param name name of the function (string)
        @param file name of file containing this function (string)
        @param lineno linenumber of the first attribute assignment (integer)
        @keyparam isSignal flag indicating a signal definition (boolean)
        """
        self.module = module
        self.name = name
        self.file = file
        self.lineno = lineno
        self.isSignal = isSignal
        self.setPublic()
        self.linenos = [lineno]

    def addAssignment(self, lineno):
        """
        Public method to add another assignment line number.

        @param lineno linenumber of the additional attribute assignment
            (integer)
        """
        if lineno not in self.linenos:
            self.linenos.append(lineno)


def readModule(module, path=None, inpackage=False, basename="",
               extensions=None, caching=True, ignoreBuiltinModules=False):
    """
    Function to read a module file and parse it.

    The module is searched in path and sys.path, read and parsed.
    If the module was parsed before, the information is taken
    from a cache in order to speed up processing.

    @param module name of the module to be parsed (string)
    @param path search path for the module (list of strings)
    @param inpackage flag indicating that module is inside a
        package (boolean)
    @param basename a path basename that is deleted from the filename of
        the module file to be read (string)
    @param extensions list of extensions, which should be considered valid
        source file extensions (list of strings)
    @param caching flag indicating that the parsed module should be
        cached (boolean)
    @param ignoreBuiltinModules flag indicating to ignore the builtin modules
        (boolean)
    @return reference to a Module object containing the parsed
        module information (Module)
    """
    global _modules

    if extensions is None:
        _extensions = ['.py', '.pyw', '.ptl', '.rb']
    else:
        _extensions = extensions[:]
    try:
        _extensions.remove('.py')
    except ValueError:
        pass

    modname = module

    if os.path.exists(module):
        path = [os.path.dirname(module)]
        if module.lower().endswith(".py"):
            module = module[:-3]
        if (
                os.path.exists(os.path.join(path[0], "__init__.py")) or
                os.path.exists(os.path.join(path[0], "__init__.rb")) or
                inpackage
        ):
            if basename:
                module = module.replace(basename, "")
            if os.path.isabs(module):
                modname = os.path.splitdrive(module)[1][len(os.sep):]
            else:
                modname = module
            modname = modname.replace(os.sep, '.')
            inpackage = 1
        else:
            modname = os.path.basename(module)
        for ext in _extensions:
            if modname.lower().endswith(ext):
                modname = modname[:-len(ext)]
                break
        module = os.path.basename(module)

    if caching and modname in _modules:
        # we've seen this module before...
        return _modules[modname]

    if not ignoreBuiltinModules and module in sys.builtin_module_names:
        # this is a built-in module
        mod = Module(modname, None, None)
        if caching:
            _modules[modname] = mod
        return mod

    # search the path for the module
    path = [] if path is None else path[:]
    f = None
    if inpackage:
        try:
            f, file, (suff, mode, moduleType) = find_module(
                module, path, _extensions)
        except ImportError:
            f = None
    if f is None:
        fullpath = path[:] + sys.path[:]
        f, file, (suff, mode, moduleType) = find_module(
            module, fullpath, _extensions)
    if f:
        f.close()
    if moduleType not in SUPPORTED_TYPES:
        # not supported source, can't do anything with this module
        _modules[modname] = Module(modname, None, None)
        return _modules[modname]

    mod = Module(modname, file, moduleType)
    try:
        src = Utilities.readEncodedFile(file)[0]
        mod.scan(src)
    except (UnicodeError, IOError):
        pass
    if caching:
        _modules[modname] = mod
    return mod


def _indent(ws):
    """
    Protected function to determine the indent width of a whitespace string.

    @param ws The whitespace string to be cheked. (string)
    @return Length of the whitespace string after tab expansion.
    """
    return len(ws.expandtabs(TABWIDTH))


def find_module(name, path, extensions):
    """
    Module function to extend the Python module finding mechanism.

    This function searches for files in the given path. If the filename
    doesn't have an extension or an extension of .py, the normal search
    implemented in the imp module is used. For all other supported files
    only path is searched.

    @param name filename or modulename to search for (string)
    @param path search path (list of strings)
    @param extensions list of extensions, which should be considered valid
        source file extensions (list of strings)
    @return tuple of the open file, pathname and description. Description
        is a tuple of file suffix, file mode and file type)
    @exception ImportError The file or module wasn't found.
    """
    for ext in extensions:
        if name.lower().endswith(ext):
            for p in path:  # only search in path
                if os.path.exists(os.path.join(p, name)):
                    pathname = os.path.join(p, name)
                    if ext == '.ptl':
                        # Quixote page template
                        return (open(pathname), pathname,
                                ('.ptl', 'r', PTL_SOURCE))
                    elif ext == '.rb':
                        # Ruby source file
                        return (open(pathname), pathname,
                                ('.rb', 'r', RB_SOURCE))
                    else:
                        return (open(pathname), pathname,
                                (ext, 'r', PY_SOURCE))
            raise ImportError

    # standard Python module file
    if name.lower().endswith('.py'):
        name = name[:-3]

    spec = importlib.machinery.PathFinder.find_spec(name, path)
    if spec is None:
        raise ImportError
    if isinstance(spec.loader, importlib.machinery.SourceFileLoader):
        ext = os.path.splitext(spec.origin)[-1]
        return (open(spec.origin), spec.origin, (ext, 'r', PY_SOURCE))

    raise ImportError


def resetParsedModules():
    """
    Module function to reset the list of modules already parsed.
    """
    _modules.clear()


def resetParsedModule(module, basename=""):
    """
    Module function to clear one module from the list of parsed modules.

    @param module Name of the module to be parsed (string)
    @param basename a path basename. This basename is deleted from
        the filename of the module file to be cleared. (string)
    """
    modname = module

    if os.path.exists(module):
        path = [os.path.dirname(module)]
        if module.lower().endswith(".py"):
            module = module[:-3]
        if os.path.exists(os.path.join(path[0], "__init__.py")):
            if basename:
                module = module.replace(basename, "")
            modname = module.replace(os.sep, '.')
        else:
            modname = os.path.basename(module)
        if (
                modname.lower().endswith(".ptl") or
                modname.lower().endswith(".pyw")
        ):
            modname = modname[:-4]
        elif modname.lower().endswith(".rb"):
            modname = modname[:-3]
        module = os.path.basename(module)

    if modname in _modules:
        del _modules[modname]
