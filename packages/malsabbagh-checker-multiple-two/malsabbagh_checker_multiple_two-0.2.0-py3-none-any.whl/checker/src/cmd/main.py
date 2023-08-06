import subprocess
import os, sys
from checker import package_dir

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("args must have length = 2") # TODO Exception
        return
    
    source_dir = os.path.join(os.getcwd(), args[0])
    output_dir = os.path.join(os.getcwd(), args[1])
    doxygen_output_dir = os.path.join(output_dir, "_doxygen")
    os.chdir(package_dir)
    subprocess.run(["make", "doxygen"], env=dict(os.environ, SOURCE_DIR=source_dir, DOXYGEN_OUTPUT_DIR=doxygen_output_dir))
    
    print("successful")