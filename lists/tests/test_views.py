from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item,List


class HomePageTest(TestCase):


	def test_root_url_resolves_to_homepage_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_homepage_returns_correct_html(self):
		request = HttpRequest()

		response = home_page(request)

		expected_html = render_to_string('home.html', request = request)
		# print expected_html
		self.assertEqual(response.content.decode(), expected_html)

		

class ListViewTest(TestCase):

	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' %(list_.id,))
		self.assertTemplateUsed(response, 'list.html')


	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		
		Item.objects.create(text = 'first', list = correct_list)
		Item.objects.create(text = 'second', list = correct_list)

		other_list = List.objects.create()

		Item.objects.create(text = 'third', list = other_list)
		Item.objects.create(text = 'fourth', list = other_list)


		
		response = self.client.get('/lists/%d/' %(correct_list.id,))
		
		self.assertContains(response, 'first')
		self.assertContains(response,'second')
		self.assertNotContains(response, 'third')
		self.assertNotContains(response,'fourth')

	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.get('/lists/%d/' %(correct_list.id,))
				
		self.assertEqual(response.context['list'], correct_list)

	def test_can_save_a_post_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			'/lists/%d/' %(correct_list.id,),
			data = {'item_text': 'A new item for an existing list'})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_post_redirects_to_list_view(self):

		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			'/lists/%d/' %(correct_list.id,),
				data = {'item_text': 'A new item for an existing list'})

		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))




class NewListTest(TestCase):

	def test_saving_a_post_request(self):
		self.client.post(
			'/lists/new',
			data = {'item_text': 'A new list item'})

		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

		
	def test_redirects_after_post(self):
		response = self.client.post(
			'/lists/new',
			data = {'item_text':'A new list item'})
		new_list = List.objects.first()

		self.assertRedirects(response, '/lists/%d/' %(new_list.id,))

	def test_validation_errors_are_sent_back_to_home_page_template(self):
		response = self.client.post('/lists/new', data = {'item_text':''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
		expected_error = "You cannot have an empty list item"
		self.assertContains(response, expected_error)

	def test_invalid_list_items_arent_saved(self):
		self.client.post('/lists/new', data = {'item_text':''})
		self.assertEqual(List.objects.count(), 0)
		self.assertEqual(Item.objects.count(), 0)