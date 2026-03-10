from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.html import escape
from django.db.models import Count
from .forms import URLScanForm
from .models import ScanResult
from .analysis import analyze_url
import json
from .analysis import api_based_score


def home(request):
    return render(request, "home.html")


def scan(request):
    if request.method == "POST":
        form = URLScanForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            result = analyze_url(url)
            obj = ScanResult.objects.create(
                url=url,
                rule_score=result["rule_score"],
                api_score=result["api_score"],
                final_score=result["final_score"],
                risk_label=result["risk_label"],
                issues=json.dumps(result["issues"]),
                api_verdict=result["api_verdict"],
                api_status=result["api_status"],
            )
            return redirect(reverse("result", kwargs={"pk": obj.pk}))
    else:
        form = URLScanForm()
    return render(request, "scan.html", {"form": form})


def result(request, pk):
    obj = get_object_or_404(ScanResult, pk=pk)
    issues = []
    try:
        issues = json.loads(obj.issues) if obj.issues else []
    except Exception:
        issues = []
    return render(
        request,
        "result.html",
        {
            "item": obj,
            "issues": issues,
        },
    )


def about(request):
    return render(request, "about.html")


def dashboard(request):
    level = request.GET.get("level")
    qs = ScanResult.objects.all()
    if level in {"Safe", "Suspicious", "Highly Dangerous"}:
        qs = qs.filter(risk_label=level)
    counts = (
        ScanResult.objects.values("risk_label")
        .annotate(total=Count("id"))
    )
    bucket = {"Safe": 0, "Suspicious": 0, "Highly Dangerous": 0}
    for c in counts:
        bucket[c["risk_label"]] = c["total"]
    chart = {
        "labels": ["Safe", "Suspicious", "Highly Dangerous"],
        "data": [bucket["Safe"], bucket["Suspicious"], bucket["Highly Dangerous"]],
    }
    return render(request, "dashboard.html", {"items": qs[:200], "chart": chart, "level": level or ""})


def api_status(request):
    test_url = "https://www.google.com/"
    score, verdict, status = api_based_score(test_url)
    return render(
        request,
        "api_status.html",
        {"test_url": test_url, "score": score, "verdict": verdict, "status": status},
    )
