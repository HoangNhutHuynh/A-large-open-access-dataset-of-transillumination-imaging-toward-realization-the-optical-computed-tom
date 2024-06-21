from PIL import Image
import numpy as np
import os

absorbance = 0.1
save_dir_image = f'Data_absorbance_{absorbance}'
os.makedirs(save_dir_image, exist_ok=True)

i1 = Image.open('absorber_square_10mm.tif')
i1 = np.array(i1)

i4 = i1 * absorbance
i4 = i4 + np.max(i4)

#i4 = i4 - np.min(np.min(i4))
i4 = 65535 * i4 / np.max(i4)
    
i4_image = Image.fromarray(i4.astype(np.uint16))
output_path = os.path.join(save_dir_image, "scaled_image.tif")
i4_image.save(output_path)

print(f"Grayscale image saved successfully as {save_dir_image}")