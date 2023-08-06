from typing import Final, Generator, Type
import ast


__version__: Final[str] = "1.0"


AF100: Final[str] = "AF100 Found assert"


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: list[tuple[int, int, str]] = []

    def visit_Assert(self, node: ast.Assert) -> None:
        self.errors.append((node.lineno, node.col_offset, AF100))


class Plugin:
    name = "flake8-assert-finder"
    version = __version__

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    def run(self) -> Generator[tuple[int, int, str, Type["Plugin"]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)
        for line, col, msg in visitor.errors:
            yield line, col, msg, type(self)
