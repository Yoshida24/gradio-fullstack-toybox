import pandas as pd
import logging

from datetime import datetime

from modules.util import directory_util
from modules.embeddings.openai_embeddings import (
    check_token,
    embeddings,
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

TITLE = "CSV with Embeddings"
OUTPUT_FILEPATH = "tmp/csv_with_embeddings/"
EMBEDDING_COLUMN = "embeddings"
CONTENT_TRANSFORM = lambda title, content: f"# Title\n{title}\n\n# Content\n{content}"


def transform_csv(df: pd.DataFrame) -> pd.DataFrame:
    # DataFrameの各行に対してEmbeddingsを計算し、新しいカラムに追加
    embeddings_list = []
    for i, row in df.iterrows():
        embedding = embeddings(CONTENT_TRANSFORM(row["title"], row["content"]))
        embeddings_list.append(embedding)

    # 新しく作成したカラムをDataFrameに追加
    df[EMBEDDING_COLUMN] = embeddings_list

    return df


def check_tokens_for_csv(df) -> int:
    wk_token = 0
    for i, row in df.iterrows():
        wk_token += check_token(CONTENT_TRANSFORM(row["title"], row["content"]))
    return wk_token


def on_load_csv_file(file):
    if file is None:
        return [pd.DataFrame([]), pd.DataFrame([])]
    else:
        # CSVファイルを UTF-8 で読み込み、空白データを "None" に変換
        df = pd.read_csv(file).fillna("None")
        tokens = check_tokens_for_csv(df)
        print(f"Tokens: {tokens}")
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


def csv_with_embeddings_tab(gr):
    with gr.Tab(TITLE):
        # ステートの定義
        # データ保持用の不可視データフレーム
        input_data_df = gr.Dataframe(visible=False)

        # UIの定義
        with gr.Row():
            gr.Markdown(
                "CSVファイルにEmbeddingsカラムを追加したデータを作成し、DLします。"
            )
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
                            "CSVファイルを変換(Embeddingsを各行に追加)"
                        )

                # 入力CSVプレビュー
                gr.Markdown("### 入力プレビュー")
                input_table_with_json_preview = gr.Dataframe()
            with gr.Column():
                gr.Markdown("### 出力")
                # JSONプロフィールを追加するボタン

                output_json_file = gr.File(label="Download CSV")

                # 出力CSVプレビュー
                output_table_with_json_preview = gr.Dataframe()

        # ハンドラの定義

        tokens = check_token("Hello World!")
        print(tokens)

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
