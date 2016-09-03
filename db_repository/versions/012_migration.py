from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
systemsettings = Table('systemsettings', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('websitename', String),
    Column('images', String),
    Column('picture', String),
    Column('icon', String),
    Column('about_website', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['systemsettings'].columns['about_website'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['systemsettings'].columns['about_website'].drop()