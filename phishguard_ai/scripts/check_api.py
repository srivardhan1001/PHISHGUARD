import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phishguard_ai.settings")
import django
django.setup()
from scanner.analysis import api_based_score

if __name__ == "__main__":
    score, verdict, status = api_based_score("https://www.google.com/")
    print({"score": score, "verdict": verdict, "status": status})

