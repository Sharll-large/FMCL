pip install --upgrade pip
pip install zstandard
pip install requests
pip install nuitka
pip install ordered-set
nuitka --standalone --onefile --remove-output main.py
