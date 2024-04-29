import gradio as gr
from features.csv_transformation.tab import csv_transformation_tab
from features.csv_with_embeddings.tab import csv_with_embeddings_tab
from features.recursive_url_loader.tab import recursive_url_loader_tab
import dotenv


dotenv.load_dotenv()


with gr.Blocks() as demo:
    # add tabs
    csv_with_embeddings_tab(gr)
    recursive_url_loader_tab(gr)
    csv_transformation_tab(gr)


demo.launch(share=False)
