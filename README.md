# DevHomesRepo

DevHomes is a real estate listing Django project. It holds multiple apartments and houses for sale, has a credit calculator function, and supports a message board for customers.

--- Tech Stack:---

* Python 3.13+
* Django (latest stable)
* PostgreSQL
* HTML / CSS
* Django ORM
* psycopg2-binary

--- Key features:---

The project contains four main apps:

// Listings //  
Users can create, edit and delete listings for properties for sale. They can also link them to messages and credit requests.

- Property CRUD - brokers / superusers only
- Amenity CRUD - brokers / superusers only
- Many-to-many Amenities
- Dynamic search filtering
- Pagination

//Accounts//  
Customers can create messages and link existing listings to their message.

- Contact inquiry submission - logged-in users only
- Inquiry dashboard
- Status tracking (New, In Progress, Closed)
- CRUD for inquiries - logged-in users only
- Phone validation
- Listing-linked inquiries

//Credit Calculator//  
Any user can estimate their monthly payment for their property credit, or plan theyr realy mortgage repayment.

- Loan calculation form
- Stores credit requests
- Dashboard for submitted requests
- Form for calculation of current and possible early repayment based on real-world data
- PDF downloadable report for the early repayment plan

  // Users //  
User management including Customers (logged in users) and Brokers (logged in Broker accounts).
- Unauthorized accounts have access to read all listings, and inquiries, and to create credit requests.
- Customers can view listings, and create and edit inquiries.
- Brokers can create and edit Listings and amenities, as well as inquiries.
- Superusers can edit all listings and inquiries.
- Each logged-in customer or broker has Many-to-Many relationship with Favourite functionality to Listings.
- Each logged-in customer or broker has a dashboard with their listings/inquiries/credit requests. 

//Homepage//  
The homepage of the site offers statistics and key listings to the users. It also has a search field for easy call-to-action.

//API-Listings Endpoint//  
There is an API endpoint for the Listings app exposed to enable CRUD on a permission-based restriction in accordance with the rest of the app. 

--- Notes ---
Superuser created for Softuni testing: SuperUser, pass: TheBestPass123

--logging--
Logging is enabled via django-easy-audit. All CRUD operations are logged in the DB, and are visible through the Admin panel (superuser accessible) in the CRUD section.

