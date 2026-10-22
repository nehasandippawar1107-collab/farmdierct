import unittest
import json
import os
import app
import data_manager

class FarmDirectTestCase(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.app.test_client()
        data_manager.initialize_database()

    def test_01_homepage(self):
        """Verify home page loads with clean green theme and featured products."""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        content = res.get_data(as_text=True)
        self.assertIn("FarmDirect", content)
        self.assertIn("Farm Fresh Harvest", content)
        self.assertIn("Browse Marketplace", content)

    def test_02_marketplace_and_filters(self):
        """Verify marketplace, category filtering, and search functionality."""
        # General marketplace
        res = self.client.get('/marketplace')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Farm Fresh Marketplace", res.get_data(as_text=True))

        # Search filter for tomatoes
        res_search = self.client.get('/marketplace?q=tomatoes')
        self.assertEqual(res_search.status_code, 200)
        self.assertIn("Tomatoes", res_search.get_data(as_text=True))

        # Category filter for Fruits
        res_cat = self.client.get('/marketplace?category=Fruits')
        self.assertEqual(res_cat.status_code, 200)
        self.assertIn("Apples", res_cat.get_data(as_text=True))

    def test_03_cart_and_checkout_flow(self):
        """Test adding item to cart, viewing cart, and placing an order with UPI payment."""
        # 1. Add product to cart via API
        prod = data_manager.get_all_products()[0]
        initial_stock = prod['stock']

        res_add = self.client.post('/api/cart/add', data={
            'product_id': prod['id'],
            'quantity': 2
        }, follow_redirects=True)
        self.assertEqual(res_add.status_code, 200)

        # 2. View Cart
        res_cart = self.client.get('/cart')
        self.assertEqual(res_cart.status_code, 200)
        cart_content = res_cart.get_data(as_text=True)
        self.assertIn(prod['title'], cart_content)
        self.assertIn("Order Summary", cart_content)
        self.assertIn("You saved approx.", cart_content)

        # 3. Checkout with UPI payment option
        res_checkout = self.client.post('/checkout', data={
            'full_name': 'Test Shopper',
            'email': 'shopper@test.com',
            'phone': '+91 99999 11111',
            'address': 'Plot 10, Green Meadows',
            'city': 'Pune',
            'pincode': '411001',
            'notes': 'Please call before arrival',
            'payment_method': 'UPI (Google Pay)'
        }, follow_redirects=True)
        self.assertEqual(res_checkout.status_code, 200)
        checkout_content = res_checkout.get_data(as_text=True)
        self.assertIn("Order Placed Successfully", checkout_content)
        self.assertIn("UPI (Google Pay)", checkout_content)

        # Verify stock was deducted
        updated_prod = data_manager.get_product_by_id(prod['id'])
        self.assertEqual(updated_prod['stock'], initial_stock - 2)

    def test_04_order_tracking(self):
        """Verify order tracking stepper and history."""
        orders = data_manager.get_all_orders()
        self.assertTrue(len(orders) > 0)
        sample_order = orders[0]

        res = self.client.get(f"/order/track/{sample_order['id']}")
        self.assertEqual(res.status_code, 200)
        content = res.get_data(as_text=True)
        self.assertIn(sample_order['id'], content)
        self.assertIn("tracking-stepper", content)
        self.assertIn("Order Placed", content)

    def test_05_farmer_dashboard_and_product_crud(self):
        """Verify farmer login, dashboard access, and status updates."""
        # Farmer login
        login_res = self.client.post('/login', data={
            'email': 'ramesh@farmdirect.com',
            'password': 'farmer123'
        }, follow_redirects=True)
        self.assertEqual(login_res.status_code, 200)
        self.assertIn("Farmer Dashboard", login_res.get_data(as_text=True))

        # Check farmer dashboard
        dash_res = self.client.get('/farmer/dashboard')
        self.assertEqual(dash_res.status_code, 200)
        self.assertIn("My Produce Catalog", dash_res.get_data(as_text=True))

        # Add a new produce item
        add_res = self.client.post('/farmer/product/add', data={
            'title': 'Crisp Organic Cucumbers',
            'category': 'Vegetables',
            'price': 30,
            'unit': '1 kg',
            'stock': 40,
            'harvest_date': 'Harvested Today Morning',
            'description': 'Farm fresh crisp cucumbers grown without chemical sprays.',
            'image': 'https://images.unsplash.com/photo-1590165482129-1b8b27698780?w=600&auto=format&fit=crop&q=80',
            'organic': '1'
        }, follow_redirects=True)
        self.assertEqual(add_res.status_code, 200)
        self.assertIn("Crisp Organic Cucumbers", add_res.get_data(as_text=True))

    def test_06_admin_dashboard_and_approvals(self):
        """Verify admin login, platform statistics, and farmer approval toggle."""
        # Admin login
        login_res = self.client.post('/login', data={
            'email': 'admin@farmdirect.com',
            'password': 'admin123'
        }, follow_redirects=True)
        self.assertEqual(login_res.status_code, 200)

        # Access admin dashboard
        res = self.client.get('/admin/dashboard')
        self.assertEqual(res.status_code, 200)
        admin_content = res.get_data(as_text=True)
        self.assertIn("Platform Master Administration", admin_content)
        self.assertIn("Total Platform GMV", admin_content)

        # Approve farmer Anand Verma
        anand = [u for u in data_manager.get_all_users() if u.get('email') == 'anand@farmdirect.com'][0]
        res_approve = self.client.post('/admin/farmer/status', data={
            'farmer_id': anand['id'],
            'status': 'approved'
        }, follow_redirects=True)
        self.assertEqual(res_approve.status_code, 200)
        updated_anand = data_manager.get_user_by_id(anand['id'])
        self.assertEqual(updated_anand['status'], 'approved')

    def test_07_contact_submission(self):
        """Verify contact form submission saves inquiry in messages.json."""
        res = self.client.post('/contact', data={
            'name': 'Suresh Kumar',
            'email': 'suresh@example.com',
            'role_inquiry': 'Farmer',
            'subject': 'Partnering with my pomegranate orchard',
            'message': 'Hello, I have 10 acres of Bhagwa pomegranates in Solapur and want to list on FarmDirect.'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Thank you for reaching out", res.get_data(as_text=True))

        messages = data_manager.get_all_messages()
        self.assertTrue(any(m['name'] == 'Suresh Kumar' for m in messages))

if __name__ == '__main__':
    unittest.main()
