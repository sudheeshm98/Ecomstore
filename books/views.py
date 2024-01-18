from decimal import Decimal

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from .models import Book, Order, Cart, CartItem


# Create your views here.

def home(request):
    return render(request, 'home.html')


class SearchResultsView(ListView):
    model = Book
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__contains=query) | Q(author__contains=query)
        )


class BookList(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'list.html'


class BookDetail(DetailView):
    model = Book
    fields = '__all__'
    template_name = 'detail.html'


class BookCheckoutView(DetailView):
    model = Book
    template_name = 'checkout.html'
    

def PaymentComplete(request, pk):
    product = Book.objects.get(id=pk)
    Order.objects.create(
        product=product
    )
    return JsonResponse('payment completed', safe = False)


@login_required
def cart(request):
    cart_qs = Cart.objects.filter(user=request.user)
    total = 0.0
    if cart_qs.exists():
        cart_obj = cart_qs.first()
        cart_items = CartItem.objects.filter(cart=cart_obj)

        for cart_item in cart_items:
            total += cart_item.total_price()

    else:
        cart_obj = None
        cart_items = []

    context = {
        'cart' : cart_obj,
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'mycart.html', context)


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_qs = Cart.objects.filter(user=request.user)
    if cart_qs.exists():
        cart_obj = cart_qs.first()
    else:
        cart_obj = Cart.objects.create(user=request.user, total_price=Decimal('0.00'))

    cart_item, created = CartItem.objects.get_or_create(book=book, cart=cart_obj)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    cart_obj.total_price += Decimal(str(book.price))
    cart_obj.save()
    return redirect('mycart')


@login_required
def remove_from_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_qs = Cart.objects.filter(user=request.user)

    if cart_qs.exists():
        cart_obj = cart_qs.first()
        cart_item_qs = CartItem.objects.filter(book=book, cart=cart_obj)

        if cart_item_qs.exists():
            cart_item = cart_item_qs.first()
            if cart_item.quantity >= 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

            cart_obj.total_price -= Decimal(str(book.price))
            cart_obj.save()

    return redirect('mycart')
