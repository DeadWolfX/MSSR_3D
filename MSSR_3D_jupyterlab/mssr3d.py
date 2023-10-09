import numpy as np
import imageio
from tqdm import tqdm
from scipy.interpolate import RegularGridInterpolator
from scipy.ndimage import map_coordinates
from PIL import Image

def mssr3d(path,amplification, psf, order, interpolation):
    hs = int(0.5 * psf * amplification)
    if hs <0:
        hs=1
    print("Starting process...")
    
    if isinstance(path, str):
        I=imageio.v2.imread(path).transpose(1,0,2).astype(np.float64) 
    
    elif isinstance(path, np.ndarray):
        I=path.transpose(1,0,2).astype(np.float64) 

    

    sz = I.shape

    if amplification > 1:
        if interpolation.lower() != "bicubic" and interpolation.lower() != "fourier":
            print('The interpolation parameter should be bicubic or fourier, but as there is no match, bicubic will be used.')
            interpolation='bicubic'
        
        if interpolation.lower() == "bicubic":
            new_height = int(sz[0] * amplification)
            new_width = int(sz[1] * amplification)
            new_anchor=int(sz[0]* amplification)
            new_shape=(new_height,new_width,new_anchor)
            AMP =tricubic(I, new_shape)
            
        else:
            if interpolation.lower() == "fourier":
                AMP = FourierMag(I, amplification)

    else:            
        AMP = I
    
    
    hs_k = 2 * hs**2
    
    xPad = np.pad(AMP,[(hs, hs), (hs, hs), (hs_k, hs_k)], mode='symmetric')
    
    interval = np.arange(-hs, hs + 1)
    
    int_k_vals = np.arange(-hs_k, hs_k + 1)
    
    height, width, slices= AMP.shape
    
    M = np.zeros((height,width,slices),dtype=np.float64)
    print("1/2 in progress...")
    for i in tqdm(interval):
        for j in interval:
            for k in int_k_vals:
                if (i != 0 or j != 0 or k != 0):
                    xThis = xPad[hs + i:height + hs + i, hs + j:width + hs + j,hs_k + k:slices + hs_k + k]
                    M=np.maximum(M, np.abs(AMP - xThis))
                
    weightAccum = np.zeros((height,width,slices), dtype=np.float64)
    yAccum = np.zeros((height,width,slices), dtype=np.float64)
    
    print("2/2 in progress...")
    for i in tqdm(interval):
        for j in interval:
            for k in int_k_vals:
                if (i != 0 or j != 0 or k != 0):
                    spatialKernel =1 #np.exp(-(i ** 2 + j ** 2) / (hs ** 2))
                    xThis = xPad[hs + i:height + hs + i, hs + j:width + hs + j,hs_k + k:slices + hs_k + k]
                    xDiffSq0 = ((AMP - xThis) / M) ** 2
                    intensityKernel = np.exp(-1*xDiffSq0)
                    weightThis = spatialKernel * intensityKernel
                    weightAccum= weightAccum +weightThis
                    yAccum= yAccum+(xThis * weightThis)

    MS = AMP - (yAccum / weightAccum)
    MS[MS < 0] = 0
    MS[np.isnan(MS)] = 0
    
    I3 = MS / np.max(MS)
    
    x3 = AMP / np.max(AMP)

    for i in range(order):
        I4 = x3 - I3  # Diff
        I5 = np.max(I4) - I4  # Diff complement
        I5 = I5 / np.max(I5)  # Normalization
        I6 = I5 * I3  # Intensity weighting
        I7 = I6 / np.max(I6)  # Final normalization
        x3 = I3
        I3 = I7
        
    I7=I3/np.max(I3)
   
    return  I7.transpose(2,1,0) 


def FourierMag(Img,mg):
    """
    This function takes the image and magnification to compute a Fourier Magnification.

    Args:
    
         Img (matrix): It is a matrix representing pixel values of the image.

         mg (int): Factor of magnification.


    Returns:
        iFM matrix: It is a matrix representing pixel values of the processed image.
    """
    img = np.fft.fftn(Img)
    szx, szy, szz = img.shape
    mdX = int(np.ceil(szx / 2))
    mdY = int(np.ceil(szy / 2))
    mdZ = int(np.ceil(szz / 2))
    
    szFx = szx * mg
    szFy = szy * mg
    szFz = szz * mg
    
    fM = np.zeros((szFx, szFy, szFz), dtype=complex)
    
    lnX = np.abs(mdX - szx)
    lnY = np.abs(mdY - szy)
    lnZ = np.abs(mdZ - szz)
    
    img = mg * mg * mg * img
    
    fM[0:mdX, 0:mdY, 0:mdZ] = img[0:mdX, 0:mdY, 0:mdZ]  # izq sup cuadrante
    fM[0:mdX, 0:mdY, (szFz - lnZ):szFz] = img[0:mdX, 0:mdY, mdZ:szz]  # der sup cuadrante
    fM[0:mdX, (szFy - lnY):szFy, 0:mdZ] = img[0:mdX, mdY:szy, 0:mdZ]  # izq inf cuadrante
    fM[0:mdX, (szFy - lnY):szFy, (szFz - lnZ):szFz] = img[0:mdX, mdY:szy, mdZ:szz]  # der inf cuadrante
    
    fM[(szFx - lnX):szFx, 0:mdY, 0:mdZ] = img[mdX:szx, 0:mdY, 0:mdZ]  # izq sup cuadrante
    fM[(szFx - lnX):szFx, 0:mdY, (szFz - lnZ):szFz] = img[mdX:szx, 0:mdY, mdZ:szz]  # der sup cuadrante
    fM[(szFx - lnX):szFx, (szFy - lnY):szFy, 0:mdZ] = img[mdX:szx, mdY:szy, 0:mdZ]  # izq inf cuadrante
    fM[(szFx - lnX):szFx, (szFy - lnY):szFy, (szFz - lnZ):szFz] = img[mdX:szx, mdY:szy, mdZ:szz]  # der inf cuadrante
    
    iFM = np.fft.ifftn(fM).real
    
    return iFM


def tricubic(data, new_shape):
    """
    Realiza interpolación tricubica en una matriz tridimensional para cambiar su tamaño.

    Args:
        data (ndarray): Matriz tridimensional de entrada.
        new_shape (tuple): Tupla con las nuevas dimensiones de la matriz tridimensional.

    Returns:
        ndarray: Matriz tridimensional interpolada con las nuevas dimensiones.
    """
    # Crear una matriz de coordenadas para las nuevas dimensiones deseadas
    x_new = np.linspace(0, data.shape[0] - 1, new_shape[0])
    y_new = np.linspace(0, data.shape[1] - 1, new_shape[1])
    z_new = np.linspace(0, data.shape[2] - 1, new_shape[2])
    
    # Crear una malla de coordenadas de las nuevas dimensiones
    x_mesh, y_mesh, z_mesh = np.meshgrid(x_new, y_new, z_new, indexing='ij')
    
    # Coordenadas de entrada para la interpolación tricubica
    coordinates = np.vstack((x_mesh.ravel(), y_mesh.ravel(), z_mesh.ravel()))
    
    # Realizar la interpolación tricubica utilizando map_coordinates
    interpolated_data = map_coordinates(data, coordinates, order=3).reshape(new_shape)
    
    return np.array(interpolated_data)
