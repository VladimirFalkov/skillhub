from django_filters.views import FilterView

from django_tables2 import SingleTableView
import pymorphy2
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Count, F
from django.http import Http404
from django.views.generic import DetailView
from django.utils.html import format_html

from core.models import AllCoursesPageConfig
from courses.filters import CourseFilter
from courses.models import Category, Course
from courses.paginators import CustomPaginator
from courses.serializers import CourseUploadSerializer
from courses.tables import CourseTable
from schools.models import School


morph = pymorphy2.MorphAnalyzer(lang='ru')


class CourseListView(FilterView, SingleTableView):
    model = Course
    table_class = CourseTable
    template_name = 'courses/index.html'
    filterset_class = CourseFilter
    paginator_class = CustomPaginator
    paginate_by = 10

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        slug = self.request.resolver_match.kwargs.get('slug')
        if slug:
            try:
                category = Category.objects.get(slug=slug)
                data['category'] = category
                data['meta'] = category.as_meta(self.request)
            except Category.DoesNotExist:
                pass
        else:
            config = AllCoursesPageConfig.get_solo()
            data['config'] = config
            data['meta'] = config.as_meta(self.request)

        data['schools'] = School.objects.all()

        return data

    def get_template_names(self):
        if self.request.is_ajax() or self.request.GET.get('ajax_partial'):
            return 'courses/table.html'
        return super().get_template_names()

    def get_queryset(self):
        qs = Course.objects.filter(
            status=Course.PUBLIC,
            school__is_active=True,
        ).annotate(
            popularity=Count('school__reviews', distinct=True) + (F('id')*0.1),
        )

        slug = self.request.resolver_match.kwargs.get('slug')

        if slug:
            try:
                category = Category.objects.get(slug=slug)
                categories = category.get_descendants(include_self=True)
                qs = qs.filter(categories__in=categories).distinct()
            except Category.DoesNotExist:
                raise Http404()

        return qs


class CourseDetailView(DetailView):
    model = Course
    context_object_name = 'course'
    slug_url_kwarg = 'slug'
    template_name = 'courses/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        rating_points = course.school.rating or 0
        rating_points_style = 'low-rating' if rating_points < 4 else 'high-rating'
        rating_icon_style = 'low-rating-icon' if rating_points < 4 else 'high-rating-icon'
        rating_icon = f'<span class="{rating_icon_style}"></span>'
        rating_tag = f'<span class="{rating_points_style}">{rating_points}</span>'
        rating = f'{rating_icon}{rating_tag}' if rating_points else ''
        rating_html = format_html(f'{course.school.name}{rating}')

        price_html = course.price_formatted

        duration_type = dict(Course.DURATION_TYPE)[course.duration_type].lower()
        duration_type = morph.parse(duration_type)[0]
        duration_type = duration_type.make_agree_with_number(course.duration).word
        duration_html = f'{course.duration} {duration_type}'

        context['rating_html'] = rating_html
        context['price_html'] = price_html
        context['duration_html'] = duration_html

        return context



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
