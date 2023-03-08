from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.CarListView.as_view(), name='cars'),
    path('car/<int:pk>', views.CarDetailView.as_view(), name='car'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order'),
    path('my/cars', views.UserCarListView.as_view(), name='user_cars'),
    path('my/car/new/', views.UserOrderCreateView.as_view(), name='user_order_create'),
    path('my/car/<int:pk>/update/', views.UserOrderUpdateView.as_view(), name='user_order_update'),
    path('my/order/comment/<int:pk>/delete/', views.UserCommentDeleteView.as_view(), name='user_comment_delete'),
    path('data/', views.car_model_data, name='data'),
]