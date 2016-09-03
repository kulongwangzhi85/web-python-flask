from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
userprofile = Table('userprofile', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('firstname', String),
    Column('lastname', String),
    Column('email', String),
    Column('picture', String),
    Column('location', String),
    Column('phone', Integer),
    Column('about_me', PickleType),
    Column('about_me_text', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['userprofile'].columns['about_me_text'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['userprofile'].columns['about_me_text'].drop()
