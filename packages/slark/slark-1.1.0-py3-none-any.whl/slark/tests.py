import os
import random
import unittest
from faker import Faker
from slark import SlarkDB, SlarkObject


fake = Faker()


class TestSum(unittest.TestCase):
    db_name = 'test.json'

    def setUp(self):
        self.db = SlarkDB(self.db_name)

    def tearDown(self):
        os.remove(self.db_name)

    def test_create_db(self):
        SlarkDB(self.db_name)
        self.assertTrue(os.path.exists(self.db_name))

    def test_create_one_user(self):
        user = self.db.table('User').create(name='Ali')
        self.assertTrue(isinstance(user, SlarkObject))
        self.assertEqual(user.data, {'name': 'Ali'})

    def test_count_one_user(self):
        self.db.table('User').create(name='Ali')
        users_count = self.db.table('User').count(name='Ali')
        self.assertEqual(users_count, 1)

    def test_count_n_users(self):
        actual_users_count = random.randint(2, 20)
        for _ in range(actual_users_count):
            self.db.table('User').create(first_name=fake.first_name(), last_name=fake.last_name())
        users_count = self.db.table('User').all()
        self.assertEqual(len(users_count), actual_users_count)

    def test_delete_only_one_user(self):
        self.db.table('User').create(first_name='Ali', last_name='Rn')
        self.db.table('User').delete_one(first_name='Ali')
        users_count = self.db.table('User').all()
        self.assertEqual(len(users_count), 0)

    def test_delete_one_user(self):
        self.db.table('User').create(first_name='Ali', last_name='Rn')
        actual_users_count = random.randint(2, 20)
        for _ in range(actual_users_count):
            self.db.table('User').create(first_name=fake.first_name(), last_name=fake.last_name())
        self.db.table('User').delete_one(first_name='Ali')
        users_count = self.db.table('User').all()
        self.assertEqual(len(users_count), actual_users_count)

    def test_delete_many_users(self):
        self.db.table('User').create(first_name='Ali', last_name='Rn')
        self.db.table('User').create(first_name='Sepehr', last_name='Rn')
        self.db.table('User').create(first_name='Saba', last_name='Rn')
        actual_users_count = random.randint(2, 20)
        for _ in range(actual_users_count):
            self.db.table('User').create(first_name=fake.first_name(), last_name=fake.last_name())
        self.db.table('User').delete_many(last_name='Rn')
        users_count = self.db.table('User').all()
        self.assertEqual(len(users_count), actual_users_count)

    def test_delete_many_users(self):
        self.db.table('User').create(first_name='Ali', last_name='Rn')
        self.db.table('User').create(first_name='Sepehr', last_name='Rn')
        self.db.table('User').create(first_name='Saba', last_name='Rn')
        actual_users_count = random.randint(2, 20)
        for _ in range(actual_users_count):
            self.db.table('User').create(first_name=fake.first_name(), last_name=fake.last_name())
        self.db.table('User').delete_many(last_name='Rn')
        users_count = self.db.table('User').all()
        self.assertEqual(len(users_count), actual_users_count)

    def test_get_one_user(self):
        first_name = f'{fake.first_name()}_Unique'
        last_name = f'{fake.last_name()}_Unique'
        self.db.table('User').create(first_name=first_name, last_name=last_name)

        for _ in range(random.randint(2, 20)):
            self.db.table('User').create(first_name=fake.first_name(), last_name=fake.last_name())

        user = self.db.table('User').get(first_name=first_name)
        self.assertTrue(isinstance(user, SlarkObject))
        self.assertEqual(user.data['first_name'], first_name)
        self.assertEqual(user.data['last_name'], last_name)

    def test_get_only_one_user(self):
        first_name = f'{fake.first_name()}_Unique'
        last_name = f'{fake.last_name()}_Unique'
        self.db.table('User').create(first_name=first_name, last_name=last_name)

        user = self.db.table('User').get(first_name=first_name)
        self.assertTrue(isinstance(user, SlarkObject))
        self.assertEqual(user.data['first_name'], first_name)
        self.assertEqual(user.data['last_name'], last_name)

    def test_filter_one_user(self):
        first_name = f'{fake.first_name()}_Unique'
        last_name = f'{fake.last_name()}_Unique'
        self.db.table('User').create(first_name=first_name, last_name=last_name)

        users = self.db.table('User').filter(first_name=first_name)
        self.assertTrue(isinstance(users, list))
        user = users[0]
        self.assertTrue(isinstance(user, SlarkObject))
        self.assertEqual(user.data['first_name'], first_name)
        self.assertEqual(user.data['last_name'], last_name)

    def test_filter_users(self):
        first_name = f'{fake.first_name()}_Unique'
        last_name = f'{fake.last_name()}_Unique'
        actual_users_count = random.randint(2, 20)
        for _ in range(actual_users_count):
            self.db.table('User').create(first_name=first_name, last_name=last_name)

        for _ in range(random.randint(2, 20)):
            self.db.table('User').create(first_name=fake.first_name(), last_name=fake.last_name())

        users = self.db.table('User').filter(first_name=first_name)
        self.assertTrue(isinstance(users, list))
        self.assertEqual(len(users), actual_users_count)
        user = users[0]
        self.assertTrue(isinstance(user, SlarkObject))
        self.assertEqual(user.data['first_name'], first_name)
        self.assertEqual(user.data['last_name'], last_name)

    def test_all_users(self):
        actual_users_count = random.randint(2, 20)
        for _ in range(actual_users_count):
            self.db.table('User').create(first_name=fake.first_name(), last_name=fake.last_name())

        users = self.db.table('User').all()
        self.assertTrue(isinstance(users, list))
        self.assertEqual(len(users), actual_users_count)

    def test_after_create_update_user(self):
        first_name = f'{fake.first_name()}_Unique'
        user = self.db.table('User').create(first_name=first_name, last_name=fake.last_name())

        user.update(first_name=fake.first_name())
        _user = self.db.table('User').all()[0]
        self.assertNotEqual(_user.data['first_name'], first_name)

    def test_update_normal_user(self):
        first_name = f'{fake.first_name()}_Unique'
        self.db.table('User').create(first_name=first_name, last_name=fake.last_name())
        user = self.db.table('User').get(first_name=first_name)
        user.update(first_name=fake.first_name())
        _user = self.db.table('User').all()[0]
        self.assertNotEqual(_user.data['first_name'], first_name)

    def test_update_one_users_count(self):
        first_name = f'{fake.first_name()}_Unique'
        actual_users_count = random.randint(2, 20)

        for _ in range(actual_users_count):
            self.db.table('User').create(first_name=first_name, last_name=fake.last_name())
        for _ in range(random.randint(2, 20)):
            self.db.table('User').create(first_name=fake.first_name(), last_name=fake.last_name())

        users_count_1 = self.db.table('User').count(first_name=first_name)
        self.assertEqual(users_count_1, actual_users_count)

        self.db.table('User').update_one({'first_name': first_name}, first_name=fake.first_name())
        users_count_2 = self.db.table('User').count(first_name=first_name)
        self.assertEqual(users_count_2, actual_users_count - 1)

    def test_update_one_users_data(self):
        first_name = f'{fake.first_name()}_Unique'
        actual_users_count = random.randint(2, 20)

        for _ in range(actual_users_count):
            self.db.table('User').create(first_name=first_name, last_name=fake.last_name())
        for _ in range(random.randint(2, 20)):
            self.db.table('User').create(first_name=fake.first_name(), last_name=fake.last_name())

        users_count_1 = self.db.table('User').count(first_name=first_name)
        self.assertEqual(users_count_1, actual_users_count)

        new_first_name = fake.first_name()
        result = self.db.table('User').update_one({'first_name': first_name}, first_name=new_first_name)
        self.assertTrue(result)
        updated_user = self.db.table('User').get(first_name=new_first_name)
        self.assertEqual(updated_user.data['first_name'], new_first_name)

    def test_update_many_users(self):
        first_name = f'{fake.first_name()}_Unique'
        actual_users_count = random.randint(2, 20)

        for _ in range(actual_users_count):
            self.db.table('User').create(first_name=first_name, last_name=fake.last_name())
        for _ in range(random.randint(2, 20)):
            self.db.table('User').create(first_name=fake.first_name(), last_name=fake.last_name())

        users_count_1 = self.db.table('User').count(first_name=first_name)
        self.assertEqual(users_count_1, actual_users_count)

        self.db.table('User').update_many({'first_name': first_name}, first_name=fake.first_name())
        users_count_2 = self.db.table('User').count(first_name=first_name)

        self.assertEqual(users_count_2, 0)


if __name__ == '__main__':
    unittest.main()
