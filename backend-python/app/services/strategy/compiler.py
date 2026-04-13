"""Strategy code compiler and validator."""

import ast
import traceback
from dataclasses import dataclass, field


@dataclass
class CompilationResult:
    success: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class StrategyCompiler:
    """Compile and validate strategy code."""

    FORBIDDEN_IMPORTS = {"os", "sys", "subprocess", "shutil", "pathlib", "socket", "http"}
    REQUIRED_METHODS = {"on_init", "on_bar"}

    def compile(self, code: str, strategy_type: str = "script") -> CompilationResult:
        result = CompilationResult()
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            result.success = False
            result.errors.append(f"Syntax error at line {e.lineno}: {e.msg}")
            return result

        self._check_imports(tree, result)
        if strategy_type == "script":
            self._check_required_methods(tree, result)
        return result

    def _check_imports(self, tree: ast.AST, result: CompilationResult) -> None:
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in self.FORBIDDEN_IMPORTS:
                        result.success = False
                        result.errors.append(f"Forbidden import: {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split(".")[0] in self.FORBIDDEN_IMPORTS:
                    result.success = False
                    result.errors.append(f"Forbidden import: {node.module}")

    def _check_required_methods(self, tree: ast.AST, result: CompilationResult) -> None:
        defined_functions = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defined_functions.add(node.name)
        missing = self.REQUIRED_METHODS - defined_functions
        if missing:
            result.warnings.append(f"Missing recommended methods: {', '.join(missing)}")

    def execute_safe(self, code: str, context: dict | None = None) -> dict:
        safe_globals = {"__builtins__": {}}
        if context:
            safe_globals.update(context)
        try:
            exec(code, safe_globals)  # noqa: S102
            return {"success": True, "namespace": {k: v for k, v in safe_globals.items() if not k.startswith("_")}}
        except Exception:
            return {"success": False, "error": traceback.format_exc()}
