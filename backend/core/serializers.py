from rest_framework import serializers
from .models import *

class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    rol_principal = serializers.SerializerMethodField()

    def get_roles(self, obj):
        return list(obj.roles_sistema.values_list('nombre_rol', flat=True))
    
    def get_rol_principal(self, obj):
        roles = list(obj.roles_sistema.values_list('nombre_rol', flat=True))
        # Jerarquía de mayor a menor prioridad
        PRIORIDAD = ['Administrador', 'Entrenador', 'Nutricionista', 'Miembro']
        for rol in PRIORIDAD:
            if rol in roles:
                return rol
        return roles[0] if roles else 'Miembro'

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'firebase_uid', 'cedula_identidad',
                  'first_name', 'last_name', 'fecha_nacimiento', 'genero', 'telefono',
                  'peso', 'estatura', 'roles_sistema', 'roles', 'rol_principal',
                  'id_sede_preferida', 'url_foto_perfil', 'fecha_registro']

class UsuarioBriefSerializer(serializers.ModelSerializer):
    """Serializer lite para enriquecer datos anidados (ej: en Pago)"""
    nombre_completo = serializers.SerializerMethodField()
    def get_nombre_completo(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.email
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'cedula_identidad', 'nombre_completo', 'url_foto_perfil']

class PlanBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'nombre_plan', 'precio_mensualidad', 'precio_inscripcion']

class GaleriaSedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GaleriaSede
        fields = '__all__'

class TestimonioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonio
        fields = '__all__'

class UsuarioPlanSerializer(serializers.ModelSerializer):
    plan_detalle = PlanBriefSerializer(source='id_plan', read_only=True)
    
    class Meta:
        model = UsuarioPlan
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    usuario_detalle = UsuarioBriefSerializer(source='id_usuario', read_only=True)
    banco_origen_display = serializers.SerializerMethodField()

    def get_banco_origen_display(self, obj):
        if obj.banco_origen:
            from .models import Pago as PagoModel
            for code, label in PagoModel.BANCOS_VE:
                if code == obj.banco_origen:
                    return label
        return None

    class Meta:
        model = Pago
        fields = '__all__'
        read_only_fields = ['codigo_unico_confirmacion', 'estado_pago', 'fecha_pago',
                            'id_administrador_verificador', 'fecha_verificacion']

class PreInscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreInscripcion
        fields = '__all__'

class TipoEntrenamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEntrenamiento
        fields = '__all__'

class ComodidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comodidad
        fields = '__all__'

class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = '__all__'

class RutinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rutina
        fields = '__all__'

class RutinaEjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RutinaEjercicio
        fields = '__all__'

class UsuarioRutinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioRutina
        fields = '__all__'

class AlimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alimento
        fields = '__all__'

class DietaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dieta
        fields = '__all__'

class DietaAlimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietaAlimento
        fields = '__all__'

class UsuarioDietaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioDieta
        fields = '__all__'
