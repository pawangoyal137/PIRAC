# clone the SEAL
cd ~
git clone https://github.com/microsoft/SEAL
cd SEAL

# switch to version 4.0.0
git switch 4.0.0

# install the seal package
cmake -S . -B build
cmake --build build
sudo cmake --install build

# clone SEAL PIR
cd ~
git clone https://github.com/microsoft/SealPIR
cd SealPIR

# build and test
cmake .
make
ctest .