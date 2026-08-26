from django.utils.translation import gettext_lazy as _
from erp_framework.reporting.registry import register_report_view
from erp_framework.reporting.views import ReportView
from .models import Sale, SaleItem, Product, Client


@register_report_view
class SalesByClientReport(ReportView):
    report_title = _("Sales by Client")
    report_slug = "sales_by_client"
    base_model = Client
    report_model = Sale
    group_by = "client"
    columns = ["slug", "name", "__total__"]
    chart_settings = [
        {
            "id": "pie",
            "name": _("Sales by Client"),
            "type": "pie",
            "data_source": ["__total__"],
            "title_source": ["name"],
        },
    ]


@register_report_view
class SalesByProductReport(ReportView):
    report_title = _("Sales by Product")
    report_slug = "sales_by_product"
    base_model = Product
    report_model = SaleItem
    group_by = "product"
    columns = ["slug", "name", "__balance_quantity__", "__balance__"]
    chart_settings = [
        {
            "id": "pie",
            "name": _("Sales by Product"),
            "type": "pie",
            "data_source": ["__balance__"],
            "title_source": ["name"],
        },
    ]


@register_report_view
class SalesDetailedReport(ReportView):
    report_title = _("Sales Detail")
    report_slug = "sales_detail"
    base_model = Client
    report_model = Sale
    group_by = None
    columns = ["slug", "date", "client__name", "value"]
