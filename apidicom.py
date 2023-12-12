import base64

from flask import Flask, jsonify, request, send_file, abort
from io import BytesIO
import pydicom
from PIL import Image
import numpy as np
import os
import io

from flask_cors import CORS

app = Flask(__name__)

### PARA CONSEGUIR RODAR A API E A APLICAÇÃO NO MESMO SERVIDOR
CORS(app)

### ordem de execucao:
###
### ->CONVERTER TODAS AS IMAGENS
### http://127.0.0.1:5000/api/imagem_dicom_to_png
###
### ->LISTAR TODAS AS IMAGENS
### http://127.0.0.1:5000/api/images
###
### ->CONSULTAR UMA IMAGEM
### http://127.0.0.1:5000/api/images/00010004.png


def is_dicom_file(file_path):
    try:
        dicom_image = pydicom.dcmread(file_path)
        return True
    except pydicom.errors.InvalidDicomError:
        return False

@app.route('/api/exemplo', methods=['GET'])
def exemplo():
    data = {'mensagem': 'Esta é uma resposta da API!'}
    return jsonify(data)

def obter_dimensoes(image_array, pixel_spacing, slice_thickness=None):
    # Verifica se as informações de PixelSpacing estão presentes
    if not pixel_spacing or len(pixel_spacing) != 2:
        return 0, 0

    # Calcula as dimensões em milímetros dos eixos X (largura) e Y (altura)
    largura_mm = pixel_spacing[0] * image_array.shape[1]
    altura_mm = pixel_spacing[1] * image_array.shape[0]

    # Se SliceThickness estiver disponível, considera também a espessura da fatia
    if slice_thickness:
        altura_mm *= slice_thickness
    return largura_mm, altura_mm

def read_dicom_image(localDoArquivo,file_path):
    dicom_image = pydicom.dcmread(file_path)

    image_array = dicom_image.pixel_array



    if 'PhotometricInterpretation' in dicom_image and dicom_image.PhotometricInterpretation == 'RGB':
        image_pil = Image.fromarray(image_array)
    else:
        image_array_normalized = (
                (image_array - np.min(image_array)) / (np.max(image_array) - np.min(image_array)) * 255).astype(
            np.uint8)
        image_pil = Image.fromarray(image_array_normalized)

    local=localDoArquivo+'/imagem_salva3.png'
    image_pil.save(local, format='PNG')
    # Obtém informações de resolução espacial
    largura_mm = 0.0
    altura_mm = 0.0
    # Verifique se a tag de metadados 'PixelSpacing' está presente
    if hasattr(dicom_image, 'PixelSpacing'):
        # Verifique se o valor é diferente de None (ou qualquer outro critério específico)
        if dicom_image.PixelSpacing is not None:
            pixel_spacing = dicom_image.PixelSpacing
            print("Pixel Spacing:", pixel_spacing)
            pixel_spacing = dicom_image.PixelSpacing
            slice_thickness = getattr(dicom_image, 'SliceThickness', None, )
            largura_mm, altura_mm = obter_dimensoes(image_array, pixel_spacing,
                                                    slice_thickness)  # Retorna o nome do arquivo salvo
        else:
            print("SE3M dicom_image.PixelSpacing")


    return local, largura_mm, altura_mm


@app.route('/imagem_processar', methods=['POST'])
def imagem_processar():
    if 'file' not in request.files:
        return {'error': 'Nenhum arquivo encontrado'}

    file = request.files['file']

    # Verifica se o arquivo parece ser um arquivo DICOM
    if not is_dicom_file(file.filename):
        return {'error': 'Formato de arquivo não suportado'}

    file_path = 'imagens/temp.dcm'
    file.save(file_path)

    # Lê a imagem DICOM e obtém o nome do arquivo salvo
    image_file_name, largura_mm, altura_mm = read_dicom_image(localDoArquivo="png/",file_path=file_path)
    print(largura_mm)
    print(altura_mm)

    # Retorna o arquivo salvo usando send_file
    return send_file(image_file_name, mimetype='image/png')

    ## Lê a imagem DICOM e obtém a imagem e as dimensões dos eixos X e Y
    #image_bytes_io = read_dicom_image(file)

    print(image_file_name)
    # Converta a imagem para um objeto Image
    imagem_pillow = Image.open(io.BytesIO(image_file_name))

    # Converta a imagem para um array de bytes
    array_de_bytes = io.BytesIO()
    imagem_pillow.save(array_de_bytes, format='PNG')
    array_de_bytes = array_de_bytes.getvalue()

    # Converta a imagem para base64
    imagem_base64 = base64.b64encode(array_de_bytes).decode('utf-8')
    print(imagem_base64)
    #strIMG=image_file_name.getvalue().decode('latin1')

    # Dados que você deseja retornar em formato JSON
    dados = {
        'largura_mm': largura_mm,
        'altura_mm': altura_mm
    }

    # Utilize jsonify para converter os dados em uma resposta JSON
    resposta_json = jsonify(dados)
