import pytest

# First party modules
from api.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        
        yield client
        

        
# @pytest.fixture(scope='function')
# def db_session(db, request):
#     """Creates a new database session for a test."""
#     engine = create_engine(
#                             DefaultConfig.SQLALCHEMY_DATABASE_URI,
#                             connect_args={"options": "-c timezone=utc"})
#     DbSession = sessionmaker(bind=engine)
#     session = DbSession()
#     connection = engine.connect()
#     transaction = connection.begin()
#     options = dict(bind=connection, binds={})
#     session = db.create_scoped_session(options=options)
#     db.session = session

#     yield session

#     transaction.rollback()
#     connection.close()
#     session.remove()

