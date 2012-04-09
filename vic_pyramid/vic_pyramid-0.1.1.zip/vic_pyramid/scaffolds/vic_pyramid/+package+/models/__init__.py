import transaction
from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
    
def setup_database(global_config, **settings):
    """Setup database
    
    """

    if 'read_engine' not in settings:
        settings['read_engine'] = \
            engine_from_config(settings, 'sqlalchemy.read.')
            
    if 'write_engine' not in settings:
        settings['write_engine'] = \
            engine_from_config(settings, 'sqlalchemy.write.')
    
    if 'read_session_maker' not in settings:
        settings['read_session_maker'] = scoped_session(sessionmaker(
            extension=ZopeTransactionExtension(),
            bind=settings['read_engine']
        ))
        
    if 'write_session_maker' not in settings:
        settings['write_session_maker'] = scoped_session(sessionmaker(
            extension=ZopeTransactionExtension(),
            bind=settings['write_engine']
        ))
    return settings