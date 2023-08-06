import gradio as gr
import os
import util_json, util_qr
import json
from pyzbar.pyzbar import decode


def get_choices(path, file_type):
    if not os.path.exists(path):
        print(f"!!!!{path} deosn't exists!!!!")
        return

    files = os.listdir(path) 

    for file in files:
        if not file.endswith(file_type):
            files.remove(file)

    for i in range(len(files)):
        files[i] = os.path.join(path, files[i])

    return files

sessions = get_choices("sessions", ".json")
csvs = get_choices("csvs", ".csv")
session = ""
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

def btn_submit_click(img1, img2, img3, img4, img5, img6, img7, img8, img9, img10):
    img_list = []
    qr_list = []
    for img in [img1, img2, img3, img4, img5, img6, img7, img8, img9, img10]:
        if img is not None:
            img_list.append(img)

    for img in img_list:
        qr_list.append(util_qr.read_qr_code(img))

    print(qr_list)
    for qr in qr_list:
        if qr == None:
            qr_list.remove(qr)
    return qr_list



with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            with gr.Column():
                new_session_name = gr.Textbox(label="Create new session")
                new_session_csv = gr.Dropdown(choices=csvs, label = "Import csv from")
                selected_session = gr.Dropdown(sessions, label = "Choose your session", interactive=True)
                session_textbox = gr.Textbox(label="Session info")
                with gr.Row():
                    btn_new_session = gr.Button(value="Create")
                    btn_select_session = gr.Button(value="Select")
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
            output = gr.Textbox(label="output")


    btn_new_session.click(btn_new_session_click, inputs=[new_session_name, new_session_csv], outputs=selected_session)
    btn_select_session.click(btn_select_session_click, inputs=selected_session, outputs=session_textbox)
    btn_submit.click(btn_submit_click, inputs=[img1, img2, img3, img4, img5, img6, img7, img8, img9, img10],outputs=output)


if __name__ == "__main__":

    demo.launch(debug=True, share = True)
    # print(get_choices("./csvs", ".csv"))
