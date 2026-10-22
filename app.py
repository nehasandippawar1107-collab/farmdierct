from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import functools
import os
import data_manager

app = Flask(__name__)
# Secret key for session signing
app.secret_key = os.environ.get('SECRET_KEY', 'farmdirect-secret-key-super-secure-2026')

# -------------------------------------------------------------
# CONTEXT PROCESSORS & HELPERS
# -------------------------------------------------------------
@app.context_processor
def inject_global_data():
    """Injects user session info and cart item count to all Jinja templates."""
    cart = session.get('cart', {})
    cart_count = sum(cart.values()) if isinstance(cart, dict) else 0
    current_user = None
    if 'user_id' in session:
        current_user = data_manager.get_user_by_id(session['user_id'])
    
    return {
        'cart_count': cart_count,
        'current_user': current_user,
        'user_role': session.get('user_role'),
        'user_name': session.get('user_name')
    }

def login_required(view):
    """Decorator to require login for a route."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login', next=request.url))
        return view(**kwargs)
    return wrapped_view

def role_required(allowed_roles):
    """Decorator to require specific user roles."""
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if 'user_id' not in session:
                flash("Please log in to continue.", "warning")
                return redirect(url_for('login', next=request.url))
            if session.get('user_role') not in allowed_roles:
                flash("Access denied. You do not have permission to view this page.", "danger")
                return redirect(url_for('index'))
            return view(**kwargs)
        return wrapped_view
    return decorator


# -------------------------------------------------------------
# HOME & PUBLIC ROUTES
# -------------------------------------------------------------
@app.route('/')
def index():
    """Home page with hero section, featured produce, benefits, and stats."""
    all_products = data_manager.get_all_products()
    # Featured products or latest 6 products
    featured_products = [p for p in all_products if p.get('featured')]
    if not featured_products:
        featured_products = all_products[:6]
    else:
        featured_products = featured_products[:6]

    # Quick statistics
    stats = {
        'farmers_count': len([u for u in data_manager.get_all_users() if u.get('role') == 'farmer']),
        'products_count': len(all_products),
        'orders_count': len(data_manager.get_all_orders()),
        'middleman_cut_eliminated': '100%',
        'farmer_earnings_boost': '+40%'
    }
    return render_template('index.html', featured_products=featured_products, stats=stats)


@app.route('/marketplace')
def marketplace():
    """
    Marketplace with live search, category filtering, price range,
    farmer location filtering, and sorting.
    """
    products = data_manager.get_all_products()
    
    # Filter parameters
    search_query = request.args.get('q', '').strip().lower()
    category = request.args.get('category', 'All').strip()
    location = request.args.get('location', 'All').strip()
    max_price = request.args.get('max_price', '')
    sort_by = request.args.get('sort', 'featured')

    # Apply search filter
    if search_query:
        products = [
            p for p in products
            if search_query in p.get('title', '').lower()
            or search_query in p.get('description', '').lower()
            or search_query in p.get('farmer_name', '').lower()
            or search_query in p.get('farm_name', '').lower()
            or search_query in p.get('location', '').lower()
        ]

    # Apply category filter
    if category and category != 'All':
        products = [p for p in products if p.get('category', '').lower() == category.lower()]

    # Apply location filter
    if location and location != 'All':
        products = [p for p in products if location.lower() in p.get('location', '').lower()]

    # Apply price filter
    if max_price:
        try:
            max_p = float(max_price)
            products = [p for p in products if float(p.get('price', 0)) <= max_p]
        except ValueError:
            pass

    # Apply sorting
    if sort_by == 'price_asc':
        products = sorted(products, key=lambda x: float(x.get('price', 0)))
    elif sort_by == 'price_desc':
        products = sorted(products, key=lambda x: float(x.get('price', 0)), reverse=True)
    elif sort_by == 'rating':
        products = sorted(products, key=lambda x: float(x.get('rating', 0)), reverse=True)
    else:  # featured / default
        products = sorted(products, key=lambda x: (not x.get('featured', False), x.get('id', '')))

    # Get unique categories and locations for filter dropdowns
    all_raw_products = data_manager.get_all_products()
    all_categories = sorted(list(set(p.get('category') for p in all_raw_products if p.get('category'))))
    all_locations = sorted(list(set(p.get('location').split(',')[0].strip() for p in all_raw_products if p.get('location'))))

    return render_template(
        'marketplace.html',
        products=products,
        search_query=search_query,
        selected_category=category,
        selected_location=location,
        selected_sort=sort_by,
        max_price=max_price,
        all_categories=all_categories,
        all_locations=all_locations,
        total_found=len(products)
    )


@app.route('/product/<product_id>')
def product_detail(product_id):
    """Detailed view for an individual farm produce with farmer background."""
    product = data_manager.get_product_by_id(product_id)
    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for('marketplace'))

    # Farmer info
    farmer = data_manager.get_user_by_id(product.get('farmer_id'))
    
    # Related products from same farmer or same category
    all_products = data_manager.get_all_products()
    related = [
        p for p in all_products 
        if p.get('id') != product_id and (p.get('farmer_id') == product.get('farmer_id') or p.get('category') == product.get('category'))
    ][:3]

    return render_template('product_detail.html', product=product, farmer=farmer, related_products=related)


@app.route('/about')
def about():
    """Explains FarmDirect's mission, values, and direct impact on farmers."""
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form for consumer support, farmer onboarding, and inquiries."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        role_inquiry = request.form.get('role_inquiry', 'Customer').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            flash("Please fill in all required fields (Name, Email, Message).", "danger")
            return render_template('contact.html')

        data_manager.create_message({
            'name': name,
            'email': email,
            'role_inquiry': role_inquiry,
            'subject': subject,
            'message': message
        })

        flash("Thank you for reaching out! Our agricultural team has received your message and will respond shortly.", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html')


# -------------------------------------------------------------
# AUTHENTICATION (CUSTOMER, FARMER, ADMIN)
# -------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Unified login with instant demo credentials for Customer, Farmer, and Admin."""
    if 'user_id' in session:
        role = session.get('user_role')
        if role == 'farmer':
            return redirect(url_for('farmer_dashboard'))
        elif role == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('marketplace'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        user = data_manager.verify_user(email, password)

        if user:
            # Check if pending farmer
            if user.get('role') == 'farmer' and user.get('status') == 'pending':
                flash("Your farmer profile is currently under review by our agricultural verification team. You can explore the marketplace in the meantime!", "info")

            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_role'] = user['role']
            session['user_email'] = user['email']

            flash(f"Welcome back, {user['name']}!", "success")
            next_url = request.args.get('next')
            if next_url:
                return redirect(next_url)

            if user['role'] == 'farmer':
                return redirect(url_for('farmer_dashboard'))
            elif user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('marketplace'))
        else:
            flash("Invalid email or password. Please verify your credentials.", "danger")

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Allows Customers or Farmers to create an account."""
    if 'user_id' in session:
        return redirect(url_for('index'))

    role_selected = request.args.get('role', 'customer')

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        phone = request.form.get('phone', '').strip()
        role = request.form.get('role', 'customer').strip().lower()

        if not name or not email or not password:
            flash("Please provide all required fields (Name, Email, Password).", "danger")
            return render_template('register.html', role_selected=role)

        user_data = {
            'name': name,
            'email': email,
            'password': password,
            'phone': phone,
            'role': role
        }

        if role == 'farmer':
            user_data['farm_name'] = request.form.get('farm_name', f"{name}'s Farm").strip()
            user_data['location'] = request.form.get('location', '').strip()
            user_data['farming_type'] = request.form.get('farming_type', 'Organic').strip()
            user_data['bio'] = request.form.get('bio', 'Dedicated to cultivating pure, fresh harvest directly for local consumers.').strip()
            user_data['status'] = 'approved'  # Approved for prototype ease of use
        else:
            user_data['address'] = request.form.get('address', '').strip()
            user_data['status'] = 'approved'

        user, err = data_manager.create_user(user_data)
        if err:
            flash(err, "danger")
            return render_template('register.html', role_selected=role)

        # Auto-login after registration
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_role'] = user['role']
        session['user_email'] = user['email']

        flash(f"Account created successfully! Welcome to FarmDirect, {user['name']}.", "success")
        if role == 'farmer':
            return redirect(url_for('farmer_dashboard'))
        return redirect(url_for('marketplace'))

    return render_template('register.html', role_selected=role_selected)


@app.route('/logout')
def logout():
    """Logs out the active user and clears session credentials."""
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_role', None)
    session.pop('user_email', None)
    flash("You have been securely logged out.", "info")
    return redirect(url_for('index'))


# -------------------------------------------------------------
# SHOPPING CART & CHECKOUT
# -------------------------------------------------------------
@app.route('/cart')
def cart():
    """Display shopping cart with items, direct farmer details, and savings."""
    cart_session = session.get('cart', {})
    items = []
    subtotal = 0.0

    products_map = {p['id']: p for p in data_manager.get_all_products()}

    for pid, qty in cart_session.items():
        if pid in products_map:
            p = products_map[pid]
            line_total = float(p.get('price', 0)) * qty
            subtotal += line_total
            items.append({
                'product': p,
                'quantity': qty,
                'line_total': line_total
            })

    # Calculations: Free shipping above ₹300, otherwise ₹30
    delivery_fee = 0 if subtotal >= 300 or subtotal == 0 else 30
    # Estimated middleman savings (traditional retail marks up 35-50%)
    middleman_savings = round(subtotal * 0.35, 2)
    grand_total = subtotal + delivery_fee

    return render_template(
        'cart.html',
        items=items,
        subtotal=round(subtotal, 2),
        delivery_fee=delivery_fee,
        grand_total=round(grand_total, 2),
        middleman_savings=middleman_savings
    )


@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """Add a product to cart (AJAX / Form submission)."""
    product_id = request.form.get('product_id') or (request.json and request.json.get('product_id'))
    quantity = int(request.form.get('quantity') or (request.json and request.json.get('quantity')) or 1)

    product = data_manager.get_product_by_id(product_id)
    if not product:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        flash("Product not found.", "danger")
        return redirect(url_for('marketplace'))

    cart_session = session.get('cart', {})
    current_qty = cart_session.get(product_id, 0)
    new_qty = current_qty + quantity

    # Verify against stock
    stock = int(product.get('stock', 0))
    if new_qty > stock:
        new_qty = stock
        flash(f"Only {stock} units available for {product['title']}.", "warning")

    cart_session[product_id] = new_qty
    session['cart'] = cart_session
    session.modified = True

    if request.is_json:
        return jsonify({
            'success': True,
            'message': f"Added {product['title']} to cart!",
            'cart_count': sum(cart_session.values()),
            'product_name': product['title']
        })

    flash(f"Added {quantity} x {product['title']} to your cart!", "success")
    return redirect(request.referrer or url_for('cart'))


@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    """Update item quantity or remove item from cart."""
    product_id = request.form.get('product_id')
    action = request.form.get('action') # 'increase', 'decrease', 'remove'

    cart_session = session.get('cart', {})
    if product_id in cart_session:
        product = data_manager.get_product_by_id(product_id)
        stock = int(product.get('stock', 99)) if product else 99

        if action == 'increase':
            if cart_session[product_id] < stock:
                cart_session[product_id] += 1
            else:
                flash(f"Maximum available stock reached ({stock}).", "warning")
        elif action == 'decrease':
            cart_session[product_id] -= 1
            if cart_session[product_id] <= 0:
                del cart_session[product_id]
        elif action == 'remove':
            del cart_session[product_id]

    session['cart'] = cart_session
    session.modified = True
    return redirect(url_for('cart'))


@app.route('/api/cart/clear', methods=['POST'])
def clear_cart():
    """Empty the current shopping cart."""
    session['cart'] = {}
    session.modified = True
    flash("Cart cleared.", "info")
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """
    Checkout page with delivery address and realistic payment options:
    - Cash on Delivery
    - Instant UPI QR / ID
    - Credit/Debit Card
    - Net Banking
    """
    cart_session = session.get('cart', {})
    if not cart_session:
        flash("Your cart is empty. Add fresh produce from the marketplace first!", "warning")
        return redirect(url_for('marketplace'))

    products_map = {p['id']: p for p in data_manager.get_all_products()}
    items = []
    subtotal = 0.0

    for pid, qty in cart_session.items():
        if pid in products_map:
            p = products_map[pid]
            line_total = float(p.get('price', 0)) * qty
            subtotal += line_total
            items.append({
                'product_id': p['id'],
                'title': p['title'],
                'price': float(p.get('price', 0)),
                'unit': p.get('unit', '1 kg'),
                'quantity': qty,
                'total': round(line_total, 2),
                'farmer_id': p.get('farmer_id'),
                'farmer_name': p.get('farmer_name', 'Local Farmer'),
                'farm_name': p.get('farm_name', 'Organic Farm')
            })

    delivery_fee = 0 if subtotal >= 300 else 30
    grand_total = round(subtotal + delivery_fee, 2)

    # Pre-fill with user info if logged in
    user_info = {}
    if 'user_id' in session:
        user_info = data_manager.get_user_by_id(session['user_id']) or {}

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        city = request.form.get('city', '').strip()
        pincode = request.form.get('pincode', '').strip()
        notes = request.form.get('notes', '').strip()
        payment_method = request.form.get('payment_method', 'Cash on Delivery')

        if not full_name or not email or not phone or not address:
            flash("Please fill in all required delivery contact and address details.", "danger")
            return render_template('checkout.html', items=items, subtotal=subtotal, delivery_fee=delivery_fee, grand_total=grand_total, user_info=user_info)

        # Build order
        full_address = f"{address}, {city} - {pincode}".strip(" ,-")
        order_data = {
            'customer_id': session.get('user_id', f"guest-{email}"),
            'customer_name': full_name,
            'customer_email': email,
            'customer_phone': phone,
            'delivery_address': full_address,
            'items': items,
            'subtotal': round(subtotal, 2),
            'delivery_fee': delivery_fee,
            'total_amount': grand_total,
            'payment_method': payment_method,
            'payment_status': 'Paid' if payment_method != 'Cash on Delivery' else 'Pending on Delivery',
            'transaction_id': f"TXN-FD-{os.urandom(4).hex().upper()}",
            'notes': notes
        }

        created_order = data_manager.create_order(order_data)

        # Clear shopping cart after successful order
        session['cart'] = {}
        session.modified = True

        flash(f"Order #{created_order['id']} placed successfully! Fresh harvest preparation has begun.", "success")
        return redirect(url_for('order_success', order_id=created_order['id']))

    return render_template(
        'checkout.html',
        items=items,
        subtotal=round(subtotal, 2),
        delivery_fee=delivery_fee,
        grand_total=grand_total,
        user_info=user_info
    )


@app.route('/order-success/<order_id>')
def order_success(order_id):
    """Order confirmation and receipt summary page."""
    order = data_manager.get_order_by_id(order_id)
    if not order:
        flash("Order not found.", "danger")
        return redirect(url_for('index'))
    return render_template('order_success.html', order=order)


# -------------------------------------------------------------
# ORDER TRACKING
# -------------------------------------------------------------
@app.route('/orders')
def orders():
    """View customer order history and active tracking."""
    customer_id = session.get('user_id')
    user_orders = []
    
    if customer_id:
        user_orders = data_manager.get_orders_by_customer(customer_id)
    else:
        # If guest, check if query param provides order_id
        q_order_id = request.args.get('order_id', '').strip()
        if q_order_id:
            single = data_manager.get_order_by_id(q_order_id)
            if single:
                return redirect(url_for('track_order', order_id=single['id']))
            else:
                flash(f"No order found matching ID '{q_order_id}'.", "warning")

    return render_template('orders.html', orders=user_orders)


@app.route('/order/track/<order_id>')
def track_order(order_id):
    """Detailed visual order tracking with timeline steps."""
    order = data_manager.get_order_by_id(order_id)
    if not order:
        flash("Order not found. Please check your order ID.", "danger")
        return redirect(url_for('orders'))

    status_steps = [
        {"key": "Placed", "label": "Order Placed", "desc": "Order verified & payment processed"},
        {"key": "Farmer Confirmed", "label": "Farmer Confirmed", "desc": "Direct farmer received harvest schedule"},
        {"key": "Harvested & Packed", "label": "Harvested & Packed", "desc": "Picked fresh & eco-packaged"},
        {"key": "Out for Delivery", "label": "Out for Delivery", "desc": "Cold-chain express delivery en route"},
        {"key": "Delivered", "label": "Delivered", "desc": "Freshness arrived at your door"}
    ]

    current_idx = 0
    order_status = order.get('order_status', 'Placed')
    step_keys = [s['key'] for s in status_steps]
    if order_status in step_keys:
        current_idx = step_keys.index(order_status)

    return render_template('order_track.html', order=order, status_steps=status_steps, current_idx=current_idx)


# -------------------------------------------------------------
# FARMER DASHBOARD & PRODUCT MANAGEMENT
# -------------------------------------------------------------
@app.route('/farmer/dashboard')
@role_required(['farmer', 'admin'])
def farmer_dashboard():
    """
    Farmer portal:
    - View products & manage stock/pricing
    - View incoming orders containing their produce
    - Quick earnings analytics
    """
    farmer_id = session.get('user_id')
    
    # If admin is checking, allow viewing as first farmer or all
    if session.get('user_role') == 'admin':
        farmers = [u for u in data_manager.get_all_users() if u.get('role') == 'farmer']
        if farmers:
            farmer_id = request.args.get('farmer_id', farmers[0]['id'])

    farmer_user = data_manager.get_user_by_id(farmer_id)
    products = data_manager.get_products_by_farmer(farmer_id)
    orders = data_manager.get_orders_for_farmer(farmer_id)

    # Calculate statistics
    total_revenue = sum(o.get('farmer_subtotal', 0) for o in orders)
    pending_orders_count = sum(1 for o in orders if o.get('order_status') in ['Placed', 'Farmer Confirmed'])
    total_units_sold = sum(
        sum(int(itm.get('quantity', 0)) for itm in o.get('farmer_items', []))
        for o in orders
    )

    stats = {
        'total_products': len(products),
        'total_orders': len(orders),
        'total_revenue': round(total_revenue, 2),
        'pending_orders': pending_orders_count,
        'total_units_sold': total_units_sold
    }

    return render_template(
        'farmer_dashboard.html',
        farmer=farmer_user,
        products=products,
        orders=orders,
        stats=stats
    )


@app.route('/farmer/product/add', methods=['GET', 'POST'])
@role_required(['farmer', 'admin'])
def add_product():
    """Allows a farmer to publish a new fresh crop listing."""
    farmer_id = session.get('user_id')
    farmer = data_manager.get_user_by_id(farmer_id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', 'Vegetables').strip()
        price = float(request.form.get('price', 0))
        unit = request.form.get('unit', '1 kg').strip()
        stock = int(request.form.get('stock', 0))
        harvest_date = request.form.get('harvest_date', 'Harvested Today').strip()
        description = request.form.get('description', '').strip()
        image = request.form.get('image', '').strip()
        is_organic = bool(request.form.get('organic'))

        if not title or price <= 0:
            flash("Please enter a valid product title and price.", "danger")
            return render_template('farmer_product_form.html', action='add')

        product_data = {
            'farmer_id': farmer['id'],
            'farmer_name': farmer['name'],
            'farm_name': farmer.get('farm_name', f"{farmer['name']}'s Farm"),
            'location': farmer.get('location', 'Maharashtra'),
            'title': title,
            'category': category,
            'price': price,
            'unit': unit,
            'stock': stock,
            'harvest_date': harvest_date,
            'organic': is_organic,
            'description': description,
            'image': image
        }

        data_manager.create_product(product_data)
        flash(f"Successfully listed '{title}' on the FarmDirect marketplace!", "success")
        return redirect(url_for('farmer_dashboard'))

    return render_template('farmer_product_form.html', action='add', farmer=farmer)


@app.route('/farmer/product/edit/<product_id>', methods=['GET', 'POST'])
@role_required(['farmer', 'admin'])
def edit_product(product_id):
    """Allows a farmer to edit their product price, stock, and details."""
    product = data_manager.get_product_by_id(product_id)
    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for('farmer_dashboard'))

    # Security check: verify owner unless admin
    if session.get('user_role') != 'admin' and product.get('farmer_id') != session.get('user_id'):
        flash("You are not authorized to edit this product.", "danger")
        return redirect(url_for('farmer_dashboard'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        price = float(request.form.get('price', 0))
        unit = request.form.get('unit', '1 kg').strip()
        stock = int(request.form.get('stock', 0))
        harvest_date = request.form.get('harvest_date', '').strip()
        description = request.form.get('description', '').strip()
        image = request.form.get('image', '').strip()
        is_organic = bool(request.form.get('organic'))

        update_fields = {
            'title': title,
            'category': category,
            'price': price,
            'unit': unit,
            'stock': stock,
            'harvest_date': harvest_date,
            'organic': is_organic,
            'description': description
        }
        if image:
            update_fields['image'] = image

        data_manager.update_product(product_id, update_fields)
        flash(f"Updated '{title}' successfully!", "success")
        return redirect(url_for('farmer_dashboard'))

    return render_template('farmer_product_form.html', action='edit', product=product)


@app.route('/farmer/product/delete/<product_id>', methods=['POST'])
@role_required(['farmer', 'admin'])
def delete_product(product_id):
    """Deletes a product listing."""
    product = data_manager.get_product_by_id(product_id)
    if product:
        if session.get('user_role') != 'admin' and product.get('farmer_id') != session.get('user_id'):
            flash("Unauthorized action.", "danger")
            return redirect(url_for('farmer_dashboard'))

        data_manager.delete_product(product_id)
        flash("Product removed from marketplace.", "info")

    return redirect(url_for('farmer_dashboard'))


@app.route('/farmer/order/update-status', methods=['POST'])
@role_required(['farmer', 'admin'])
def farmer_update_order():
    """Farmer updates progress of an order (e.g. Farmer Confirmed -> Packed -> Shipped)."""
    order_id = request.form.get('order_id')
    new_status = request.form.get('new_status')
    comment = request.form.get('comment', '')

    valid_statuses = ['Placed', 'Farmer Confirmed', 'Harvested & Packed', 'Out for Delivery', 'Delivered']
    if new_status in valid_statuses:
        data_manager.update_order_status(order_id, new_status, comment)
        flash(f"Order #{order_id} status updated to '{new_status}'.", "success")
    else:
        flash("Invalid status selection.", "warning")

    return redirect(request.referrer or url_for('farmer_dashboard'))


# -------------------------------------------------------------
# ADMIN DASHBOARD
# -------------------------------------------------------------
@app.route('/admin/dashboard')
@role_required(['admin'])
def admin_dashboard():
    """
    Master Admin Control Panel:
    - Platform KPIs (Gross sales, order count, registered farmers, customers)
    - Approve/Revoke Farmer accounts
    - View and moderate all products
    - View all customer orders & delivery statuses
    - Customer and Farmer inquiries from contact page
    """
    all_users = data_manager.get_all_users()
    all_products = data_manager.get_all_products()
    all_orders = data_manager.get_all_orders()
    all_messages = data_manager.get_all_messages()

    farmers = [u for u in all_users if u.get('role') == 'farmer']
    customers = [u for u in all_users if u.get('role') == 'customer']

    total_gross_sales = sum(float(o.get('total_amount', 0)) for o in all_orders)
    pending_farmers = [f for f in farmers if f.get('status') == 'pending']

    stats = {
        'total_sales': round(total_gross_sales, 2),
        'total_orders': len(all_orders),
        'farmers_count': len(farmers),
        'customers_count': len(customers),
        'products_count': len(all_products),
        'pending_farmers_count': len(pending_farmers),
        'unread_messages': sum(1 for m in all_messages if m.get('status') == 'unread')
    }

    return render_template(
        'admin_dashboard.html',
        stats=stats,
        farmers=farmers,
        customers=customers,
        products=all_products,
        orders=all_orders,
        messages=all_messages
    )


@app.route('/admin/farmer/status', methods=['POST'])
@role_required(['admin'])
def admin_toggle_farmer():
    """Approve or suspend a farmer."""
    farmer_id = request.form.get('farmer_id')
    new_status = request.form.get('status', 'approved') # 'approved' or 'pending'

    data_manager.update_user_status(farmer_id, new_status)
    flash(f"Farmer status updated to '{new_status}'.", "success")
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/message/read', methods=['POST'])
@role_required(['admin'])
def admin_mark_message():
    """Mark an inquiry message as resolved/read."""
    msg_id = request.form.get('msg_id')
    data_manager.mark_message_read(msg_id)
    flash("Message marked as read.", "info")
    return redirect(url_for('admin_dashboard'))


# -------------------------------------------------------------
# RUN APPLICATION
# -------------------------------------------------------------
if __name__ == '__main__':
    # Initialize JSON files
    data_manager.initialize_database()
    print("=" * 60)
    print(" FarmDirect - Farmer-to-Customer Marketplace")
    print(" Running at: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5000)
