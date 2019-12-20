#import sqlalchemy as sa

from sqlalchemy import Column, Integer, String, ForeignKey, MetaData, Table
from sqlalchemy_utils.types.password import PasswordType
from .serializers import JSONSerializeTable

metadata = MetaData()


"""{'Users_id': 1, 'Users_account': '100001001', 'Users_password': 'any', 'Users_token': None, 'Users_re_token': None,
 'Users_street': 'Володина', 'Users_house': '12', 'Users_appartment': '29', 'Users_company': 1,
  'Companies_id': 1, 'Companies_name': 'Комфортный дом'}"""            

users = JSONSerializeTable(
    'Users', metadata, 
    Column('id', Integer, primary_key=True), 
    Column('account', String(255)),
    Column('password', PasswordType(schemes=['pbkdf2_sha512'])),
    Column('re_token', String(255)),
    Column('street', String(255)),
    Column('house', String(255)),
    Column('appartment', String(255)),
    Column('company', Integer, ForeignKey('Companies.id')),
    Column('group', Integer, ForeignKey('UsersGroups.id'))
)

companies = Table(
    'Companies', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255))
)

users_groups = Table(
    'UsersGroups', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
)


"""users.db_result_to_json({'Users_id': 1, 'Users_account': '100001001', 'Users_password': 'any', 'Users_token': None, 'Users_re_token': None,
 'Users_street': 'Володина', 'Users_house': '12', 'Users_appartment': '29', 'Users_company': 1,
  'Companies_id': 1, 'Companies_name': 'Комфортный дом'})"""

""""""