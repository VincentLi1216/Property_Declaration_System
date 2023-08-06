import gradio as gr

# 定義一個函數，該函數將輸入的數字乘以 2
def double_number(input_str):
    number = float(input_str)
    print(f"the number is {number}")
    return number * 2

# 建立一個 gradio 介面
iface = gr.Interface(
    fn=double_number,  # 呼叫的函數
    inputs="text",  # 輸入類型是文字框
    outputs="text",  # 輸出類型也是文字
)

# 運行介面
iface.launch(share=True)

