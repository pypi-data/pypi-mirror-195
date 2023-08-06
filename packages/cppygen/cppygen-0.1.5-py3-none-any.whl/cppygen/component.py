from typing import Dict, List, Tuple, cast


class Function(object):
    """
    Function を表すクラス。
    必要な情報を詰め込み、 to_pybind_string で生成する。
    """

    def __init__(self):
        self._return_type: str = ""
        self._arguments: List[Tuple[str, str]] = []
        self._name: str | None = None
        self._full_name: str | None = None
        self._namespace: List[str] = []
        self._description = ""
        self._module: str | None = None
        self._pyname: str | None = None

    def set_name(self, name: str, namespace: List[str]):
        self._name = name
        self._namespace = namespace
        self._full_name = f"{'::'.join(namespace)}::{name}"

    def set_return_type(self, type: str):
        self._return_type = type

    def set_argument_types(self, types: List[Tuple[str, str]]):
        """
        parameter: [(name, type),]
        """
        self._arguments = types

    @property
    def pyname(self):
        self._pyname

    @pyname.setter
    def pyname(self, python_name: str):
        self._pyname = python_name

    def add_argument_type(self, type: Tuple[str, str]):
        """
        parameter: (name, type)
        """
        self._arguments.append(type)

    def set_description(self, description: str):
        self._description = description

    def set_module(self, module: str):
        self._module = module

    def to_pybind_string(self):
        if self._name == None or self._full_name == None or self._module == None:
            print("Parse Error Skipping ...")
            return ""
        args = [f', pybind11::arg("{i[0]}")' for i in self._arguments]
        if self._pyname is not None:
            return (
                f'{self._module}.def("{self._pyname}", &{self._full_name}, "{self._description}"'
                f'{"".join(args)});'
            )
        else:
            return (
                f'{self._module}.def("{self._name}", &{self._full_name}, "{self._description}"'
                f'{"".join(args)});'
            )

    def to_decl_string(self):
        if self._name == None or self._full_name == None or self._module == None:
            print("Parse Error Skipping ...")
            return ""
        args = [f"{i[1]} {i[0]}" for i in self._arguments]
        return (
            f'namespace {"::".join(self._namespace)} '
            f'{{ {self._return_type} {self._name}({", ".join(args)}); }}'
        )

    def signature(self) -> str:
        args = [f"{i[1]} {i[0]}" for i in self._arguments]
        return f'{"::".join(self._namespace)}::{self._name}({", ".join(args)}) -> {self._return_type}'

    def __eq__(self, obj):
        if isinstance(obj, Function):
            return self._full_name == obj._full_name
        else:
            return False


class StructOrClass:
    """
    Struct や Class を表すクラス
    必要な情報を詰め込み、 to_pybind_string で生成する。
    """

    def __init__(self):
        self._name: str | None = None
        self._namespace: List[str] = []
        self._members: list[Dict[str, bool | str]] = []
        self._member_funcs: list[Dict[str, bool | str | List[Tuple[str, str]]]] = []
        self._module: str | None = None
        self._description = ""

    def set_name(self, name: str, namespace: List[str]):
        self._name = name
        self._namespace = namespace
        self._full_name = f"{'::'.join(namespace)}::{name}"

    def add_member(
        self, name: str, type: str, description: str = "", private: bool = False
    ):
        self._members.append(
            {
                "name": name,
                "type": type,
                "description": description,
                "private": private,
            }
        )

    def add_member_func(
        self,
        name: str,
        type: str,
        args: List[Tuple[str, str]],  # list[(name, type)]
        description: str = "",
        private: bool = False,
    ):
        self._member_funcs.append(
            {
                "name": name,
                "return_type": type,
                "description": description,
                "private": private,
                "args": args,
            }
        )

    def set_module(self, module: str):
        self._module = module

    def set_description(self, description: str):
        self._description = description

    def get_members(self):
        return self._members

    def get_member_funcs(self):
        return self._member_funcs

    def to_pybind_string(self):
        if self._name == None or self._module == None:
            print("Parse Error Skipping ...")
            return ""
        return (
            f'pybind11::class_<::{self._full_name}>({self._module}, "{self._name}")\n'
            "\t\t.def(pybind11::init())"
            ## Member 変数の宣言
            + "\n".join(
                [""]
                + [
                    f'\t\t.def_readwrite("{i["name"]}",'
                    f' &{self._full_name}::{i["name"]}, "{i["description"]}")'
                    for i in self._members
                    if not i["private"]
                ]
            )
            ## Member 関数の宣言
            + "\n".join(
                [""]
                + [
                    f'\t\t.def("{i["name"]}",'
                    f' &{self._full_name}::{i["name"]}, "{i["description"]}")'
                    for i in self._member_funcs
                    if not i["private"]
                ]
            )
            + ";"
        )

    def signature(self) -> str:
        return f"{self._full_name}"


class Submodule:
    """
    Submodule を表すクラス
    必要な情報を詰め込み、 to_pybind_string で生成する。
    """

    def __init__(self):
        self._name: str | None = None
        self._description = ""
        self._parents: List[str] = []

    @property
    def cpp_name(self) -> str:
        if self._name == None:
            print("Parse Error Skipping ...")
            return ""
        return "_".join(self._parents) + "_" + self._name

    @property
    def cpp_parent_name(self) -> str:
        if self._name == None:
            print("Parse Error Skipping ...")
            return ""
        return "_".join(self._parents)

    def set_name(self, name: str):
        self._name = name

    def set_description(self, description: str):
        self._description = description

    def set_parent(self, parents: List[str]):
        self._parents = parents

    def to_pybind_string(self):
        if self._name == None:
            print("Parse Error Skipping ...")
            return ""
        return f'auto {self.cpp_name} = {self.cpp_parent_name}.def_submodule("{self._name}", "{self._description}");'

    def __eq__(self, obj):
        if isinstance(obj, Submodule):
            return self.cpp_name == obj.cpp_name
        else:
            return False

