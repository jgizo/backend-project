from django.urls import path
from .views import FileListView, upload_file, download_file, delete_file

urlpatterns = [
    path("", FileListView.as_view(), name="file_home"),
    path("upload/", upload_file, name="file-upload"),
    path("download/<int:pk>/", download_file, name="file-download"),
    path("delete/<int:pk>/", delete_file, name="file-delete"),
]
