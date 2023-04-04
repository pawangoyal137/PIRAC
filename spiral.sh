sudo apt-get install curl zip unzip tar
sudo apt-get install -y clang-12 git-lfs
git lfs install
cd ~
git clone https://github.com/Microsoft/vcpkg.git
./vcpkg/bootstrap-vcpkg.sh -disableMetrics
./vcpkg/vcpkg install hexl
git clone https://github.com/menonsamir/spiral.git
