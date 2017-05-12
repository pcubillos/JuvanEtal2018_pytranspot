# From the directory where this file is located, execute (this will make things easier):
topdir=`pwd`

# Clone (download) the PB code:
git clone --recursive https://github.com/pcubillos/pyratbay
cd $topdir/pyratbay
git checkout 85b2d18

# Compile the PB code:
cd $topdir/pyratbay
make


# Download HITRAN/HITEMP data:
cd $topdir/inputs/opacity
wget --user=HITRAN --password=getdata -N -i wget_hitemp_W41b.txt
unzip '*.zip'
rm -f *.zip

# Make TLI opacity file:
cd $topdir/run
$topdir/pyratbay/pbay.py -c tli_HITEMP.cfg

# Make atmospheric file:
cd $topdir/run
$topdir/pyratbay/pbay.py -c atm_wasp41_001Xsolar.cfg


# Compute WASP-41b spectrum and plot:
cd $topdir/run
$topdir/make_spectrum.py
