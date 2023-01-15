import random
import string
from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template import loader
from django.utils import timezone

from .forms import BranchForm
from .models import *


def password_generator():
    res = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=6))
    return res


def home_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        reg_no = request.POST.get('reg_no')
        branch_name = request.POST.get('branch')
        message = request.POST.get('message')
        branch = Branch.objects.get(branch_name=branch_name)
        date_time = datetime.now(tz=timezone.utc)
        ticket_counter = Ticket_counter.objects.get_or_create(date=date_time.date())[0]
        ticket_count = (ticket_counter.count_number + 1)
        ticket_count_str = format(ticket_count, '05d')
        ticket_no = branch.branch_code + str(date_time.year) + str(date_time.day) + str(ticket_count_str)
        Ticket(ticket_no=ticket_no, email=email, full_name=full_name, reg_no=reg_no, branch_name=branch, complaint=message, ticket_status="unsolved",
               date_time=date_time).save()
        ticket_counter.count_number = ticket_count
        ticket_counter.save()
        html_message = loader.render_to_string('emails/complaint.html', {'ticket_no': ticket_no, 'message': message})
        send_mail('Complaint', '', settings.EMAIL_HOST_USER, [email], html_message=html_message, fail_silently=False)
        return render(request, 'thank_you.html', {'ticket_no': ticket_no})
    branches = Branch.objects.values_list("branch_name", flat=True).distinct()
    return render(request, 'home_page.html', {'branches': branches})


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_administrator:
                login(request, user)
                return redirect('/administrator/')
            elif user.is_branch_user:
                login(request, user)
                return redirect('/branch_user/')
        else:
            messages.error(request, "Wrong Username and Password ")
            return render(request, 'login_page.html')
    return render(request, 'login_page.html')


def search_by_ticket_no(request):
    if request.method == "POST":
        ticket_no = request.POST.get("ticket_no")
        email = request.POST.get("email")
        try:
            ticket = Ticket.objects.get(ticket_no=ticket_no, email=email)
            return render(request, 'search_by_ticket_no.html', {'ticket': ticket})
        except:
            return redirect(home_page)

@login_required(login_url="/login_page")
@user_passes_test(lambda user: user.is_administrator, login_url="/login_page/")
def administrator(request):
    all_tickets = Ticket.objects.all()
    today_date = datetime.now()
    tickets_created_today = all_tickets.filter(date_time__date=today_date.date()).count()
    tickets_solved_today = all_tickets.filter(date_time__date=today_date.date(), ticket_status="solved").count()
    tickets_created_till_today = all_tickets.all().count()
    tickets_solved_till_today = all_tickets.filter(ticket_status="solved").count()
    data = {
        'tickets_created_today': tickets_created_today,
        'tickets_solved_today': tickets_solved_today,
        'tickets_left_today': tickets_created_today - tickets_solved_today,
        'tickets_created_till_today': tickets_created_till_today,
        'tickets_solved_till_today': tickets_solved_till_today,
        'tickets_left_till_today': tickets_created_till_today - tickets_solved_till_today,

    }
    return render(request, 'administrator.html', data)

@login_required(login_url="/login_page")
@user_passes_test(lambda user: user.is_administrator, login_url="/login_page/")
def add_branch(request):
    form = BranchForm()
    if request.method == "POST":
        my_form = BranchForm(request.POST)
        if my_form.is_valid():
            my_form.save()
            messages.success(request, "Branch Created successfully")
            return redirect(administrator)
        else:
            return render(request, 'add_branch.html', {'form': my_form})
    return render(request, 'add_branch.html', {'form': form})

@login_required(login_url="/login_page")
@user_passes_test(lambda user: user.is_administrator, login_url="/login_page/")
def add_branch_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('name')
        emp_id = request.POST.get('emp_id')
        contact_number = request.POST.get('contact_no')
        branch_name = request.POST.get('branch')
        branch = Branch.objects.get(branch_name=branch_name)
        password = password_generator()
        request.session['new_password'] = password
        html_message = loader.render_to_string('emails/branch_created_email.html', {'password': password})
        mail = send_mail('Password', '', settings.EMAIL_HOST_USER, [email], html_message=html_message, fail_silently=False)
        if mail:
            my_user = User.objects.create(email=email, password=make_password(password), is_branch_user=True)
            Branch_user(user=my_user, branch_name=branch, name=name, emp_id=emp_id, contact_number=contact_number).save()
            messages.success(request, "Branch Created successfully")
            return redirect(administrator)
        else:
            messages.error(request, "Branch not created")
            return render(request, 'add_branch_user.html')
    branches = Branch.objects.values_list("branch_name", flat=True).distinct()
    return render(request, 'add_branch_user.html', {'branches': branches})

@login_required(login_url="/login_page")
@user_passes_test(lambda user: user.is_administrator, login_url="/login_page/")
def all_solved_tickets(request):
    all_tickets = Ticket.objects.filter(ticket_status="solved").order_by('date_time')
    solved = True
    return render(request, 'show_tickets.html', {'all_tickets': all_tickets, 'solved': solved})

@login_required(login_url="/login_page")
@user_passes_test(lambda user: user.is_administrator, login_url="/login_page/")
def all_unsolved_tickets(request):
    all_tickets = Ticket.objects.filter(ticket_status="unsolved")
    print(all_tickets)
    solved = False
    return render(request, 'show_tickets.html', {'all_tickets': all_tickets, 'solved': solved})

@login_required(login_url="/login_page")
@user_passes_test(lambda user: user.is_branch_user, login_url="/login_page/")
def branchUser(request):
    branch_user = Branch_user.objects.get(user=request.user)
    branch = branch_user.branch_name
    tickets = Ticket.objects.filter(branch_name=branch)
    return render(request, 'branch_user.html', {'tickets': tickets, 'branches': branch})


@login_required(login_url="/login_page")
def user_logout(request):
    logout(request)
    return redirect('/')


@login_required(login_url="/login_page")
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        password = request.POST.get('new_password')
        if check_password(old_password, request.user.password):
            new_password = make_password(password)
            request.user.password = new_password
            request.user.save()
            if request.user.is_administrator:
                return redirect(administrator)
            elif request.user.is_branch_user:
                return redirect(branchUser)

        else:
            messages.error(request, "Old password is Wrong")
    return render(request, 'change_password.html')
@login_required(login_url="/login_page")
@user_passes_test(lambda user: user.is_branch_user, login_url="/login_page/")
def modifyStatus(request,id):
    ticket_id = Ticket.objects.get(id=id)
    return render(request, 'modify_Status.html',{'data':ticket_id})
