# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    username = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
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


class DocResults(models.Model):
    id = models.IntegerField(blank=True, primary_key=True)
    project_id = models.IntegerField(blank=True, null=True)
    doc_ext = models.TextField(blank=True, null=True)
    doc_url = models.TextField(blank=True, null=True)
    doc_location = models.TextField(blank=True, null=True)
    doc_full_location = models.TextField(blank=True, null=True)
    doc_meta_exif = models.TextField(blank=True, null=True)
    doc_author = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'doc_results'


class LinkedinCompanyEmployees(models.Model):
    id = models.IntegerField(blank=True, primary_key=True)
    project_id = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    job_title = models.TextField(blank=True, null=True)
    linkedin_url = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'linkedin_company_employees'


class LinkedinCompanyInfo(models.Model):
    id = models.IntegerField(blank=True, primary_key=True)
    project_id = models.IntegerField(blank=True, null=True)
    company_name = models.IntegerField(blank=True, null=True)
    company_linkedin_url = models.IntegerField(blank=True, null=True)
    company_description = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'linkedin_company_info'


class MailHarvestResults(models.Model):
    id = models.IntegerField(blank=True, primary_key=True)
    project_id = models.IntegerField(blank=True, null=True)
    mail_results = models.TextField(blank=True, null=True)
    mail_pgp_results = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'mail_harvest_results'


class MainDomainResults(models.Model):
    id = models.IntegerField(blank=True, primary_key=True)
    project_id = models.IntegerField(blank=True, null=True)
    domain = models.TextField(blank=True, null=True)
    domain_whois = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    domain_reputation = models.TextField(blank=True, null=True)
    domain_blacklist = models.TextField(blank=True, null=True)
    ns_record = models.TextField(db_column='NS_record', blank=True, null=True)  # Field name made lowercase.
    mx_record = models.TextField(db_column='MX_record', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'main_domain_results'


class Projects(models.Model):
    project_id = models.IntegerField(blank=True, primary_key=True)
    project_domain = models.TextField(blank=True, null=True)
    project_org = models.TextField(blank=True, null=True)
    started_time = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'projects'

    def __unicode__(self):
        return self.project_domain

class SubdomainResults(models.Model):
    id = models.IntegerField(blank=True, primary_key=True)
    project_id = models.IntegerField(blank=True, null=True)
    subdomain = models.TextField(blank=True, null=True)
    ip_address = models.TextField(blank=True, null=True)
    banner = models.TextField(blank=True, null=True)
    wappalyzer = models.TextField(blank=True, null=True)
    robots_txt = models.TextField(blank=True, null=True)
    is_contain_git = models.IntegerField(blank=True, null=True)
    is_contain_svn = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'subdomain_results'
