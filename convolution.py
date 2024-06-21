import os
import numpy as np
from PIL import Image
from scipy.signal import convolve2d

# Parameters
d_values = [0]

for d in d_values:
    print(d)
    fread = f'original_{d}_2025_2025.jpg'
    fr = os.path.join('Sample_1201', fread)
    i = np.array(Image.open(fr)).astype(float) / 255.0

    PSF5 = np.genfromtxt('Data_Excel/PSF_1_0.00536_5.0.csv', delimiter=',')

    i = i - np.min(i)
    i = i / np.max(i)
    i = np.ones((1201, 1201)) - i

    PSF5 = PSF5 - np.min(PSF5)
    PSF5 = PSF5 / np.max(PSF5)

    i5 = convolve2d(i, PSF5, mode='same', boundary='symm')
    fn = f'model_{d}_depth_5.0'
    fn_png = f'{fn}.png'
    P = i5
    P2 = P - np.min(P)
    P2 = P2 / np.max(P2)
    P2 = np.ones((1201, 1201)) - P2
    P2 = (65535 * P2).astype(np.uint16)
    Image.fromarray(P2).save(fn_png)
