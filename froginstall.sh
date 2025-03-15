git clone https://github.com/relyadev/frogram
version=$(python3 -c "import sys; print('{}.{}'.format(*sys.version_info[:2]))")
pip install requests --break-system-packages
sudo cp ~/frogram/frogram.py /lib/python${version}
