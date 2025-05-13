from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),


    path('moderator/', moderator_dashboard, name='moderator_dashboard'),
    path('moderate_post/', moderate_post, name='moderate_post'),
    path('moderate_event/', moderate_event, name='moderate_event'),
    path('user_event/', user_event, name='user_event'),
    path('user_post/', user_post, name='user_post'),
    path('events_u/participate/', participate_event, name='participate_event'),
    

    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('user/dashboard/', user_dashboard, name='user_dashboard'),


    path('group/dashboard/', group_dashboard, name='group_dashboard'),
    path('group/event_detail/', event_detail, name='event_detail'),
    path('group/add_event/', add_event, name='add_event'),
    path('group/edit_event/', edit_event, name='edit_event'),
    path('group/money/', money_view, name='money'),
    path('events/create/<int:group_id>/', create_event, name='create_event'),

    path('api/members/<int:member_id>/', update_member, name='update-member'),
    path('group/profile/', profile_view, name='profile'),
    path('group/admin_detail/', admin_detail, name='admin_detail'),
    path('group/noti/', notification_view, name='noti'),
    path('group/member/', member_view, name='member'),
    
    # Quản lý thành viên
    path('members/', member_management, name='member-management'),
    path('members/add/', add_member, name='add-member'),
    path('members/view/', view_members, name='view-members'),
    path('members/import/', import_excel, name='import-excel'),  # Thêm URL cho import Excel
    path('api/members/filter_members/', filter_members, name='filter-members'),
    path('api/members/<int:member_id>/', update_member, name='update-member'),



    # Quản lý danh mục
    path('categories/', category_management, name='category-management'),
    path('categories/add/', add_category, name='add-category'),
    path('categories/view/', view_categories, name='view-categories'),
    path('api/categories/<int:category_id>/', update_category, name='update_category'),
    path('delete-category/<int:category_id>/', delete_category, name='delete_category'),  # Xóa danh mục

    # Quản lý bài đăng
    path('posts/', post_management, name='post-management'),
    path('events/', event_management, name='event-management'),
    path('statistics/', statistics, name='statistics'),
    path('orders/', orders, name='order'),
    path('orders_u/approve_order/<int:offer_id>/', approve_order, name='approve_order'),  # Handle approval/rejection

    path('posts_u/buy_post/', buy_post, name='buy_post'),
    path('posts_u/add/', add_post, name='add_post'),
    path('posts_u/', post_list, name='post_list'),
    path('events_u/', event_list, name='event_list'),
    path('events_list_group/', event_list_group, name='event_list_group'),
    # urls.py
    #path('events/create/', create_event, name='create_event'),

    path('groups_u/', group_list, name='group_list'),
    path('profile_u/', profile_view_u, name='profile_u'),
    path('groups_u/join/<int:group_id>/', join_group_view, name='join_group'),
    path('groups_u/leave/<int:group_id>/', leave_group_view, name='leave_group'),
    path('groups_u/detail/<int:group_id>/', group_detail_view, name='group_detail'),
    path('events_u/join/<int:event_id>/', join_event_view, name='join_event'),  # Thêm path tham gia sự kiện


    path('events_u/approve_participant/<int:participate_form_id>/<str:action>/', approve_participant, name='approve_participant'),
    path('posts_u/report_post/', report_post, name='report_post'),
    path('noti_u/', user_notification_view, name='noti_u'),
    path('rate_post/', rate_post, name='rate_post'),


    path('bibi/', bibi_home_view, name='bibi_home'),
    path('bibi/login/', bibi_login_view, name='bibi_login'),
    path('bibi/logout/', bibi_logout_view, name='bibi_logout'),
    path('bibi/dashboard/', bibi_dashboard, name='bibi_dashboard'),
    path('bibi/transfer/', bibi_transfer, name='bibi_transfer'),
    path('bibi/activity/', bibi_balance_activity, name='bibi_balance_activity'),

]
