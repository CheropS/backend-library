"""File contains tests for all book api endpoints"""

from tests.base_test import TestHelloBooks
import json

class BookTestCase(TestHelloBooks):
    """Test class for all book api endpoints"""

    def test_get_books(self):
        """Tests get books API endpoint"""
        self._extracted_from_test_get_books_3(404, 1000)
        bad_argument = self.get_book('kk')
        self.assertEqual(bad_argument.status_code, 400)
        add_book = self.add_book(self.book_data)
        self._extracted_from_test_get_books_3(200, 1)

    # TODO Rename this here and in `test_get_books`
    def _extracted_from_test_get_books_3(self, arg0, arg1):
        no_books = self.get_all_books()
        self.assertEqual(no_books.status_code, arg0)
        no_book = self.get_book(arg1)
        self.assertEqual(no_book.status_code, arg0)

    def test_add_book(self):
        """Tests add book api endpoint"""
        empty_book = self.add_book(self.empty_book_data)
        self.assertEqual(empty_book.status_code, 400)
        no_title = self.add_book(self.book_data_no_title)
        self.assertEqual(no_title.status_code, 400)
        no_author = self.add_book(self.book_data_no_author)
        self.assertEqual(no_author.status_code, 400)
        no_isbn = self.add_book(self.book_data_no_isbn)
        self.assertEqual(no_isbn.status_code, 400)
        no_publisher = self.add_book(self.book_data_no_publisher)
        self.assertEqual(no_publisher.status_code, 400)
        no_quantity = self.add_book(self.book_data_no_quantity)
        self.assertEqual(no_quantity.status_code, 400)
        add_book = self.add_book(self.book_data)
        self.assertEqual(add_book.status_code, 201)
        add_book2 = self.add_book(self.book_data)
        self.assertEqual(add_book2.status_code, 409)

    def test_update_book(self):
        """Tests update book api endpoint"""
        self.add_book(self.book_data)
        no_book = self.update_book(self.update_book_data_no_quantity, 100)
        self.assertEqual(no_book.status_code, 404)
        update_empty = self.update_book(self.update_book_data_empty, 1)
        self.assertEqual(update_empty.status_code, 403)
        invalid_args = self.update_book(self.update_book_data, "kk")
        self.assertEqual(invalid_args.status_code, 400)
        no_title = self.update_book(self.update_book_data_no_title, 1)
        self.assertEqual(no_title.status_code, 403)
        no_author = self.update_book(self.update_book_data_no_author, 1)
        self.assertEqual(no_author.status_code, 403)
        no_isbn = self.update_book(self.update_book_data_no_isbn, 1)
        self.assertEqual(no_title.status_code, 403)
        no_publisher = self.update_book(self.update_book_data_no_publisher, 1)
        self.assertEqual(no_publisher.status_code, 403)
        no_quantity = self.update_book(self.update_book_data_no_quantity, 1)
        self.assertEqual(no_quantity.status_code, 403)
        update_book = self.update_book(self.update_book_data, 1)
        self.assertEqual(update_book.status_code, 200)

    def test_delete_book(self):
        """Tests delete book api endpoint"""
        self.add_book(self.book_data)
        no_book = self.delete_book(1000)
        self.assertEqual(no_book.status_code, 404)
        delete_book = self.delete_book(1)
        self.assertEqual(delete_book.status_code, 200)
