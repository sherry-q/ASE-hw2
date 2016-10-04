import os
import unittest

from shopping_list import app, db
from shopping_list import shopping_list

class MyTest(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_make_list(self):
		l1 = shopping_list(name='test1', quantity='1')
		db.session.add(l1)
		db.session.commit()

		assert l1 in db.session

	def test_remove_list(self):
		l2 = shopping_list(name='test2', quantity='2')
		db.session.add(l2)
		db.session.commit()

		assert l2 in db.session

		db.session.delete(l2)
		db.session.commit()

		testname = 'test2'

		q = shopping_list.query.filter_by(name=testname).first()

		assert q is None

	def test_not_exist(self):
		l3 = shopping_list(name='test3', quantity='1')
		db.session.add(l3)
		db.session.commit()

		assert l3 in db.session
		testname = 'test100'

		q = shopping_list.query.filter_by(name=testname).first()

		assert q is None

if __name__ == '__main__':
	unittest.main()
	session.close()