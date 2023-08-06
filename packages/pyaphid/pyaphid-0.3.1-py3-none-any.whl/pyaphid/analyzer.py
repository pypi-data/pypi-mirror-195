from __future__ import annotations

import abc
import os
import os.path
import typing as t

import ast_comments as ast

from pyaphid.helpers import echo_with_line_ref


class ImportFrom(t.NamedTuple):
    value: ast.ImportFrom
    import_string: str
    alias: str | None


class Import(t.NamedTuple):
    value: ast.Import
    import_string: str
    alias: str | None


class CallMatch(t.NamedTuple):
    call: ast.Call
    match: str


def get_call_signature(call: ast.Call) -> tuple[str, str]:
    basename = ""
    path = ""
    if isinstance(call.func, ast.Attribute):
        basename = call.func.attr
        call_func = call.func.value
        while isinstance(call_func, ast.Attribute):
            path = f".{call_func.attr}{path}"
            call_func = call_func.value

        if isinstance(call_func, ast.Name):
            path = call_func.id + path
        elif isinstance(call_func, ast.Call):
            sub_path, sub_basename = get_call_signature(call_func)
            path = f"{sub_path}.{sub_basename}(){path}"

    elif isinstance(call.func, ast.Name):
        basename = call.func.id

    return (path, basename)


def replace_alias(import_: ImportFrom | Import, path: str):
    if import_.alias and (path == import_.alias or path.startswith(import_.alias)):
        return path.replace(import_.alias, import_.import_string, 1)
    return path


def expand_call(call: ast.Call, imports: list[Import], import_froms: list[ImportFrom]):
    """
    Expand call with the matching import string.
    If the call does not match an import and is not a built-in function, None is returned
    """
    (path, basename) = get_call_signature(call)
    if "(" in path or ")" in path:
        return None
    work_path = path
    if path:
        for import_ in reversed(imports):
            work_path = replace_alias(import_, work_path)
            if work_path == import_.import_string or work_path.startswith(
                f"{import_.import_string}."
            ):
                return f"{work_path}.{basename}"
            work_path = path
    for import_from in reversed(import_froms):
        imported_name: str = import_from.import_string.rsplit(".", 1)[1]
        if path:
            work_path = replace_alias(import_from, work_path)
            if work_path == imported_name or work_path.startswith(f"{imported_name}."):
                return f"{work_path.replace(imported_name, import_from.import_string, 1)}.{basename}"  # noqa: E501
        elif (
            import_from.alias
            and basename == import_from.alias
            or imported_name == basename
        ):
            return import_from.import_string
    return basename if not path and basename in __builtins__ else None  # type: ignore


TContextDef = t.TypeVar(
    "TContextDef", bound="ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef"
)


