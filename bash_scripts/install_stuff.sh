temporary_pwd=$(pwd)

apt update
cd /Documents/NotMyTools/mcnptoolsINSFE
bash install.sh

cd /Documents/Tools/INS-Analysis
bash install.sh

cd $temporary_pwd

pip3 install -r requirements.txt