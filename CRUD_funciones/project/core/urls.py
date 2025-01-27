from django.urls import path
# importamos las vistas
from .views import confirmation_email, person_data, lists_person, updated_person, delete_person, password_updated

# lista de urls
urlpatterns = [
    path('lists_person/', lists_person, name='lists_person'),
    path('formulary/', confirmation_email, name='confirmation_emial'),
    path('person_data/<int:id>/', person_data, name='person_data'),
    path('updated/<int:updated_id>/', updated_person, name='updated_person'),
    path('password_updated/<int:updated_id>/', password_updated, name='password_updated'),
    path('delete_person/<int:id>/', delete_person, name='delete_person'),
]