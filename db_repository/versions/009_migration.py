from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
postcategory = Table('postcategory', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('small', String),
    Column('image', String),
    Column('manager', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['postcategory'].columns['manager'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['postcategory'].columns['manager'].drop()
