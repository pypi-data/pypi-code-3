"""basic tests of lazy loaded attributes"""

from test.lib import testing
from sqlalchemy.orm import mapper, relationship, create_session, immediateload
from test.lib.testing import eq_
from test.orm import _fixtures


class ImmediateTest(_fixtures.FixtureTest):
    run_inserts = 'once'
    run_deletes = None

    def test_basic_option(self):
        Address, addresses, users, User = (self.classes.Address,
                                self.tables.addresses,
                                self.tables.users,
                                self.classes.User)

        mapper(Address, addresses)
        mapper(User, users, properties={
            'addresses':relationship(Address)
        })
        sess = create_session()

        l = sess.query(User).options(immediateload(User.addresses)).filter(users.c.id==7).all()
        eq_(len(sess.identity_map), 2)

        sess.close()

        eq_(
            [User(id=7, addresses=[Address(id=1, email_address='jack@bean.com')])],
            l
        )


    def test_basic(self):
        Address, addresses, users, User = (self.classes.Address,
                                self.tables.addresses,
                                self.tables.users,
                                self.classes.User)

        mapper(Address, addresses)
        mapper(User, users, properties={
            'addresses':relationship(Address, lazy='immediate')
        })
        sess = create_session()

        l = sess.query(User).filter(users.c.id==7).all()
        eq_(len(sess.identity_map), 2)
        sess.close()

        eq_(
            [User(id=7, addresses=[Address(id=1, email_address='jack@bean.com')])],
            l
        )


