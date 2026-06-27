from rest_framework import viewsets, permissions
from files.models import File
from .serializers import FileSerializer
from users.permissions import IsDirector
from rest_framework.decorators import action

class FileViewSet(viewsets.ModelViewSet):
    # queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated, IsDirector]

    def get_queryset(self):
        qs = File.objects.all()
        content_type = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')
        if content_type:
            qs = qs.filter(content_type__model=content_type)
        if object_id:
            qs = qs.filter(object_id=object_id)
        return qs

    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        file_obj = self.get_object()
        from django.http import FileResponse
        return FileResponse(file_obj.file.open('rb'), as_attachment=True, filename=file_obj.original_name)
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)