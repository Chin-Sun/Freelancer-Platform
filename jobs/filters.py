import django_filters
from django_filters import CharFilter
from .models import *


class BusinessFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Business
        fields = ['name']

class FreelancerFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    skills = CharFilter(field_name='skills', lookup_expr='icontains')
    class Meta:
        model = Freelancer
        fields = ['name', 'skills']


class ProjectFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Project
        fields = ['name', 'owner', 'category', 'programming_languages']