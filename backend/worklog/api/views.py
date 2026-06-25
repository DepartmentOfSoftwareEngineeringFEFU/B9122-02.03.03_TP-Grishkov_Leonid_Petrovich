from rest_framework import viewsets, permissions
from users.permissions import IsDirector
from worklog.models import WorkLog, WorkEntry
from .serializers import WorkLogSerializer, WorkEntrySerializer


class WorkLogViewSet(viewsets.ModelViewSet):
    serializer_class = WorkLogSerializer

    def get_queryset(self):
        user = self.request.user
        # Директор видит все
        if hasattr(user, 'employee') and user.employee.position.name == 'Директор':
            return WorkLog.objects.all()
        # Сотрудник видит только свои
        if hasattr(user, 'employee'):
            return WorkLog.objects.filter(employee=user.employee)
        return WorkLog.objects.none()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]


class WorkEntryViewSet(viewsets.ModelViewSet):
    queryset = WorkEntry.objects.all()
    serializer_class = WorkEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsDirector]