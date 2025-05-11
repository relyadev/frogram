# Frogram python libary


## Hand install
```bash
git clone https://github.com/relyadev/frogram
version=$(python3 -c "import sys; print('{}.{}'.format(*sys.version_info[:2]))")
pip install requests --break-system-packages
sudo cp ~/frogram/frogram.py /lib/python${version}
```
## Auto install
```bash
curl -L -o froginstall.sh "https://raw.githubusercontent.com/relyadev/frogram/refs/heads/main/froginstall.sh" && chmod +x froginstall.sh && ./froginstall.sh
```
