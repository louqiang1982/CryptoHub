"""Indicator code quality checker.

Analyses user-submitted indicator/strategy code for:
- Security issues (forbidden imports, dangerous calls)
- Code style (PEP 8 basics, naming conventions)
- Performance hints (nested loops, repeated calculations)
- API completeness (required method signatures)
"""

from __future__ import annotations

import ast
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class IssueSeverity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class CodeIssue:
    severity: IssueSeverity
    code: str
    message: str
    line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "line": self.line,
        }


@dataclass
class QualityReport:
    score: float  # 0–100
    issues: list[CodeIssue] = field(default_factory=list)
    passed: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": round(self.score, 1),
            "passed": self.passed,
            "issues": [i.to_dict() for i in self.issues],
            "error_count": sum(1 for i in self.issues if i.severity == IssueSeverity.ERROR),
            "warning_count": sum(1 for i in self.issues if i.severity == IssueSeverity.WARNING),
        }


# Modules forbidden for security reasons
FORBIDDEN_MODULES = {
    "os", "subprocess", "sys", "shutil", "glob", "pathlib",
    "socket", "urllib", "http", "requests", "httpx",
    "builtins", "importlib", "__import__", "eval", "exec",
    "open", "compile", "pickle", "marshal",
}

# Required methods for a valid strategy class
REQUIRED_STRATEGY_METHODS = {"on_bar", "on_init"}
OPTIONAL_STRATEGY_METHODS = {"on_start", "on_stop", "on_order", "on_position"}


class IndicatorCodeQualityChecker:
    """Analyse indicator/strategy code for quality and security issues."""

    def check(self, code: str) -> QualityReport:
        issues: list[CodeIssue] = []

        # 1. Parse AST
        try:
            tree = ast.parse(code)
        except SyntaxError as exc:
            return QualityReport(
                score=0.0,
                passed=False,
                issues=[
                    CodeIssue(
                        severity=IssueSeverity.ERROR,
                        code="E001",
                        message=f"Syntax error: {exc.msg}",
                        line=exc.lineno,
                    )
                ],
            )

        # 2. Security checks
        issues.extend(self._check_security(tree))

        # 3. Method completeness
        issues.extend(self._check_methods(tree))

        # 4. Code style
        issues.extend(self._check_style(code, tree))

        # 5. Performance hints
        issues.extend(self._check_performance(tree))

        # Calculate score
        error_count = sum(1 for i in issues if i.severity == IssueSeverity.ERROR)
        warning_count = sum(1 for i in issues if i.severity == IssueSeverity.WARNING)
        score = max(0.0, 100.0 - error_count * 25.0 - warning_count * 5.0)
        passed = error_count == 0

        return QualityReport(score=score, issues=issues, passed=passed)

    # ------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------

    def _check_security(self, tree: ast.AST) -> list[CodeIssue]:
        issues: list[CodeIssue] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in FORBIDDEN_MODULES:
                        issues.append(CodeIssue(
                            severity=IssueSeverity.ERROR,
                            code="S001",
                            message=f"Forbidden import: '{alias.name}'",
                            line=node.lineno,
                        ))
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split(".")[0] in FORBIDDEN_MODULES:
                    issues.append(CodeIssue(
                        severity=IssueSeverity.ERROR,
                        code="S001",
                        message=f"Forbidden import: '{node.module}'",
                        line=node.lineno,
                    ))
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile"}:
                    issues.append(CodeIssue(
                        severity=IssueSeverity.ERROR,
                        code="S002",
                        message=f"Dangerous call: '{node.func.id}'",
                        line=node.lineno,
                    ))
        return issues

    def _check_methods(self, tree: ast.AST) -> list[CodeIssue]:
        issues: list[CodeIssue] = []
        class_defs = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        if not class_defs:
            return issues

        for cls in class_defs:
            method_names = {
                n.name for n in ast.walk(cls) if isinstance(n, ast.FunctionDef)
            }
            for required in REQUIRED_STRATEGY_METHODS:
                if required not in method_names:
                    issues.append(CodeIssue(
                        severity=IssueSeverity.WARNING,
                        code="M001",
                        message=f"Missing recommended method: '{required}'",
                        line=cls.lineno,
                    ))
        return issues

    def _check_style(self, code: str, tree: ast.AST) -> list[CodeIssue]:
        issues: list[CodeIssue] = []
        lines = code.splitlines()
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append(CodeIssue(
                    severity=IssueSeverity.INFO,
                    code="C001",
                    message=f"Line too long ({len(line)} > 120 characters)",
                    line=i,
                ))
        return issues

    def _check_performance(self, tree: ast.AST) -> list[CodeIssue]:
        issues: list[CodeIssue] = []
        for node in ast.walk(tree):
            # Detect nested for loops (potential O(n²) issues in on_bar)
            if isinstance(node, ast.For):
                for child in ast.walk(node):
                    if child is not node and isinstance(child, ast.For):
                        issues.append(CodeIssue(
                            severity=IssueSeverity.INFO,
                            code="P001",
                            message="Nested loop detected — may be slow in on_bar()",
                            line=node.lineno,
                        ))
                        break
        return issues
