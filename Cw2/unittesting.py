import os
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models, forms

class Unittesting(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        #the basedir lines could be added like the original db
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        pass

    def test_user_model(self):
        user = models.UserModel("Tadas", "Tadas123", "SomeURL")

        db.session.add(user)
        db.session.commit()

        dbUser = models.UserModel.query.filter_by(username="Tadas").first()

        assert dbUser is not None
        assert dbUser.username == "Tadas" 
        assert dbUser.password == "Tadas123"
        assert dbUser.image_url == "SomeURL"

    def test_recipe_model(self):
        user = models.UserModel("Ponas", "Ponas123", "SomeURL")
        db.session.add(user)
        db.session.commit()

        recipe = models.RecipeModel("Cake", "{Flour|500g.}{Sugar|10g.}", "Just bake it", "SomeURL", user.id)

        db.session.add(recipe)
        db.session.commit()

        dbUser = models.UserModel.query.filter_by(username="Ponas").first()
        dbRecipe = dbUser.recipes[0]

        assert dbRecipe is not None
        assert dbRecipe.name == "Cake" 
        assert dbRecipe.ingrediants == "{Flour|500g.}{Sugar|10g.}"
        assert dbRecipe.instructions == "Just bake it"
        assert dbRecipe.image_url == "SomeURL"

    def test_user_favorites(self):
        user = models.UserModel("Kodas", "Kodas123", "SomeURL")
        db.session.add(user)
        db.session.commit()

        recipe = models.RecipeModel("Giraffe", "{Flour|500g.}{Sugar|10g.}", "Just bake it", "SomeURL", user.id)

        db.session.add(recipe)
        db.session.commit()

        dbUser = models.UserModel.query.filter_by(username="Kodas").first()
        dbUser.favorites.append(recipe)
        db.session.commit()

        firstFollower = recipe.followers[0]

        assert firstFollower.username == user.username

    def test_index(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_user_registration(self):
        response = self.register('Tadas', 'FlaskIsAwesome', 'FlaskIsAwesome', 'SomeURL', True)
        self.assertEqual(response.status_code, 200)

    def test_valid_user_login(self):
        user = models.UserModel("Kodas", "Kodas123", "SomeURL")
        db.session.add(user)
        db.session.commit()

        response = self.login('Kodas', 'Kodas123')
        self.assertEqual(response.status_code, 200)

    def test_valid_user_login(self):
        user = models.UserModel("Kodas", "Kodas123", "SomeURL")
        db.session.add(user)
        db.session.commit()

        self.login('Kodas', 'Kodas123')

        response = self.logout()

        self.assertEqual(response.status_code, 200)


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def register(self, username, password, confirmPassword, profileUrl, terms):
        return self.app.post(
        '/register',
        data=dict(username=username, password=password, confirmPassword=confirmPassword, profileUrl = profileUrl, terms = terms),
        follow_redirects=True
        )
        
    def login(self, username, password):
        return self.app.post(
        '/login',
        data=dict(username=username, password=password),
        follow_redirects=True
        )
        
    def logout(self):
        return self.app.get(
        '/logout',
        follow_redirects=True
        )

if __name__ == "__main__":
    unittest.main()