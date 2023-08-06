import gradio as gr
import os

#     b = gr.Number(label="b")
#     with gr.Row():
#         add_btn = gr.Button("Add")
#         sub_btn = gr.Button("Subtract")
#     c = gr.Number(label="sum")

#     def add(num1, num2):
#         return num1 + num2
#     add_btn.click(add, inputs=[a, b], outputs=c)

#     def sub(data):
#         return data[a] - data[b]
#     sub_btn.click(sub, inputs={a, b}, outputs=c)

sessions = ["session1", "session2"]

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

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            with gr.Column():
                gr.Textbox(label="New PD session")
                gr.Dropdown(choices=csvs, label = "Import csv from")
                gr.Dropdown(choices=sessions, label = "Choose your session")
                with gr.Row():
                    gr.Button(value="Create New session")
                    gr.Button(value="Select session")
        with gr.Column():
            gr.Textbox(label="output")

if __name__ == "__main__":

    demo.launch()
    # print(get_choices("./csvs", ".csv"))
