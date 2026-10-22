import json
import os
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

USERS_FILE = os.path.join(DATA_DIR, 'users.json')
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.json')
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.json')
MESSAGES_FILE = os.path.join(DATA_DIR, 'messages.json')

def ensure_data_directory():
    """Ensure the data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)

def read_json(file_path, default=None):
    """Safely read JSON data from file."""
    if default is None:
        default = []
    if not os.path.exists(file_path):
        return default
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return default

def write_json(file_path, data):
    """Safely write JSON data to file with formatting."""
    ensure_data_directory()
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")
        return False

# ==========================================
# INITIAL SEED DATA
# ==========================================
def initialize_database():
    """Seeds the JSON database with rich initial realistic data if empty."""
    ensure_data_directory()

    # 1. Seed Users
    if not os.path.exists(USERS_FILE) or len(read_json(USERS_FILE)) == 0:
        seed_users = [
            {
                "id": "usr-admin-1",
                "name": "Platform Administrator",
                "email": "admin@farmdirect.com",
                "password_hash": generate_password_hash("admin123"),
                "role": "admin",
                "phone": "+91 99999 00001",
                "status": "approved",
                "created_at": "2026-01-10 10:00:00"
            },
            {
                "id": "usr-farmer-1",
                "name": "Ramesh Patel",
                "email": "ramesh@farmdirect.com",
                "password_hash": generate_password_hash("farmer123"),
                "role": "farmer",
                "farm_name": "Green Valley Organic Farm",
                "location": "Nashik, Maharashtra",
                "phone": "+91 98765 43210",
                "farming_type": "Certified Organic",
                "experience_years": 14,
                "bio": "Specializing in soil-enriched vine vegetables and exotic greens. Zero chemical pesticides used.",
                "status": "approved",
                "avatar": "https://images.unsplash.com/photo-1544717305-2782549b5136?w=200&auto=format&fit=crop&q=80",
                "created_at": "2026-01-15 08:30:00"
            },
            {
                "id": "usr-farmer-2",
                "name": "Sunita Sharma",
                "email": "sunita@farmdirect.com",
                "password_hash": generate_password_hash("farmer123"),
                "role": "farmer",
                "farm_name": "Himalayan Ridge Orchards & Apiary",
                "location": "Shimla, Himachal Pradesh",
                "phone": "+91 98765 43211",
                "farming_type": "Natural Mountain Agriculture",
                "experience_years": 9,
                "bio": "Cold-climate high-altitude orchard producing crispy apples, stone fruits, and pure mountain forest honey.",
                "status": "approved",
                "avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=200&auto=format&fit=crop&q=80",
                "created_at": "2026-01-18 11:20:00"
            },
            {
                "id": "usr-farmer-3",
                "name": "Gurpreet Singh",
                "email": "gurpreet@farmdirect.com",
                "password_hash": generate_password_hash("farmer123"),
                "role": "farmer",
                "farm_name": "Golden Fields Agri-Hub",
                "location": "Amritsar, Punjab",
                "phone": "+91 98765 43212",
                "farming_type": "Regenerative Grains",
                "experience_years": 20,
                "bio": "Growing heritage long-grain aromatic Basmati rice and stone-ground traditional wheat with zero stubble burning.",
                "status": "approved",
                "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&auto=format&fit=crop&q=80",
                "created_at": "2026-02-01 14:00:00"
            },
            {
                "id": "usr-farmer-4",
                "name": "Anand Verma",
                "email": "anand@farmdirect.com",
                "password_hash": generate_password_hash("farmer123"),
                "role": "farmer",
                "farm_name": "Deccan Fresh Hydroponics",
                "location": "Pune, Maharashtra",
                "phone": "+91 98765 43213",
                "farming_type": "Hydroponic & Protected Cultivation",
                "experience_years": 4,
                "bio": "Modern sustainable indoor farm growing crisp butterhead lettuce and microgreens with 90% less water.",
                "status": "pending",  # Pending for Admin to review and approve!
                "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&auto=format&fit=crop&q=80",
                "created_at": "2026-10-18 09:15:00"
            },
            {
                "id": "usr-cust-1",
                "name": "Priya Sharma",
                "email": "priya@gmail.com",
                "password_hash": generate_password_hash("customer123"),
                "role": "customer",
                "phone": "+91 91234 56789",
                "address": "Flat 402, Lotus Greens, Bandra West, Mumbai 400050",
                "status": "approved",
                "created_at": "2026-02-10 16:45:00"
            }
        ]
        write_json(USERS_FILE, seed_users)

    # 2. Seed Products
    if not os.path.exists(PRODUCTS_FILE) or len(read_json(PRODUCTS_FILE)) == 0:
        seed_products = [
            {
                "id": "prod-1",
                "farmer_id": "usr-farmer-1",
                "farmer_name": "Ramesh Patel",
                "farm_name": "Green Valley Organic Farm",
                "location": "Nashik, Maharashtra",
                "title": "Fresh Farm Vine Tomatoes",
                "category": "Vegetables",
                "price": 38,
                "unit": "1 kg",
                "stock": 140,
                "harvest_date": "Harvested Today Morning",
                "organic": True,
                "description": "Naturally ripened on the vine without carbide or chemicals. Rich in lycopene, deeply flavorful, and perfect for salads, curries, and sauces.",
                "image": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=600&auto=format&fit=crop&q=80",
                "rating": 4.9,
                "reviews_count": 48,
                "featured": True,
                "created_at": "2026-10-15 08:00:00"
            },
            {
                "id": "prod-2",
                "farmer_id": "usr-farmer-2",
                "farmer_name": "Sunita Sharma",
                "farm_name": "Himalayan Ridge Orchards & Apiary",
                "location": "Shimla, Himachal Pradesh",
                "title": "Royal Delicious Mountain Apples",
                "category": "Fruits",
                "price": 160,
                "unit": "1 kg (approx 5-6 apples)",
                "stock": 85,
                "harvest_date": "Picked 2 Days Ago",
                "organic": True,
                "description": "Crisp, sweet, and fragrant apples cultivated at 7,000 ft altitude in Shimla's sunny valley slopes. No wax coating, 100% natural blush.",
                "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=600&auto=format&fit=crop&q=80",
                "rating": 4.9,
                "reviews_count": 62,
                "featured": True,
                "created_at": "2026-10-16 09:30:00"
            },
            {
                "id": "prod-3",
                "farmer_id": "usr-farmer-3",
                "farmer_name": "Gurpreet Singh",
                "farm_name": "Golden Fields Agri-Hub",
                "location": "Amritsar, Punjab",
                "title": "Traditional Aromatic Basmati Rice",
                "category": "Grains",
                "price": 220,
                "unit": "2 kg Bag",
                "stock": 120,
                "harvest_date": "Naturally Aged 18 Months",
                "organic": True,
                "description": "Authentic long-grain traditional Basmati. Cooked grains elongate to over twice their length with exquisite aroma and non-sticky fluffy texture.",
                "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=600&auto=format&fit=crop&q=80",
                "rating": 4.8,
                "reviews_count": 39,
                "featured": True,
                "created_at": "2026-10-14 11:00:00"
            },
            {
                "id": "prod-4",
                "farmer_id": "usr-farmer-1",
                "farmer_name": "Ramesh Patel",
                "farm_name": "Green Valley Organic Farm",
                "location": "Nashik, Maharashtra",
                "title": "Tender Organic Baby Spinach (Palak)",
                "category": "Vegetables",
                "price": 28,
                "unit": "500g Bunch",
                "stock": 60,
                "harvest_date": "Harvested Today at Dawn",
                "organic": True,
                "description": "Crisp, nutrient-packed dark green spinach leaves washed with clean well water. Packed with dietary iron, vitamins A & C.",
                "image": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=600&auto=format&fit=crop&q=80",
                "rating": 4.7,
                "reviews_count": 27,
                "featured": False,
                "created_at": "2026-10-17 06:15:00"
            },
            {
                "id": "prod-5",
                "farmer_id": "usr-farmer-2",
                "farmer_name": "Sunita Sharma",
                "farm_name": "Himalayan Ridge Orchards & Apiary",
                "location": "Shimla, Himachal Pradesh",
                "title": "Raw Himalayan Wild Forest Honey",
                "category": "Dairy & Honey",
                "price": 380,
                "unit": "500g Glass Jar",
                "stock": 45,
                "harvest_date": "Bottled Oct 2026",
                "organic": True,
                "description": "Unheated, unfiltered multi-flora forest honey harvested from wild mountain bee colonies. Contains natural pollen, enzymes, and antioxidants.",
                "image": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=600&auto=format&fit=crop&q=80",
                "rating": 5.0,
                "reviews_count": 54,
                "featured": True,
                "created_at": "2026-10-10 13:40:00"
            },
            {
                "id": "prod-6",
                "farmer_id": "usr-farmer-3",
                "farmer_name": "Gurpreet Singh",
                "farm_name": "Golden Fields Agri-Hub",
                "location": "Amritsar, Punjab",
                "title": "Stone-Ground Whole Wheat Atta",
                "category": "Grains",
                "price": 210,
                "unit": "5 kg Bag",
                "stock": 90,
                "harvest_date": "Freshly Milled this Week",
                "organic": True,
                "description": "100% whole grain flour milled slowly using traditional stone chakki to retain fiber, wheat germ, and high mineral content. Makes super soft rotis.",
                "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&auto=format&fit=crop&q=80",
                "rating": 4.8,
                "reviews_count": 31,
                "featured": False,
                "created_at": "2026-10-12 10:00:00"
            },
            {
                "id": "prod-7",
                "farmer_id": "usr-farmer-1",
                "farmer_name": "Ramesh Patel",
                "farm_name": "Green Valley Organic Farm",
                "location": "Nashik, Maharashtra",
                "title": "Sweet Crunchy Carrots",
                "category": "Vegetables",
                "price": 45,
                "unit": "1 kg",
                "stock": 110,
                "harvest_date": "Harvested Yesterday",
                "organic": True,
                "description": "Soil-grown sweet red carrots rich in beta carotene. Juicy and crunchy, ideal for fresh juices, salads, and traditional gajar halwa.",
                "image": "https://images.unsplash.com/photo-1598170845058-32b9d6a5c317?w=600&auto=format&fit=crop&q=80",
                "rating": 4.6,
                "reviews_count": 22,
                "featured": False,
                "created_at": "2026-10-18 07:20:00"
            },
            {
                "id": "prod-8",
                "farmer_id": "usr-farmer-2",
                "farmer_name": "Sunita Sharma",
                "farm_name": "Himalayan Ridge Orchards & Apiary",
                "location": "Shimla, Himachal Pradesh",
                "title": "Organic Kashmiri Soft-Shell Walnuts",
                "category": "Fruits",
                "price": 420,
                "unit": "500g Pack",
                "stock": 35,
                "harvest_date": "Autumn 2026 Harvest",
                "organic": True,
                "description": "Kagzi walnuts that crack easily in hand. Extra light kernels packed with brain-boosting omega-3 fatty acids and natural oils.",
                "image": "https://images.unsplash.com/photo-1563227812-0ea4c22e6cc8?w=600&auto=format&fit=crop&q=80",
                "rating": 4.9,
                "reviews_count": 18,
                "featured": False,
                "created_at": "2026-10-11 15:10:00"
            },
            {
                "id": "prod-9",
                "farmer_id": "usr-farmer-1",
                "farmer_name": "Ramesh Patel",
                "farm_name": "Green Valley Organic Farm",
                "location": "Nashik, Maharashtra",
                "title": "Fresh Sweet Golden Corn",
                "category": "Vegetables",
                "price": 35,
                "unit": "2 Cobs Pack",
                "stock": 75,
                "harvest_date": "Harvested Today",
                "organic": True,
                "description": "Sweet, tender and milky corn cobs picked at peak sugar content before sunrise. Great for grilling or steaming.",
                "image": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=600&auto=format&fit=crop&q=80",
                "rating": 4.7,
                "reviews_count": 15,
                "featured": False,
                "created_at": "2026-10-19 09:00:00"
            },
            {
                "id": "prod-10",
                "farmer_id": "usr-farmer-3",
                "farmer_name": "Gurpreet Singh",
                "farm_name": "Golden Fields Agri-Hub",
                "location": "Amritsar, Punjab",
                "title": "Cold-Pressed Pure Yellow Mustard Oil",
                "category": "Grains",
                "price": 190,
                "unit": "1 Litre Bottle",
                "stock": 50,
                "harvest_date": "Pressed 3 Days Ago",
                "organic": True,
                "description": "Extracted via traditional wooden kachi ghani below 40°C to preserve natural pungency, aroma, and heart-healthy antioxidants.",
                "image": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=600&auto=format&fit=crop&q=80",
                "rating": 4.9,
                "reviews_count": 42,
                "featured": False,
                "created_at": "2026-10-13 12:30:00"
            }
        ]
        write_json(PRODUCTS_FILE, seed_products)

    # 3. Seed Orders
    if not os.path.exists(ORDERS_FILE) or len(read_json(ORDERS_FILE)) == 0:
        seed_orders = [
            {
                "id": "ORD-FD-84920",
                "customer_id": "usr-cust-1",
                "customer_name": "Priya Sharma",
                "customer_email": "priya@gmail.com",
                "customer_phone": "+91 91234 56789",
                "delivery_address": "Flat 402, Lotus Greens, Bandra West, Mumbai 400050",
                "items": [
                    {
                        "product_id": "prod-1",
                        "title": "Fresh Farm Vine Tomatoes",
                        "price": 38,
                        "unit": "1 kg",
                        "quantity": 2,
                        "total": 76,
                        "farmer_id": "usr-farmer-1",
                        "farmer_name": "Ramesh Patel",
                        "farm_name": "Green Valley Organic Farm"
                    },
                    {
                        "product_id": "prod-2",
                        "title": "Royal Delicious Mountain Apples",
                        "price": 160,
                        "unit": "1 kg (approx 5-6 apples)",
                        "quantity": 1,
                        "total": 160,
                        "farmer_id": "usr-farmer-2",
                        "farmer_name": "Sunita Sharma",
                        "farm_name": "Himalayan Ridge Orchards & Apiary"
                    }
                ],
                "subtotal": 236,
                "delivery_fee": 30,
                "discount": 0,
                "total_amount": 266,
                "payment_method": "UPI (Google Pay)",
                "payment_status": "Paid",
                "transaction_id": "UPI-TXN-984210452",
                "order_status": "Out for Delivery", # Statuses: 'Placed', 'Farmer Confirmed', 'Harvested & Packed', 'Out for Delivery', 'Delivered'
                "timeline": [
                    {"status": "Placed", "time": "2026-10-20 14:10:00", "description": "Order submitted and paid successfully."},
                    {"status": "Farmer Confirmed", "time": "2026-10-20 15:30:00", "description": "Farmers accepted harvest requests."},
                    {"status": "Harvested & Packed", "time": "2026-10-21 07:45:00", "description": "Fresh produce carefully harvested, inspected & eco-boxed."},
                    {"status": "Out for Delivery", "time": "2026-10-21 17:00:00", "description": "Dispatch runner is on the way to Lotus Greens, Bandra."}
                ],
                "notes": "Please leave at door if doorbell is unanswered.",
                "created_at": "2026-10-20 14:10:00"
            }
        ]
        write_json(ORDERS_FILE, seed_orders)

    # 4. Seed Messages
    if not os.path.exists(MESSAGES_FILE) or len(read_json(MESSAGES_FILE)) == 0:
        seed_messages = [
            {
                "id": "msg-1",
                "name": "Kavita Deshmukh",
                "email": "kavita.deshmukh@gmail.com",
                "role_inquiry": "Consumer",
                "subject": "Bulk orders for apartment community cooperative",
                "message": "Hello FarmDirect team! We have 80 families in our housing society who wish to organize a weekly collective delivery directly from Ramesh Patel's farm. Can we arrange regular scheduled slots?",
                "status": "unread",
                "created_at": "2026-10-21 11:20:00"
            },
            {
                "id": "msg-2",
                "name": "Balwant Singh",
                "email": "balwant.singh@punjaborganic.org",
                "role_inquiry": "Farmer",
                "subject": "Onboarding 15 organic mustard and pulse farmers",
                "message": "Greetings, we run a smallholder collective in Bathinda with NPOP organic certification. We want to list our cold-pressed oils on FarmDirect. Please contact us for verification.",
                "status": "unread",
                "created_at": "2026-10-21 16:40:00"
            }
        ]
        write_json(MESSAGES_FILE, seed_messages)

# ==========================================
# USER OPERATIONS
# ==========================================
def get_all_users():
    return read_json(USERS_FILE, [])

def get_user_by_id(user_id):
    users = get_all_users()
    for u in users:
        if u.get('id') == user_id:
            return u
    return None

def get_user_by_email(email):
    users = get_all_users()
    for u in users:
        if u.get('email', '').strip().lower() == email.strip().lower():
            return u
    return None

def verify_user(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user.get('password_hash', ''), password):
        return user
    return None

def create_user(user_dict):
    users = get_all_users()
    # Check if email exists
    for u in users:
        if u.get('email', '').strip().lower() == user_dict.get('email', '').strip().lower():
            return None, "An account with this email already exists."

    user_dict['id'] = f"usr-{uuid.uuid4().hex[:8]}"
    if 'password' in user_dict:
        user_dict['password_hash'] = generate_password_hash(user_dict['password'])
        del user_dict['password']
    
    if 'created_at' not in user_dict:
        user_dict['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # If farmer, default status to pending or approved
    if user_dict.get('role') == 'farmer' and 'status' not in user_dict:
        user_dict['status'] = 'approved' # Allow seamless immediate demo while allowing admin to toggle
    elif 'status' not in user_dict:
        user_dict['status'] = 'approved'

    users.append(user_dict)
    write_json(USERS_FILE, users)
    return user_dict, None

def update_user_status(user_id, new_status):
    users = get_all_users()
    for u in users:
        if u.get('id') == user_id:
            u['status'] = new_status
            write_json(USERS_FILE, users)
            return True
    return False

# ==========================================
# PRODUCT OPERATIONS
# ==========================================
def get_all_products():
    return read_json(PRODUCTS_FILE, [])

def get_product_by_id(product_id):
    products = get_all_products()
    for p in products:
        if p.get('id') == product_id:
            return p
    return None

def get_products_by_farmer(farmer_id):
    products = get_all_products()
    return [p for p in products if p.get('farmer_id') == farmer_id]

def create_product(product_dict):
    products = get_all_products()
    product_dict['id'] = f"prod-{uuid.uuid4().hex[:8]}"
    if 'created_at' not in product_dict:
        product_dict['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if 'rating' not in product_dict:
        product_dict['rating'] = 5.0
    if 'reviews_count' not in product_dict:
        product_dict['reviews_count'] = 1
    if 'featured' not in product_dict:
        product_dict['featured'] = False

    # Image fallback if not provided
    if not product_dict.get('image'):
        category = product_dict.get('category', '').lower()
        if 'fruit' in category:
            product_dict['image'] = 'https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=600&auto=format&fit=crop&q=80'
        elif 'grain' in category:
            product_dict['image'] = 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=600&auto=format&fit=crop&q=80'
        elif 'dairy' in category or 'honey' in category:
            product_dict['image'] = 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=600&auto=format&fit=crop&q=80'
        else:
            product_dict['image'] = 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600&auto=format&fit=crop&q=80'

    products.insert(0, product_dict)
    write_json(PRODUCTS_FILE, products)
    return product_dict

def update_product(product_id, updated_fields):
    products = get_all_products()
    for p in products:
        if p.get('id') == product_id:
            for k, v in updated_fields.items():
                p[k] = v
            write_json(PRODUCTS_FILE, products)
            return p
    return None

def delete_product(product_id):
    products = get_all_products()
    new_products = [p for p in products if p.get('id') != product_id]
    if len(new_products) != len(products):
        write_json(PRODUCTS_FILE, new_products)
        return True
    return False

# ==========================================
# ORDER OPERATIONS
# ==========================================
def get_all_orders():
    orders = read_json(ORDERS_FILE, [])
    # Return sorted with newest first
    return sorted(orders, key=lambda x: x.get('created_at', ''), reverse=True)

def get_order_by_id(order_id):
    orders = get_all_orders()
    for o in orders:
        if o.get('id') == order_id:
            return o
    return None

def get_orders_by_customer(customer_id):
    orders = get_all_orders()
    return [o for o in orders if o.get('customer_id') == customer_id]

def get_orders_for_farmer(farmer_id):
    """Returns orders containing at least one product by this farmer."""
    orders = get_all_orders()
    farmer_orders = []
    for o in orders:
        farmer_items = [item for item in o.get('items', []) if item.get('farmer_id') == farmer_id]
        if farmer_items:
            o_copy = dict(o)
            o_copy['farmer_items'] = farmer_items
            o_copy['farmer_subtotal'] = sum(item.get('total', 0) for item in farmer_items)
            farmer_orders.append(o_copy)
    return farmer_orders

def create_order(order_dict):
    orders = read_json(ORDERS_FILE, [])
    order_dict['id'] = f"ORD-FD-{uuid.uuid4().hex[:6].upper()}"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    order_dict['created_at'] = now_str
    
    # Initialize timeline
    order_dict['order_status'] = 'Placed'
    order_dict['timeline'] = [
        {
            "status": "Placed",
            "time": now_str,
            "description": f"Order received. Payment method: {order_dict.get('payment_method', 'Online')}"
        }
    ]

    # Deduct product stock
    products = get_all_products()
    prod_map = {p['id']: p for p in products}
    for itm in order_dict.get('items', []):
        pid = itm.get('product_id')
        qty = int(itm.get('quantity', 1))
        if pid in prod_map:
            prod_map[pid]['stock'] = max(0, int(prod_map[pid].get('stock', 0)) - qty)
    write_json(PRODUCTS_FILE, list(prod_map.values()))

    orders.insert(0, order_dict)
    write_json(ORDERS_FILE, orders)
    return order_dict

def update_order_status(order_id, new_status, comment=""):
    orders = get_all_orders()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for o in orders:
        if o.get('id') == order_id:
            o['order_status'] = new_status
            if 'timeline' not in o:
                o['timeline'] = []
            
            desc = comment or f"Status updated to '{new_status}' by agricultural fulfillment hub."
            o['timeline'].append({
                "status": new_status,
                "time": now_str,
                "description": desc
            })
            write_json(ORDERS_FILE, orders)
            return o
    return None

# ==========================================
# MESSAGE / INQUIRY OPERATIONS
# ==========================================
def get_all_messages():
    messages = read_json(MESSAGES_FILE, [])
    return sorted(messages, key=lambda x: x.get('created_at', ''), reverse=True)

def create_message(msg_dict):
    messages = read_json(MESSAGES_FILE, [])
    msg_dict['id'] = f"msg-{uuid.uuid4().hex[:6]}"
    msg_dict['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg_dict['status'] = 'unread'
    messages.insert(0, msg_dict)
    write_json(MESSAGES_FILE, messages)
    return msg_dict

def mark_message_read(msg_id):
    messages = get_all_messages()
    for m in messages:
        if m.get('id') == msg_id:
            m['status'] = 'read'
            write_json(MESSAGES_FILE, messages)
            return True
    return False

# Initialize seed data on load
initialize_database()
