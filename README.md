# Exercício Integrado: Transformações e Processamento de Imagens com Gradio

**Objetivo:** Implemente um aplicativo interativo que permita realizar diversas operações de processamento de imagens, incluindo transformações geométricas, manipulação de cores e ajustes de iluminação. O aplicativo deve ser desenvolvido usando a biblioteca Gradio para criar uma interface amigável.

Tarefas a serem implementadas:

1. **Transformações Geométricas**

Translação: Permita ao usuário especificar os valores de deslocamento horizontal e vertical

Rotação: Ofereça um controle deslizante para selecionar o ângulo de rotação (0° a 360°)

Escala: Inclua opções para ampliar/reduzir a imagem com fatores configuráveis

2. **Operações de Cores**

Conversão de espaços de cor: RGB para Grayscale, HSV e outros

Ajuste de contraste: Multiplicação por constante com slider para controle

3. **Correção Gamma e Clareamento**

Controle de gamma: Implemente um slider para ajustar o valor gamma (0.1 a 3.0)

Visualização progressiva: Mostre o efeito cumulativo do ajuste gamma

> Lembre-se que permitar que as imagens modificadas possam ser salvas.

---
### Primeiras implementações:

Como primeiro passo a ser realizado, devemos primeiro garantir que o nosso projeto esteja coletando a imagem para se trabalhar em cima. Utilizando a biblioteca Gradio, temos disponível uma função pronta para realizar essa "coleta" de imagem.
```python 
def upload_image(input_img):
    return input_img
```

Sabemos também que precisamos criar a nossa interface e colocar os "blocos" (widgets) do programa que vão executar cada coisa na tela (similar ao que é feito no Flutter). Sendo assim, criamos o nosso bloco do gr.Blocks() com o nome de demo, e lançamos o nosso bloco demo para ser executado com o demo.launch()
```python 
def create_interface():
    with gr.Blocks() as demo:
    ...
    demo.launch()
```
Criamos como uma função chamada create_interface apenas para organizar e definir onde deve ser chamada a criação e execução da nossa interface Gradio no código do projeto.

### Conversão da imagem para a biblioteca OpenCV:
Com a nossa imagem em mãos, precisamos agora fazer com que ela seja "aceita" pela biblioteca da OpenCV para realizar as operações desejadas na imagem. Vamos transformar a imagem em um array numpy, e com esse array numpy, realizar a conversão de BGR para RGB (visto que a entrada de imagem no opencv sempre será BGR).
```python
def upload_image(input_img):
    # Converte a imagem de entrada para um numpy array
    img_array = np.array(input_img)
    # Converte de RBG (da entrada no gradio) para o BGR que o OpenCV recebe de entrada
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    # Converte de BGR para RGB
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return img_rgb
```
De primeira, parece um pouco "enrolado", mas se não fazemos essa conversão inicial de RGB da entrada para o BGR que o opencv trabalha como padrão, ao convertermos depois para RGB, teremos na verdade o resultado "contrário", obtendo BGR.

Ok, temos a nossa imagem coletada e no "formato" opencv. Vamos agora criar nossa função para coletar a imagem (chamar a função de upload com as conversões) e pegar o input da opção, com a função retornando ambos e podendo assim realizar apenas uma chamada de função na construção da interface
```python
def process_image_and_option(image, option):
    processed_image = upload_image(image)
    
    return processed_image, f"Selected option: {option}"
```

### Criação da interface
Sendo assim, com os processamentos de imagem e funções criadas, podemos construir nossa interface.
```python
with gr.Blocks() as demo:
    # Quadrado do input
    image_input = gr.Image(label="Upload Image", type="pil")
        
    # Botões de opção
    option = gr.Radio(["Option 1", "Option 2", "Option 3"], label="Choose an option")
        
    # Saídas de texto
    output_image = gr.Image(label="Processed Image")
    output_text = gr.Textbox(label="Selected Option")
        
    # Triggers pra mudança de imagem
    image_input.change(fn=process_image_and_option, inputs=[image_input, option], outputs=[output_image, output_text])
    option.change(fn=process_image_and_option, inputs=[image_input, option], outputs=[output_image, output_text])
    
    demo.launch()
```
#### ⚠️ Em Construção