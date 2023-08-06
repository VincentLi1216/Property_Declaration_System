import os
import json
import pandas as pd

# 假設你有一個字典 data

def create_session(csv, session_name, path="./sessions"):
    # 確保父目錄存在
    os.makedirs(os.path.dirname(path), exist_ok=True)

    data = {"csv":csv ,"all":[], "checked":[], "not_checked":[]}


    # 讀取 CSV 文件
    df = pd.read_csv(csv)

    # 選取一個 column 的全部資料
    column_data = df['資產編號']
    column_data = column_data.tolist()

    data["not_checked"] = column_data
    data["all"] = column_data


    os.chdir(path)
    file_name = f"{session_name}.json"
    # 現在你可以安全地寫入文件
    with open(file_name, 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    create_session(csv="./csvs/Newcsv.csv", session_name="my_session")

