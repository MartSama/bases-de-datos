"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    
    path('personal/', views.personal, name='personal'), # PERSONAL #
    path('propietarios/', views.propietarios, name='propietarios'), # PROPIETARIOS #
    path('mascotas/', views.mascotas, name='mascotas'),  # MASCOTAS #
    path('expedientes/', views.expedientes, name='expedientes'),  # EXPEDIENTES #
    path('proveedores/', views.proveedores, name='proveedores'), # PROVEEDORES #
    path('inventario/', views.inventario, name='inventario'), # INVENTARIO #
    path('nomina/', views.nomina, name='nomina'), #NOMINA #
    path('recetasMedicas/', views.recetasMedicas, name='recetasMedicas'), # RECETAS #
    path('ventas/', views.ventas, name='ventas'), # VENTAS #
    
    
    # Otras rutas aquí...
    path('tasks/all_tasks/', views.task_manager, name='task_manager'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('pet/', views.pet_page, name='pet_page'),### PET ###
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),

    #
    path('personals_view/', views.personals_view, name='personals_view'),### Personal SQL ###
    path('nomina_s/', views.nomina_s, name='nomina_s'),                 ### Nomina SQL ###
    path('propietarios_s/', views.propietarios_s, name='propietarios_s'),### Propietarios SQL ###
    path('proveedores_s/', views.proveedores_s, name='proveedores_s'),### Proveedores SQL ###
    path('inventario_s/', views.inventario_s, name='inventario_s'), ### Inventario ###
    path('proveedores_productos_s/', views.proveedores_productos_s, name='proveedores_productos_s'), ### ProveedoresProductos ###
    path('mascotas_s/', views.mascotas_s, name='mascotas_s'),  ### Mascotas SQL ###
    path('expedientes_s/', views.expedientes_s, name='expedientes_s'),  ### EXPEDIENTES SQL ###
    path('recetasMedicas_s/', views.recetasMedicas_s, name='recetasMedicas_s'), ### RECETAS SQL ###
    path('ventas_s/', views.ventas_s, name='ventas_s'), ### VENTAS SQL ###


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
