from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'sedes', SedeViewSet)
router.register(r'planes', PlanViewSet)
router.register(r'roles', RolViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'galerias-sede', GaleriaSedeViewSet)
router.register(r'testimonios', TestimonioViewSet)
router.register(r'usuario-planes', UsuarioPlanViewSet, basename='usuarioplan')
router.register(r'pagos', PagoViewSet, basename='pago')
router.register(r'pre-inscripciones', PreInscripcionViewSet)
router.register(r'tipos-entrenamiento', TipoEntrenamientoViewSet)
router.register(r'comodidades', ComodidadViewSet)
router.register(r'ejercicios', EjercicioViewSet)
router.register(r'rutinas', RutinaViewSet)
router.register(r'rutina-ejercicios', RutinaEjercicioViewSet)
router.register(r'usuario-rutinas', UsuarioRutinaViewSet)
router.register(r'alimentos', AlimentoViewSet)
router.register(r'dietas', DietaViewSet)
router.register(r'dieta-alimentos', DietaAlimentoViewSet)
router.register(r'usuario-dietas', UsuarioDietaViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
