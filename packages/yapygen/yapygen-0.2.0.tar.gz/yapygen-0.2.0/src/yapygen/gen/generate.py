import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from InquirerPy.prompts.confirm import ConfirmPrompt

from yapygen.gen.template_utils import render
from yapygen.meta.meta import Meta


def generate_project(meta: Meta) -> None:
    """生成整个项目

    Args:
        meta (Meta): 元信息
    """
    current_dir: bool = ConfirmPrompt(
        message="Generate in current directory:", default=False
    ).execute()
    output = Path.cwd() if current_dir else Path.cwd() / meta.name
    setup(output)
    generate_files(meta, output)
    generate_directories(meta, output)


def generate_directories(meta: Meta, output: Path) -> None:
    """生成项目的子目录

    主要是生成源代码目录 src 与测试代码目录 tests

    Args:
        meta (Meta): 元信息
        output (Path): 输出目录
    """
    src = output / "src"
    src.mkdir()
    (src / meta.package).mkdir()
    (src / meta.package / "__init__.py").touch()
    tests = output / "tests"
    tests.mkdir()
    (tests / f"test_{meta.package}").mkdir()
    (tests / f"test_{meta.package}" / "__init__.py").touch()


def generate_files(meta: Meta, output: Path) -> None:
    """生成项目文件

    Args:
        meta (Meta): 元信息
        output (Path): 输出目录
    """
    (output / ".gitignore").write_text(render("gitignore", meta), encoding="utf-8")
    (output / ".flake8").write_text(render(".flake8", meta), encoding="utf-8")
    (output / ".pre-commit-config.yaml").write_text(
        render("pre-commit", meta), encoding="utf-8"
    )
    (output / meta.license_name).write_text(
        render(f"licenses/{meta.license}", meta, year=str(datetime.now().year)),
        encoding="utf-8",
    )
    (output / "pyproject.toml").write_text(
        render(
            "pyproject",
            meta,
            license_name=meta.license_name,
        ),
        encoding="utf-8",
    )
    (output / "README.md").write_text(render("README", meta), encoding="utf-8")


def setup(output: Path) -> None:
    """初始化项目根目录

    Args:
        output (Path): 根目录
    """
    if not output.exists():
        output.mkdir()
    if any(output.iterdir()):
        if ConfirmPrompt(
            message=f"Target {output.name} is not empty, remove contents:",
            default=False,
        ).execute():
            for i in output.iterdir():
                if i.is_dir():
                    shutil.rmtree(i)
                else:
                    os.remove(i)
        else:
            print("Exit without generate project.")
            sys.exit(0)
