
import gradio as gr
import time
import json
import tempfile
from utils.router import auto_route_response

def respond(user_message, chat_history):
    start_time = time.time()
    response, chosen_model, token_count = auto_route_response(user_message)
    elapsed_time = round(time.time() - start_time, 2)

    metadata = {
        "chosen_model": chosen_model,
        "tokens_used": token_count,
        "inference_time": f"{elapsed_time}s"
    }

    json_response = json.dumps({
        "request": {"user_message": user_message},
        "response": {"text": response, "metadata": metadata}
    }, ensure_ascii=False, indent=2)

    chat_history.append({"role": "user", "content": f"[{chosen_model}] {user_message}"})
    chat_history.append({"role": "assistant", "content": response})
    return "", chat_history, json_response

def download_history(history):
    content = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as tmp:
        tmp.write(content)
        return tmp.name

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# **MCP-Style Multi-Model Chatbot(Lightweight Version)**")

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="대화 내용", type="messages", height=400)
            msg = gr.Textbox(label="질문 입력", placeholder="질문을 입력하세요...")
            json_output = gr.Code(label="Response JSON", language="json", interactive=False)
            download_btn = gr.Button("대화 내역 다운로드")
        with gr.Column(scale=1):
            gr.Markdown("### **Feature Description**\n- Automatic Model Selection (MCP-style)\n- Lightweight Model Architecture\n- Fixed Download Handling")

    msg.submit(respond, [msg, chatbot], [msg, chatbot, json_output])
    download_btn.click(download_history, chatbot, gr.File(file_types=[".txt"], label="다운로드"))

if __name__ == "__main__":
    demo.launch()
