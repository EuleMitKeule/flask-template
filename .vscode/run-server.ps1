If (!(test-path "venv"))
{
    python -m venv venv
}

.\venv\Scripts\activate.ps1

pip install -r requirements.txt

cd src
python app.py --config ../config/config.yml