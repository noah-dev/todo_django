from django.conf.urls import url

from . import views

app_name = 'todo'
urlpatterns = [
    # url(r'^$', views.IndexView.as_view(), name='generic_index'),
    # url(r'^ajax/$', views.IndexView.ajax(), name='generic_index'),

    url(r'^$', views.index, name='index'),
    url(r'^show_item/$', views.show_item, name='show_item'),
    url(r'^add_item/$', views.add_item, name='add_item'),
    url(r'^complete_item/$', views.complete_item, name='complete_item'),
    url(r'^delete_item/(?P<item_id>\d+)/$', views.delete_item, name='delete_item'),
    url(r'^test_add/$', views.test_add, name="test_add"),
]
