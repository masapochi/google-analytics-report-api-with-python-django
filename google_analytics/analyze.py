"""Hello Analytics Reporting API V4."""

from django.conf import settings

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

from . import site_list


APP_DIR = settings.BASE_DIR.joinpath("google_analytics")
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
KEY_FILE_LOCATION = APP_DIR.joinpath(settings.GOOGLE_ANALYTICS_CLIENT_SECRETS_JSON)

VIEW_ID = settings.GOOGLE_ANALYTICS_VIEW_ID

sites = site_list.site_list

dimentionFilter = {
    "dimensionName": "ga:pagePath",
    "not": False,
    "operator": "IN_LIST" if len(sites) > 0 else "REGEXP",
    "expressions": sites if len(sites) > 0 else ["^([^?\r\n]+)$"],
}


def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES
    )

    # Build the service object.
    analytics = build("analyticsreporting", "v4", credentials=credentials)

    return analytics


def get_report(start=None, end=None):
    analytics = initialize_analyticsreporting()

    """Queries the Analytics Reporting API V4.
    Args:
      analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
      The Analytics Reporting API V4 response.
    """
    return (
        analytics.reports()
        .batchGet(
            body={
                "reportRequests": [
                    {
                        "viewId": VIEW_ID,
                        "dateRanges": [{"startDate": start, "endDate": end}],
                        "metrics": [
                            {"expression": "ga:pageviews", "alias": "pageviews"},
                            {"expression": "ga:sessions", "alias": "sessions"},
                        ],
                        "dimensions": [
                            {"name": "ga:pagePath"},
                        ],
                        "dimensionFilterClauses": [
                            {
                                "operator": "OR",
                                "filters": [dimentionFilter],
                            }
                        ],
                        "orderBys": [
                            {"fieldName": "ga:pagePath", "sortOrder": "ASCENDING"},
                        ],
                    }
                ]
            }
        )
        .execute()
    )


def format_reports(response):
    headers = ("URL", "SESSIONS", "PAGE VIEWS")
    report = response.get("reports", [])[0]
    rows = report.get("data", {}).get("rows", [])

    data = []
    for row in rows:
        url = row.get("dimensions", [])
        values = row.get("metrics", [])[0].get("values", [])
        data.append(url + values)

    return headers, data
