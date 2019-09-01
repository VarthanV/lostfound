from django.urls import path 
from . import views
urlpatterns=[
    path('login/',views.LoginView.as_view()),
    path('register/',views.RegisterView.as_view()),
    path('postlost/',views.LostPostView.as_view()), # This url,if same save in record else pass 
    path('postfound/',views.FoundPostView.as_view()),# This url ,if same save in record else pass 
    path('foundhome/',views.FounderHomeView.as_view()),
    path('losthome/',views.LoserHomeView.as_view()) ,
    path('test/',views.TestView.as_view()),
    path('testing/',views.TestingView.as_view(),name='test')
]
