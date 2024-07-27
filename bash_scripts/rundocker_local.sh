tempwd=$(pwd)

cd ~
docker run -it --rm -p 8501:8501 -v $(pwd)/Documents/Tools/INS-Analysis:/Documents/Tools/INS-Analysis -v $(pwd)/Documents/Tools/INS-Analysis-FE:/Documents/Tools/INS-Analysis-FE ins-analysis-fe bash 

cd $tempwd