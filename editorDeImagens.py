import gradio as gr
import cv2
import numpy as np
from PIL import Image

# PIL → OpenCV
def pil_to_cv(image_pil):
    return cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

# OpenCV → PIL
def cv_to_pil(image_cv):
    if len(image_cv.shape) == 2:
        return Image.fromarray(image_cv)
    else:
        image_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
        return Image.fromarray(image_rgb)

# ===== TRANSFORMAÇÕES =====

def apply_translation(image, dx, dy):
    img = pil_to_cv(image)
    rows, cols = img.shape[:2]
    matrix = np.float32([[1, 0, dx], [0, 1, dy]])
    translated = cv2.warpAffine(img, matrix, (cols, rows))
    return cv_to_pil(translated)

def apply_rotation(image, angle):
    img = pil_to_cv(image)
    rows, cols = img.shape[:2]
    center = (cols // 2, rows // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1)
    rotated = cv2.warpAffine(img, matrix, (cols, rows))
    return cv_to_pil(rotated)

def apply_scaling(image, scale_factor):
    img = pil_to_cv(image)
    scaled = cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    return cv_to_pil(scaled)

# ===== CORES =====

def color_space_transform(image, option):
    img = pil_to_cv(image)
    if option == "RGB para Grayscale":
        return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    elif option == "RGB para HSV":
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return Image.fromarray(cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB))
    return image

def apply_contrast(image, value):
    img = np.array(image).astype(np.float32)
    img = np.clip(img * value, 0, 255).astype(np.uint8)
    return Image.fromarray(img)

# ===== GAMMA =====

def apply_gamma_correction(image, gamma_value):
    inv_gamma = 1.0 / gamma_value
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in np.arange(256)]).astype("uint8")
    img = pil_to_cv(image)
    corrected = cv2.LUT(img, table)
    return cv_to_pil(corrected)

# ===== PROCESSAMENTO GERAL =====

def process_image(image, main_option, sub_option, contrast, dx, dy, angle, scale, gamma):
    if main_option == "Operações de Cores":
        if sub_option in ["RGB para Grayscale", "RGB para HSV"]:
            return color_space_transform(image, sub_option), f"{main_option} - {sub_option}"
        elif sub_option == "Ajuste de contraste":
            return apply_contrast(image, contrast), f"{main_option} - Contraste"

    elif main_option == "Transformações Geométricas":
        if sub_option == "Translação":
            return apply_translation(image, dx, dy), f"{main_option} - Translação"
        elif sub_option == "Rotação":
            return apply_rotation(image, angle), f"{main_option} - Rotação"
        elif sub_option == "Escala":
            return apply_scaling(image, scale), f"{main_option} - Escala"

    elif main_option == "Correção Gamma e Clareamento":
        if sub_option == "Controle de gamma":
            return apply_gamma_correction(image, gamma), f"{main_option} - Gamma {gamma:.2f}"

    return image, "Nenhuma operação realizada"

# ===== INTERFACE GRADIO =====

def update_suboptions(main_option):
    if main_option == "Operações de Cores":
        return gr.update(choices=["RGB para Grayscale", "RGB para HSV", "Ajuste de contraste"], visible=True)
    elif main_option == "Transformações Geométricas":
        return gr.update(choices=["Translação", "Rotação", "Escala"], visible=True)
    elif main_option == "Correção Gamma e Clareamento":
        return gr.update(choices=["Controle de gamma"], visible=True)
    else:
        return gr.update(visible=False)

def update_controls(sub_option):
    return (
        gr.update(visible=sub_option == "Ajuste de contraste"),  # contraste
        gr.update(visible=sub_option == "Translação"),          # dx
        gr.update(visible=sub_option == "Translação"),          # dy
        gr.update(visible=sub_option == "Rotação"),             # ângulo
        gr.update(visible=sub_option == "Escala"),              # escala
        gr.update(visible=sub_option == "Controle de gamma")    # gamma
    )

def create_interface():
    with gr.Blocks() as demo:
        gr.Markdown("## CV Image Editor - by Kawan Oliveira")

        with gr.Row():
            image_input = gr.Image(type="pil", label="Imagem de Entrada")
            output_image = gr.Image(label="Imagem Processada")

        output_text = gr.Textbox(label="Descrição da Operação")

        main_option = gr.Radio(["Transformações Geométricas", "Operações de Cores", "Correção Gamma e Clareamento"],
                               label="Categoria:")
        sub_option = gr.Radio([], label="Operação:", visible=False)

        contrast_slider = gr.Slider(0.5, 3.0, 1.0, 0.1, label="Contraste", visible=False)
        dx_slider = gr.Slider(-300, 300, 0, 1, label="Deslocamento Horizontal", visible=False)
        dy_slider = gr.Slider(-300, 300, 0, 1, label="Deslocamento Vertical", visible=False)
        angle_slider = gr.Slider(0, 360, 0, 1, label="Ângulo de Rotação (°)", visible=False)
        scale_slider = gr.Slider(0.1, 3.0, 1.0, 0.1, label="Fator de Escala", visible=False)
        gamma_slider = gr.Slider(0.1, 3.0, 1.0, 0.1, label="Valor Gamma", visible=False)

        main_option.change(fn=update_suboptions, inputs=main_option, outputs=sub_option)
        sub_option.change(fn=update_controls, inputs=sub_option,
                          outputs=[contrast_slider, dx_slider, dy_slider, angle_slider, scale_slider, gamma_slider])

        process_btn = gr.Button("Processar imagem")

        process_btn.click(
            fn=process_image,
            inputs=[image_input, main_option, sub_option, contrast_slider,
                    dx_slider, dy_slider, angle_slider, scale_slider, gamma_slider],
            outputs=[output_image, output_text]
        )

    demo.launch()

# Chama a função que cria a interface
create_interface()