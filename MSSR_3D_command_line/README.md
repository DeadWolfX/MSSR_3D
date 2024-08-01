<p>In the main directory of the code, MSSR_3D_command_line, there exists a requirements.txt file that contains the necessary packages and their versions for this code. You can install them manually or let the code itself verify and install the required packages.<br><br>

The next files are examples to try the code:</p>
  <ul>
  <li><b>Ts_568_0_5um_confocal.tif</b></li>
  </ul>
  <p>The main code is analysis3d.py, which applies MSSR 3D. It needs to be executed with the following arguments:</p>
  
  <ul>
  <li><b>image_path</b>(string):</li> the path of the image to analize or the image as numpy array
  <li><b>amplification</b>(int):</li> the factor of amplification for the image
  <li><b>psf</b>(float):</li> point spread function
  <li><b>order</b>(int):</li> order for the MSSR algorithm
  <li><b>interpolation</b>(string):</li> the tipe of interpolation for the amplification ("bicubic" or "fourier")
  </ul>

<p>For example, to run the code with the parameters:<br><br>

img_path = "path/image_name.tif"<br>
amplification=2<br>
order=0<br>
psf=2.77<br>
interpolation="bicubic"<br><br>

If you are excecuting the code outside the MSSR_3D_command_line  directory you need to execute in the command line:</p>

```bash
python3 /path/analysis3d.py path/image_name.tif 2 0 2.77 bicubic
```

If you are excecuting the code inside the MSSR_3D_command_line  directory you need to execute in the command line:

```bash
python3 analysis3d.py image_name.tif 2 0 2.77 bicubic 
