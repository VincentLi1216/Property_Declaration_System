import gradio as gr
import pandas as pd
import os
import pds_gradio as pds

csvs = pds.get_choices("csvs", ".csv")

def btn_merge_click(csvA, csvB, file_name):
    save_path = os.path.join("./csv", file_name)
    print(save_path)
    merge_csv_files(csvA, csvB, os.path.join("./csvs", file_name), pk="資產編號")


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
    # print(f"合併檔在在\"{output_path}\"")

with gr.Blocks() as demo:
    gr.Markdown("# CSV Merge System")
    csvA = gr.Dropdown(csvs, label="csv-A (你的csv)")
    csvB = gr.Dropdown(csvs, label="csv-B (總務的csv)")
    new_file_name = gr.Textbox(label="New File Name")
    btn_merge = gr.Button(value="Merge csv")
    btn_merge.click(btn_merge_click,inputs=[csvA, csvB, new_file_name])


if __name__ == "__main__":
    # a_path = input("請輸入你的.csv檔案位置：")
    # b_path = input("請輸入新的.csv檔案位置：")
    # output_path = input("請輸入新的檔案名稱：")
    # merge_csv_files(a_path, b_path, output_path, "資產編號")
    demo.launch(debug=True, share = True)
    

