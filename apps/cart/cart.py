from django.conf import settings


from apps.product.models import Product


class Cart():
    """_summary_
        The Cart Session Class
    """
    def __init__(self, request):
        """_summary_
            search the session stored in request.session for dict(cart_session_id)
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterates over the Cart session id got to get individual product

        """
        for id in self.cart.keys():
            self.cart[str(id)]['product'] = Product.objects.get(pk=id)

        for item in self.cart.values():

            item['total_price'] = item['product'].price * item['quantity']
            yield item

    def __len__(self) -> float:
        """
        A return sum of the quantity of the of items in the cart session
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product_id: str, quantity=1, update_quantity=False):
        """_summary_

        Args:
            product_id (str): _description_
            quantity (int, optional): _description_. Defaults to 1.
            update_quantity (bool, optional): _description_. Defaults to False.

        Adds and Update the cart session on the fly
        """
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity,
                                     'id': product_id
                                    }

        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)

            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
        self.save()

    def remove(self, product_id):


        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

