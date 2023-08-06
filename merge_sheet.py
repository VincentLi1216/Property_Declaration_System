import pandas as pd

def merge_csv_files(a_csv_path, b_csv_path, output_csv_path, pk):
    # 讀取A版和B版的CSV檔
    a_df = pd.read_csv(a_csv_path)
    b_df = pd.read_csv(b_csv_path)

    # 合併兩個DataFrame，只保留B版中有更新的內容
    merged_df = a_df.merge(b_df, on=pk, how='left', suffixes=('', '_y'))

    # 更新A版的資料
    for column in a_df.columns:
        if column != pk and column+'_y' in merged_df:
            merged_df[column].update(merged_df.pop(column+'_y'))

    # 寫入新的CSV檔
    merged_df.to_csv(output_csv_path, index=False)

# 呼叫函式
merge_csv_files('活頁簿A.csv', '活頁簿B.csv', '輸出.csv', 'pk')
