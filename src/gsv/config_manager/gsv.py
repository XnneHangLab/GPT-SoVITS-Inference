"""运行 Streamlit 应用前将当前项目的根目录绝对路径写入配置文件
因为 Streamlit 应用启动后，读取根目录绝对路径会默认变成 `.`, 无法访问 `packages`, 而 packages 存储了各自模块的 ui, 必须访问。
所以这里将根目录绝对路径写入配置文件 `root.toml` 中。在 Streamlit 启动前运行，然后供它全局使用。
"""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field

from gsv.config_manager.config import load_settings_file, search_for_settings_file


class GPTSoVITSSetting(BaseModel):
    i18n_dir: Annotated[str, Field("./i18n", title="存放 i18n locale 的目录")]  # 项目根目录, 实时计算绝对目录。



def main():
    path = search_for_settings_file("gpt_sovits.toml")
    if path is not None:
        path.unlink()
    settings = load_settings_file("gpt_sovits.toml", GPTSoVITSSetting)