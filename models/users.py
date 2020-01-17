from sqlalchemy import Column, Integer, String, ForeignKey, MetaData, Table, Text, DateTime, Boolean
from sqlalchemy_utils.types.password import PasswordType
from sqlalchemy_utils.types import EmailType
from .serializers import JSONSerializeTable

metadata = MetaData()


"""{'Users_id': 1, 'Users_account': '100001001', 'Users_password': 'any', 'Users_token': None, 'Users_re_token': None,
 'Users_street': 'Володина', 'Users_house': '12', 'Users_appartment': '29', 'Users_company': 1,
  'Companies_id': 1, 'Companies_name': 'Комфортный дом'}"""
  

users = JSONSerializeTable(
    'Users', metadata, 
    Column('id', Integer, primary_key=True),   
    Column('first_name', String(255)),
    Column('middle_name', String(255)),
    Column('last_name', String(255)),
    Column('street', String(255)),
    Column('house', String(255)),
    Column('appartment', String(255)),
    Column('phone', String(255)),
    Column('email', EmailType),
    Column('note', Text)
)

companies = Table(
    'Companies', metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('name', String(255))
)

logins = JSONSerializeTable(
    'Logins', metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('username', String(255)),
    Column('password', PasswordType(schemes=['pbkdf2_sha512'])),
    Column('create', DateTime(timezone=True)),
    Column('logged_in', DateTime(timezone=True)),
    Column('logged_out', DateTime(timezone=True)),
    Column('blocked', Boolean, unique=False, default=False),
    Column('user_profile', Integer, ForeignKey('Users.id'))
)

accounts = Table(
    'Accounts', metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('account', String(255)),
    Column('company', Integer, ForeignKey('Companies.id')),
    Column('user', Integer, ForeignKey('Users.id'))
)

groups = Table(
    'Groups', metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('name', String(255))
)

roles = Table(
    'Roles', metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('name', String(255))
)

memberships = JSONSerializeTable(
    'Memberships', metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('user', Integer, ForeignKey('Users.id')),
    Column('group', Integer, ForeignKey('Groups.id')),
    Column('role', Integer, ForeignKey('Roles.id')),
    Column('company', Integer, ForeignKey('Companies.id')),
)

user_tables = {
    'users': users,
    'companies': companies,
    'logins': logins,
    'accounts': accounts,
    'groups': groups,
    'roles': roles,
    'memberships': memberships,
}
"""users.db_result_to_json({'Users_id': 1, 'Users_account': '100001001', 'Users_password': 'any', 'Users_token': None, 'Users_re_token': None,
 'Users_street': 'Володина', 'Users_house': '12', 'Users_appartment': '29', 'Users_company': 1,
  'Companies_id': 1, 'Companies_name': 'Комфортный дом'})"""

""""""