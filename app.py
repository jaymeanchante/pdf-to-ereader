import gradio as gr

# State for configuration values
config_state = gr.State({
    "base_url": "http://localhost:1234/v1",
    "api_key": "123",
    "model": "ocr-model"
})

def process_pdf(pdf_file):
    if pdf_file is None:
        return None, "No file uploaded yet"
    # For now, just display the file name
    file_name = pdf_file.name.split("/")[-1] if "/" in pdf_file.name else pdf_file.name.split("\\")[-1]
    return pdf_file, f"Uploaded file: {file_name}"

def update_config(config, base_url, api_key, model):
    config["base_url"] = base_url
    config["api_key"] = api_key
    config["model"] = model
    return config

def open_config(config):
    return (
        gr.update(visible=True),
        config["base_url"],
        config["api_key"],
        config["model"]
    )

def close_config():
    return gr.update(visible=False)

with gr.Blocks() as demo:
    gr.Markdown("# PDF to e-reader")
    
    # State for configuration
    config_state = gr.State({
        "base_url": "http://localhost:1234/v1",
        "api_key": "123",
        "model": "ocr-model"
    })
    
    # First row: Title and configuration button
    with gr.Row():
        with gr.Column(scale=9):
            gr.Markdown("## Upload your PDF, wait a few minutes and you will have a nicely formatted file")
        with gr.Column(scale=1):
            config_btn = gr.Button("⚙️")
    
    # Configuration modal (initially hidden)
    with gr.Row(visible=False) as config_modal:
        with gr.Column():
            gr.Markdown("### Configuration")
            base_url_input = gr.Textbox(label="base_url", value="http://localhost:1234/v1")
            api_key_input = gr.Textbox(label="api_key", value="123")
            model_input = gr.Textbox(label="model", value="ocr-model")
            with gr.Row():
                save_config_btn = gr.Button("Save", variant="primary")  # Orange button
                close_config_btn = gr.Button("Close")
    
    # Second row: Upload button and text display
    with gr.Row():
        pdf_upload = gr.File(label="Upload PDF", file_types=[".pdf"], scale=1, height=75)
    with gr.Row():
        with gr.Column(scale=1):
            pdf_viewer = gr.Textbox(label="PDF Preview", lines=20)  # For side-by-side comparison
        with gr.Column(scale=1):
            text_output = gr.Textbox(label="Converted Text", lines=20)
    
    # Event handling
    pdf_upload.change(
        process_pdf,
        inputs=pdf_upload,
        outputs=[pdf_viewer, text_output]
    )
    
    # Configuration modal toggle
    config_btn.click(
        open_config,
        inputs=config_state,
        outputs=[config_modal, base_url_input, api_key_input, model_input]
    )
    
    save_config_btn.click(
        update_config,
        inputs=[config_state, base_url_input, api_key_input, model_input],
        outputs=config_state
    ).then(
        close_config,
        None,
        config_modal
    )
    
    close_config_btn.click(
        close_config,
        None,
        config_modal
    )

if __name__ == "__main__":
    demo.launch()