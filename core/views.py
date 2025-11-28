from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Membership, Book, Transaction
from .forms import MembershipForm, UpdateMembershipForm, IssueBookForm, ReturnBookForm, AddBookForm
from datetime import timedelta, date

def is_admin(user):
    return user.groups.filter(name='Admin').exists() or user.is_superuser

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
@user_passes_test(is_admin)
def maintenance(request):
    return render(request, 'maintenance/maintenance.html')

@login_required
@user_passes_test(is_admin)
def add_membership(request):
    if request.method == 'POST':
        form = MembershipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('update_membership')
    else:
        form = MembershipForm(initial={'duration': '6m'})
    return render(request, 'maintenance/add_membership.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def update_membership(request):
    membership = None
    message = ""
    if 'search' in request.GET:
        membership_number = request.GET.get('membership_number')
        try:
            membership = Membership.objects.get(membership_number=membership_number)
        except Membership.DoesNotExist:
            message = "Membership not found."

    if request.method == 'POST':
        membership_number = request.POST.get('membership_number_hidden')
        membership = get_object_or_404(Membership, membership_number=membership_number)
        
        if 'extend' in request.POST:
            membership.end_date += timedelta(days=30*6)
            membership.status = 'Active'
            membership.save()
            message = "Membership extended by 6 months."
        elif 'cancel' in request.POST:
            membership.status = 'Cancelled'
            membership.save()
            message = "Membership cancelled."
            
    return render(request, 'maintenance/update_membership.html', {'membership': membership, 'message': message})

@login_required
def reports(request):
    memberships = Membership.objects.all()
    return render(request, 'reports.html', {'memberships': memberships})

@login_required
def transactions(request):
    return render(request, 'transactions.html')

@login_required
def issue_book(request):
    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']
            member = form.cleaned_data['membership_number']
            
            # Create Transaction
            Transaction.objects.create(book=book, member=member)
            
            # Update Book Status
            book.status = 'Issued'
            book.save()
            
            return redirect('transactions')
    else:
        form = IssueBookForm()
    return render(request, 'transactions/issue_book.html', {'form': form})

@login_required
def return_book(request):
    message = ""
    if request.method == 'POST':
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            isbn = form.cleaned_data['book_isbn']
            try:
                book = Book.objects.get(isbn=isbn)
                if book.status == 'Issued':
                    transaction = Transaction.objects.filter(book=book, status='Issued').last()
                    if transaction:
                        transaction.return_date = date.today()
                        transaction.status = 'Returned'
                        transaction.save()
                        
                        book.status = 'Available'
                        book.save()
                        message = "Book returned successfully."
                    else:
                        message = "No active transaction found for this book."
                else:
                    message = "This book is not currently issued."
            except Book.DoesNotExist:
                message = "Book not found."
    else:
        form = ReturnBookForm()
    return render(request, 'transactions/return_book.html', {'form': form, 'message': message})

@login_required
@user_passes_test(is_admin)
def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance')
    else:
        form = AddBookForm()
    return render(request, 'maintenance/add_book.html', {'form': form})


