from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from decimal import Decimal
from .models import Users, Accounts, Transactions, Notification

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from django.utils import timezone

def home_view(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không chính xác.')

    return render(request, 'login.html')


@login_required(login_url='/login/')
def dashboard(request):
    try:
        user_obj = Users.objects.get(username=request.user.username)
        accounts = Accounts.objects.filter(user=user_obj)
        return render(request, 'dashboard.html', {'user': user_obj, 'accounts': accounts})
    except Users.DoesNotExist:
        messages.error(request, 'Không tìm thấy thông tin người dùng.')
        return redirect('logout')


@login_required(login_url='/login/')
def transfer(request):
    try:
        user_obj = Users.objects.get(username=request.user.username)
    except Users.DoesNotExist:
        messages.error(request, 'Không tìm thấy thông tin người dùng.')
        return redirect('logout')

    if request.method == 'POST':
        from_account_id = request.POST['from_account_id']
        to_account_id = request.POST['to_account_id']
        amount = Decimal(request.POST['amount'])
        content = request.POST['content']

        try:
            from_account = Accounts.objects.get(account_id=from_account_id, user=user_obj)
            to_account = Accounts.objects.get(account_id=to_account_id)

            if from_account.balance >= amount:
                # Cập nhật số dư
                from_account.balance -= amount
                from_account.save()

                to_account.balance += amount
                to_account.save()

                # Lưu giao dịch
                Transactions.objects.create(
                    from_account=from_account,
                    to_account=to_account,
                    amount=amount,
                    transaction_type="transfer",
                    transaction_date=timezone.now(),
                    status="completed",
                    content=content
                )

                # Tạo thông báo
                Notification.objects.create(
                    user=user_obj,
                    message=f"Chuyển tiền thành công từ tài khoản {from_account.account_id} đến {to_account.account_id}. Số tiền: {amount} VNĐ"
                )

                messages.success(request, 'Chuyển tiền thành công!')
            else:
                messages.error(request, 'Số dư không đủ để thực hiện giao dịch.')

        except Accounts.DoesNotExist:
            messages.error(request, 'Tài khoản không tồn tại hoặc không thuộc quyền sở hữu.')

    accounts = Accounts.objects.filter(user=user_obj)
    return render(request, 'transfer.html', {'accounts': accounts})


@login_required(login_url='/login/')
def balance_activity(request):
    try:
        user_obj = Users.objects.get(username=request.user.username)
        account_list = Accounts.objects.filter(user=user_obj)
        if not account_list.exists():
            messages.error(request, 'Không có tài khoản nào được liên kết.')
            return redirect('dashboard')

        # Lấy tất cả giao dịch liên quan đến tài khoản của người dùng
        transactions = Transactions.objects.filter(
            Q(from_account__in=account_list) | Q(to_account__in=account_list)
        ).order_by('-transaction_date')

        return render(request, 'balance_activity.html', {
            'transactions': transactions,
            'accounts': account_list
        })

    except Users.DoesNotExist:
        messages.error(request, 'Không tìm thấy thông tin người dùng.')
        return redirect('logout')


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('home')

import random
import string

# Hàm tạo tài khoản ngân hàng ngẫu nhiên (4 chữ số)
def generate_account_id():
    # Sinh ra một số tài khoản ngẫu nhiên 4 chữ số
    return ''.join(random.choices(string.digits, k=4))

# Hàm kiểm tra tài khoản ngân hàng có trùng không
def is_account_id_exists(account_id):
    return Accounts.objects.filter(account_id=account_id).exists()

# Hàm xử lý đăng ký người dùng
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Kiểm tra mật khẩu nhập lại
        if password != confirm_password:
            messages.error(request, 'Mật khẩu nhập lại không khớp.')
            return redirect('register')

        # Kiểm tra tên đăng nhập có trùng với người khác không
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.')
            return redirect('register')

        # Tạo tài khoản người dùng trong AuthUser (Django User model)
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Lưu mật khẩu đã mã hóa vào AuthUser
        user.password = make_password(password)
        user.save()

        # Tạo bản ghi trong bảng Users
        user_obj = Users.objects.create(
            user_id=user.id,
            username=username,
            email=email,
            password_hash=user.password,
            created_at=timezone.now()
        )

        # Tạo tài khoản ngân hàng ngẫu nhiên
        account_id = generate_account_id()

        # Kiểm tra tài khoản ngân hàng có trùng không, nếu trùng thì sinh lại
        while is_account_id_exists(account_id):
            account_id = generate_account_id()

        # Tạo tài khoản ngân hàng cho người dùng
        Accounts.objects.create(
            user=user_obj,
            account_id=account_id,
            balance=0.0,  # Số dư ban đầu là 0
            account_type='checking',  # Loại tài khoản
            status='active',  # Tình trạng tài khoản
            created_at=timezone.now()
        )

        messages.success(request, 'Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.')
        return redirect('login')

    return render(request, 'register.html')