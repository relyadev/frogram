# Frogram python libary
![Untitled (8) (1)](https://github.com/user-attachments/assets/bb680245-f67f-44b8-bff3-e6b20fa8bca6)


## Hand install
```bash
git clone https://github.com/relyadev/frogram
version=$(python3 -c "import sys; print('{}.{}'.format(*sys.version_info[:2]))")
pip install requests --break-system-packages
sudo cp ~/frogram/frogram.py /lib/python${version}
```
## Auto install
```bash
curl -L -o install.sh "https://github.com/relyadev/frogram/releases/download/v0.0.1/install.sh" && chmod +x install.sh && ./install.sh
```
