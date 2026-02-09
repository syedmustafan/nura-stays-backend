"""
Views for Team app.
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import TeamMember
from .serializers import TeamMemberSerializer


# ─── Public Views ────────────────────────────────────────────────────────────

class TeamMemberListView(generics.ListAPIView):
    """List all team members."""
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [AllowAny]
    pagination_class = None


# ─── Admin Views ─────────────────────────────────────────────────────────────

class AdminTeamMemberListCreateView(generics.ListCreateAPIView):
    """Admin: list all team members or create a new one."""
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]


class AdminTeamMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: retrieve, update, or delete a team member."""
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
