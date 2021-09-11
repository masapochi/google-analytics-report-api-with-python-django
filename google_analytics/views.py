from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

import pandas as pd

from .analyze import get_report, format_reports
from .dt_utilities import convert_dt_to_str, calc_beginning_of_week

TODAY = timezone.now().date()
STR_TODAY = convert_dt_to_str(TODAY)
BEGINNING_OF_WEEK = calc_beginning_of_week()
STR_BEGINNING_OF_WEEK = convert_dt_to_str(BEGINNING_OF_WEEK)


def home(request):
    context = {
        "start": STR_BEGINNING_OF_WEEK,
        "end": STR_TODAY,
    }
    return render(request, "google_analytics/home.html", context)


def analyze(request):
    start = request.GET.get("start", STR_BEGINNING_OF_WEEK)
    end = request.GET.get("end", STR_TODAY)

    report = get_report(start=start, end=end)
    headers, rows = format_reports(report)

    start_date = start.replace("-", "_")
    end_date = end.replace("-", "_")
    filename = f"Analytics__{start_date}__{end_date}.csv"

    context = {
        "start": start,
        "end": end,
        "headers": headers,
        "rows": rows,
        "filename": filename,
    }

    return render(request, "google_analytics/analyze.html", context)


def download(request, filename, start, end):

    report = get_report(start=start, end=end)
    headers, rows = format_reports(report)

    df = pd.DataFrame(index=None, data=rows, columns=headers)

    response = HttpResponse(content_type="text/csv; charset=utf8")
    response["Content-Disposition"] = f"attachment; filename={filename}"

    df.to_csv(path_or_buf=response, encoding="utf_8_sig", index=False)

    return response
