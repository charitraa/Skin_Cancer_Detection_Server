from django.urls import path
from core.views import PredictSkinCancerView , LoginView, UserAllDetailView, UserUpdateView ,UserCreateView, UserMeView

urlpatterns = [
    path('predict/', PredictSkinCancerView.as_view(), name='predict_skin_cancer'),  # New endpoint
    path('auth/', UserCreateView.as_view(), name='user_create'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('user/all/', UserAllDetailView.as_view(), name='user_detail'),
    path('user/update/', UserUpdateView.as_view(), name='user_update'),
    path('user/me/', UserMeView.as_view(), name='user_me'),
]
