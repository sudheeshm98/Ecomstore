from django.urls import path
from . import views
from .views import BookList, BookDetail, BookCheckoutView, PaymentComplete, SearchResultsView, cart

urlpatterns = [
    path("search/", SearchResultsView.as_view(), name="search-results"),
    path('', BookList.as_view(), name='list'),
    path('details/<int:pk>', BookDetail.as_view(), name='details'),
    path('checkout/<int:pk>/', BookCheckoutView.as_view(), name='checkout'),
    path('complete/', PaymentComplete, name='complete'),
    path('cart/', cart, name='mycart'),
    path("cart/add/<int:book_id>", views.add_to_cart, name="add-to-cart"),
    path("cart/remove/<int:book_id>/", views.remove_from_cart, name="remove-from-cart")
]