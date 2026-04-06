# DevHomes

DevHomes is a Django real estate platform for browsing and managing property listings, sending property-related inquiries, and using mortgage and early repayment calculators.

Live site: http://dev-homes.site/  
The project is deployed on AWS using a PostgreSQL, Celery and Redis.
Listings API: http://dev-homes.site/api/listings/

---

## Tech Stack

- Python 3.10+
- Django
- PostgreSQL
- Django REST Framework
- Celery
- Redis
- HTML / CSS
- Django ORM
- ReportLab
- Pillow
- psycopg2-binary
- django-easy-audit

---

## Main Features

The project contains four main apps:

### Listings
Users can browse and manage property listings for apartments and houses for sale.

- Property CRUD for brokers and superusers
- Amenity CRUD for brokers and superusers
- Many-to-many relationship between properties and amenities
- Search and filtering
- Pagination
- Property favourites
- Price per square meter calculation

### Accounts
Customers can create listing-linked inquiries and brokers can manage them.

- Contact inquiry submission for logged-in users
- Inquiry dashboard
- Status tracking: New, In Progress, Closed
- Inquiry detail, edit and delete functionality
- Listing-linked inquiries
- Phone number validation
- Reply/edit flow for inquiries
- Custom permission handling for owners, listing brokers, and superusers

### Credit Calculator
Users can estimate mortgage payments and compare standard vs early repayment plans.

- Standard loan monthly payment calculator
- Stored credit requests
- Early repayment calculator with real-world cost estimates
- Asynchronous PDF report generation for early repayment comparison
- Background processing with Celery
- Redis as message broker / result backend
- Dashboard visibility for generated repayment reports
- Downloadable generated PDF report

### Users
Role-based user management for customers, brokers, and superusers.

- Registration with role selection
- User groups for broker/customer roles
- Profile edit
- Password reset flow
- Delete account flow with confirmation screen
- Personal dashboard with:
  - favorite listings
  - inquiries
  - credit requests
  - early repayment reports
  - broker listings

### Homepage
The homepage includes:
- summary statistics
- featured listings
- call-to-action search

### API
A REST API endpoint is exposed for listings.

- Listings API endpoint: `http://dev-homes.site/api/listings/`
- Permission-aware CRUD behavior aligned with the rest of the platform

---

## Async Early Repayment Report Flow

The early repayment calculator supports asynchronous report generation.

### How it works
1. A logged-in user submits an early repayment report request
2. Django saves the report request in the database
3. A Celery task is queued
4. Redis acts as the broker between Django and Celery
5. The Celery worker:
   - calculates the repayment comparison
   - generates a PDF report
   - stores the generated file
   - updates the report status
6. The user can later view the report status and download the PDF from their dashboard

### Benefits
- Faster HTTP response time
- Non-blocking report generation
- Better production readiness for heavier background tasks

---

## Roles and Permissions

### Guest users
- Can browse listings
- Can use the credit calculator
- Can access public pages

### Customers
- Can create and manage their own inquiries
- Can favorite listings
- Can access their personal dashboard
- Can request early repayment reports

### Brokers
- Can create, edit, and delete listings
- Can manage amenities
- Can manage inquiries related to their listings
- Can access their personal dashboard and broker listings

### Superusers
- Full admin access
- Can manage all objects through Django admin and the site where permissions allow

---

## Logging and Audit Trail

Logging is enabled via `django-easy-audit`.

- CRUD operations are logged in the database
- Logs are visible in the Django admin panel
- This supports traceability during testing and administration

---

## Environment Variables

Create a `.env` file in the project root.

### Example `.env` for local development

```env
DEBUG=True
SECRET_KEY=replace-me
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=devhomesaws
DB_USER=postgres
DB_PASSWORD=121212
DB_HOST=localhost
DB_PORT=5432

DEFAULT_FROM_EMAIL=noreply@devhomes.local

CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
```

Local Setup & Running
- Create a PostgreSQL instance and update the .env file with its settings.
1. Install dependencies
pip install -r requirements.txt
2. Apply migrations
python manage.py migrate
3. Run the application
python manage.py runserver

The app will be available at:

http://127.0.0.1:8000/


-- Important:
--- !!! User groups need to be manually created via Superuser in the Admin panel and their permissions need to be set up manually. If the groups are called Customer and Broker, new users should be auto-assigned to the groups during profile registration. 

The application runs successfully with the default configuration after installing dependencies and applying migrations.
The project includes asynchronous background processing for:
-Early repayment PDF report generation

The application works without Redis and Celery, but:
- Async reports will not complete
- Reports will remain in "Pending" or "Processing" state

Enable Async Functionality

To fully test background processing, start the following services:

Terminal 1 – Redis:

- redis-server
  
Terminal 2 – Celery Worker:

- celery -A DevHomesDjango worker -l info
  
Terminal 3 – Django Server:

- python manage.py runserver

Notes:
- The project is fully runnable without additional services.
- Celery and Redis are required only for async functionality.
- All required environment variables are listed above for local testing.
