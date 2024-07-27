temporary_pwd=$(pwd)

apt update

apt install -y git

rm -rf _mcnptools
cp -r mcnptools _mcnptools
cd _mcnptools
bash install.sh

cd $temporary_pwd

pip3 install -r requirements.txt