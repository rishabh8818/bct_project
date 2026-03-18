from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import StudentProfile, Book, IssuedBook, Notice, EBook
import re  # Validation ke liye

# 1. Home Page
def index(request):
    return render(request, 'index.html')

# 2. Registration Logic (Strict Validation with English Messages)
def register_view(request):
    error_msg = None
    if request.method == "POST":
        u = request.POST.get('student_id')
        p = request.POST.get('password')
        name = request.POST.get('name')
        roll = request.POST.get('roll')
        branch = request.POST.get('branch')

        # --- VALIDATION CHECKS ---
        # A. Name Check: Only Alphabets and Spaces
        if not all(x.isalpha() or x.isspace() for x in name):
            error_msg = "Please enter alphabets only in Name!"
            
        # B. Roll No Check: Only Numbers
        elif not roll.isdigit():
            error_msg = "Please enter digits only in Roll No!"
            
        # C. Student ID Check: Must start with NIT/202
        elif not u.startswith("NIT/202"):
            error_msg = "Invalid Student ID! Format must start with NIT/202 (e.g., NIT/2024/001)"
            
        # D. User Exist Check
        elif User.objects.filter(username=u).exists():
            error_msg = "Student ID already registered!"
            
        else:
            # Sab sahi hai toh user create karo
            user = User.objects.create_user(username=u, password=p)
            StudentProfile.objects.create(user=user, full_name=name, roll_no=roll, branch=branch)
            return redirect('login_url')
            
    return render(request, 'register.html', {'error': error_msg})

# 3. Login Logic (Role-Based Security Added)
def login_view(request):
    error_msg = None
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        role = request.POST.get('role')  # Dropdown se role uthata hai

        user = authenticate(username=u, password=p)
        
        if user is not None:
            # Check 1: Agar dropdown Admin hai par user Staff nahi
            if role == "Admin" and not user.is_staff:
                error_msg = "Access Denied! You are not an Administrator."
            
            # Check 2: Agar dropdown Student hai par user Admin hai
            elif role == "Student" and user.is_staff:
                error_msg = "Please login as Librarian/Admin from the dropdown."

            else:
                # Sab match hone par login
                login(request, user)
                if user.is_staff:
                    return redirect('/admin/')
                return redirect('dashboard')
        else:
            error_msg = "Invalid ID or Password!"
            
    return render(request, 'login.html', {'error': error_msg})

# 4. Dashboard (Working - Original Logic)
@login_required(login_url='login_url')
def dashboard(request):
    profile = StudentProfile.objects.filter(user=request.user).first()
    full_name = profile.full_name if profile else request.user.username
    
    user_books = IssuedBook.objects.filter(student=request.user).order_by('-issue_date')
    book_data = []
    for b in user_books:
        book_data.append({
            'title': b.book.title,
            'issue_date': b.issue_date,
            'return_date': b.return_date,
            'fine': b.current_fine,
        })
    
    all_notices = Notice.objects.all().order_by('-date_posted')[:5]
    all_ebooks = EBook.objects.all().order_by('-uploaded_on')
    all_vault_books = Book.objects.filter(available_quantity__gt=0)

    context = {
        'full_name': full_name,
        'books': book_data,
        'notices': all_notices,
        'ebooks': all_ebooks,
        'vault_books': all_vault_books
    }
    return render(request, 'dashboard.html', context)

# 5. Notice Page
def notice_view(request):
    all_notices = Notice.objects.all().order_by('-date_posted')
    return render(request, 'notice.html', {'notices': all_notices})

# 6. Rules Page
def rules_view(request):
    return render(request, 'rules.html')

# 7. Logout
def logout_view(request):
    logout(request)
    return redirect('index')