"""
Django management command to seed the database with demo data.
This creates sample clients, products, sales, and sale items for testing.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import models
from demo_app.models import Client, Product, Sale, SaleItem
from datetime import datetime, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with demo data for ERP Framework Demo'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed demo data...'))
        
        # Create or get admin user
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@demo.com',
                'is_superuser': True,
                'is_staff': True,
                'is_active': True
            }
        )
        
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user: admin/admin123'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
        
        # Create demo user
        demo_user, _ = User.objects.get_or_create(
            username='demo_user',
            defaults={
                'email': 'demo@demo.com',
                'is_staff': True,
                'is_active': True
            }
        )
        if demo_user.password == '':
            demo_user.set_password('demo123')
            demo_user.save()
        
        # Client names and data
        client_data = [
            {'name': 'Acme Corporation', 'email': 'sales@acme.com', 'phone': '+1-555-0101'},
            {'name': 'Globex Inc', 'email': 'contact@globex.com', 'phone': '+1-555-0102'},
            {'name': 'Wayne Enterprises', 'email': 'info@wayne.com', 'phone': '+1-555-0103'},
            {'name': 'Stark Industries', 'email': 'support@stark.com', 'phone': '+1-555-0104'},
            {'name': 'Initech', 'email': 'hello@initech.com', 'phone': '+1-555-0105'},
        ]
        
        # Create clients
        self.stdout.write(self.style.HTTP_INFO('Creating clients...'))
        clients = []
        for client_info in client_data:
            client, created = Client.objects.get_or_create(
                name=client_info['name'],
                defaults={
                    'email': client_info['email'],
                    'phone': client_info['phone'],
                    'address': f"{client_info['name']} HQ, Business District",
                    'notes': f"Demo client - {client_info['name']}",
                    'owner': user,
                    'lastmod_user': user
                }
            )
            clients.append(client)
            if created:
                self.stdout.write(f"  Created: {client.name}")
        
        # Product data
        product_data = [
            {'name': 'Laptop Pro X', 'code': 'PROD001', 'price': 1200.00, 'stock': 50, 'category': 'Electronics'},
            {'name': 'Wireless Mouse', 'code': 'PROD002', 'price': 45.99, 'stock': 200, 'category': 'Accessories'},
            {'name': 'Mechanical Keyboard', 'code': 'PROD003', 'price': 120.00, 'stock': 150, 'category': 'Accessories'},
            {'name': '4K Monitor', 'code': 'PROD004', 'price': 650.00, 'stock': 75, 'category': 'Electronics'},
            {'name': 'Noise Cancelling Headphones', 'code': 'PROD005', 'price': 250.00, 'stock': 100, 'category': 'Electronics'},
            {'name': 'Desk Lamp', 'code': 'PROD006', 'price': 35.50, 'stock': 300, 'category': 'Accessories'},
            {'name': 'Office Chair', 'code': 'PROD007', 'price': 280.00, 'stock': 60, 'category': 'Furniture'},
            {'name': 'Webcam HD', 'code': 'PROD008', 'price': 85.00, 'stock': 120, 'category': 'Electronics'},
        ]
        
        # Create products
        self.stdout.write(self.style.HTTP_INFO('Creating products...'))
        products = []
        for product_info in product_data:
            product, created = Product.objects.get_or_create(
                name=product_info['name'],
                defaults={
                    'code': product_info['code'],
                    'price': product_info['price'],
                    'stock': product_info['stock'],
                    'category': product_info['category'],
                    'notes': f"Demo product - {product_info['name']}",
                    'owner': user,
                    'lastmod_user': user
                }
            )
            products.append(product)
            if created:
                self.stdout.write(f"  Created: {product.name} (${product.price})")
        
        # Create sales (10-15 sales)
        self.stdout.write(self.style.HTTP_INFO('Creating sales...'))
        num_sales = random.randint(10, 15)
        sales = []
        for i in range(1, num_sales + 1):
            sale_date = datetime.now() - timedelta(days=random.randint(1, 90))
            client = random.choice(clients)
            
            sale, created = Sale.objects.get_or_create(
                slug=f'SALE{i:04d}',
                defaults={
                    'date': sale_date,
                    'client': client,
                    'notes': f'Demo sale #{i} for {client.name}',
                    'owner': user,
                    'lastmod_user': user
                }
            )
            sales.append(sale)
            if created:
                self.stdout.write(f"  Created: Sale #{sale.slug} for {client.name}")
            
            # Create sale items (1-4 items per sale)
            num_items = random.randint(1, 4)
            for j in range(num_items):
                product = random.choice(products)
                quantity = random.randint(1, 5)
                discount = random.choice([0, 5, 10, 15, 20])
                
                # Check if this item already exists for this sale
                existing_item = SaleItem.objects.filter(
                    sale=sale,
                    product=product
                ).first()
                
                if not existing_item:
                    SaleItem.objects.create(
                        sale=sale,
                        product=product,
                        quantity=quantity,
                        price=product.price,
                        discount=discount,
                        owner=user,
                        lastmod_user=user
                    )
        
        # Update product stock based on sales
        self.stdout.write(self.style.HTTP_INFO('Updating product stock...'))
        for product in products:
            # Calculate total sold
            total_sold = SaleItem.objects.filter(product=product).aggregate(
                total_quantity=models.Sum('quantity')
            )['total_quantity'] or 0
            
            # Update stock
            product.stock = max(0, product.stock - total_sold)
            product.save()
        
        # Print summary
        self.stdout.write(self.style.SUCCESS('\n--- Demo Data Summary ---'))
        self.stdout.write(f"Users: {User.objects.count()}")
        self.stdout.write(f"Clients: {Client.objects.count()}")
        self.stdout.write(f"Products: {Product.objects.count()}")
        self.stdout.write(f"Sales: {Sale.objects.count()}")
        self.stdout.write(f"Sale Items: {SaleItem.objects.count()}")
        
        # Print access info
        self.stdout.write(self.style.SUCCESS('\n--- Access Information ---'))
        self.stdout.write('Admin URL: http://localhost:8000/admin/')
        self.stdout.write('ERP System URL: http://localhost:8000/erp-system/')
        self.stdout.write('Username: admin')
        self.stdout.write('Password: admin123')
        
        self.stdout.write(self.style.SUCCESS('\nDemo data seeded successfully!'))
