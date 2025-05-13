from datetime import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import now
from .models import *
import json
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

THRESHOLD_REPORT = 20


def home(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            member = Users.objects.get(username=username)
            role_redirects = {
                'học sinh': 'user_dashboard',
                'giáo viên': 'user_dashboard',
                'kiểm duyệt viên': 'moderator_dashboard',
                'quản trị viên': 'admin_dashboard',
                'hội nhóm': 'group_dashboard'
            }
            return redirect(role_redirects.get(member.role, 'home'))

        return render(request, 'home.html', {'login_failed': True})

    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def get_dashboard_data():
    return {
        'post_thanh_ly': Post.objects.filter(status='Chưa duyệt', type_post='thanh lý'),
        'post_trao_doi': Post.objects.filter(status='Chưa duyệt', type_post='trao đổi'),
        'event_gay_quy': Event.objects.filter(status='Chưa duyệt', type='Gây quỹ'),
        'event_quyen_gop': Event.objects.filter(status='Chưa duyệt', type='Quyên góp'),
        'unverified_posts': Post.objects.filter(status='Chưa duyệt'),
        'unverified_events': Event.objects.filter(status='Chưa duyệt'),
        'approved_posts': Post.objects.filter(status='Đã duyệt' or 'Đã đặt' or 'Đã bán'),
        'rejected_posts': Post.objects.filter(status='Từ chối'),
        'approved_events': Event.objects.filter(status='Đã duyệt' or 'Đã đặt' or 'Đã bán'),
        'rejected_events': Event.objects.filter(status='Từ chối'),
        'categories': Category.objects.all(), 
        'su_kien': Event.objects.all(),
        'bai_dang_thanh_ly': Post.objects.filter(status='Đã duyệt' or 'Đã đặt' or 'Đã bán', type_post='thanh lý'),
        'bai_dang_trao_doi': Post.objects.filter(status='Đã duyệt' or 'Đã đặt' or 'Đã bán', type_post='trao đổi'),
    }


def moderator_dashboard(request):
    data = get_dashboard_data()
    data.update({
        'moderator': request.user,
        'user': Users.objects.get(username=request.user.username)
    })
    return render(request, 'moderator.html', data)


def moderate_event(request):
    if request.method == "POST":
        id_event = request.POST.get('id_event')
        new_status = request.POST.get('status')
        rejection_reason = request.POST.get('rejection_reason', '').strip()

        event = get_object_or_404(Event, id_event=id_event)
        if event.status == 'Chưa duyệt':
            event.status = new_status
            event.verified_person = Users.objects.get(username=request.user.username)
            event.date_verified = now()
            if new_status == "Từ chối":
                event.rejection_reason = rejection_reason
            event.save()

            noti_content = (
                f'Sự kiện "{event.name}" của bạn đã bị từ chối.\nLý do: {rejection_reason}'
                if new_status == "Từ chối"
                else f'Sự kiện "{event.name}" của bạn đã được duyệt.'
            )

            Notification.objects.create(
                content=noti_content,
                title='Trạng thái sự kiện',
                id_user=event.id_group,
                id_event=event,
                noti_time=now(),
                status_read='Chưa đọc'
            )
    return redirect('moderator_dashboard')



def user_event(request):
    if request.method == "POST":
        id_event = request.POST.get('id_event')
        new_status = request.POST.get('status')
        rejection_reason = request.POST.get('rejection_reason', '').strip()

        event = get_object_or_404(Event, id_event=id_event)
        if event.status == 'Chưa duyệt':
            event.status = new_status
            event.verified_person = Users.objects.get(username=request.user.username)
            event.date_verified = now()
            if new_status == "Từ chối":
                event.rejection_reason = rejection_reason
            event.save()

            noti_content = (
                f'Sự kiện "{event.name}" của bạn đã bị từ chối.\nLý do: {rejection_reason}'
                if new_status == "Từ chối"
                else f'Sự kiện "{event.name}" của bạn đã được duyệt.'
            )

            Notification.objects.create(
                content=noti_content,
                title='Trạng thái sự kiện',
                id_user=event.id_group,
                id_event=event,
                noti_time=now(),
                status_read='Chưa đọc'
            )
    return redirect('user_dashboard')

def user_post(request):
    if request.method == "POST":
        id_event = request.POST.get('id_event')
        new_status = request.POST.get('status')
        rejection_reason = request.POST.get('rejection_reason', '').strip()

        event = get_object_or_404(Event, id_event=id_event)
        if event.status == 'Chưa duyệt':
            event.status = new_status
            event.verified_person = Users.objects.get(username=request.user.username)
            event.date_verified = now()
            if new_status == "Từ chối":
                event.rejection_reason = rejection_reason
            event.save()

            noti_content = (
                f'Sự kiện "{event.name}" của bạn đã bị từ chối.\nLý do: {rejection_reason}'
                if new_status == "Từ chối"
                else f'Sự kiện "{event.name}" của bạn đã được duyệt.'
            )

            Notification.objects.create(
                content=noti_content,
                title='Trạng thái sự kiện',
                id_user=event.id_group,
                id_event=event,
                noti_time=now(),
                status_read='Chưa đọc'
            )
    return redirect('user_dashboard')




def moderate_post(request):
    if request.method == "POST":
        id_post = request.POST.get('id_post')
        new_status = request.POST.get('status')
        rejection_reason = request.POST.get('rejection_reason', '').strip()

        post = get_object_or_404(Post, id_post=id_post)
        if post.status == 'Chưa duyệt':
            post.status = new_status
            post.verified_person = Users.objects.get(username=request.user.username)
            post.date_verified = now()
            if new_status == "Từ chối":
                post.rejection_reason = rejection_reason
            post.save()

            noti_content = (
                f'Bài đăng "{post.title}" của bạn đã bị từ chối.\nLý do: {rejection_reason}'
                if new_status == "Từ chối"
                else f'Bài đăng "{post.title}" của bạn đã được duyệt.'
            )

            Notification.objects.create(
                content=noti_content,
                title='Trạng thái bài đăng',
                id_user=post.id_user,
                id_post=post,
                noti_time=now(),
                status_read='Chưa đọc'
            )
    return redirect('moderator_dashboard')


from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.core.serializers.json import DjangoJSONEncoder
import json

def admin_dashboard(request):
    posts = Post.objects.all()
    users = Users.objects.all()

    # === Biểu đồ 1: Bài viết theo tháng và loại ===
    post_stats = posts.annotate(month=ExtractMonth('date_created')) \
        .values('month', 'type_post') \
        .annotate(count=Count('id_post')) \
        .order_by('month')

    post_types = ['trao đổi', 'thanh lý']
    post_months = sorted({entry['month'] for entry in post_stats if entry['month'] is not None})
    post_month_index = {m: i for i, m in enumerate(post_months)}
    post_chart_data = {ptype: [0] * len(post_months) for ptype in post_types}

    for entry in post_stats:
        if entry['month'] is None:
            continue
        idx = post_month_index[entry['month']]
        post_chart_data[entry['type_post']][idx] = entry['count']

    # === Biểu đồ 2: Bài viết theo danh mục ===
    category_stats = posts.values('id_category__name') \
        .annotate(count=Count('id_post')) \
        .order_by('-count')

    category_labels = [entry['id_category__name'] or "Không xác định" for entry in category_stats]
    category_counts = [entry['count'] for entry in category_stats]

    # === Biểu đồ 3: Người dùng theo vai trò và tháng ===
    user_stats = users.filter(created_at__isnull=False) \
        .annotate(month=ExtractMonth('created_at')) \
        .values('month', 'role') \
        .annotate(count=Count('id_user')) \
        .order_by('month')

    user_roles = ['học sinh', 'giáo viên', 'quản trị viên', 'kiểm duyệt viên', 'hội nhóm']
    user_months = sorted({entry['month'] for entry in post_stats if entry['month'] is not None})
    user_month_index = {m: i for i, m in enumerate(user_months)}
    user_chart_data = {role: [0] * len(user_months) for role in user_roles}

    for entry in user_stats:
        if entry['month'] is None:
            continue
        idx = user_month_index[entry['month']]
        user_chart_data[entry['role']][idx] = entry['count']

    # === 4. Biểu đồ người dùng theo trường học ===
    school_stats = Users.objects.filter(role__in=['học sinh', 'giáo viên']) \
        .values('id_school__name') \
        .annotate(count=Count('id_user')) \
        .order_by('-count')

    name_school = [entry['id_school__name'] or 'Không xác định' for entry in school_stats]
    school_counts = [entry['count'] for entry in school_stats]

    # === Biểu đồ 5: Sự kiện theo trạng thái ===
    # Lấy tất cả các trạng thái duy nhất từ bảng Event
    status_labels = Event.objects.values('status').distinct().order_by('status')
    status_labels = [status['status'] for status in status_labels]

    # Lấy số lượng sự kiện theo trạng thái và loại (Gây quỹ, Quyên góp)
    fundraising_data = Event.objects.filter(type='Gây quỹ').values('status').annotate(count=Count('id_event')).order_by('status')
    donation_data = Event.objects.filter(type='Quyên góp').values('status').annotate(count=Count('id_event')).order_by('status')

    # Khởi tạo dữ liệu mặc định cho mỗi trạng thái
    fundraising_dict = {status: 0 for status in status_labels}
    donation_dict = {status: 0 for status in status_labels}

    # Cập nhật dữ liệu từ query
    for item in fundraising_data:
        fundraising_dict[item['status']] = item['count']

    for item in donation_data:
        donation_dict[item['status']] = item['count']

    
    context = {
        'months': json.dumps([f"Th{m}" for m in post_months]),
        'trao_doi_data': json.dumps(post_chart_data['trao đổi']),
        'thanh_ly_data': json.dumps(post_chart_data['thanh lý']),

        'categories_data': json.dumps(category_labels),
        'post_category': json.dumps(category_counts),

        'member_labels': json.dumps([f"Th{m}" for m in user_roles]),
        'hocsinh': json.dumps(user_chart_data['học sinh']),
        'giaovien': json.dumps(user_chart_data['giáo viên']),
        'quantrivien': json.dumps(user_chart_data['quản trị viên']),
        'kiemduyetvien': json.dumps(user_chart_data['kiểm duyệt viên']),

        'name_school': json.dumps(name_school),
        'school': json.dumps(school_counts),

        'statusLabels': json.dumps(status_labels),
        'fundraising_data': json.dumps(list(fundraising_dict.values())),
        'donation_data': json.dumps(list(donation_dict.values())),
    }

    return render(request, 'admin/dashboard.html', context)



'''
const member_labels = {{ member_labels|safe }};
        const hocsinh = {{ hocsinh|safe }};
        const giaovien = {{ giaovien|safe }};

'''

# Quản lý thành viên
def member_management(request):
    return render(request, 'admin/member_management.html')



from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.hashers import make_password  # Để mã hóa mật khẩu
from .models import Users, School

from django.db import IntegrityError

def add_member(request):
    if request.method == 'POST':
        # Lấy thông tin từ form
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        school_id = request.POST.get('school')


        # Kiểm tra các trường bắt buộc
        if not email or not password or not role or not school_id:
            messages.error(request, 'Vui lòng điền đầy đủ tất cả các thông tin!')
            return redirect('/members/add/')

        # Kiểm tra email đã tồn tại chưa
        if Users.objects.filter(email=email).exists():
            messages.error(request, 'Email đã tồn tại trong hệ thống. Vui lòng dùng email khác.')
            return redirect('/members/add/')

        # Tạo username tự động
        account_len = Users.objects.count()
        user_roles = {'học sinh': 'student', 
                      'giáo viên': 'teacher', 
                      'quản trị viên': 'admin', 
                      'kiểm duyệt viên': 'moderator', 
                      'hội nhóm': 'group'}

        username = user_roles[role] + f"{account_len + 1}"

        try:
            school = School.objects.get(id_school=school_id)
            user = Users(
                full_name=name,
                username=username,
                email=email,
                password=password,
                role=role,
                id_school=school,
                created_at=timezone.now(),
            )
            user.save()
            messages.success(request, f'Thêm thành viên thành công, username = {username}!')
            
            if role == 'hội nhóm':
                group = GroupInfo.objects.create(
                    name=name,
                )
                GroupUser.objects.create(
                    id_group=group,
                    id_user=user,
                    role_in_group='main system',
                )
                print(f"✅ Nhóm '{group.name}' đã được tạo và gán user '{user}' làm quản trị viên.")

                        # Tạo tài khoản ngân hàng ngẫu nhiên
                account_id = generate_account_id()

                # Kiểm tra tài khoản ngân hàng có trùng không, nếu trùng thì sinh lại
                while is_account_id_exists(account_id):
                    account_id = generate_account_id()

                # Tạo tài khoản ngân hàng cho người dùng
                Accounts.objects.create(
                    user=user,
                    account_id=account_id,
                    balance=0.0,  # Số dư ban đầu là 0
                    account_type='checking',  # Loại tài khoản
                    status='active',  # Tình trạng tài khoản
                    created_at=timezone.now()
                )
                        
            if not AuthUser.objects.filter(username=username).exists():
                AuthUser.objects.create(
                    username=username,
                    email=email,
                    password=make_password(password),
                    first_name='',
                    last_name='',
                    is_superuser=False,
                    is_staff=False,
                    is_active=True,
                    date_joined=timezone.now() or timezone.now(),
                    last_login=None
                )
            print(f'Migrated {username}')
        except IntegrityError:
            messages.error(request, 'Đã xảy ra lỗi khi lưu người dùng. Có thể email hoặc username đã tồn tại.')
        except School.DoesNotExist:
            messages.error(request, 'Không tìm thấy trường học phù hợp.')

        return redirect('/members/add/')

    schools = School.objects.all()

    return render(request, 'admin/add_members.html', {'schools': schools})

@csrf_exempt
def update_member(request, member_id):
    if request.method == 'PUT':
        try:
            # Lấy dữ liệu JSON từ body của request
            data = json.loads(request.body)

            # Kiểm tra xem thành viên có tồn tại không
            user = Users.objects.get(id=member_id)
            
            # Cập nhật các trường thông tin
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.role = data.get('role', user.role)
            user.school = data.get('school', user.school)

            # Lưu lại thay đổi vào cơ sở dữ liệu
            user.save()

            # Trả về kết quả thành công
            return JsonResponse({'message': 'Cập nhật thành viên thành công!'}, status=200)

        except Users.DoesNotExist:
            return JsonResponse({'error': 'Thành viên không tồn tại!'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Phương thức không hợp lệ'}, status=405)

import openpyxl # type: ignore
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.hashers import make_password

def import_excel(request):
    if request.method == 'POST' and request.FILES['excelFile']:
        file = request.FILES['excelFile']
        
        # Kiểm tra định dạng file
        if not file.name.endswith('.xlsx'):
            messages.error(request, 'Vui lòng chọn file Excel (.xlsx).')
            return redirect('/members/add/')

        # Mở file Excel
        try:
            wb = openpyxl.load_workbook(file)
            sheet = wb.active
        except Exception as e:
            messages.error(request, f'Đã xảy ra lỗi khi mở file: {str(e)}')
            return redirect('/members/add/')

        # Duyệt qua các dòng trong sheet (bỏ qua hàng đầu tiên nếu là tiêu đề)
        for row in sheet.iter_rows(min_row=2, values_only=True):
            name, email, password, role, school_id = row
            if not name or not email or not password or not role or not school_id:
                continue  # Bỏ qua dòng không đủ thông tin

            # Kiểm tra email đã tồn tại chưa
            if Users.objects.filter(email=email).exists():
                messages.error(request, f'Email {email} đã tồn tại. Bỏ qua dòng này.')
                continue

            # Tạo username tự động
            account_len = Users.objects.count()
            username = f"user{account_len + 1}"

            # Mã hóa mật khẩu
            hashed_password = make_password(password)

            try:
                school = School.objects.get(id_school=school_id)
                user = Users(
                    full_name=name,
                    username=username,
                    email=email,
                    password=hashed_password,
                    role=role,
                    id_school=school,
                    created_at=timezone.now(),
                )
                user.save()
            except School.DoesNotExist:
                messages.error(request, f'Không tìm thấy trường học với ID: {school_id}. Bỏ qua dòng này.')
                continue

        messages.success(request, 'Thêm thành viên từ file Excel thành công!')
        return redirect('/members/add/')

    return render(request, 'admin/add_members.html')



def view_members(request):
    schools = School.objects.all()
    return render(request, 'admin/view_members.html', {'schools': schools})
 

from django.http import JsonResponse

def filter_members(request):
    # Lấy giá trị filter từ request
    role = request.GET.get('role', 'all')
    id_school = request.GET.get('school', 'all')

    # Lọc danh sách thành viên theo phân quyền và trường học
    members = Users.objects.all()
    school = School.objects.all()
    if role != 'all':
        members = members.filter(role=role)

    if id_school != 'all':
        members = members.filter(id_school=id_school)
    # Chuyển đổi thành viên thành danh sách dictionary
    member_data = []
    for member in members:
        member_data.append({
            'id': member.id_user,
            'username': member.username,
            'email': member.email,
            'role': member.role,
            'id_school': member.id_school.id_school if member.id_school else None,
            'school': member.id_school.name if member.id_school else '',  # Giả sử school là một ForeignKey
        })


    return JsonResponse({'members': member_data})

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def member_detail(request, member_id):
    print(member_id)
    try:
        member = Users.objects.get(id=member_id)
    except Users.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({
            'id_user': member.id,
            'username': member.username,
            'email': member.email,
            'role': member.role,
            'school': member.school
        })

    if request.method == 'PUT':
        data = json.loads(request.body)
        member.username = data.get('username', member.username)
        member.email = data.get('email', member.email)
        member.password = data.get('password', member.password)  # Cần mã hóa mật khẩu nếu có
        member.role = data.get('role', member.role)
        member.school = data.get('school', member.school)
        member.save()
        return JsonResponse({'message': 'Member updated successfully'})

    return JsonResponse({'error': 'Invalid method'}, status=405)

# Quản lý danh mục
def category_management(request):
    return render(request, 'admin/category_management.html')

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('categoryName')
        description = request.POST.get('categoryDescription')
        category_type = request.POST.get('categoryList')

        # Kiểm tra nếu có giá trị đầy đủ
        if name and category_type:
            try:
                # Tạo đối tượng Category và lưu vào database
                new_category = Category(name=name, type=category_type, description=description)
                new_category.save()

                # Thông báo thành công
                messages.success(request, "Thêm danh mục thành công!")
                return redirect('add-category')  # Redirect lại về trang thêm danh mục (hoặc trang khác nếu muốn)
            except Exception as e:
                # Nếu có lỗi xảy ra, thông báo thất bại
                messages.error(request, "Có lỗi xảy ra khi thêm danh mục. Vui lòng thử lại!")
                return redirect('add-category')
        else:
            # Nếu không có tên hoặc loại danh mục, thông báo lỗi
            messages.error(request, "Vui lòng nhập đầy đủ thông tin!")
            return redirect('add-category')

    return render(request, 'admin/add_category.html')



def view_categories(request):
    category_type = request.GET.get('category_type', None)  # Lấy giá trị loại danh mục từ GET parameter
    if category_type and category_type != 'Tất cả':
        categories = Category.objects.filter(type=category_type)  # Lọc danh mục theo loại
    else:
        categories = Category.objects.all()  # Nếu không lọc, lấy tất cả danh mục
    
    return render(request, 'admin/view_categories.html', {'categories': categories})

@csrf_exempt
def update_category(request, category_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            category = Category.objects.get(id_category=category_id)
            category.name = data.get('name', category.name)
            category.type = data.get('type', category.type)
            category.save()
            return JsonResponse({'message': 'Cập nhật thành công!'})
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Không tìm thấy danh mục.'}, status=404)
    return JsonResponse({'error': 'Phương thức không hợp lệ'}, status=400)


# View để xóa danh mục
def delete_category(request, category_id):
    category = get_object_or_404(Category, id_category=category_id)
    category.delete()
    messages.success(request, "Xóa danh mục thành công!")
    return redirect('view-categories')  # Redirect lại trang danh mục


@csrf_exempt
def update_member(request, member_id):
    if request.method == 'PUT':
        try:
            member = Users.objects.get(id_user=member_id)
        except Users.DoesNotExist:
            return JsonResponse({'error': 'Member not found'}, status=404)

        # Lấy dữ liệu từ body request
        data = json.loads(request.body)

        # Cập nhật thông tin thành viên
        member.username = data.get('username', member.username)
        member.email = data.get('email', member.email)
        member.role = data.get('role', member.role)

        # Lưu các thay đổi vào cơ sở dữ liệu
        member.save()

        return JsonResponse({'message': 'Member updated successfully'}, status=200)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)



# Quản lý bài đăng
def post_management(request):
    return render(request, 'admin/post_management.html')

# Quản lý sự kiện
def event_management(request):
    return render(request, 'admin/event_management.html')


def event_detail(request):
    events = []

    # Fetch events and their participants
    for event in Event.objects.all():
        participants_data = []

        # Filter ParticipateForm entries for this event
        forms = ParticipateForm.objects.filter(id_event=event)

        for form in forms:
            user = form.id_user
            if not user:
                continue
            school_name = user.id_school.name if user.id_school else "Không rõ"
            contribution = form.donated_amount  # You can calculate the actual contribution here if needed

            # Add participant data, including event and participant IDs
            from django.utils.timezone import localtime
            participants_data.append({
                'name': user.full_name or user.username,
                'date': localtime(form.time_create_form).strftime('%d/%m/%Y') if form.time_create_form else "Không rõ",
                'contribution': contribution,  # Placeholder for contribution (can be calculated if you have transaction data)
                'school': school_name,
                'participant_id': form.id_user.id_user,  # Include participant ID
                'event_id': event.id_event,  # Include event ID
                'school_name': school_name,  # Include school name
                'id_participate_form': form.id_participate_form,  # Include id_participate_form
                'status_form': form.status_form, 
                'name_event': event.name,
            })

        events.append({
            'name': event.name,
            'participants': participants_data
        })

    context = {
        'events': events,
        'schools': School.objects.values_list('name', flat=True).distinct()
    }

    return render(request, 'group/event_detail.html', context=context)

def add_event(request):
    return render(request, 'group/add_event.html')

def edit_event(request):
    return render(request, 'group/edit_event.html')

def money_view(request):

    user = Users.objects.get(username=request.user.username)
    account = Accounts.objects.get(user=user)

    if request.method == 'POST':
        # Handle deposit
        if 'deposit' in request.POST:
            amount = int(request.POST.get('amount'))
            if amount > 0:
                account.balance += amount  # Add to balance
                account.save()
                # Create a transaction record
                Transactions.objects.create(
                    from_account=None,
                    to_account=account,
                    amount=amount,
                    transaction_type='deposit',
                    transaction_date=timezone.now(),
                    content=f"Nạp tiền vào tài khoản {account.account_id}",
                )
            return redirect('money')  # Redirect to avoid form resubmission

        # Handle withdrawal
        elif 'withdraw' in request.POST:
            amount = int(request.POST.get('amount'))
            if amount > 0 and account.balance >= amount:
                account.balance -= amount  # Subtract from balance
                account.save()
                Transactions.objects.create(
                    from_account=account,
                    to_account=None,
                    amount=- amount,
                    transaction_type='withdrawal',
                    transaction_date=timezone.now(),
                    content=f"Rút tiền từ tài khoản {account.account_id}",
                )
            return redirect('money')  # Redirect to avoid form resubmission

    context = {
        'account': account,  # Pass the account balance to the template
    }

    return render(request, 'group/money.html', context)

def member_view(request):
    group = get_object_or_404(GroupInfo, id_group=request.user.id)
    
    # Lấy các thành viên của nhóm thông qua GroupUser
    members = Users.objects.filter(groupuser__id_group=group)

    return render(request, 'group/member.html', {'members': members})

def group_dashboard(request):
    if request.user.is_authenticated:
        username = request.user.username
        print("Người dùng hiện tại:", username)
    
    return redirect(profile_view)



# def my_data(my_id):
#     return {
#         'post_thanh_ly': Post.objects.filter(status='Chưa duyệt', type_post='thanh lý'),
#         'post_trao_doi': Post.objects.filter(status='Chưa duyệt', type_post='trao đổi'),
#         'event_gay_quy': Event.objects.filter(status='Chưa duyệt', type='Gây quỹ'),
#         'event_quyen_gop': Event.objects.filter(status='Chưa duyệt', type='Quyên góp'),
#         'unverified_posts': Post.objects.filter(status='Chưa duyệt'),
#         'unverified_events': Event.objects.filter(status='Chưa duyệt'),
#         'approved_posts': Post.objects.filter(status='Đã duyệt'),
#         'rejected_posts': Post.objects.filter(status='Từ chối'),
#         'approved_events': Event.objects.filter(status='Đã duyệt'),
#         'rejected_events': Event.objects.filter(status='Từ chối'),
#         'categories': Category.objects.all(), 
#         'su_kien': Event.objects.all(),
#         'bai_dang_thanh_ly': Post.objects.filter(status='Đã duyệt', type_post='thanh lý'),
#         'bai_dang_trao_doi': Post.objects.filter(status='Đã duyệt', type_post='trao đổi'),
#     }




def profile_view(request):
    group_info = get_object_or_404(GroupInfo, id_group=request.user.id)
    admins = Users.objects.filter(
        id_user__in=GroupUser.objects.filter(id_group=group_info).exclude(id_user=request.user.id).values('id_user').distinct(),
        role='quản trị viên'
    )
    group = Users.objects.get(username=request.user.username)
    context = {
        'user': group,
        'admins': admins,
    }

    return render(request, 'group/profile.html', context)


def post_list(request):
    posts = Post.objects.filter(status='Đã duyệt')
    categories = Category.objects.all()

    return render(request, 'user_/post.html', {
        'posts': posts,
        'categories': categories,
        'user': Users.objects.get(username=request.user.username),
    })

def add_post(request):
    if request.method == 'POST':
        # Get data from the form
        category_id = request.POST.get('category')
        post_type = request.POST.get('post_type')
        title = request.POST.get('title')
        price = request.POST.get('price', 0)
        exchange_item = request.POST.get('exchange_item')
        
        # Get the current user (assuming the user is logged in)
        user = Users.objects.get(username=request.user.username)

        # Get category object
        category = Category.objects.get(id_category=category_id)

        if post_type == 'trao đổi':    
            post = Post.objects.create(
                id_user=user,
                id_category=category,
                title=title,
                content=exchange_item,
                type_post=post_type,
                status='Chưa duyệt',  # Default status
                date_created=timezone.now()
            )
            
        else:
            post = Post.objects.create(
                id_user=user,
                id_category=category,
                title=title,
                type_post=post_type,
                price=price,
                status='Chưa duyệt',  # Default status
                date_created=timezone.now()
            )

        # Return a JSON response with success message
        return JsonResponse({'success': True})

    # Render the page with categories to show the form
    categories = Category.objects.all()
    return render(request, 'user_/add_post.html', {'categories': categories})

def event_list(request):
    events = Event.objects.filter(status="Đã duyệt")
    return render(request, 'user_/event.html', {'events': events})

def group_list(request):
    groups = GroupInfo.objects.all()
    return render(request, 'user_/group.html', {'groups': groups})


# View để tham gia nhóm
def join_group_view(request, group_id):
    if request.method == "POST":
        user = Users.objects.get(username=request.user.username)
        group = GroupInfo.objects.get(id_group=group_id)

        # Kiểm tra xem người dùng đã tham gia nhóm này chưa
        if GroupUser.objects.filter(id_user=user, id_group=group).exists():
            messages.info(request, "Bạn đã tham gia nhóm này.")
        else:
            GroupUser.objects.create(
                id_user=user,
                id_group=group,
                role_in_group="member"
            )
            messages.success(request, f"Tham gia nhóm {group.name} thành công!")

    return redirect('group_list')

# View để rời khỏi nhóm
def leave_group_view(request, group_id):
    if request.method == "POST":
        user = Users.objects.get(username=request.user.username)
        group = GroupInfo.objects.get(id_group=group_id)

        # Kiểm tra xem người dùng có tham gia nhóm không
        try:
            group_user = GroupUser.objects.get(id_user=user, id_group=group)
            group_user.delete()  # Xóa thành viên khỏi nhóm
            messages.success(request, f"Bạn đã rời khỏi nhóm {group.name} thành công!")
        except GroupUser.DoesNotExist:
            messages.info(request, "Bạn chưa tham gia nhóm này.")

    return redirect('group_list')

# View để xem chi tiết nhóm
def group_detail_view(request, group_id):
    group = GroupInfo.objects.get(id_group=group_id)
    admins = Users.objects.filter(
        id_user__in=GroupUser.objects.filter(id_group=group).exclude(id_user=request.user.id).values('id_user')
    )
    events = Event.objects.filter(id_group=group)

    context = {
        'group': group,
        'admins': admins,
        'events': events,
        'user': request.user
    }

    return render(request, 'user_/group_detail.html', context)


def profile_view_u(request):
    data = get_dashboard_data()

    # Lấy user hiện tại
    user = Users.objects.get(username=request.user.username)
    data['user'] = user

    # Sự kiện đã tham gia
    joined_event_ids = ParticipateForm.objects.filter(id_user=user).values_list('id_event', flat=True)
    data['joined_events'] = Event.objects.filter(id_event__in=joined_event_ids)

    # Bài đăng của user
    data['user_posts'] = Post.objects.filter(id_user=user)


    approved_offers = TradingOffer.objects.filter(status="Đã duyệt", id_user=user)

    print(approved_offers)
    
# Get the posts associated with the approved offers where the buyer is the current user
    buyer_posts = Post.objects.filter(
        id_post__in=approved_offers.values('id_post')
    )

    # Assign the result to the data dictionary
    data['completed_posts'] = buyer_posts

    # Thống kê theo tháng
    mua_stats = Post.objects.filter(verified_person=user, type_post='thanh lý') \
        .annotate(month=ExtractMonth('complete_post')) \
        .values('month') \
        .annotate(count=Count('id_post'))

    trao_doi_stats = Post.objects.filter(verified_person=user, type_post='trao đổi') \
        .annotate(month=ExtractMonth('complete_post')) \
        .values('month') \
        .annotate(count=Count('id_post'))

    su_kien_stats = Event.objects.filter(id_event__in=joined_event_ids) \
        .annotate(month=ExtractMonth('start_time')) \
        .values('month') \
        .annotate(count=Count('id_event'))

    all_months = sorted(set(
        [e['month'] for e in mua_stats] +
        [e['month'] for e in trao_doi_stats] +
        [e['month'] for e in su_kien_stats]
    ))

    def extract_data(stats, months):
        mapping = {e['month']: e['count'] for e in stats}
        return [mapping.get(m, 0) for m in months]

    data['month_labels'] = [f"Tháng {m}" for m in all_months]
    data['mua_data'] = extract_data(mua_stats, all_months)
    data['trao_doi_data'] = extract_data(trao_doi_stats, all_months)
    data['su_kien_data'] = extract_data(su_kien_stats, all_months)

    return render(request, 'user_/profile.html', data)


# View để tham gia sự kiện
def join_event_view(request, event_id):
    if request.method == 'POST':
        user = Users.objects.get(username=request.user.username)
        event = Event.objects.get(id_event=event_id)

        # Kiểm tra xem người dùng đã tham gia sự kiện chưa
        if event.participants.filter(id_user=user).exists():
            return JsonResponse({'success': False, 'message': 'Bạn đã tham gia sự kiện này rồi!'})
        
        # Thêm người tham gia vào sự kiện
        event.participants.create(id_user=user, status="Đang tham gia")
        return JsonResponse({'success': True, 'message': 'Tham gia sự kiện thành công!'})

    return JsonResponse({'success': False, 'message': 'Yêu cầu không hợp lệ!'})



def admin_detail(request):
    return render(request, 'group/admin_detail.html')

def notification_view(request):
    user = Users.objects.get(username=request.user.username)
    notifications = Notification.objects.order_by('-noti_time').filter(id_user=user)
    return render(request, 'group/noti.html', {'notifications': notifications})


def user_dashboard(request):
    return redirect('post_list')





# Báo cáo thống kê
def statistics(request):
    posts = Post.objects.all()
    users = Users.objects.all()

    # === Biểu đồ 1: Bài viết theo tháng và loại ===
    post_stats = posts.annotate(month=ExtractMonth('date_created')) \
        .values('month', 'type_post') \
        .annotate(count=Count('id_post')) \
        .order_by('month')

    post_types = ['trao đổi', 'thanh lý']
    post_months = sorted({entry['month'] for entry in post_stats if entry['month'] is not None})
    post_month_index = {m: i for i, m in enumerate(post_months)}
    post_chart_data = {ptype: [0] * len(post_months) for ptype in post_types}

    for entry in post_stats:
        idx = post_month_index[entry['month']]
        post_chart_data[entry['type_post']][idx] = entry['count']

    # === Biểu đồ 2: Bài viết theo danh mục ===
    category_stats = posts.values('id_category__name') \
        .annotate(count=Count('id_post')) \
        .order_by('-count')

    category_labels = [entry['id_category__name'] or "Không xác định" for entry in category_stats]
    category_counts = [entry['count'] for entry in category_stats]

    # === Biểu đồ 3: Người dùng theo vai trò và tháng ===
    user_stats = users.annotate(month=ExtractMonth('created_at')) \
        .values('month', 'role') \
        .annotate(count=Count('id_user')) \
        .order_by('month')

    user_roles = ['học sinh', 'giáo viên', 'quản trị viên', 'kiểm duyệt viên', 'hội nhóm']
    user_months = sorted({entry['month'] for entry in post_stats if entry['month'] is not None})
    user_month_index = {m: i for i, m in enumerate(user_months)}
    user_chart_data = {role: [0] * len(user_months) for role in user_roles}

    for entry in user_stats:
        if entry['month'] is None:
            continue
        idx = user_month_index[entry['month']]
        user_chart_data[entry['role']][idx] = entry['count']

    # === 4. Biểu đồ người dùng theo trường học ===
    school_stats = Users.objects.filter(role__in=['học sinh', 'giáo viên']) \
        .values('id_school__name') \
        .annotate(count=Count('id_user')) \
        .order_by('-count')

    name_school = [entry['id_school__name'] or 'Không xác định' for entry in school_stats]
    school_counts = [entry['count'] for entry in school_stats]

    # === Biểu đồ 5: Sự kiện theo trạng thái ===
    # Lấy tất cả các trạng thái duy nhất từ bảng Event
    status_labels = Event.objects.values('status').distinct().order_by('status')
    status_labels = [status['status'] for status in status_labels]

    # Lấy số lượng sự kiện theo trạng thái và loại (Gây quỹ, Quyên góp)
    fundraising_data = Event.objects.filter(type='Gây quỹ').values('status').annotate(count=Count('id_event')).order_by('status')
    donation_data = Event.objects.filter(type='Quyên góp').values('status').annotate(count=Count('id_event')).order_by('status')

    # Khởi tạo dữ liệu mặc định cho mỗi trạng thái
    fundraising_dict = {status: 0 for status in status_labels}
    donation_dict = {status: 0 for status in status_labels}

    # Cập nhật dữ liệu từ query
    for item in fundraising_data:
        fundraising_dict[item['status']] = item['count']

    for item in donation_data:
        donation_dict[item['status']] = item['count']

    
    context = {
        'months': json.dumps([f"Th{m}" for m in post_months]),
        'trao_doi_data': json.dumps(post_chart_data['trao đổi']),
        'thanh_ly_data': json.dumps(post_chart_data['thanh lý']),

        'categories_data': json.dumps(category_labels),
        'post_category': json.dumps(category_counts),

        'member_labels': json.dumps([f"Th{m}" for m in user_roles]),
        'hocsinh': json.dumps(user_chart_data['học sinh']),
        'giaovien': json.dumps(user_chart_data['giáo viên']),
        'quantrivien': json.dumps(user_chart_data['quản trị viên']),
        'kiemduyetvien': json.dumps(user_chart_data['kiểm duyệt viên']),

        'name_school': json.dumps(name_school),
        'school': json.dumps(school_counts),

        'statusLabels': json.dumps(status_labels),
        'fundraising_data': json.dumps(list(fundraising_dict.values())),
        'donation_data': json.dumps(list(donation_dict.values())),
    }

    return render(request, 'admin/statistics.html', context)

from django.http import JsonResponse
from django.utils import timezone
from .models import ParticipateForm, Event, Notification, Users
import json

# View to handle participation form submission
def participate_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        event_id = data.get('event_id')
        title = data.get('title')
        content = data.get('content')
        contribution = data.get('contribution', 0)

        try:
            event = Event.objects.get(id_event=event_id)
            user = Users.objects.get(username=request.user.username)
            # Create participation form instance with contribution
            participate_form = ParticipateForm.objects.create(
                id_event=event,
                title=title,
                content=content,
                status_form='Chưa duyệt',  # Initially pending
                id_user=user,
                donated_amount=contribution,
                time_create_form=timezone.now()
            )

            return JsonResponse({'success': True, 'message': 'Tham gia sự kiện thành công!'})

        except Event.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Sự kiện không tồn tại'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

from django.http import JsonResponse
from .models import ParticipateForm

def approve_participant(request, participate_form_id, action):
    if request.method == 'POST':
        try:
            # Find the ParticipateForm by its primary key (id_participate_form)
            participate_form = ParticipateForm.objects.get(id_participate_form=participate_form_id)
            if participate_form.status_form != 'Chưa duyệt':
                return JsonResponse({'success': False, 'message': 'Tham gia sự kiện đã được xử lý trước đó'})
            # Perform the action: approve or reject
            if action == 'approve':
            
                account = Accounts.objects.get(user=participate_form.id_user)
                # Deduct the contribution amount from the user's account
                if participate_form.donated_amount > 0 and account.balance >= participate_form.donated_amount:
                    account.balance -= participate_form.donated_amount
                    account_group = Accounts.objects.get(user=Users.objects.get(username=request.user.username))
                    account_group.balance += participate_form.donated_amount
                    account_group.save()
                    account.save()

                    # Create a record of the transaction
                    Transactions.objects.create(
                        from_account=account,
                        to_account=account_group,
                        amount=participate_form.donated_amount,
                        transaction_type='donation',
                        transaction_date=timezone.now(),
                        content=f"Người dùng {participate_form.id_user.username} đã tham gia sự kiện: {participate_form.id_event.name} với số tiền {participate_form.donated_amount} VNĐ."
                    )

                else: 
                    return JsonResponse({'success': False, 'message': 'Số tiền đóng góp không hợp lệ hoặc không đủ tiền trong tài khoản'})


                participate_form.status_form = 'Đã duyệt'  # Mark as approved
                participate_form.save()
                return JsonResponse({'success': True, 'message': 'Đã duyệt tham gia sự kiện!'})

            elif action == 'reject':
                participate_form.status_form = 'Từ chối'  # Mark as rejected
                participate_form.save()
                return JsonResponse({'success': True, 'message': 'Đã từ chối tham gia sự kiện!'})

            return JsonResponse({'success': False, 'message': 'Hành động không hợp lệ'})
        except ParticipateForm.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Tham gia sự kiện không tồn tại'})

    return JsonResponse({'success': False, 'message': 'Yêu cầu không hợp lệ'})

from django.http import JsonResponse
from django.utils import timezone
from my_app.models import Post, Users, TradingOffer, Accounts
def buy_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get('post_id')
        exchange_item_info = data.get('exchange_item_info', None)  # Get exchange item info if any

        try:
            # Fetch the post and the buyer
            post = Post.objects.get(id_post=post_id)
            buyer = Users.objects.get(username=request.user.username)
            buyer_account = Accounts.objects.get(user=buyer)  # Get the user's account

            # Handle sale posts (thanh lý)
            if post.type_post == 'thanh lý':
                # Check if the buyer has enough balance
                if buyer_account.balance >= post.price:
                    # Create a new TradingOffer instance for sale
                    trading_offer = TradingOffer.objects.create(
                        product_name=post.title,
                        id_post=post,
                        id_user=buyer,
                        status="Chờ duyệt",  # Initially the offer is waiting for approval
                        created_at=timezone.now(),
                        description=f'Giá: {post.price} VNĐ',  # Add price as description
                    )

                    # Update the post status to "Đã đặt"
                    post.status = "Đã đặt"
                    post.save()

                    # Subtract the post price from the buyer's account balance
                    buyer_account.balance -= post.price
                    buyer_account.save()

                    return JsonResponse({'success': True, 'message': 'Đặt bài thành công!'})

                else:
                    return JsonResponse({'success': False, 'message': 'Bạn không đủ tiền để mua bài đăng'})

            # Handle exchange posts (trao đổi)
            elif post.type_post == 'trao đổi':
                if exchange_item_info:
                    # Create a new TradingOffer instance for exchange
                    trading_offer = TradingOffer.objects.create(
                        product_name=post.title,
                        id_post=post,
                        id_user=buyer,
                        status="Chờ duyệt",  # Initially the offer is waiting for approval
                        created_at=timezone.now(),
                        description=exchange_item_info,  # Add exchange item info as description
                    )

                    # Update the post status to "Đã đặt"
                    post.status = "Đã đặt"
                    post.save()

                    return JsonResponse({'success': True, 'message': 'Giao dịch trao đổi đã được tạo thành công!'})

                else:
                    return JsonResponse({'success': False, 'message': 'Vui lòng nhập thông tin vật phẩm muốn trao đổi'})

        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Bài đăng không tồn tại'})
        except Users.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Người dùng không tồn tại'})
        except Accounts.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Tài khoản người dùng không tồn tại'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def orders(request):
    user = Users.objects.get(username=request.user.username)

    posts = Post.objects.filter(id_user=user)

    # Get the trading offers for those posts
    trading_offers = TradingOffer.objects.filter(id_post__in=posts, status='Chờ duyệt')

    context = {
        'trading_offers': trading_offers
    }
    return render(request, 'user_/order.html', context)
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import TradingOffer, Post, Accounts, Transactions

def approve_order(request, offer_id):
    if request.method == 'POST':
        # Parse the data sent from frontend
        data = json.loads(request.body)
        action = data.get('action')

        try:
            offer = get_object_or_404(TradingOffer, id_trading_offer=offer_id)
            post = offer.id_post
            
            # Handle the action (approve or reject)
            if action == 'approve':
                # Approve the order based on post type
                if post.type_post == 'thanh lý':  # Sale post
                    # Approve the sale and change post status to "Đã bán"
                    post.status = 'Đã bán'  # Set post status to "Sold"
                    post.save()
                    offer.status = 'Đã duyệt'  # Change offer status to 'Approved'
                    offer.save()

                    # Handle the financial transaction
                    buyer = offer.id_user
                    buyer_account = Accounts.objects.get(user=buyer)
                    buyer_account.balance -= post.price  # Deduct the price from the buyer's account
                    buyer_account.save()

                    seller = post.id_user
                    seller_account = Accounts.objects.get(user=seller)
                    seller_account.balance += post.price  # Add the price to the seller's account
                    seller_account.save()

                    # Record the transaction
                    Transactions.objects.create(
                        from_account=buyer_account,
                        to_account=seller_account,
                        amount=post.price,
                        transaction_type='buy',
                        transaction_date=timezone.now(),
                        status='completed',
                        content=f"Người dùng {buyer.username} đã mua bài đăng: {post.title} với giá {post.price} VNĐ từ người dùng {seller.username}."
                    )

                elif post.type_post == 'trao đổi':  # Exchange post
                    # Approve the exchange and change post status to "Đã trao đổi"
                    post.status = 'Đã trao đổi'  # Set post status to "Exchanged"
                    post.save()
                    offer.status = 'Đã duyệt'  # Change offer status to 'Approved'
                    offer.save()

                    # Handle the exchange process
                    buyer = offer.id_user
                    exchange_item_info = offer.description  # Assuming the buyer's exchange item info is saved in the offer's description
                    # Create a transaction or notification for exchange if needed, e.g.:
                    # You can handle specific logic for the exchange item info if needed (e.g. notifying the seller)
                    

                # Optionally, you can delete the trading offer after processing
                # offer.delete()

                return JsonResponse({'success': True, 'message': 'Đơn hàng đã được phê duyệt thành công!'})

            elif action == 'reject':
                # Reject the order and revert post status to "Đã duyệt"
                post.status = 'Đã duyệt'  # Set post status back to "Approved"
                post.save()
                offer.status = 'Từ chối'  # Change offer status to 'Rejected'
                offer.save()

                return JsonResponse({'success': True, 'message': 'Đơn hàng đã bị từ chối'})

        except TradingOffer.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Đơn hàng không tồn tại'})

    return JsonResponse({'success': False, 'message': 'Yêu cầu không hợp lệ'})






def bibi_home_view(request):
    if request.user.is_authenticated:
        return redirect('bibi_dashboard')
    return redirect('home')


def bibi_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('bibi_dashboard')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không chính xác.')

    return render(request, 'bibi/login.html')


def bibi_dashboard(request):
    user = Users.objects.get(username=request.user.username)
    account = Accounts.objects.get(user=user)

    if request.method == 'POST':
        # Handle deposit
        if 'deposit' in request.POST:
            amount = int(request.POST.get('amount'))
            if amount > 0:
                account.balance += amount  # Add to balance
                account.save()
                # Create a transaction record
                Transactions.objects.create(
                    from_account=None,
                    to_account=account,
                    amount=amount,
                    transaction_type='deposit',
                    transaction_date=timezone.now(),
                    content=f"Nạp tiền vào tài khoản {account.account_id}",
                )
            return redirect('bibi_dashboard')  # Redirect to avoid form resubmission

        # Handle withdrawal
        elif 'withdraw' in request.POST:
            amount = int(request.POST.get('amount'))
            if amount > 0 and account.balance >= amount:
                account.balance -= amount  # Subtract from balance
                account.save()
                Transactions.objects.create(
                    from_account=account,
                    to_account=None,
                    amount=- amount,
                    transaction_type='withdrawal',
                    transaction_date=timezone.now(),
                    content=f"Rút tiền từ tài khoản {account.account_id}",
                )
            return redirect('bibi_dashboard')  # Redirect to avoid form resubmission

    
    return render(request, 'bibi/dashboard.html', {'user': user, 'accounts': {account}})
    

def bibi_transfer(request):
    try:
        user_obj = Users.objects.get(username=request.user.username)
    except Users.DoesNotExist:
        messages.error(request, 'Không tìm thấy thông tin người dùng.')
        return redirect('logout')

    if request.method == 'POST':
        from_account_id = request.POST['from_account_id']
        to_account_id = request.POST['to_account_id']
        from decimal import Decimal
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
    return render(request, 'bibi/transfer.html', {'accounts': accounts})


def bibi_balance_activity(request):
    try:
        user_obj = Users.objects.get(username=request.user.username)
        account_list = Accounts.objects.filter(user=user_obj)
        if not account_list.exists():
            messages.error(request, 'Không có tài khoản nào được liên kết.')
            return redirect('bibi_dashboard')

        # Lấy tất cả giao dịch liên quan đến tài khoản của người dùng
        transactions = Transactions.objects.filter(
            Q(from_account__in=account_list) | Q(to_account__in=account_list)
        ).order_by('-transaction_date')

        return render(request, 'bibi/balance_activity.html', {
            'transactions': transactions,
            'accounts': account_list
        })

    except Users.DoesNotExist:
        messages.error(request, 'Không tìm thấy thông tin người dùng.')
        return redirect('logout')

def bibi_logout_view(request):
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
