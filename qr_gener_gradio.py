import gradio as gr
import util_qr_gener
import os
import pds_gradio, util_json
import json
import cv2

sessions = pds_gradio.get_choices("./sessions", ".json")

def btn_indiv_click(item_name, item_id, path):
    qr = util_qr_gener.create_one_qr_sticker(item_id, item_name)
    path = os.path.join("./qr_cache",path)
    os.makedirs(path,exist_ok=True)
    cv2.imwrite(os.path.join(path, f"{item_id}.png"), qr)
    return qr

def btn_loc_click(session, loc, x_num, y_num, path):
    qrs = util_qr_gener.create_qr_stickers4location(session, loc, int(x_num), int(y_num))
    path = os.path.join("./qr_cache",path)
    os.makedirs(path,exist_ok=True)
    # print(path)
    for i in range(len(qrs)):
        cv2.imwrite(os.path.join(path, f"{loc}{i}.png"), qrs[i])
        # print(os.path.join(path, f"{loc}-{i+1}.png"))
    cwd = os.getcwd()
    return f"Done\nFolder path: {os.path.join(cwd, 'qr_cache', path)}"

def btn_session_click(session, x_num, y_num,path):
    qrs,loc_dict = util_qr_gener.create_qr_stickers4session(session, int(x_num), int(y_num))
    path = os.path.join("./qr_cache",path)
    os.makedirs(path,exist_ok=True)
    print(loc_dict)
    for i in range(len(qrs)):
        cv2.imwrite(os.path.join(path, f"{i+1}.png"), qrs[i])
        # cv2.imwrite(os.path.join(path, f"{i}-{loc_dict[i]}.png"), qrs[i])
        # print(os.path.join(path, f"{loc}-{i+1}.png"))
    cwd = os.getcwd()
    return f"Done\nFolder path: {os.path.join(cwd, 'qr_cache', path)}"
    

def dp_session_change(session):
    with open(session, "r") as f:
        data = json.load(f)
    csv = data["csv"]
    locs = util_json.get_all_locs(csv)
    # print(locs)

    return gr.Dropdown.update(choices=locs)


with gr.Blocks() as demo:
    gr.Markdown("# QR Code Generator\n ### github: https://github.com/VincentLi1216/Property_Declaration_System")
    with gr.Tab("Session"):
        dp_session = gr.Dropdown(sessions)
        with gr.Row():
            x_num_session = gr.Textbox(label="Number of Column")
            y_num_session = gr.Textbox(label="Number of Row")
        tb_name_session = gr.Textbox(label="Enter the Folder Name")
        btn_session = gr.Button(value="Generate QR Code")
        output_session = gr.Textbox(label="Completion")
    with gr.Tab("Location"):
        dp_session_loc = gr.Dropdown(sessions)
        dp_loc_loc = gr.Dropdown(interactive=True)
        with gr.Row():
            x_num = gr.Textbox(label="Number of Column")
            y_num = gr.Textbox(label="Number of Row")
        tb_name_loc = gr.Textbox(label="Enter the Folder Name")
        btn_loc = gr.Button(value="Generate QR Code")
        output_loc = gr.Textbox(label="Completion")
    with gr.Tab("Individual"):
        tb_item_name_indiv = gr.Textbox(label="Enter Item's Name")
        tb_item_id_indiv = gr.Textbox(label="Enter Item's ID")
        tb_name_indiv = gr.Textbox(label="Enter the Folder Name")
        btn_indiv = gr.Button(value="Generate QR Code")

        output_indiv = gr.Image()

    dp_session_loc.change(dp_session_change, inputs=[dp_session_loc], outputs=[dp_loc_loc])
    btn_indiv.click(btn_indiv_click, inputs=[tb_item_name_indiv, tb_item_id_indiv,tb_name_indiv], outputs=[output_indiv])
    btn_loc.click(btn_loc_click, inputs=[dp_session_loc, dp_loc_loc, x_num, y_num, tb_name_loc], outputs=output_loc)
    btn_session.click(btn_session_click, inputs=[dp_session, x_num_session, y_num_session, tb_name_session], outputs=[output_session])


if __name__ == "__main__":
    demo.launch(debug=True, share=True)
        

