from django.conf import settings
from product.models import Product


class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            # save an empty cart in the session
            cart = self.session['cart'] = {}
        self.cart = cart

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_slug = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(slug=product_slug)
        for product in products:
            self.cart[product.slug]['product'] = product

        for item in self.cart.values():
            item['price'] = item['price']
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, product_slug, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        if product_slug not in self.cart:
            self.cart[product_slug] = {'quantity': 1}
        print(self.cart)
        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_slug = product.slug
        if product_slug in self.cart:
            del self.cart[product_slug]
            self.save()

    def save(self):
        # update the session cart
        self.session['cart'] = self.cart
        print(self.session['cart'])

    def clear(self):
        # empty cart
        self.session['cart'] = {}
        self.session.modified = True

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

