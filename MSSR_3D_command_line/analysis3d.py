import mssr3d as ms
import napari
import subprocess
import sys
import numpy as np

def install_missing_packages(missing_requirements):
    try:
        for requirement in missing_requirements:
            subprocess.check_call(["pip", "install", requirement])
        
    except Exception as e:
        print(f"Error to install mising dependencies: {str(e)}")


def check_requirements():
    try:
        with open('requirements.txt') as f:
            requirements = f.read().splitlines()
            installed_requirements = [line.split('==')[0] for line in subprocess.check_output(["pip", "freeze"]).decode().split('\n') if line]
            missing_requirements = [requirement for requirement in requirements if requirement.split('==')[0] not in installed_requirements]
            
            if missing_requirements:
                install_missing_packages(missing_requirements)
    except Exception as e:
        print(f"Error to verify dependences: {str(e)}")


def main_analysis():
    path=sys.argv[1]
    amplification=int(sys.argv[2])
    psf=float(sys.argv[3])
    order=int(sys.argv[4])
    interpolation=str(sys.argv[5])
    
    

    I= ms.mssr3d(path=path, amplification=amplification,psf=psf, order=order,interpolation=interpolation)

   

    viewer = napari.Viewer()
    viewer.add_image(I,name='Processed volume')
    
    napari.run()


if __name__ == "__main__":
    check_requirements()
    main_analysis()
