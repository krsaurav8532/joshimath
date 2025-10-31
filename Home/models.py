from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
import random
from django.core.exceptions import ValidationError
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
import re

def generate_pass_id():
    return random.randint(100000, 999999)  # 6-digit random number

# Stop words for SEO-friendly slugs
STOP_WORDS = {'and', 'the', 'of', 'in', 'to', 'for', 'with'}

def clean_slug_words(title):
    return ' '.join(word for word in title.split() if word.lower() not in STOP_WORDS)

class Event(models.Model):
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='event_thumbnails/')
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        # Temporarily save to get the ID
        if is_new:
            super().save(*args, **kwargs)
            base_slug = slugify(clean_slug_words(self.title))[:50]
            self.slug = f"{base_slug}-{self.id}"
            kwargs["force_insert"] = False  # avoid insert error on second save

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('Home:event_detail', kwargs={'slug': self.slug})


class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images/')

    def __str__(self):
        return f"Image for {self.event.title}"


class Announcement(models.Model):
    keywords = models.CharField(max_length=50, blank=True, null=True, default='announcement')
    title = models.CharField(max_length=100)
    content = models.TextField()
    location = models.CharField(max_length=200, blank=True, null=True, default='Joshimath')
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            base_slug = slugify(clean_slug_words(self.title))[:50]
            self.slug = f"{base_slug}-{self.id}"
            kwargs["force_insert"] = False
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('Home:announcement_detail', kwargs={'slug': self.slug})

class AnnouncementImage(models.Model):
    announcement = models.ForeignKey(Announcement, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='announcement_images/') 
    def __str__(self):
        return f"Image for {self.announcement.title}"
        

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)        
    def __str__(self):
        return f"Contact from {self.name} on {self.date_submitted.strftime('%Y-%m-%d %H:%M:%S')}"
    def get_absolute_url(self):
        return reverse('contact_detail', kwargs={'pk': self.pk})
    

#Resources
class StotraCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  

        super().save(*args, **kwargs)
        

    def __str__(self):
        return self.name    
    

