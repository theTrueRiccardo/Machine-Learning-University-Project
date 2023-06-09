import os
from PIL import Image
import numpy as np
import cv2 as cv

COLORI=1
SCALA_DI_GRIGIO=2
BIANCO_E_NERO=3

def carica_tutto(path_fiori, grandezza, tipo_immagine, flatten):
    cartelle = os.listdir(path_fiori)
    base=grandezza[0]
    altezza=grandezza[1]
    numero_foto=0
    classi_fiori = {}
    for cartella in cartelle:
        numero_foto = numero_foto + len(os.listdir(os.path.join(path_fiori,cartella)))
        classi_fiori[cartella] = cartelle.index(cartella)
    dataset = []
    labels = []
    foto_associate = []
    if tipo_immagine==COLORI and flatten:
        dataset = np.ones( (numero_foto, base*altezza * 3) )
    elif tipo_immagine != COLORI and flatten:
        dataset = np.ones( (numero_foto, base*altezza) )
    elif tipo_immagine == COLORI and not flatten:
        dataset = np.ones( (numero_foto, base, altezza, 3) )
    else:
        dataset = np.ones( (numero_foto, base, altezza) )
    i=0
    for cartella in cartelle:
        for immagine in os.listdir(os.path.join(path_fiori,cartella)):
            path = os.path.join(path_fiori, cartella, immagine)
            fiore = Image.open(path)
            fiore = fiore.resize(grandezza)
            if tipo_immagine==BIANCO_E_NERO:
                fiore = fiore.convert('1')
            elif tipo_immagine==SCALA_DI_GRIGIO:
                fiore = fiore.convert('L')
            foto_associate.append(fiore)
            fiore = np.asarray(fiore)
            if tipo_immagine==COLORI and flatten:
                fiore = fiore.reshape((base*altezza*3))
            elif flatten:
                fiore = fiore.reshape((base*altezza))
            dataset[i, :] = fiore
            labels.append(cartelle.index(cartella))
            i = i + 1
    return (dataset, np.array(labels), foto_associate, classi_fiori)


def carica_foto(path_fiori, grandezza, libreria):
    cartelle = os.listdir(path_fiori)
    cartelle.sort() #per riproducibilità
    numero_foto=0
    classi_fiori = {}
    for cartella in cartelle:
        numero_foto = numero_foto + len(os.listdir(os.path.join(path_fiori, cartella)))
        classi_fiori[cartella] = cartelle.index(cartella)
    foto_associate = []
    labels = []
    for cartella in cartelle:
        for immagine in os.listdir(os.path.join(path_fiori, cartella)):
            path = os.path.join(path_fiori, cartella, immagine)
            if libreria == "cv":
                fiore = cv.imread(path)
                fiore = cv.resize(fiore, grandezza)
            else:
                fiore = Image.open(path)
                fiore = fiore.resize(grandezza)
            foto_associate.append(fiore)
            labels.append(classi_fiori[cartella])
    return (foto_associate, labels)