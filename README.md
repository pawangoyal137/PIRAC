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

## Getting everything to run (tested on Ubuntu, CentOS, and MacOS)

|Dependency |Install dependencies (Ubuntu): | Install dependencies (CentOS):|
|--------------|--------------|-----------|
|GMP library |```sudo apt-get install libgmp3-dev```| ```sudo yum install gmp-devel```|
|Go |```sudo apt-get install golang-go```| ```sudo yum install golang```|
|OpenSSL |```sudo apt install libssl-dev```|```sudo yum install openssl-devel```|
|Make |```sudo apt-get install build-essential``` |  ```sudo yum groupinstall 'Development Tools'```|
|Cmake |```sudo apt-get install cmake```| ```sudo yum install cmake```|


## Python Packages
```
sudo apt install python3-pip
sudo apt-get install python3-numpy
sudo apt-get install python3-matplotlib
```
## Setup

### Create shared library
```
cd acpir/src
make test.so
```

### Setup Spiral
```
sudo apt-get install curl zip unzip tar
sudo apt-get install -y clang-12 git-lfs
git lfs install
cd ~
git clone https://github.com/Microsoft/vcpkg.git
./vcpkg/bootstrap-vcpkg.sh -disableMetrics
./vcpkg/vcpkg install hexl
git clone https://github.com/menonsamir/spiral.git
```

### Setup Seal
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
