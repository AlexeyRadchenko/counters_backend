import sqlalchemy as sa


metadata = sa.MetaData()

users = sa.Table(
    'Users', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('username', sa.String(255)),
    sa.Column('password', sa.String(255)),
    sa.Column('token', sa.String(255)),
    sa.Column('re_token', sa.String(255)),
    sa.Column('street', sa.String(255)),
    sa.Column('house', sa.String(255)),
    sa.Column('appartments', sa.String(255)),
    sa.Column('company', sa.Integer, sa.ForeignKey('Companies.id'))
)

companies = sa.Table(
    'Companies', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(255))
)

tables_list = [users]