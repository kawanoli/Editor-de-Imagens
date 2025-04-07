import matplotlib.pyplot as plt
import gradio as gr
import cv2
import numpy as np

# Function to process the image and convert it (this is the modified version of your upload_image function)
def upload_image(input_img):
    # Converte a imagem de entrada para um numpy array
    img_array = np.array(input_img)
    # Converte de RBG (da entrada no gradio) para o BGR que o OpenCV recebe de entrada
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    # Converte de BGR para RGB
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return img_rgb

# Funcão para pegar a imagem (chama função upload) e a opção
def process_image_and_option(image, option):
    # processa a imagem
    processed_image = upload_image(image)
    
    # Retorna a imagem e a opção
    return processed_image, f"Opção selecionada: {option}"

# Função pra criar a interface (unica função é armazenar o gr.Blocks())
def create_interface():
    with gr.Blocks() as demo:
        # Label do input
        image_input = gr.Image(label="Imagem upada", type="pil")
        
        # Botões de opção
        option = gr.Radio(["Transformações Geométricas", "Operações de Cores", "Correção Gamma e Clareamento"], label="Escolha uma opção:")
        
        # Saídas de texto
        output_image = gr.Image(label="Imagem processada")
        output_text = gr.Textbox(label="Opção selecionada")
        
        # Triggers de ação pra mudança de imagem
        image_input.change(fn=process_image_and_option, inputs=[image_input, option], outputs=[output_image, output_text])
        option.change(fn=process_image_and_option, inputs=[image_input, option], outputs=[output_image, output_text])
    
    demo.launch()

# Chamada da função que cria a interface
create_interface()