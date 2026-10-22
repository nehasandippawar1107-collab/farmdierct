# 🌾 FarmDirect - Farmer-to-Customer Marketplace

**FarmDirect** is a modern, responsive, and beginner-friendly web application designed to connect local farmers directly with consumers, completely eliminating unnecessary middlemen, APMC mandi commission cuts, and retail markups.

Built with **Python (Flask)**, a **JSON-based database**, and a **clean green-and-white theme**, FarmDirect delivers a fast, transparent, and direct farm-to-table shopping experience.

---

## ✨ Features Implemented

1. **🌿 Home Page (`/`)**:
   - Website branding with sprout logo and clean navigation bar.
   - Hero banner with quick crop search bar and action buttons (*Explore Marketplace*, *Sell as a Farmer*).
   - Real-time impact counters (100% Middlemen Cut Eliminated, +40% Farmer Earnings).
   - Interactive category pills (Vegetables, Fruits, Grains, Dairy & Honey).
   - Featured fresh produce grid with instant **Add to Cart** action.
   - Step-by-step visual explanation of how FarmDirect works.

2. **👤 Customer Login & Registration (`/login`, `/register?role=customer`)**:
   - Customer account creation with delivery address and mobile number.
   - 1-Click Demo Login button to test customer functionality instantly.
   - Secure session handling.

3. **🚜 Farmer Login & Registration (`/login`, `/register?role=farmer`)**:
   - Farmer onboarding with farm name, location, farming practice (Certified Organic, Natural, Hydroponic), and bio.
   - Pre-seeded with realistic local farmers (Ramesh Patel, Sunita Sharma, Gurpreet Singh).

4. **🛒 Product Marketplace (`/marketplace`)**:
   - Full catalog of fresh vegetables, orchard fruits, stone-ground flours, and pure wild honey.
   - Live display of farm price, unit of measure, stock quantity, harvest date, and farmer profile tags.
   - Product detail page (`/product/<id>`) with farmer backstory and organic certifications.

5. **🔍 Search & Filter (`/marketplace`)**:
   - Keyword search across product titles, descriptions, and farmer names.
   - Category filter pills (Vegetables, Fruits, Grains, Dairy & Honey).
   - Price cap slider/input (e.g. products under ₹100 / ₹200).
   - Farmer region filter (Nashik, Shimla, Punjab, Pune).
   - Sorting options: Featured, Price Low to High, Price High to Low, Highest Rated.

6. **🛍️ Shopping Basket (`/cart`)**:
   - Add products from Marketplace, Home, or Detail pages.
   - Increment, decrement, or remove items with automatic subtotal updates.
   - Live **Middleman Savings calculation** (*"You saved ~₹X vs supermarket retail markups!"*).
   - Free delivery threshold notice (Free above ₹300).

7. **📦 Order Tracking (`/orders`, `/order/track/<order_id>`)**:
   - Itemized order history for customers.
   - Guest order tracking by Order ID search.
   - **5-Stage Visual Stepper Timeline**:
     1. `Order Placed`
     2. `Farmer Confirmed`
     3. `Harvested & Packed`
     4. `Out for Delivery`
     5. `Delivered`
   - Real-time timestamps and fulfillment commentary for each stage.

8. **🧑‍🌾 Farmer Dashboard (`/farmer/dashboard`)**:
   - Real-time KPI summary cards: Listed Products, Orders Received, Direct Revenue (₹), Pending Confirmations.
   - **Produce Catalog Management**: Add fresh harvest (`/farmer/product/add`), edit price/stock, delete listing.
   - **Order Fulfillment Control**: View incoming orders and advance their progress (`Placed` ➔ `Farmer Confirmed` ➔ `Harvested & Packed` ➔ `Out for Delivery` ➔ `Delivered`).

9. **🛡️ Admin Dashboard (`/admin/dashboard`)**:
   - Platform KPI metrics: Gross GMV Sales, Total Orders, Active Farmers, Products, Customer count.
   - **Farmer Verification**: View pending farmer applications and approve or suspend with one click.
   - **Master Order Log**: Complete oversight of all transactions across all farms.
   - **Inquiries Desk**: View and mark customer/farmer contact messages as resolved.

10. **📖 About Us & Contact (`/about`, `/contact`)**:
    - The story behind FarmDirect, our anti-middleman charter, and fair price pledge.
    - Contact form with inquiry categorization (Customer, Farmer, Cooperative). Messages are stored in `messages.json` and visible in the Admin dashboard.
    - FAQ accordion for common direct-delivery questions.

