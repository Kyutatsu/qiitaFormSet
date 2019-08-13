from django.urls import path
from first import views


app_name = 'first'
urlpatterns = [
        path('', views.make_test_formset, name='test1'),
        path('modelformset_1/', views.make_test_modelformset,
                                                name='model1'),
        path('diff_form/', views.make_diff_type_forms,
                                                name='diff'),
        path('multiple/', views.make_multiple_formsets,
                                                name='mul'),
        path('author/<int:pk>/', views.AuthorDetailView.as_view(),
                                            name='author'),
        path('inline/<int:author_id>/', views.make_inline_formset, 
                                            name='inline'),
]