class Stotra(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(StotraCategory, related_name='stotras', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        # Temporarily save to get the ID
        if is_new:
            super().save(*args, **kwargs)
            base_slug = slugify(clean_slug_words(self.title))[:50]
            self.slug = f"{base_slug}"
            kwargs["force_insert"] = False  # avoid insert error on second save

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('stotra_detail', kwargs={'slug': self.slug})
    

class Carausel(models.Model):
    image = models.ImageField(upload_to='carasoul_images/')
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"
    
    
class Branches(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)


    def __str__(self):
        return self.name
    

#Jooja Booking 
class Puja(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()

    
    def __str__(self):
        return f"{self.name} (₹{self.price})"

class Priest(models.Model):
    name = models.CharField(max_length=100)
    available_pujas = models.ManyToManyField(Puja)

    def __str__(self):
        return self.name
    

class Booking(models.Model):
    puja = models.ForeignKey(Puja, on_delete=models.CASCADE)
    priest = models.ForeignKey(Priest, on_delete=models.SET_NULL, null=True, blank=True)
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    user_phone = PhoneNumberField(max_length=15, region='IN')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed')], default='Pending')


class Epass(models.Model):
    id = models.PositiveIntegerField(primary_key=True, default=generate_pass_id, editable=False, max_length=10, unique=True)
    name = models.CharField()
    number_of_people = models.PositiveIntegerField()
    date_of_visit = models.DateField()
    contact_number = PhoneNumberField(max_length=15, region='IN')
    email = models.EmailField()
    purpose = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"E-Pass {self.id} - {self.name}"
    
    def clean(self):
        if self.date_of_visit < timezone.now().date():
            raise ValidationError("You cannot book an E-pass for a past date.")
        



# Optional: emoji remover if you plan to use emojis in text
EMOJI_PATTERN = re.compile(
    "[" 
    u"\U0001F300-\U0001F5FF"
    u"\U0001F600-\U0001F64F"
    u"\U0001F680-\U0001F6FF"
    u"\U0001F700-\U0001F77F"
    u"\U0001F780-\U0001F7FF"
    u"\U0001F800-\U0001F8FF"
    u"\U0001F900-\U0001F9FF"
    u"\U0001FA00-\U0001FA6F"
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    "]+", flags=re.UNICODE
)

def generate_epass_image(Epass):
    # Canvas
    img_w, img_h = 700, 450
    img = Image.new("RGB", (img_w, img_h), color=(255, 248, 220))  # cream
    draw = ImageDraw.Draw(img)

    # Border
    draw.rectangle([(10, 10), (img_w - 10, img_h - 10)], outline=(218,165,32), width=6)

    # Fonts
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except Exception:
        try:
            title_font = ImageFont.truetype("arial.ttf", 24)
            text_font = ImageFont.truetype("arial.ttf", 20)
        except Exception:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

    # --- Logo Top-Left ---
    logo_x, logo_y, logo_width = 20, 20, 0  # defaults if logo missing
    try:
        logo_path = "static/images/logo.jpg"  # PNG recommended
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((60, 60))
        logo_width = logo.width
        img.paste(logo, (logo_x, logo_y), logo)
    except Exception as e:
        print("Logo error:", e) 

    # --- Title Next to Logo ---
    title_text = "Shree BodhGaya Math E-Pass"
    title_x = logo_x + logo_width + 30  # safe even if logo missing
    draw.text((title_x, logo_y + 10), title_text, fill=(128,0,0), font=title_font)

    # --- Visitor Details (Left) ---
    left_x = 80
    top_y = 120
    spacing = 36
    draw.text((left_x, top_y + spacing * 0), f"E-Pass ID: {Epass.id}", font=text_font, fill=(0,0,0))
    draw.text((left_x, top_y + spacing * 1), f"Name: {Epass.name}", font=text_font, fill=(0,0,0))
    draw.text((left_x, top_y + spacing * 2), f"Date: {Epass.date_of_visit}", font=text_font, fill=(0,0,0))
    draw.text((left_x, top_y + spacing * 3), f"Visitors: {Epass.number_of_people}", font=text_font, fill=(0,0,0))

    # --- QR Code (Right) ---
    qr = qrcode.make(str(Epass.id))
    qr_size = 180
    qr = qr.resize((qr_size, qr_size))
    qr_x = img_w - qr_size - 80
    qr_y = top_y
    img.paste(qr, (qr_x, qr_y))

    # --- Footer Centered ---
    footer_text = "Valid only on selected date • Jai Shri Ram 🙏"
    bbox = draw.textbbox((0,0), footer_text, font=text_font)
    footer_width = bbox[2] - bbox[0]
    footer_x = (img_w - footer_width) // 2
    draw.text((footer_x, img_h - 60), footer_text, fill=(128,0,0), font=text_font)

    # Save Image
    folder = "media/epasses"
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"epass_{str(Epass.id)}.png")
    img.save(filename)

    return filename

# def generate_epass_image(Epass):
#     # Create blank image
#     img = Image.new("RGB", (600, 400), color=(255, 248, 220))
#     draw = ImageDraw.Draw(img)
    

#     # Fonts (use system TTF)
#     font_title = ImageFont.truetype("arial.ttf", 20)
#     font_text = ImageFont.truetype("arial.ttf", 20)
#     draw.rectangle([(10, 10), (590, 390)], outline=(218,165,32), width=5)  # golden border

#     # Add Temple Name
#     # draw.text((200, 20), "🌸 Shree BodhGaya Math E-Pass 🌸", fill=(128,0,0), font=font_title)
#     title_text = "🌸 Shree BodhGaya Math E-Pass 🌸"
#     image_width = 600

#     # Measure text width with bounding box (more accurate than textsize)
#     bbox = draw.textbbox((0, 0), title_text, font=font_title)
#     text_width = bbox[2] - bbox[0]

#     # Calculate x so that text is centered
#     x_position = (image_width - text_width) // 2

#     # Draw text in center
#     draw.text((x_position, 30), title_text, fill=(128,0,0), font=font_title)


#     # Add E-pass details
#     draw.text((50, 100), f"E-Pass ID: {Epass.id}", fill="black", font=font_text)
#     draw.text((50, 140), f"Name: {Epass.name}", fill="black", font=font_text)
#     draw.text((50, 180), f"Date: {Epass.date_of_visit}", fill="black", font=font_text)
#     draw.text((50, 260), f"Visitors: {Epass.number_of_people}", fill="black", font=font_text)

#     # Generate QR Code
#     qr = qrcode.make(f"E-pass ID: {Epass.id}")
#     qr = qr.resize((120, 120))
#     img.paste(qr, (450, 250))

#     # Save image
#     folder = "media/epasses"
#     os.makedirs(folder, exist_ok=True)
#     filename = f"{folder}/epass_{str(Epass.id)}.png"
#     img.save(filename)

#     return filename
