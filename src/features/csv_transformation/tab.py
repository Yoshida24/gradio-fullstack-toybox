import pandas as pd
import json
import logging

from datetime import datetime
import time

from modules.util import directory_util

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

OUTPUT_FILEPATH = "tmp/csv_transformation/"


def transform_csv(df) -> pd.DataFrame:
    # DataFrameの各行にJSONプロフィールを追加
    transformed_df = df.copy()
    result = []

    for i, row in df.iterrows():
        logger.debug(f"{i} / {len(df)}")
        profile = json.dumps(dict(row))
        result.append(profile)
        time.sleep(0.5)
    transformed_df["json"] = result
    return transformed_df


def on_load_csv_file(file):
    # CSVファイルを読み込む
    df = pd.read_csv(file)
    full_data = df
    preview_data = df
    return [full_data, preview_data]


def on_convert_csv_button_clicked(df):
    converted_df = transform_csv(df)
    preview_data = converted_df
    filename = f"output_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    filepath = directory_util.create_csv_file_and_path(
        converted_df,
        filepath=f"{OUTPUT_FILEPATH}{filename}",
    )
    return [preview_data, filepath]


def csv_transformation_tab(gr):
    with gr.Tab("CSV Transformation"):
        # ステートの定義
        # データ保持用の不可視データフレーム
        input_data_df = gr.Dataframe(visible=False)

        # UIの定義
        with gr.Row():
            gr.Markdown("CSVファイルにJSON列を追加したデータを作成し、DLします。")
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 入力")
                with gr.Row():
                    with gr.Column():
                        # CSVファイルをアップロードするための入力インターフェース
                        file_input = gr.File(label="CSVファイルをアップロード")
                    with gr.Column():
                        # JSONプロフィールを追加するボタン
                        convert_csv_button = gr.Button(
                            "CSVファイルを変換(JSONを各行に追加)"
                        )

                # 入力CSVプレビュー
                gr.Markdown("### 入力プレビュー")
                input_table_with_json_preview = gr.Dataframe()
            with gr.Column():
                gr.Markdown("### 出力")
                # JSONプロフィールを追加するボタン

                output_json_file = gr.File(label="Download JSON Profile")

                # 出力CSVプレビュー
                output_table_with_json_preview = gr.Dataframe()

        # ハンドラの定義

        # CSVファイルアップロードのハンドラ
        file_input.change(
            on_load_csv_file,
            inputs=[file_input],
            outputs=[
                input_data_df,
                input_table_with_json_preview,
            ],
        )

        # JSONプロフィールを追加するボタンのハンドラ
        convert_csv_button.click(
            fn=on_convert_csv_button_clicked,
            inputs=[input_data_df],
            outputs=[
                output_table_with_json_preview,
                output_json_file,
            ],
        )
