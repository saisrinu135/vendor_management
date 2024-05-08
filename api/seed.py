import random
from datetime import datetime, timedelta
from faker import Faker
from django.utils import timezone
from api.models import Vendor, PurchaseOrder

fake = Faker()
Faker.seed(0)  # Set a seed for consistent results

# Generate fake vendors


class Vendors:
    
    def ponumber():
        number =  f"PO-{fake.uuid4()[:8]}"
        if number not in PurchaseOrder.objects.values_list("po_number", flat=True):
            return number
        else:
            return Vendors.ponumber()
    def vendors():
    # Generate fake purchase orders
        for vendor in Vendor.objects.all():
            for _ in range(random.randint(5, 15)):
                order_date = fake.date_time_between(start_date="-1y", end_date="now", tzinfo=timezone.get_current_timezone())
                delivery_date = order_date + timedelta(days=random.randint(7, 30))
                status = random.choice(["pending", "completed", "canceled"])

                if status == "completed":
                    delivered_date = delivery_date + timedelta(days=random.randint(-5, 5))
                    quality_rating = fake.pyfloat(left_digits=2, right_digits=1, positive=True, min_value=1, max_value=5)
                else:
                    delivered_date = None
                    quality_rating = None

                issue_date = order_date + timedelta(days=random.randint(1, 5))
                acknowledgment_date = issue_date + timedelta(hours=random.randint(1, 24))

                items = [
                    {"name": fake.word(), "price": fake.pyint(min_value=100, max_value=2000)} for _ in range(random.randint(1, 5))
                ]
                quantity = sum(item["price"] for item in items)

                po_number = Vendors.ponumber()
                purchase_order = PurchaseOrder.objects.create(
                    po_number=po_number,
                    vendor=vendor,
                    order_date=order_date,
                    delivery_date=delivery_date,
                    delivered_date=delivered_date,
                    items=items,
                    quantity=quantity,
                    status=status,
                    quality_rating=quality_rating,
                    issue_date=issue_date,
                    acknowledgment_date=acknowledgment_date,
                )
