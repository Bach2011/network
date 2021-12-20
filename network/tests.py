import unittest
from django.test import TestCase
from network.models import *
# Create your tests here.
user = User.objects.create(username="bach123", password="bach1234")
class NetworkTestcase(TestCase):
    def setUp(self):
        #create Post
        post1 = Post.objects.create(user=user, content="Hi!")

    def test_valid_post(self):
        like = Like.objects.create(like=0, post_id=Post.objects.last().id + 1)
        a = Post.objects.create(user=user, content="Hi!", like=like)
        self.assertTrue(a.is_valid_post())

    def test_invalid_like(self):
        like = Like.objects.create(like=-1, post_id=Post.objects.last().id+1)
        post = Post.objects.create(user=user, content="Hello", like=like)
        self.assertFalse(post.is_valid_post())

    def test_invalid_content(self):
        like = Like.objects.create(like=0, post_id=Post.objects.last().id + 1)
        a = Post.objects.create(user=user, content="", like=like)
        self.assertFalse(a.is_valid_post())