11. **💳 Comprehensive Payment Options (`/checkout`)**:
    - **Cash on Delivery (Pay on Delivery)**: Simple, zero advance hassle.
    - **Instant UPI / QR Code**: Interactive scanner with dynamic FarmDirect QR code and VPA verification.
    - **Credit / Debit Cards**: Card simulation with live preview, card number, MM/YY expiry, CVV.
    - **Net Banking**: One-click selection of major banks (SBI, HDFC, ICICI, Axis).
    - Immediate order generation and automated inventory/stock deduction.

---

## 📂 Project Architecture

```
farmdirect/
├── app.py                     # Flask application routes, session handling, business logic
├── data_manager.py            # JSON database reader/writer & seed data generator
├── requirements.txt           # Python dependencies (Flask, Werkzeug)
├── README.md                  # Detailed documentation and setup guide
├── data/                      # JSON Database (Auto-generated on launch)
│   ├── users.json             # Customers, Farmers, and Admin accounts
│   ├── products.json          # Harvest produce catalog
│   ├── orders.json            # Customer orders and tracking timelines
│   └── messages.json          # Contact inquiries from the website
├── static/
│   ├── css/
│   │   └── style.css          # Modern clean green-and-white theme
│   └── js/
│       └── main.js            # AJAX cart, payment switcher, mobile nav, demo quick-fill
└── templates/
    ├── base.html              # Base layout with navbar, cart counter, footer, toasts
    ├── index.html             # Homepage with hero, featured products, and benefits
    ├── marketplace.html       # Product catalog with search, filters & sort
    ├── product_detail.html    # Detailed product view with farmer card
    ├── cart.html              # Shopping basket with savings calculator
    ├── checkout.html          # Delivery details & 4 payment options
    ├── order_success.html     # Order confirmation receipt
    ├── orders.html            # Order history and ID lookup
    ├── order_track.html       # 5-step visual tracking stepper
    ├── farmer_dashboard.html  # Farmer portal for managing products & orders
    ├── farmer_product_form.html # Add/Edit produce listings
    ├── admin_dashboard.html   # Admin master control panel
    ├── login.html             # Sign in page with 1-click test credentials
    ├── register.html          # Customer and Farmer registration
    ├── about.html             # FarmDirect mission and fair trade philosophy
    └── contact.html           # Contact form and FAQ accordion
```

---

## 🚀 How to Run in Visual Studio Code (Step-by-Step)

### Step 1: Open the Project in VS Code
1. Open **Visual Studio Code**.
2. Click **File ➔ Open Folder...** (or press `Ctrl + K, Ctrl + O`).
3. Select the project directory:
   ```
   C:\Users\Asus\.gemini\antigravity\scratch\farmdirect
   ```

### Step 2: Open Terminal in VS Code
1. In VS Code, press `` Ctrl + ` `` (Backtick) or go to **Terminal ➔ New Terminal**.

### Step 3: Install Flask
In the terminal, run:
```bash
pip install -r requirements.txt
```
*(Flask will be installed in seconds).*

### Step 4: Run the Application
Start the Flask server:
```bash
python app.py
```

You will see:
```text
============================================================
 FarmDirect - Farmer-to-Customer Marketplace
 Running at: http://127.0.0.1:5000
============================================================
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 5: Open in Your Web Browser
Hold `Ctrl` and click the link in your terminal, or open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔑 Pre-Configured Test Accounts (1-Click Login)

The `/login` page includes **1-Click Quick-Fill Buttons** so you don't even have to type passwords during testing!

| Role | Name | Email | Password | What You Can Test |
| :--- | :--- | :--- | :--- | :--- |
| **Customer** | Priya Sharma | `priya@gmail.com` | `customer123` | Add items to cart, checkout with UPI/Card/COD, track orders |
| **Farmer 1** | Ramesh Patel | `ramesh@farmdirect.com` | `farmer123` | Nashik Organic Farm: add crops, edit prices, advance order status |
| **Farmer 2** | Sunita Sharma | `sunita@farmdirect.com` | `farmer123` | Shimla Apple Orchard & Raw Honey: view earnings, update inventory |
| **Admin** | Administrator | `admin@farmdirect.com` | `admin123` | Approve pending farmers, view platform sales, review orders & messages |

---

## 🎨 Theme & Design Highlights
- **Color Palette**: Forest Harvest Green (`#2d6a4f`), Deep Organic Pine (`#1b4332`), Fresh Leaf (`#52b788`), Soft Mint (`#d8f3dc`), and Crisp White (`#ffffff`).
- **Responsive**: Fully optimized for laptops, tablets, and smartphones with mobile drawer navigation.
- **Micro-Interactions**: AJAX instant add-to-cart toast alerts, pulse animation on the cart badge, interactive credit card preview, dynamic QR code scanner.
