# Getting started
Clone the repository (fix it, assume ssh keys)
```
git clone git@github.com:pawangoyal137/PIRAC.git
```

## Dependencies 
<!-- * GMP -->
* Go 1.13 or higher 
* OpenSSL 1.1.1f 
* GNU Make
* Cmake


|Dependency |Install dependencies (Ubuntu): | Install dependencies (CentOS):|
|--------------|--------------|-----------|
|Go |```sudo apt-get install golang-go```| ```sudo yum install golang```|
|OpenSSL |```sudo apt install libssl-dev```|```sudo yum install openssl-devel```|
|Make |```sudo apt-get install build-essential``` |  ```sudo yum groupinstall 'Development Tools'```|
|Cmake |```sudo apt-get install cmake```| ```sudo yum install cmake```|


## Python Packages
Install following python packages
```
sudo apt install python3-pip
sudo apt-get install python3-numpy
sudo apt-get install python3-matplotlib
sudo apt-get install python3-pandas
```

## Setup PIR schemes

### Setup Spiral
Run following commands to download and setup Spiral PIR in home direcotry 
```
cd ~
git clone https://github.com/pawangoyal137/simplepir
```
The above repo is a copy of the original repo with slight modifications

### Setup Spiral
Run following commands to download and setup Spiral PIR in home direcotry 
```
# install dependencies
sudo apt-get install curl zip unzip tar
sudo apt-get install -y clang-12 git-lfs
git lfs install

# clone the vcpkg to build hexl
cd ~
git clone https://github.com/Microsoft/vcpkg.git
./vcpkg/bootstrap-vcpkg.sh -disableMetrics
./vcpkg/vcpkg install hexl

# clone the spiral github
git clone https://github.com/menonsamir/spiral.git
```

Run following commands to ensure spiral pir is correctly working
```
cd ~/spiral
python3 select_params.py 20 256
```
More information can be found at https://github.com/menonsamir/spiral

### Setup Seal
Run following commands to download and setup Seal PIR in home direcotry
```
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
```
More information can be found at https://github.com/microsoft/SealPIR and https://github.com/microsoft/SEAL/tree/4.0.0
## Setup

### Create shared library
```
cd acpir/src
make test.so
```
