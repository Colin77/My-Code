#!/bin/sh
cd /home/root
wget --content-disposition http://downloads.sourceforge.net/project/sp-tk/SPTK/SPTK-3.9/SPTK-3.9.tar.gz
tar -xzf SPTK-3.9.tar.gz
opkg install tcsh
ln -s /bin/tcsh /bin/csh
cd SPTK-3.9
./configure
make -j2 && make install
