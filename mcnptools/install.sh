tmppath=$(pwd)

apt update
apt install -y cmake

apt-get install -y build-essential
apt-get build-dep hdf5
apt-get install -y libhdf5-serial-dev

cmake -D CMAKE_INSTALL_PREFIX=$tmppath -D mcnptools.python_install=User $tmppath
cmake --build . --config Release
ctest --build-config Release
cmake --install . --config Release