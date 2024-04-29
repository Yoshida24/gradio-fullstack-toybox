from pathlib import Path
from pandas import DataFrame


def create_csv_file_and_path(
    df: DataFrame,
    filepath: str,
) -> str:
    """_summary_

    Args:
        df (DataFrame): input data
        filepath (str): file path (both absolute and relative are OK)

    Returns:
        str: file like string
    """
    # パスが存在しない場合はディレクトリを作成
    Path(filepath).parent.mkdir(exist_ok=True)
    # データフレームをCSV形式で保存
    df.to_csv(filepath, index=False)
    # pathを計算し返す
    return filepath
