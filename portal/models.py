from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.core.exceptions import ValidationError

# 1. Book Model
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    total_quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    def __str__(self): return self.title

# 2. Student Profile
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=50, unique=True)
    branch = models.CharField(max_length=50)
    def __str__(self): return f"{self.full_name} ({self.roll_no})"

# 3. Issued Book (With Fine & Auto-Date & Blocking)
class IssuedBook(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=date.today)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    
    @property
    def current_fine(self):
        if not self.is_returned and self.return_date:
            today = date.today()
            if today > self.return_date:
                return (today - self.return_date).days * 5 # ₹5 per day fine
        return 0

    def clean(self):
        # Auto Return Date: Issue date + 14 days
        if not self.return_date and self.issue_date:
            self.return_date = self.issue_date + timedelta(days=14)
        
        # Blocking Logic: Don't issue new book if fine exists
        if not self.pk:
            active_issues = IssuedBook.objects.filter(student=self.student, is_returned=False)
            for issue in active_issues:
                if issue.current_fine > 0:
                    raise ValidationError(f"Fine Pending! Student has ₹{issue.current_fine} fine on '{issue.book.title}'.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

# 4. NEW: Notice Model
class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

# 5. NEW: E-Book Model
class EBook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    file_link = models.URLField(help_text="Paste PDF Link here")
    uploaded_on = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

# 6. Fine Collection
class FineCollection(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    received_by = models.CharField(max_length=100)