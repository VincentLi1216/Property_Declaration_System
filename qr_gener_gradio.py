import gradio as gr
import util_qr_gener
import os
import pds_gradio, util_json
import json
import cv2

sessions = pds_gradio.get_choices("./sessions", ".json")

def btn_indiv_click(item_name, item_id, path):
    qr = util_qr_gener.create_one_qr_sticker(item_id, item_name)
    path = os.path.join("./qr_cache/",path)
    os.makedirs(path,exist_ok=True)
    cv2.imwrite(os.path.join(path, f"{item_id}.png"), qr)
    return qr



def dp_session_change(session):
    with open(session, "r") as f:
        data = json.load(f)
    csv = data["csv"]
    locs = util_json.get_all_locs(csv)
    print(locs)

    return gr.Dropdown.update(choices=locs)


with gr.Blocks() as demo:
    gr.Markdown("# QR Code Generator\n ### github: https://github.com/VincentLi1216/Property_Declaration_System")
    with gr.Tab("Session"):
        dp_session = gr.Dropdown(sessions)
        tb_name_session = gr.Textbox(label="Enter the Folder Name")
        btn_session = gr.Button(value="Generate QR Code")
    with gr.Tab("Location"):
        dp_session_loc = gr.Dropdown(sessions)
        dp_loc_loc = gr.Dropdown(interactive=True)
        tb_name_loc = gr.Textbox(label="Enter the Folder Name")
        btn_loc = gr.Button(value="Generate QR Code")
    with gr.Tab("Individual"):
        tb_item_name_indiv = gr.Textbox(label="Enter Item's Name")
        tb_item_id_indiv = gr.Textbox(label="Enter Item's ID")
        tb_name_indiv = gr.Textbox(label="Enter the Folder Name")
        btn_indiv = gr.Button(value="Generate QR Code")

        output_indiv = gr.Image()

    dp_session_loc.change(dp_session_change, inputs=[dp_session_loc], outputs=[dp_loc_loc])
    btn_indiv.click(btn_indiv_click, inputs=[tb_item_name_indiv, tb_item_id_indiv,tb_name_indiv], outputs=[output_indiv])


if __name__ == "__main__":
    demo.launch(debug=True, share=True)
        

