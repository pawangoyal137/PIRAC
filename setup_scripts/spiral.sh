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