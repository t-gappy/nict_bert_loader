mkdir tmp
cd ./tmp

wget wget --save-cookies=./cookie.txt "https://drive.google.com/u/0/uc?export=download&id=0B4y35FiV1wh7X2pESGlLREpxdXM"
CONFIRM=`cat ./cookie.txt | grep download_warning | tail -n 1 | awk '{print $7}'`
wget --trust-server-names \
     --load-cookies=./cookie.txt \
     -O "mecab-jumandic-7.0-20130310.tar.gz" \
     -c \
     "https://drive.google.com/u/0/uc?export=download&confirm=${CONFIRM}&id=0B4y35FiV1wh7X2pESGlLREpxdXM"

tar -zxvf ./mecab-jumandic-7.0-20130310.tar.gz

cd mecab-jumandic-7.0-20130310/
./configure --with-charset=utf8
sudo make
sudo make install

cd ../../
rm -r tmp/