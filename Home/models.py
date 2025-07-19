from django.db import models
from django.utils.text import slugify
from django.urls import reverse

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
    
    
