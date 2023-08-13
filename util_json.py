import os
import json
import pandas as pd
import math

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

def check_item(session_path, item_id, path="./sessions"):
    # session_path = f"{path}/{session_name}.json"
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


def get_not_done_loc_dict(session_path):
    with open(session_path, "r") as f:
        data = json.load(f)
    
    not_checked = data["not_checked"]
    csv_path = data["csv"]

    df = pd.read_csv(csv_path)

    output_list = []
    locations = []
    nan_appended = False
    loc_dict = {}

    for not_checked_id in not_checked:
        

        # 選取某一 column 的值等於特定值的 row
        selected_row = df.loc[df['資產編號'] == not_checked_id]

        # 將該 row 的所有資料以 dict 的形式返回
        row_dict = selected_row.to_dict(orient='records')[0]
        item_loc = row_dict["位置描述"] 
        print(row_dict["位置描述"])

        if item_loc not in locations:
            if str(item_loc) == "nan":
                if not nan_appended:
                    locations.append("無位置描述")
                    loc_dict["無位置描述"] = [row_dict]
                    nan_appended = True
                else:
                    loc_dict["無位置描述"].append(row_dict)
            else:
                locations.append(item_loc)
                loc_dict[item_loc] = [row_dict]

        else:
            loc_dict[item_loc].append(row_dict)

    return loc_dict

def get_all_locs(session):
    df = pd.read_csv(session)
    # print(df.columns)
    location_descriptions = df['位置描述'].tolist()
    location_descriptions = list(set(location_descriptions))

    for i in range(len(location_descriptions)):
        if str(location_descriptions[i]) == "nan":
            location_descriptions[i] = "無位置描述"
    print(location_descriptions)
    location_descriptions = sorted(location_descriptions)


    return location_descriptions






if __name__ == "__main__":
    # create_session(csv="./csvs/Newcsv.csv", session_name="my_session")
    # print(check_item("my_session","C010602131"))
    # print(get_not_done("my_session", location_filter="庫房(中)"))
    # get_not_done_loc_dict("./sessions/Iphone1.json")
    get_all_locs("./csvs/HIHI.csv")
    

