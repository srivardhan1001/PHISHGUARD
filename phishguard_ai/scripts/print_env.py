import os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phishguard_ai.settings")
import django
django.setup()
from django.conf import settings

print("GOOGLE_SAFEBROWSING_API_KEY set in settings:", bool(settings.GOOGLE_SAFEBROWSING_API_KEY))
print("GOOGLE_SAFEBROWSING_API_KEY in os.environ:", bool(os.getenv("GOOGLE_SAFEBROWSING_API_KEY")))
print("ENABLE_EXTERNAL_API:", settings.ENABLE_EXTERNAL_API)
