
import pydicom
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def read_dicom_image(file_path):
    # Carrega o arquivo DICOM
    dicom_image = pydicom.dcmread(file_path)

    # Obtém a matriz de pixels da imagem
    image_array = dicom_image.pixel_array

    #######1
   ## Normaliza a matriz de pixels para o intervalo 0-255 (uint8)
   #image_array_normalized = (
   #            (image_array - np.min(image_array)) / (np.max(image_array) - np.min(image_array)) * 255).astype(
   #    np.uint8)

   ## Converte a matriz para uma imagem PIL
   #image_pil = Image.fromarray(image_array_normalized)

   ## Salva a imagem PIL em formato PNG
   #image_pil.save('imagem_salva0.png', format='PNG')
    #######1

    #######2
    # Verifica se a imagem DICOM tem informações sobre a cor
    if 'PhotometricInterpretation' in dicom_image and dicom_image.PhotometricInterpretation == 'RGB':
        # Converte a matriz para uma imagem PIL colorida
        image_pil = Image.fromarray(image_array)
    else:
        # Se for uma imagem em escala de cinza, apenas converte para uma imagem PIL
        # Normaliza a matriz de pixels para o intervalo 0-255 (uint8)
        image_array_normalized = (
                    (image_array - np.min(image_array)) / (np.max(image_array) - np.min(image_array)) * 255).astype(
            np.uint8)
        image_pil = Image.fromarray(image_array_normalized)

    # Salva a imagem PIL em formato PNG
    image_pil.save('imagem_salva3.png', format='PNG')
    #######2


    return image_array

def plot_dicom_image(image_array):
    # Exibe a imagem usando matplotlib
    plt.imshow(image_array, cmap=plt.cm.gray)
    plt.axis('off')
    plt.show()

def read_dicom_imageC(file_path, save_path='imagem_processada.png'):
    # Carrega o arquivo DICOM
    dicom_image = pydicom.dcmread(file_path)

    # Obtém a matriz de pixels da imagem
    image_array = dicom_image.pixel_array

    # Converte a matriz para um tipo de dados numérico suportado
    image_array = image_array.astype(np.uint16)  # ou outro tipo de dados apropriado

    # Converte a matriz para uma imagem PIL
    image_pil = Image.fromarray(image_array)

    # Salva a imagem PIL
    image_pil.save(save_path, format='PNG')

    # Retorna o caminho onde a imagem foi salva
    return save_path

# Substitua 'seu_arquivo.dcm' pelo caminho do seu próprio arquivo DICOM
file_path = '00010001'

# Lê a imagem DICOM
image_array = read_dicom_image(file_path)

# Exibe a imagem
plot_dicom_image(image_array)

## Chamada da função com o caminho específico para salvar a imagem
#caminho_salvo = read_dicom_imageC('00010001C.dcm', save_path='imagem_salva.png')
#
#print(f'Imagem salva em: {caminho_salvo}')