#
    ## Retorna a imagem e as dimensões dos eixos X e Y como JSON
    return resposta_json

# Rota para obter as dimensões da imagem PNG
@app.route('/api/get_image_dimensions/<image_name>')
def get_image_dimensions(image_name):
    image_path = os.path.join("Repositorio_imagens", "png", image_name)

    # Verifica se o arquivo de imagem existe
    if not os.path.exists(image_path):
        return {'error': 'Imagem não encontrada'}

    # Abre a imagem usando o Pillow
    image = Image.open(image_path)

    # Obtém as dimensões da imagem
    largura, altura = image.size

    return {'width': largura, 'height': altura}

@app.route('/imagem_tamanho', methods=['GET'])
def imagem_tamanho():
    if 'file' not in request.files:
        return {'error': 'Nenhum arquivo encontrado'}

    file = request.files['file']

    # Verifica se o arquivo parece ser um arquivo DICOM
    if not is_dicom_file(file.filename):
        return {'error': 'Formato de arquivo não suportado'}

    file_path = 'temp.dcm'
    file.save(file_path)

    # Lê a imagem DICOM e obtém o nome do arquivo salvo
    image_file_name, largura_mm, altura_mm = read_dicom_image(localDoArquivo="imagens/",file_path=file_path)
    print(largura_mm)
    print(altura_mm)

    # Dados que você deseja retornar em formato JSON
    dados = {
        'largura_mm': largura_mm,
        'altura_mm': altura_mm
    }

    # Utilize jsonify para converter os dados em uma resposta JSON
    resposta_json = jsonify(dados)

    ## Retorna a imagem e as dimensões dos eixos X e Y como JSON
    return resposta_json


# Rota para recuperar uma imagem pelo nome do arquivo
@app.route('/api/images/<filename>', methods=['GET'])
def get_image(filename):
    try:
        # Certifique-se de que o caminho para as imagens esteja correto
        image_path = f'Repositorio_imagens/png/{filename}'
        # Verifica se o arquivo realmente existe
        if not os.path.isfile(image_path):
            abort(404)
        # Use send_file do Flask para enviar a imagem
        return send_file(image_path, mimetype='image/png')  # Mude mimetype conforme necessário
    except Exception as e:
        return str(e), 404  # Retorna um código 404 se a imagem não for encontrada


# Rota para recuperar todas as imagens do repositório
@app.route('/api/images', methods=['GET'])
def get_all_images():
    try:
        # Certifique-se de que o caminho para as imagens esteja correto
        images_directory = 'Repositorio_imagens\\png'

        # Lista todos os arquivos no diretório de imagens
        image_files = [f for f in os.listdir(images_directory) if os.path.isfile(os.path.join(images_directory, f))]

        # Constrói URLs completas para todas as imagens
        image_urls = [f'{filename}' for filename in image_files]

        # Retorna a lista de URLs
        return jsonify({'image_urls': image_urls})
    except Exception as e:
        return str(e), 404


@app.route('/api/imagem_dicom_to_png', methods=['POST'])
def imagem_DICOM_PNG():
    # Diretório com os arquivos DICOM
    dir_path_dicom = 'Repositorio_imagens\\DICOM'

    # Lista para armazenar mensagens de sucesso ou erro
    results = []

    # Itera sobre todos os arquivos DICOM no diretório
    for filename in os.listdir(dir_path_dicom):
        print(filename)
        file_path_dicom = os.path.join(dir_path_dicom, filename)

        # Verifica se o arquivo parece ser um arquivo DICOM
        if not is_dicom_file(file_path_dicom):
            results.append({'filename': filename, 'error': 'Formato de arquivo não suportado'})
            continue

        try:
            print(filename)
            # Converte o arquivo DICOM para PNG
            image_file_path, largura_mm, altura_mm = read_dicom_image(localDoArquivo="Repositorio_imagens/temp",
                                                                      file_path=file_path_dicom)

            # Salva a imagem no diretório de destino
            save_path = os.path.join("Repositorio_imagens", "png", f"{filename}.png")
            Image.open(image_file_path).save(save_path)

            results.append({'filename': filename, 'message': 'Imagem convertida e salva com sucesso'})
        except Exception as e:
            results.append({'filename': filename, 'error': f'Erro durante a conversão e salvamento da imagem: {str(e)}'})

    # Dados que você deseja retornar em formato JSON
    # Retorna resultados
    return jsonify({'results': results})


if __name__ == '__main__':
    app.run(debug=True)
