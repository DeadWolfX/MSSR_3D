In the main directory of the code, MSSR_3D_command_line, there exists a requirements.txt file that contains the necessary packages and their versions for this code. You can install them manually or let the code itself verify and install the required packages.

The next files are examples to try the code:
  -Ts_568_0_5um_confocal.tif

  The main code is analysis3d.py, which applies MSSR 3D. It needs to be executed with the following arguments:
  image_path : the path of the image to analize or the image as numpy array
  amplification: the factor of amplification for the image
  psf: point spread function
  order: order for the MSSR algorithm
  interpolation: the tipe of interpolation for the amplification ("bicubic" or "fourier")

For example, to run the code with the parameters:

img_path = "path/image_name.tif"
amplification=2
order=0
psf=2.77
interpolation="bicubic"

If you are excecuting the code outside the MSSR_3D_command_line  directory you need to execute in the command line:

python3 /path/analysis3d.py path/image_name.tif 2 0 2.77 bicubic 

If you are excecuting the code inside the MSSR_3D_command_line  directory you need to execute in the command line:

python3 analysis3d.py image_name.tif 2 0 2.77 bicubic 
