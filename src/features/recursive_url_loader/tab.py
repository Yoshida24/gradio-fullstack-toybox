import pandas as pd
import json
import logging

from datetime import datetime
import time
from modules.recursive_url_loader import recursive_url_loader

from modules.util import directory_util

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

OUTPUT_FILEPATH = "tmp/recursive_url_loader/"


def on_download_button_clicked(url_root: str, max_depth: int, selector: str):
    url_list = recursive_url_loader.read_data_and_load_csv(
        url_root, max_depth, selector
    )
    url_list_as_df = pd.DataFrame(url_list)
    filename = f"output_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    filepath = directory_util.create_csv_file_and_path(
        url_list_as_df,
        filepath=f"{OUTPUT_FILEPATH}{filename}",
    )
    return [filepath]


def recursive_url_loader_tab(gr):
    with gr.Tab("Recursive URL Loader"):
        # UIの定義
        with gr.Row():
            gr.Markdown(
                "[Recursive URL Loader](https://python.langchain.com/docs/integrations/document_loaders/recursive_url/) によりURLを取得しcsvに保存"
            )
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 入力")
                url_input = gr.Textbox(
                    value="https://docs.python.org/3.11/", label="Root URL"
                )
                max_depth = gr.Number(value=2, label="Max Depth")
                root_selector = gr.Textbox(value="body", label="Root Selector")

                # JSONプロフィールを追加するボタン
                convert_csv_button = gr.Button("ページをcsvに保存")

            with gr.Column():
                gr.Markdown("### 出力")
                # JSONプロフィールを追加するボタン

                output_csv_file = gr.File(label="Download Dataset")

        # ハンドラの定義

        # JSONプロフィールを追加するボタンのハンドラ
        convert_csv_button.click(
            fn=on_download_button_clicked,
            inputs=[url_input, max_depth, root_selector],
            outputs=[
                output_csv_file,
            ],
        )
