import os
import json
import pandas as pd

# 假設你有一個字典 data

def create_session(session_name, csv, path="./sessions"):
    cwd = os.getcwd()
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

    os.chdir(cwd)

def check_item(session_name, item_id, path="./sessions"):
    session_path = f"{path}/{session_name}.json"
    with open(session_path, "r") as f:
        data = json.load(f)
    
    if not item_id in data["all"]:
        return "item_not_in_the_session"

    if not item_id in data["not_checked"] and item_id in data["checked"]:
        return "item_checked"

    data["checked"].append(item_id)
    data["not_checked"].remove(item_id)

    with open(session_path, "w") as f:
        json.dump(data,f)

    return "done"

def get_not_done(session_name, path="./sessions", location_filter=None):
    session_path = f"{path}/{session_name}.json"
    with open(session_path, "r") as f:
        data = json.load(f)
    
    not_checked = data["not_checked"]
    csv_path = data["csv"]

    df = pd.read_csv(csv_path)

    output_list = []

    for not_checked_id in not_checked:
        # 讀取 CSV 文件

        # 選取某一 column 的值等於特定值的 row
        selected_row = df.loc[df['資產編號'] == not_checked_id]
        

        # 將該 row 的所有資料以 dict 的形式返回
        row_dict = selected_row.to_dict(orient='records')[0]

        if location_filter == None or row_dict["位置描述"] == location_filter:
            output_list.append(row_dict)
            print(row_dict)
        else:
            continue

    return output_list







if __name__ == "__main__":
    # create_session(csv="./csvs/Newcsv.csv", session_name="my_session")
    # print(check_item("my_session","C010602131"))
    print(get_not_done("my_session", location_filter="庫房(中)"))
    

