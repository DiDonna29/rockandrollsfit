from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.db import IntegrityError
import secrets
import string
from .models import *
from .serializers import *

class SedeViewSet(viewsets.ModelViewSet):
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer
    permission_classes = [AllowAny]

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [AllowAny]

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.user.is_anonymous:
            return Response({'error': 'No autorizado'}, status=401)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def recuperar_contrasena(self, request):
        mode = request.data.get('mode') # 'verificar' o 'restablecer'
        email = request.data.get('email')
        cedula = request.data.get('cedula')
        
        if not email or not cedula:
            return Response({'error': 'Email y Cédula son requeridos'}, status=400)
            
        try:
            usuario = Usuario.objects.get(email=email, cedula_identidad=cedula)
            
            if mode == 'verificar':
                # Solo confirmamos identidad
                return Response({
                    'status': 'verified',
                    'message': f'Identidad confirmada para {usuario.first_name}. Puedes proceder al cambio.'
                })
            
            elif mode == 'restablecer':
                nueva_clave = request.data.get('nueva_password')
                if not nueva_clave:
                    return Response({'error': 'La nueva contraseña es requerida'}, status=400)
                
                usuario.set_password(nueva_clave)
                usuario.save()
                return Response({
                    'status': 'success',
                    'message': '¡Contraseña actualizada con éxito! Ya puedes iniciar sesión con tu nuevo poder. 🎸'
                })
            
            return Response({'error': 'Modo de operación no válido'}, status=status.HTTP_400_BAD_REQUEST)
            
        except Usuario.DoesNotExist:
            return Response({'error': 'Los datos no coinciden con nuestros registros del gimnasio.'}, status=404)

class GaleriaSedeViewSet(viewsets.ModelViewSet):
    queryset = GaleriaSede.objects.all()
    serializer_class = GaleriaSedeSerializer
    permission_classes = [AllowAny]

class TestimonioViewSet(viewsets.ModelViewSet):
    queryset = Testimonio.objects.all()
    serializer_class = TestimonioSerializer
    permission_classes = [AllowAny]

class UsuarioPlanViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioPlanSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return UsuarioPlan.objects.none()
        # Los admins o staff pueden ver todos los planes
        roles = list(user.roles_sistema.values_list('nombre_rol', flat=True))
        if user.is_staff or 'Administrador' in roles:
            return UsuarioPlan.objects.all().select_related('id_usuario', 'id_plan')
        return UsuarioPlan.objects.filter(id_usuario=user).select_related('id_plan')

class PagoViewSet(viewsets.ModelViewSet):
    serializer_class = PagoSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Pago.objects.none()
        roles = list(user.roles_sistema.values_list('nombre_rol', flat=True))
        if user.is_staff or 'Administrador' in roles:
            return Pago.objects.all().select_related('id_usuario')
        return Pago.objects.filter(id_usuario=user)

    def _generar_codigo_unico(self):
        """Genera código único de 8 chars alfanuméricos (mayusculas+digitos). Reintentos para evitar colisiones."""
        chars = string.ascii_uppercase + string.digits
        for _ in range(10):
            codigo = ''.join(secrets.choice(chars) for _ in range(8))
            if not Pago.objects.filter(codigo_unico_confirmacion=codigo).exists():
                return codigo
        raise ValueError('No se pudo generar un código único.')

    def perform_create(self, serializer):
        codigo = self._generar_codigo_unico()
        serializer.save(id_usuario=self.request.user, codigo_unico_confirmacion=codigo)

    @action(detail=True, methods=['post'])
    def aprobar(self, request, pk=None):
        pago = self.get_object()
        pago.estado_pago = 'Aprobado'
        pago.id_administrador_verificador = request.user
        pago.fecha_verificacion = timezone.now()
        pago.observaciones = request.data.get('observaciones', 'Aprobado por administrador.')
        pago.save()
        return Response({'status': 'Pago aprobado', 'pago_id': pago.id})

    @action(detail=True, methods=['post'])
    def rechazar(self, request, pk=None):
        pago = self.get_object()
        pago.estado_pago = 'Rechazado'
        pago.id_administrador_verificador = request.user
        pago.fecha_verificacion = timezone.now()
        pago.observaciones = request.data.get('observaciones', 'Rechazado por inconsistencia en datos.')
        pago.save()
        return Response({'status': 'Pago rechazado', 'pago_id': pago.id})

    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        pagos = Pago.objects.filter(estado_pago='Pendiente').select_related('id_usuario')
        serializer = self.get_serializer(pagos, many=True)
        return Response(serializer.data)

class PreInscripcionViewSet(viewsets.ModelViewSet):
    queryset = PreInscripcion.objects.all()
    serializer_class = PreInscripcionSerializer

class TipoEntrenamientoViewSet(viewsets.ModelViewSet):
    queryset = TipoEntrenamiento.objects.all()
    serializer_class = TipoEntrenamientoSerializer

class ComodidadViewSet(viewsets.ModelViewSet):
    queryset = Comodidad.objects.all()
    serializer_class = ComodidadSerializer

class EjercicioViewSet(viewsets.ModelViewSet):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer

class RutinaViewSet(viewsets.ModelViewSet):
    queryset = Rutina.objects.all()
    serializer_class = RutinaSerializer

class RutinaEjercicioViewSet(viewsets.ModelViewSet):
    queryset = RutinaEjercicio.objects.all()
    serializer_class = RutinaEjercicioSerializer

class UsuarioRutinaViewSet(viewsets.ModelViewSet):
    queryset = UsuarioRutina.objects.all()
    serializer_class = UsuarioRutinaSerializer

class AlimentoViewSet(viewsets.ModelViewSet):
    queryset = Alimento.objects.all()
    serializer_class = AlimentoSerializer

class DietaViewSet(viewsets.ModelViewSet):
    queryset = Dieta.objects.all()
    serializer_class = DietaSerializer

class DietaAlimentoViewSet(viewsets.ModelViewSet):
    queryset = DietaAlimento.objects.all()
    serializer_class = DietaAlimentoSerializer

class UsuarioDietaViewSet(viewsets.ModelViewSet):
    queryset = UsuarioDieta.objects.all()
    serializer_class = UsuarioDietaSerializer
