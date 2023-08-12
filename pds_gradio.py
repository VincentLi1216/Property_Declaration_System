import gradio as gr
import os
import util_json, util_qr, util_zip
import json
from pyzbar.pyzbar import decode
from PIL import Image


def get_choices(path, file_type=None, check_file_type=True):
    if not os.path.exists(path):
        print(f"!!!!{path} deosn't exists!!!!")
        return

    files = os.listdir(path) 
    
    if check_file_type:
        for file in files:
            if not file.endswith(file_type):
                files.remove(file)
    else:
        for file in files:
            if file.endswith(".DS_Store"):
                files.remove(file)

    for i in range(len(files)):
        files[i] = os.path.join(path, files[i])

    return files

sessions = get_choices("sessions", ".json")
csvs = get_choices("csvs", ".csv")
session = ""
upload_folders = get_choices("./upload_img", check_file_type=False)
num_item = None
checked = None

def btn_new_session_click(session_name, csv):
    global sessions, csvs
    util_json.create_session(session_name, csv)
    sessions.append(f"sessions/{session_name}.json")
    return gr.Dropdown.update(choices=sessions)

def btn_select_session_click(session_name):
    global session, num_item, checked
    session = session_name

    with open(session_name, "r") as f:
        data = json.load(f)

    num_item = len(data["all"])
    checked = len(data["checked"])
    infos = f"Session: {session}\nTotal: {num_item}\nCompletion: {checked}/{num_item}({checked/num_item}%)"
    return infos

def btn_submit_click(img1, img2, img3, img4, img5, img6, img7, img8, img9, img10, upload_folder=""):
    img_list = []
    qr_list = []
    file_list = []
    output = ""
    black_file_list = [".DS_Store"]
    print(upload_folder)
    if upload_folder != "":
        for file in os.listdir(upload_folder):
            file_list.append(os.path.join(upload_folder, file))

        for file in os.listdir(upload_folder):
            for black_list in black_file_list:
                if file.endswith(black_list):
                    file_list.remove(os.path.join(upload_folder, file))
        for file in file_list:
            img_list.append(Image.open(file))
            
        print(img_list)
    else:
        for img in [img1, img2, img3, img4, img5, img6, img7, img8, img9, img10]:
            if img is not None:
                img_list.append(img)

    for img in img_list:
        qr_list.append(util_qr.read_qr_code(img))

    print(qr_list)
    for qr in qr_list:
        if qr == None:
            qr_list.remove(qr)
        else:
            print(util_json.check_item(session, qr))

    item_dict = util_json.get_not_done_loc_dict(session)

    for key in item_dict.keys():
        output += f"\n\n\n-----{key}-----\n"
        # print(f"\n\n-----{key}-----")
        for item in item_dict[key]:
            item_id = item["資產編號"]
            item_name = item["中文名稱"]
            output += f"{item_id} {item_name}\n"
    print(item_dict)
    print(output)
    return output


with gr.Blocks() as demo:
    gr.Markdown("# Property Declaration System\n ### github: https://github.com/VincentLi1216/Property_Declaration_System")
    with gr.Row():
        with gr.Column():
            with gr.Column():
                with gr.Tab("Select Session"):
                    selected_session = gr.Dropdown(sessions, label = "Choose your session", interactive=True)
                    session_textbox = gr.Textbox(label="Session info")
                    btn_select_session = gr.Button(value="Select")
                with gr.Tab("Create Session"):
                    new_session_name = gr.Textbox(label="Create new session")
                    new_session_csv = gr.Dropdown(choices=csvs, label = "Import csv from")
                    create_selected_session = gr.Dropdown(sessions, label = "Choose your session", interactive=True)
                    create_session_textbox = gr.Textbox(label="Session info")
                    with gr.Row():
                        btn_new_session = gr.Button(value="Create")
                        btn_create_select_session = gr.Button(value="Select")
            with gr.Tab("Upload Pictures"):
                # upload_file = gr.File()
                upload_folder = gr.Dropdown(upload_folders, label="Select Image Folder")
            with gr.Tab("Take Pictures"):
                img1 = gr.Image(label="QR code #1")
                img2 = gr.Image(label="QR code #2")
                img3 = gr.Image(label="QR code #3")
                img4 = gr.Image(label="QR code #4")
                img5 = gr.Image(label="QR code #5")
                img6 = gr.Image(label="QR code #6")
                img7 = gr.Image(label="QR code #7")
                img8 = gr.Image(label="QR code #8")
                img9 = gr.Image(label="QR code #9")
                img10 = gr.Image(label="QR code #10")
            btn_submit = gr.Button(value="Submit")
        with gr.Column():
            output = gr.Textbox(label="output", interactive=True).style(show_copy_button=True)


    btn_new_session.click(btn_new_session_click, inputs=[new_session_name, new_session_csv], outputs=selected_session)
    btn_select_session.click(btn_select_session_click, inputs=selected_session, outputs=session_textbox)
    btn_create_select_session.click(btn_select_session_click, inputs=create_selected_session, outputs=create_session_textbox)
    btn_submit.click(btn_submit_click, inputs=[img1, img2, img3, img4, img5, img6, img7, img8, img9, img10, upload_folder],outputs=output)


if __name__ == "__main__":

    demo.launch(debug=True, share = True)
    # print(get_choices("./csvs", ".csv"))
