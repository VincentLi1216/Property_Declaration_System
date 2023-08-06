import gradio as gr
import os
import util_json


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
print(sessions)

def btn_new_session_click(session_name, csv):
    global sessions, csvs
    print("hi")
    util_json.create_session(session_name, csv)
    sessions.append(f"sessions/{session_name}.json")
    return gr.Dropdown.update(choices=sessions)





with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            with gr.Column():
                new_session_name = gr.Textbox(label="New PD session")
                new_session_csv = gr.Dropdown(choices=csvs, label = "Import csv from")
                selected_session = gr.Dropdown(sessions, label = "Choose your session", interactive=True)
                with gr.Row():
                    btn_new_session = gr.Button(value="Create New session")
                    btn_select_session = gr.Button(value="Select session")
        with gr.Column():
            output = gr.Textbox(label="output")


    btn_new_session.click(btn_new_session_click, inputs=[new_session_name, new_session_csv], outputs=selected_session)


if __name__ == "__main__":

    demo.launch(debug=True)
    # print(get_choices("./csvs", ".csv"))
