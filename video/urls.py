from django.urls import path
# from .views import upload_video
from .views import UploadVideoView, SearchView

urlpatterns = [
    path('upload/', UploadVideoView.as_view(), name='upload'),
    # path('upload/', upload_video, name='upload_video'),
    path('search/', SearchView.as_view(), name='search'),
]
