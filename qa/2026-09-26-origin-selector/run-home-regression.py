"""Reuse the existing 117-check home journey without overwriting its evidence."""
from pathlib import Path
import os
HERE=Path(__file__).resolve().parent
output=HERE/'journey';output.mkdir(exist_ok=True)
os.environ['ARTIDORO_REVIEW_URL']=os.environ.get('ARTIDORO_REVIEW_URL','http://127.0.0.1:4175')
source=HERE.parent/'2026-09-25-home'/'verify-home.py'
exec(compile(source.read_text(encoding='utf-8-sig'),str(source),'exec'),{'__file__':str(output/'verify-home.py'),'__name__':'__main__'})
