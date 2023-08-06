from importlib.resources import files
from string import Template

from yapygen.meta import Meta


def load_template(name: str) -> Template:
    """加载模板文件

    Args:
        name (str): 文件名

    Returns:
        Template: 加载后的模板
    """
    root = files("yapygen.gen").joinpath("templates")
    content = root.joinpath(name).read_text(encoding="utf-8")
    return Template(content)


def render(name: str, meta: Meta, /, **kwargs: str) -> str:
    """根据元信息渲染模板

    Args:
        name (str): 模板名称
        meta (Meta): 元信息

    Returns:
        str: 渲染后的字符串
    """
    param = meta._asdict()
    param.update(kwargs)
    return load_template(name).safe_substitute(param)
