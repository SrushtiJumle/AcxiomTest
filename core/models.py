from django.db import models
from datetime import date, timedelta

class Membership(models.Model):
    DURATION_CHOICES = [
        ('6m', '6 Months'),
        ('1y', '1 Year'),
        ('2y', '2 Years'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Cancelled', 'Cancelled'),
    ]

    membership_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    start_date = models.DateField(default=date.today)
    end_date = models.DateField()
    duration = models.CharField(max_length=2, choices=DURATION_CHOICES, default='6m')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def save(self, *args, **kwargs):
        if not self.end_date:
            if self.duration == '6m':
                self.end_date = self.start_date + timedelta(days=30*6)
            elif self.duration == '1y':
                self.end_date = self.start_date + timedelta(days=365)
            elif self.duration == '2y':
                self.end_date = self.start_date + timedelta(days=365*2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.membership_number} - {self.first_name} {self.last_name}"

class Book(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Issued', 'Issued'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return f"{self.title} ({self.isbn})"

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('Issued', 'Issued'),
        ('Returned', 'Returned'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Membership, on_delete=models.CASCADE)
    issue_date = models.DateField(default=date.today)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Issued')

    def __str__(self):
        return f"{self.book.title} - {self.member.membership_number}"
