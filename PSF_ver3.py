import numpy as np
from PIL import Image
import os
def PSF_ver2(musp, mua, d, X, Y, L):
    # Setting of various parameters
    kd = abs((3 * mua * (musp + mua)) ** 0.5) # kd
    Po = 1  # Intensity of incident light 1 is usually not a problem
    X0 = round(X / 2)  # Origin coordinate position (horizontal direction)
    Y0 = round(Y / 2)  # Origin coordinate position (vertical direction)

    # Calculation of the PSF
    P = np.zeros((Y, X))
    for y in range(Y):
        for x in range(X):
            rho = (((x - X0) * L) ** 2 + ((y - Y0) * L) ** 2) ** 0.5
            rhod = (rho ** 2 + d ** 2) ** 0.5
            p1 = kd + 1 / rhod
            p2 = d * (1 / rhod)
            p3 = (np.exp((-kd * rhod))) / rhod
            P[y, x] = ((3 * Po) / ((4 * np.pi) ** 2)) * ((musp + mua) + (p1 * p2)) * p3

    P = P / np.sum(np.sum(P))

    # Display and storage of PSF
    fn = f'PSF_{musp}_{mua}_{d}'
    #fn_fig = f'{fn}.fig'
    fn_csv = f'{fn}.csv'

    save_dir_image = 'Data_PSF'
    save_dir_excel = 'Data_Excel'

    # Save PSF as CSV file
    os.makedirs(save_dir_excel, exist_ok=True)  # Create directory if it doesn't exist
    fn_csv = os.path.join(save_dir_excel, f'{fn}.csv')
    np.savetxt(fn_csv, P, delimiter=',', fmt='%.15f')


    os.makedirs(save_dir_image, exist_ok=True)  # Create directory if it doesn't exist
    fn_tif = os.path.join(save_dir_image, f'{fn}.tif')

    P2 = P - np.min(P)
    P2 = 65535 * P2 / np.max(P2)
    P2 = P2.astype(np.uint16)
    Image.fromarray(P2).save(fn_tif)  # Saved in 16-bit TIFF format

    return P

# Parameters
musp = 1  # [/mm]
mua = 0.00536  # [/mm]
L = 100 / 1324  # Length per pixel [mm]
X = 2025
Y = 2025

start_d = 0.1
end_d = 100.0
step_d = 0.1

d_values = np.arange(start_d, end_d + step_d, step_d)

for d in d_values:
    print(d)
    PSF = PSF_ver2(musp, mua, d, X, Y, L)
