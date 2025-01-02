"""
URL configuration for web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls,name="adminDjango"),
    path('',views.get_home,name='home'),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout,name="logout"),
    path("postsignin/",views.login,name="postsignin"),
    path("signup/",views.signup_view,name="signup"),
    path("products/",views.products_view,name="homeListProduct"),
    path("products/male",views.products_view_male,name="homeListProductMale"),
    path("products/female",views.products_view_female,name="homeListProductFemale"),
    path("user/info/",views.view_info_user,name="infoUser"),
    path("cart/",views.view_cart,name="cartView"),
    path("user/update-info/",views.update_info_user,name="updateInfoUser"),
    path("user/list-order/",views.list_order,name="listOrder"),
    path("user/detail-order/<str:invoice_id>/",views.detail_order,name="detailOrder"),
    path("postsignup",views.postsignup,name="postsignup"),
    path('admin-view/', views.view_admin,name="adminView"),
    path('staff-view/', views.view_staff,name="staffView"),
    path('admin-view/list-user', views.view_list_user,name="listUser"),
    path("admin-view/list-product",views.view_list_product,name="listProduct"),
    path("admin-view/add-product",views.view_add_product,name="viewAddProduct"),
    path("admin-view/post-add-product",views.post_add_product,name="postAddProduct"),
    path("delete-product/<str:product_id>/", views.delete_product,name="deleteProduct"),
    path("update-product/<str:product_id>/", views.update_product_view,name="updateProductView"),
    path("post-update-product/<str:product_id>/", views.update_product,name="updateProduct"),
    path("delete-user/<str:user_id>/", views.delete_user,name="deleteUser"),
    path("product/<str:product_id>/", views.product_detail,name="productDetail"),
    path("add-cart/<str:product_id>/", views.add_cart,name="addCart"),
    path("cart/increase-quantity/<str:product_id>/", views.increaseQuantity,name="increaseQuantity"),
    path("cart/decrease-quantity/<str:product_id>/", views.decreaseQuantity,name="decreaseQuantity"),
    path("cart/delete-product/<str:product_id>/", views.deleteProductCart,name="decreaseQuantity"),
    path("pay/<str:user_id>/", views.saveInvoice,name="saveInvoice"),
    path("decentralization/<str:user_id>/",views.decentralization,name="decentralization"),
    path("detail-invoice/<str:invoice_id>/",views.detailInvoice,name="detailInvoice"),
    path("reject-invoice/<str:invoice_id>/",views.rejectInvoice,name="rejectInvoice"),
    path("accept-invoice/<str:invoice_id>/",views.acceptInvoice,name="acceptInvoice"),
    path("cancel-invoice/<str:invoice_id>/",views.cancelInvoice,name="cancelInvoice")
]