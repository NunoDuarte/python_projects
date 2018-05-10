# Instructions to get it running on Ubuntu 16.04 (for me it was the only way)

To run Pupil software from source comment the anaconda3 path exported to $PATH

Also, you need to close and open a new terminal. Otherwise, it will say that some libraries are missing when they are correctly installed

# Pupil
For more information go to website https://github.com/pupil-labs/pupil

# Notes:
export CPLUS_INCLUDE_PATH=/home/nduarte/software/opencv/build/INSTALL/include - to add the include dirs 

# if you want to direct a library to the paths that the compiler checks do the following
1. ld -l<library> --verbose -> this gives you the places where the compiler looks for 
2. sudo ln -s /usr/lib/lib<library>.so <one of the libraries that 'ld' gave you>
