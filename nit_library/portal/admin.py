from django.contrib import admin
from .models import Book, StudentProfile, IssuedBook, FineCollection, Notice, EBook
from datetime import date

# Portal 1: Book List & Inventory (SAME)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'available_quantity', 'total_quantity')
    list_editable = ('available_quantity', 'total_quantity')
    search_fields = ('title',)

# Portal 2: Student Details (SAME)
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'roll_no', 'branch')
    search_fields = ('full_name', 'roll_no')

# Portal 3: Issue/Return Book (SAME LOGIC)
@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'issue_date', 'return_date', 'is_returned', 'get_fine')
    raw_id_fields = ('student', 'book')
    list_filter = ('is_returned',)

    def get_fine(self, obj):
        return f"₹{obj.current_fine}"
    get_fine.short_description = "Calculated Fine"

    def save_model(self, request, obj, form, change):
        # Automatic Stock Update
        if not change: # Fresh Issue
            obj.book.available_quantity -= 1
            obj.book.save()
        
        if change and obj.is_returned: # Returning Book
            orig = IssuedBook.objects.get(pk=obj.pk)
            if not orig.is_returned:
                obj.return_date = date.today() # Auto-fill return date
                obj.book.available_quantity += 1
                obj.book.save()
        super().save_model(request, obj, form, change)

# Portal 4: Fine Collector (SAME)
@admin.register(FineCollection)
class FineAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount_paid', 'payment_date', 'received_by')
    search_fields = ('student__roll_no',)

# --- NAYE FEATURES (ADMIN SE PUBLISH KARNE KE LIYE) ---

# Portal 5: Library Notifications
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted')
    search_fields = ('title', 'content')

# Portal 6: E-Book Management
@admin.register(EBook)
class EBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'uploaded_on')
    search_fields = ('title', 'author')