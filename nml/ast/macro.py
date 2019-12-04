__license__ = """
NML is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

NML is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with NML; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA."""

from nml import generic, global_constants
from nml.ast import base_statement
from nml.expression import Type

class Macro(base_statement.BaseStatement):
    def __init__(self, name, param_list, expr, pos):
        base_statement.BaseStatement.__init__(self, "macro", pos, False, False)
        if name in global_constants.macros:
            raise generic.ScriptError("Macro with name '{}' has already been defined".format(name), pos)
        self.name = name
        self.param_list = []
        for p in param_list:
            if p in self.param_list:
                raise generic.ScriptError("Duplicate parameter '{}'".format(p), pos)
            self.param_list.append(p)
        self.expr = expr
        global_constants.macros[name.value] = self

    def debug_print(self, indentation):
        generic.print_dbg(indentation, 'Macro declaration:', self.name.value)
        generic.print_dbg(indentation + 2, 'Parameters:')
        for param in self.param_list:
            param.debug_print(indentation + 4)
        generic.print_dbg(indentation + 2, 'Expression:')
        self.expr.debug_print(indentation + 4)

    def get_action_list(self):
        return []

    def __str__(self):
        return "macro {}({}) {};\n".format(str(self.name), ", ".join([str(param) for param in self.param_list]), str(self.expr))

    def type(self):
        return Type.FUNCTION_PTR

    def call(self, params = []):
        if len(params) != len(self.param_list):
            raise generic.ScriptError("Macro '{}' expected {} parameters, got {}".format(self.name, len(self.param_list), len(params)))
        param_dict = {}
        for i, param in enumerate(self.param_list):
            param_dict[param.value] = params[i]
        return self.expr.reduce([(param_dict, lambda a,b: a)] + global_constants.const_list)
