from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views.home import Index
from .views.signup import Signup
from .views.login import Login,logout
from .views.forgetPassword import ForgetPassword
from .views.verifyOtp import VeryfyOTP
from .views.resetPassword import ResetPassword
from .views.userProfile import UserProfile
from .views.products import product
from .views.productDetail import product_detail
from .views.cart import add_to_cart,Remove_From_Cart,increment_quantity,decrement_quantity,cart_view,Cart_Totle_Count,clear_cart
from .views.cart_count import Cart_Count
# from .views.wishlist import Wishlist,add_to_wishlist,remove_from_wishlist,Wishlist_Count
from .views.wishlist import  Wishlist,add_to_wishlist,remove_from_wishlist,clear_wishlist,add_to_cart_wishlist
from .views.wishlist_count import Wishlist_Count
from .views.checkout_page import Chckout_Page,Checkout_View
from .views.blog import blog_view
from EcommApp.views.blogdetails import blog_details_view
from EcommApp.views.about import About_us
from EcommApp.views.contact import Contact
urlpatterns = [
    path("",Index.as_view(),name='home'),
    path("signup",Signup.as_view(),name='signup'),
    path("login",Login.as_view(),name='login'),
    path("logout",logout,name='logout'),
    path("forget-password",ForgetPassword.as_view(),name="forgetpassword"),
    path("verify-otp", VeryfyOTP.as_view(), name="verifyotp"), 
    path("reset-password", ResetPassword.as_view(), name="resetpassword"),
    path("user-profile", UserProfile.as_view(), name="userprofile"),
    path("products", product, name="product"),  
    path("product/<int:product_id>/", product_detail, name="product_detail"), 
# Add to cart from general product view
path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),

# Add to cart from wishlist
path("wishlist/cart/add/<int:product_id>/", add_to_cart_wishlist, name="add_to_cart_wishlist"),

    path("cart/remove/<int:product_id>/", Remove_From_Cart, name="remove_from_cart"),  
    path("cart/increment/<int:product_id>/", increment_quantity, name="cart_increment"),  
    path("cart/decrement/<int:product_id>/", decrement_quantity, name="cart_decrement"),
    path("cart", cart_view, name="cart_view"), 
    path("cartcount/", Cart_Count, name="Cart_Count"), 
    path("cart/total/", Cart_Totle_Count, name="cart_total"), 
    path('clear-cart/', clear_cart, name='clear_cart'), 
    path("wishlist",Wishlist,name='wishlist'),
    path("wishlist/add/<int:product_id>/",add_to_wishlist,name="add_to_wishlist"),
    path("wishlist/remove/<int:product_id>/",remove_from_wishlist,name="remove_from_wishlist"),
    path('wishlist/clear/', clear_wishlist, name='clear_wishlist'),
    path("wishlistcount/", Wishlist_Count, name="Wishlist_Count"),
    path("checkout_page", Chckout_Page, name="checkout_page"), 
    path("checkout/process", Checkout_View, name="checkout_view"), 
    path('blog/', blog_view, name='blog'),
    path('blog/<int:id>/', blog_details_view, name='blog_details'),
    path('about-us/', About_us, name='about_us'),
    path('contact/',Contact, name='contact'),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)