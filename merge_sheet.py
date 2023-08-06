import pandas as pd
import os

def merge_csv_files(a_csv_path, b_csv_path, output_csv_path, pk):
    
    for path in [a_csv_path, b_csv_path]:
        if not os.path.exists(path):
            print(f"!!!!\"{path}\" doesn't exists!!!!")
            return

    # 讀取A版和B版的CSV檔
    a_df = pd.read_csv(a_csv_path)
    b_df = pd.read_csv(b_csv_path)

    # 合併兩個DataFrame，保留B版中所有的內容，並補上A版可能缺失的資料
    merged_df = pd.merge(a_df, b_df, on=pk, how='outer', suffixes=('', '_y'))

    # 更新A版的資料
    for column in a_df.columns:
        if column != pk and column+'_y' in merged_df:
            merged_df[column].update(merged_df.pop(column+'_y'))

    # 寫入新的CSV檔
    merged_df.to_csv(output_csv_path, index=False)
    print(f"合併已完成")
    print(f"合併檔在在\"{output_path}\"")

if __name__ == "__main__":
    a_path = input("請輸入你的.csv檔案位置：")
    b_path = input("請輸入新的.csv檔案位置：")
    output_path = input("請輸入新的檔案名稱：")
    merge_csv_files(a_path, b_path, output_path, "資產編號")

