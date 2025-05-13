# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'category'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Event(models.Model):
    id_event = models.AutoField(primary_key=True)
    id_group = models.ForeignKey('GroupInfo', models.DO_NOTHING, db_column='id_group', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    donated_amount = models.IntegerField(blank=True, null=True, default=0)
    number_of_participants = models.IntegerField(blank=True, null=True, default=0)
    location = models.CharField(max_length=255, blank=True, null=True)
    verified_person = models.ForeignKey('Users', models.DO_NOTHING, db_column='verified_person', blank=True, null=True)
    num_of_report = models.IntegerField(blank=True, null=True)
    date_verified = models.DateTimeField(blank=True, null=True)
    id_notification = models.ForeignKey('Notification', models.DO_NOTHING, db_column='id_notification', blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    poster = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'event'


class GroupInfo(models.Model):
    id_group = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    account_bank = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    score_group = models.IntegerField(blank=True, null=True)
    avt_group = models.TextField(blank=True, null=True)
    bank = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'group_info'


class GroupUser(models.Model):
    id_group_user = models.AutoField(primary_key=True)
    id_group = models.ForeignKey(GroupInfo, models.DO_NOTHING, db_column='id_group', blank=True, null=True)
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    role_in_group = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'group_user'


class Notification(models.Model):
    id_notification = models.AutoField(primary_key=True)
    content = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    id_event = models.ForeignKey(Event, models.DO_NOTHING, db_column='id_event', blank=True, null=True)
    id_post = models.ForeignKey('Post', models.DO_NOTHING, db_column='id_post', blank=True, null=True)
    noti_time = models.DateTimeField(blank=True, null=True)
    status_read = models.CharField(max_length=50, blank=True, null=True)
    old_id_notification = models.ForeignKey('self', models.DO_NOTHING, db_column='old_id_notification', blank=True, null=True)
    id_group = models.ForeignKey(GroupInfo, models.DO_NOTHING, db_column='id_group', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'notification'


class ParticipateForm(models.Model):
    id_participate_form = models.AutoField(primary_key=True)
    id_event = models.ForeignKey(Event, models.DO_NOTHING, db_column='id_event', blank=True, null=True)
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    status_form = models.CharField(max_length=50, blank=True, null=True)
    member_verified = models.ForeignKey('Users', models.DO_NOTHING, db_column='member_verified', related_name='participateform_member_verified_set', blank=True, null=True)
    time_create_form = models.DateTimeField(blank=True, null=True)
    time_update_status_form = models.DateTimeField(blank=True, null=True)
    id_notification = models.ForeignKey(Notification, models.DO_NOTHING, db_column='id_notification', blank=True, null=True)
    donated_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)

    class Meta:
        managed = True
        db_table = 'participate_form'


class Post(models.Model):
    id_post = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='id_category', blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    product_image = models.TextField(blank=True, null=True)
    product_used_period = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    verified_person = models.ForeignKey('Users', models.DO_NOTHING, db_column='verified_person', related_name='post_verified_person_set', blank=True, null=True)
    date_verified = models.DateTimeField(blank=True, null=True)
    num_of_report = models.IntegerField(blank=True, null=True)
    type_post = models.CharField(max_length=50, blank=True, null=True)
    id_old_post = models.ForeignKey('self', models.DO_NOTHING, db_column='id_old_post', blank=True, null=True)
    complete_post = models.DateTimeField(blank=True, null=True)
    id_notification = models.ForeignKey(Notification, models.DO_NOTHING, db_column='id_notification', blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'post'


class Report(models.Model):
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    id_report = models.AutoField(primary_key=True)
    type_report = models.TextField(blank=True, null=True)
    content_report = models.TextField(blank=True, null=True)
    verified_person = models.ForeignKey('Users', models.DO_NOTHING, db_column='verified_person', related_name='report_verified_person_set', blank=True, null=True)
    report_create_at = models.DateTimeField(blank=True, null=True)
    status_solve = models.CharField(max_length=255, blank=True, null=True)
    time_update_status_report = models.DateTimeField(blank=True, null=True)
    id_notification = models.ForeignKey(Notification, models.DO_NOTHING, db_column='id_notification', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'report'


class School(models.Model):
    id_school = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email_school = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'school'


class TradingOffer(models.Model):
    id_trading_offer = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='id_category', blank=True, null=True)
    id_post = models.ForeignKey(Post, models.DO_NOTHING, db_column='id_post', blank=True, null=True)
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    product_image = models.TextField(blank=True, null=True)
    product_used_period = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    time_update_status = models.DateTimeField(blank=True, null=True)
    id_notification = models.ForeignKey(Notification, models.DO_NOTHING, db_column='id_notification', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trading_offer'


class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    social_score = models.IntegerField(blank=True, null=True, default=0)
    created_score = models.IntegerField(blank=True, null=True, default=0)
    id_school = models.ForeignKey(School, models.DO_NOTHING, db_column='id_school', blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    avt_user = models.TextField(blank=True, null=True)
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'users'

class Accounts(models.Model):
    account_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)  # ForeignKey from myapp's Users model
    balance = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    account_type = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'accounts'
        
class Transactions(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    from_account = models.ForeignKey(Accounts, models.DO_NOTHING, blank=True, null=True)
    to_account = models.ForeignKey(Accounts, models.DO_NOTHING, related_name='transactions_to_account_set', blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=50, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)  # 👈 thêm dòng này

    class Meta:
        managed = True
        db_table = 'transactions'




class Vote(models.Model):
    id_vote = models.AutoField(primary_key=True)
    id_post = models.ForeignKey(Post, models.DO_NOTHING, db_column='id_post', blank=True, null=True)
    id_event = models.ForeignKey(Event, models.DO_NOTHING, db_column='id_event', blank=True, null=True)
    id_user = models.ForeignKey(Users, models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    time_vote = models.DateTimeField(blank=True, null=True)
    id_notification = models.ForeignKey(Notification, models.DO_NOTHING, db_column='id_notification', blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'vote'
