from django.shortcuts import render
from django.http import HttpResponse
from .models import FruitPrice
from .forms import FruitPriceForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.utils.dateformat import format as date_format
from datetime import date, datetime
import os

def add_price(request):
    filter_date = request.GET.get('filter_date', str(date.today()))
    prices = FruitPrice.objects.filter(date=filter_date)

    if request.method == 'POST':
        form = FruitPriceForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['date']
            # Save default fruits
            for fruit in FruitPriceForm.FRUIT_NAMES:
                price_key = f'price_{fruit.lower().replace(" ", "_")}'
                unit_key = f'unit_{fruit.lower().replace(" ", "_")}'
                price = form.cleaned_data.get(price_key)
                unit = form.cleaned_data.get(unit_key)
                if price and unit:
                    FruitPrice.objects.update_or_create(
                        date=selected_date,
                        fruit_name=fruit,
                        defaults={'price': price, 'unit': unit}
                    )

            # Save multiple custom fruits
            custom_fruits = zip(
                request.POST.getlist('custom_fruit_name[]'),
                request.POST.getlist('custom_price[]'),
                request.POST.getlist('custom_unit[]')
            )
            for name, price, unit in custom_fruits:
                if name and price and unit:
                    FruitPrice.objects.update_or_create(
                        date=selected_date,
                        fruit_name=name,
                        defaults={'price': float(price), 'unit': unit}
                    )

            return render(request, 'prices/add_price.html', {
                'form': FruitPriceForm(),
                'message': 'Prices added!',
                'prices': prices,
                'filter_date': filter_date,
                'today': date.today()
            })
    else:
        form = FruitPriceForm()

    return render(request, 'prices/add_price.html', {
        'form': form,
        'prices': prices,
        'filter_date': filter_date,
        'today': date.today()
    })

def export_pdf(request):
    # Convert filter_date string to date object
    filter_date_str = request.GET.get('filter_date', str(date.today()))
    filter_date = datetime.strptime(filter_date_str, '%Y-%m-%d').date() if filter_date_str else date.today()
    prices = FruitPrice.objects.filter(date=filter_date)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="fresh_harvest_prices.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Letterhead
    logo_path = os.path.join(BASE_DIR, 'static', 'prices', 'fresh_harvest_logo.png')
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        p.drawImage(logo, 50, 700, width=100, height=100)
    else:
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, 700, "Logo Not Found")
    p.setFont("Helvetica-Bold", 16)
    p.drawString(160, 750, "Fresh Harvest")
    p.setFont("Helvetica", 10)
    p.drawString(160, 735, "Wholesale Fruits Supplier")
    p.drawString(160, 720, "Contact: freshharvest.hyd@gmail.com | Phone: +91 84669 87644")
    p.line(50, 710, 550, 710)

    # Title
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 680, f"Price List for {date_format(filter_date, 'd-m-Y')}")

    # Table Headers with Background
    y = 650
    p.setFillColorRGB(0.28, 0.67, 0.31)  # Green background
    p.rect(50, y-10, 470, 20, fill=1, stroke=1)  # Adjusted width, added stroke
    p.setFillColorRGB(1, 1, 1)  # White text
    p.setFont("Helvetica-Bold", 12)
    p.drawString(60, y-2, "Date")  # Adjusted x for alignment
    p.drawString(130, y-2, "Fruit Name")  # Adjusted x
    p.drawString(250, y-2, "Price (Rs)")  # Adjusted x
    p.drawString(350, y-2, "Unit")  # Adjusted x
    p.setFillColorRGB(0, 0, 0)  # Black text for data

    # Table Data with Borders
    y -= 18
    p.setFont("Helvetica", 10)
    for price in prices:
        p.rect(50, y-7, 470, 15, fill=0, stroke=1)  # Adjusted width
        p.drawString(60, y-2, date_format(price.date, 'd-m-Y'))  # Aligned
        p.drawString(130, y-2, price.fruit_name)  # Aligned
        p.drawString(250, y-2, f"Rs {price.price}")  # Aligned
        p.drawString(350, y-2, price.unit)  # Aligned
        y -= 15
        if y < 50:
            p.showPage()
            y = 750
            if os.path.exists(logo_path):
                p.drawImage(logo, 50, 700, width=100, height=100)
            p.setFont("Helvetica-Bold", 16)
            p.drawString(160, 750, "Fresh Harvest")
            p.setFont("Helvetica", 10)
            p.drawString(160, 735, "Wholesale Fruits Supplier")
            p.drawString(160, 720, "Contact: freshharvest.hyd@gmail.com | Phone: +91 84669 87644")
            p.line(50, 710, 550, 710)
            p.setFont("Helvetica-Bold", 14)
            p.drawString(50, 680, f"Price List for {date_format(filter_date, 'd-m-Y')}")
            y = 650
            p.setFillColorRGB(0.28, 0.67, 0.31)
            p.rect(50, y-10, 470, 20, fill=1, stroke=1)
            p.setFillColorRGB(1, 1, 1)
            p.setFont("Helvetica-Bold", 12)
            p.drawString(60, y-2, "Date")
            p.drawString(130, y-2, "Fruit Name")
            p.drawString(250, y-2, "Price (Rs)")
            p.drawString(350, y-2, "Unit")
            p.setFillColorRGB(0, 0, 0)
            p.line(50, y-10, 550, y-10)
            y -= 20
            p.setFont("Helvetica", 10)

    p.showPage()
    p.save()
    return response