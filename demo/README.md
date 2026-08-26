# Django ERP Framework Demo

A demo application showcasing the capabilities of **Django ERP Framework**.

This demo includes:
- **Business Models**: Clients, Products, Sales, Sale Items (inheriting from ERP Framework base models)
- **Reporting Engine**: 4 pre-configured reports demonstrating grouping, aggregation, and charting
- **Admin Integration**: Jazzmin theme with custom configuration
- **Dashboard**: Widgets for visualizing report data
- **Sample Data**: Auto-generated demo data for testing

---

## Quick Start

### Prerequisites
- Python 3.8+
- Django 3.2+
- All dependencies listed in `requirements.txt`

### Installation

1. **Clone or navigate to the project:**
   ```bash
   cd /home/alejandro/Documents/django-erp/django-erp-framework/demo
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # OR
   venv\Scripts\activate   # Windows
   ```

3. **Install dependencies:**
   
   **Option A: Install from PyPI**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Option B: Install ERP Framework from local source** (recommended for development)
   ```bash
   # First, install the framework in development mode
   cd /home/alejandro/Documents/django-erp/django-erp-framework
   pip install -e .
   
   # Then install other dependencies
   cd demo
   pip install django-crequest crispy-forms crispy-bootstrap5 reversion jazzmin django-slick-reporting
   ```
   
   **Note:** The correct package names are:
   - `django-crequest` (pip install), but Django app name is `crequest`
   - `crispy-bootstrap5` (not `crispy-bootstrap4`)
   - `tabular-permissions` is deprecated and no longer required

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Seed demo data:**
   ```bash
   python manage.py seed_demo_data
   ```
   This creates:
   - Admin user: `admin` / `admin123`
   - 5 sample clients
   - 8 sample products
   - 10-15 sample sales with items

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

---

## Access the Demo

| **URL** | **Description** | **Credentials** |
|---------|-----------------|----------------|
| http://localhost:8000/admin/ | Standard Django Admin | admin / admin123 |
| http://localhost:8000/erp-system/ | ERP Framework Admin | admin / admin123 |

---

## Models

### Entity Models (inherit from `EntityModel`)
- **Client**: Business clients with contact information
  - Fields: `name`, `slug`, `email`, `phone`, `address`, `notes`
  
- **Product**: Products available for sale
  - Fields: `name`, `slug`, `code`, `price`, `stock`, `category`, `notes`

### Transaction Models (inherit from `TransactionModel`)
- **Sale**: Sales transactions
  - Fields: `slug`, `date`, `client` (FK), `value`, `type`, `notes`
  
- **SaleItem**: Individual items in a sale (inherits from `QuantitativeTransactionItemModel`)
  - Fields: `sale` (FK), `product` (FK), `quantity`, `price`, `discount`, `value`
  - Note: `value` is automatically calculated as `(quantity * price) - (quantity * price * discount / 100)`

---

## Reports

The demo includes 4 pre-configured reports:

### 1. Sales by Client
- **Code:** `sales_by_client`
- **Type:** Grouped report
- **Fields:** Client name, email, sale date, sale value
- **Chart:** Bar chart showing sales by client
- **Access:** Available in ERP System admin under Reports

### 2. Sales by Product
- **Code:** `sales_by_product`
- **Type:** Multi-level grouped report
- **Fields:** Product name, category, quantity sold, total value, unit price
- **Chart:** Pie chart showing sales distribution by product

### 3. Inventory Report
- **Code:** `inventory_report`
- **Type:** Tabular report
- **Fields:** Product name, code, category, price, stock
- **Chart:** Bar chart showing inventory by category

### 4. Daily Sales Summary
- **Code:** `daily_sales_report`
- **Type:** Time-series report
- **Fields:** Date, total sales, client count
- **Chart:** Line chart showing daily sales trend

---

## Customization

### Adding New Models
To add a new model that integrates with ERP Framework:

```python
from erp_framework.base.models import EntityModel, TransactionModel

class NewEntity(EntityModel):
    # Your fields here
    pass

class NewTransaction(TransactionModel):
    # Your fields here
    pass
```

### Adding New Reports
1. Create a new report class in `demo_app/reports.py`:

```python
from slick_reporting import Report, SlickReportField
from erp_framework.reporting.registry import report_registry
from .models import YourModel

class YourReport(Report):
    report_model = YourModel
    
    class Meta:
        name = "your_report_code"
        title = "Your Report Title"
        description = "Report description"
    
    fields = [
        SlickReportField.create(field_name='field_name', name='Display Name', type='char'),
        # Add more fields...
    ]
    
    @classmethod
    def get_report_queryset(cls, request):
        return YourModel.objects.all()
```

2. Register the report:

```python
report_registry.register(YourReport)
```

3. The report will automatically appear in the ERP System admin.

---

## Admin Customization

### Custom Admin Classes
Use `BaseAdmin` from ERP Framework for consistency:

```python
from erp_framework.admin.base import BaseAdmin
from django.contrib import admin
from .models import YourModel

@admin.register(YourModel)
class YourModelAdmin(BaseAdmin):
    list_display = ('field1', 'field2')
    list_filter = ('field1',)
    search_fields = ('field1', 'field2')
```

---

## Configuration Options

### ERP Framework Settings
Edit `demo_project/settings.py`:

```python
ERP_FRAMEWORK_SETTING_DEFAULT = {
    "site_name": "Your Site Name",
    "site_header": "Your Site Header",
    "index_title": "Your Dashboard Title",
}
```

### Jazzmin Theme Settings
Customize the admin theme appearance:

```python
JAZZMIN_SETTINGS = {
    "site_title": "Your Title",
    "site_header": "Your Header",
    "site_brand": "Your Brand",
    "welcome_sign": "Welcome Message",
    # ... more settings
}
```

---

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: erp_framework**
   - Solution: Install the package in development mode:
     ```bash
     cd /home/alejandro/Documents/django-erp/django-erp-framework
     pip install -e .
     ```

2. **TemplateDoesNotExist errors**
   - Solution: Ensure all dependencies are installed and `INSTALLED_APPS` is correct

3. **Migration errors**
   - Solution: Delete `db.sqlite3` and run:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

4. **Static files not loading**
   - Solution: Run:
     ```bash
     python manage.py collectstatic
     ```

---

## Project Structure

```
demo/
├── manage.py
├── demo_project/
│   ├── __init__.py
│   ├── settings.py      # Django + ERP Framework settings
│   ├── urls.py          # URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── demo_app/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py        # Client, Product, Sale, SaleItem
│   ├── admin.py         # Admin configurations
│   ├── reports.py       # Report definitions
│   └── management/
│       └── commands/
│           └── seed_demo_data.py  # Data seeding command
├── requirements.txt
└── README.md
```

---

## Resources

- **Django ERP Framework Documentation:** https://django-erp-framework.readthedocs.io/
- **GitHub Repository:** https://github.com/RamezIssac/django-erp-framework
- **Slick Reporting Documentation:** https://github.com/ra-systems/django-slick-reporting

---

## License

This demo application is provided as-is for educational and demonstration purposes. The Django ERP Framework itself is licensed under the MIT License.

---

## Contributing

This is a demo project. If you find issues with the **Django ERP Framework**, please report them to the main repository.

---

## Support

For questions or support regarding Django ERP Framework:
- Check the [documentation](https://django-erp-framework.readthedocs.io/)
- Open an issue on [GitHub](https://github.com/RamezIssac/django-erp-framework)
