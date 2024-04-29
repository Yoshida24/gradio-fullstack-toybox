import gradio as gr
from features.csv_transformation.tab import csv_transformation_tab
from features.recursive_url_loader.tab import recursive_url_loader_tab
import dotenv


dotenv.load_dotenv()


with gr.Blocks() as demo:
    # add tabs
    recursive_url_loader_tab(gr)
    csv_transformation_tab(gr)


demo.launch(share=False)
