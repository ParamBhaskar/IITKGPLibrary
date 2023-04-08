from django.urls import path
from . import views

urlpatterns = [
    path('f_p/', views.f_p, name="f_p"),
    path('send_otp', views.send_otp, name='send_otp'),
    path('enter_otp', views.enter_otp, name='enter_otp'),
    path("forgot_password/", views.forgot_password, name="forgot_password"),

    path("", views.index, name="index"),
    path("login/", views.login_karo, name="login"),
    path("login/reg/", views.reg, name="reg"),
    # path("login/clerk_login/", views.clerk_login, name="clerk_login"),
    # path("registration/", views.registration, name="registration"),
    # path("student_login/", views.student_login, name="student_login"),

    path("afterlogin/", views.afterlogin, name="afterlogin"),

    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("add_book/", views.add_book, name="add_book"),
    # path("issue_book/", views.issue_book, name="issue_book"),
    path("view_issued_book/", views.view_issued_book, name="view_issued_book"),
    # path("student_issued_books/", views.student_issued_books, name="student_issued_books"),
    path("logout/", views.Logout, name="logout"),
    
    # path("list_books/", views.list_books, name="list_books"),

    path("view_books/", views.view_books, name="view_books"),
    path("view_issued_book/", views.view_issued_book, name="view_issued_book"),
    path("change_password/", views.change_password, name="change_password"),
    path("delete_book/<int:myid>/", views.delete_book, name="delete_book"),
    path("edit_book/<int:myid>/", views.edit_book, name="edit_book"),

    path("issue_book/<int:myid>/", views.issue_book, name="issue_book"),
    path("reserve_book/<int:myid>/", views.reserve_book, name="reserve_book"),
    path("return_book/<int:myid>/", views.return_book, name="return_book"),
    
    path("reminder/",views.reminder, name = "reminder"),

    path("contact/", views.contact, name="contact"),
    path("payment/", views.payment, name="payment"),
    path("bill/", views.bill, name="bill")

]