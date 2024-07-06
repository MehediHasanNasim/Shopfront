from django.urls import path
from .import views

'''--------Class-based view'''
'''--------Function-based view'''
urlpatterns = [
    path('products/',  views.ProductList.as_view()),
    path('products/<int:id>/',  views.ProductDetail.as_view()),



    # path('products/',  views.product_list),
    # path('products/<int:id>/',  views.product_detail),
    path('collections/',  views.collection_list),
    path('collections/<int:pk>/',  views.collection_detail, name='collection-detail'),

]