class ImportsTracker(metaclass=abc.ABCMeta):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.import_froms: list[ImportFrom] = []
        self.imports: list[Import] = []

    @abc.abstractmethod
    def generic_visit(self, node: ast.AST) -> t.Any:
        pass

    def _process_new_scope(self, node: TContextDef) -> TContextDef:
        old_imports = self.imports.copy()
        old_import_froms = self.import_froms.copy()
        self.generic_visit(node)
        self.imports = old_imports
        self.import_froms = old_import_froms
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        return self._process_new_scope(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        return self._process_new_scope(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        return self._process_new_scope(node)

    def visit_Import(self, node: ast.Import):
        for name in node.names:
            self.imports.append(Import(node, name.name, name.asname))
        self.generic_visit(node)
        return node

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.ImportFrom:
        if node.module is not None and node.module != "__future__" and not node.level:
            for name in node.names:
                self.import_froms.append(
                    ImportFrom(node, f"{node.module}.{name.name}", name.asname)
                )
        elif node.level:
            dir_path = os.path.dirname(os.path.abspath(self.file_path))
            import_path: list[str] = []

            while "__init__.py" in os.listdir(dir_path):
                dir_path, directory = dir_path.rsplit(os.path.sep, 1)
                import_path.insert(0, directory)

            if len(import_path) < node.level:
                return node

            if node.level > 1:
                import_path = import_path[: -node.level + 1]

            if node.module:
                import_path.append(node.module)

            for name in node.names:
                self.import_froms.append(
                    ImportFrom(
                        node,
                        f"{'.'.join(import_path[:])}.{name.name}",
                        name.asname,
                    )
                )
        self.generic_visit(node)
        return node


class CommentIgnore(metaclass=abc.ABCMeta):
    PYAPHID_IGNORE_COMMENT = "#pyaphid:ignore"

    @abc.abstractmethod
    def generic_visit(self, node: ast.AST) -> t.Any:
        pass

    def __init__(self, *args, **kwargs) -> None:
        self._ignore_lines: list[int] = []  # pragma: no cover

    @classmethod
    def _is_ignore_comment(cls, comment: str):
        return comment.replace(" ", "").lower() == cls.PYAPHID_IGNORE_COMMENT

    def check_ignore_comment_visit(self, node: ast.AST):
        if hasattr(node, "body"):
            for sub_node in node.body:  # type: ignore
                if isinstance(sub_node, ast.Comment) and self._is_ignore_comment(
                    sub_node.value
                ):
                    self._ignore_lines.append(sub_node.lineno)
        self.generic_visit(node)
        return node

    def visit_Comment(self, node: ast.Comment):
        if self._is_ignore_comment(node.value):
            self._ignore_lines.append(node.lineno)
        self.generic_visit(node)

        return node

    def visit_Expr(self, node: ast.Expr):
        return self.check_ignore_comment_visit(node)

    def visit_Return(self, node: ast.Return):
        return self.check_ignore_comment_visit(node)

    def visit_With(self, node: ast.With):
        return self.check_ignore_comment_visit(node)

    def visit_If(self, node: ast.If):
        return self.check_ignore_comment_visit(node)

    def visit_AsyncWith(self, node: ast.AsyncWith):
        return self.check_ignore_comment_visit(node)

    def visit_For(self, node: ast.For):
        return self.check_ignore_comment_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor):
        return self.check_ignore_comment_visit(node)


class ExpandedCallCollector(ast.NodeVisitor, ImportsTracker):
    def __init__(self, file_path: str, *args, **kw) -> None:
        self.calls: list[CallMatch] = []
        super().__init__(file_path)

    def visit_Call(self, node: ast.Call) -> None:
        expanded_call_signature = expand_call(node, self.imports, self.import_froms)
        if expanded_call_signature:
            self.calls.append(CallMatch(node, expanded_call_signature))

        self.generic_visit(node)


class VisitorMixIn(ImportsTracker, CommentIgnore):
    def __init__(self, file_path: str, forbidden: list[str]) -> None:
        self.file_path = file_path
        self.forbidden = forbidden.copy()
        self.ignored_forbidden: list[str] = []
        self.matches: list[CallMatch] = []
        self._nodes_in_class_context: list[ast.AST] = []
        self._ignore_lines: list[int] = []
        super().__init__(file_path=file_path)

    def is_forbidden(self, signature: str):
        for pattern in self.forbidden:
            if pattern.endswith(".*") and signature.startswith(
                pattern.rsplit(".", 1)[0]
            ):
                return True
            elif signature == pattern and signature not in self.ignored_forbidden:
                return True
        return False

    def _ignore_forbidden_assignment(self, target: ast.Name):
        if target.id not in self.ignored_forbidden:
            self.ignored_forbidden.append(target.id)

        echo_with_line_ref(
            self.file_path,
            target,
            f"Assignment of {target.id} collides with forbidden built-in. {target.id} calls will be ignored in this scope",  # noqa: E501
        )

    def visit_Assign(self, node: ast.Assign):
        if node not in self._nodes_in_class_context:
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in self.forbidden:
                    self._ignore_forbidden_assignment(target)
        self.generic_visit(node)
        return node

    def visit_AnnAssign(self, node: ast.AnnAssign):
        if node not in self._nodes_in_class_context:
            if isinstance(node.target, ast.Name) and node.target.id in self.forbidden:
                self._ignore_forbidden_assignment(node.target)
        self.generic_visit(node)
        return node

    def _process_new_scope(self, node: TContextDef) -> TContextDef:
        if node.name in self.forbidden and node not in self._nodes_in_class_context:
            if node.name not in self.ignored_forbidden:
                self.ignored_forbidden.append(node.name)
            echo_with_line_ref(
                self.file_path,
                node,
                f"Local definition of {node.name} collides with forbidden built-in. {node.name} calls will be ignored in this scope",  # noqa: E501
            )
        old_ignored_forbidden = self.ignored_forbidden.copy()
        super()._process_new_scope(node)
        self.ignored_forbidden = old_ignored_forbidden
        return node

    def visit_Call(self, node: ast.Call) -> ast.Call | None:
        expanded_call_signature = expand_call(node, self.imports, self.import_froms)
        self.generic_visit(node)
        if (
            node.lineno not in self._ignore_lines
            and expanded_call_signature
            and self.is_forbidden(expanded_call_signature)
        ):
            self.matches.append(CallMatch(node, expanded_call_signature))
            return None
        return node

    def visit_ClassDef(self, node: ast.ClassDef):
        old_nodes = self._nodes_in_class_context.copy()
        self._nodes_in_class_context.extend(node.body)
        super().visit_ClassDef(node)
        self._nodes_in_class_context = old_nodes
        return node


class Visitor(ast.NodeVisitor, VisitorMixIn):
    pass


class Transformer(ast.NodeTransformer, VisitorMixIn):
    pass
