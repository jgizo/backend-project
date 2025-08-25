from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db.models import Q
from django.http import HttpResponse
from .models import FileRecord
from minio import Minio
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User

minio_client = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)

BUCKET_NAME = "project-files"

class FileListView(LoginRequiredMixin, ListView):
    model = FileRecord
    template_name = "files/file_home.html"
    context_object_name = "files"

    def get_queryset(self):
        return FileRecord.objects.filter(
            Q(owner=self.request.user) | Q(shared_with=self.request.user)
        ).order_by('-timestamp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(id=self.request.user.id)
        return context

@login_required
def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        minio_path = f"{request.user.username}/{uploaded_file.name}"

        minio_client.put_object(
            BUCKET_NAME,
            minio_path,
            uploaded_file,
            uploaded_file.size
        )

        file_record = FileRecord.objects.create(
            owner=request.user,
            file_name=uploaded_file.name,
            minio_path=minio_path
        )

        shared_user_ids = request.POST.getlist("shared_with")
        if shared_user_ids:
            shared_users = User.objects.filter(id__in=shared_user_ids)
            file_record.shared_with.add(*shared_users)

        return redirect("file_home")
    
    users = User.objects.exlude(id=request.user.id)
    return render(request, "files/file_home.html", {"users": users})

@login_required
def download_file(request, pk):
    file = get_object_or_404(FileRecord, pk=pk)
    if file.owner != request.user and request.user not in file.shared_with.all() and request.user.role != 'admin':
        return HttpResponse("Access denied", status=403)
    
    obj = minio_client.get_object(BUCKET_NAME, file.minio_path)
    data = obj.read()
    obj.close()
    obj.release_conn()

    response = HttpResponse(data, content_type='application/octlet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file.file_name}"'
    return response

@login_required
def delete_file(request, pk):
    file = get_object_or_404(FileRecord, pk=pk)
    if file.owner != request.user and request.user.role != 'admin' and not request.user.is_superuser:
        return HttpResponse("Access denied", status=403)

    minio_client.remove_object(BUCKET_NAME, file.minio_path)
    file.delete()
    return redirect("file_home")
