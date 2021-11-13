from django_filters.views import FilterView
from django_tables2 import SingleTableView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Case, Count, OuterRef, Subquery, When

from courses.filters import CourseFilter
from courses.models import Category, Course
from courses.paginators import CustomPaginator
from courses.serializers import CourseUploadSerializer
from courses.tables import CourseTable
from reviews.models import Review
from schools.models import School


class CourseListView(FilterView, SingleTableView):
    model = Course
    table_class = CourseTable
    template_name = 'courses/index.html'
    filterset_class = CourseFilter
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        category = self.request.GET.get('categories')
        if category:
            try:
                data['category'] = Category.objects.get(pk=int(category))
            except Category.DoesNotExist:
                pass
        data['schools'] = School.objects.all()
        return data

    def get_template_names(self):
        if self.request.is_ajax() or self.request.GET.get('ajax_partial'):
            return 'courses/table.html'
        return super().get_template_names()

    def get_queryset(self):
        return Course.objects.filter(
            status=Course.PUBLIC,
            school__is_active=True,
        ).annotate(
            rewiews_count=Subquery(
                queryset=Review.objects.filter(
                    school=OuterRef('school'),
                ).annotate(
                    reviews_count=Count('id'),
                ).values('reviews_count')[:1]
            ),
            popularity=Case(
                When(
                    rewiews_count__isnull=True,
                    then=0,
                ),
                default='rewiews_count',
            )
        ).order_by('-popularity')


class UploadCourseAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = CourseUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
