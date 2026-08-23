from django.db import models
from django.contrib.auth.models import AbstractUser

class Sede(models.Model):
    nombre_sede = models.CharField(max_length=100, unique=True)
    direccion = models.TextField()
    horario_lunes_viernes_apertura = models.TimeField()
    horario_lunes_viernes_cierre = models.TimeField()
    horario_sabado_apertura = models.TimeField()
    horario_sabado_cierre = models.TimeField()
    horario_domingo_apertura = models.TimeField()
    horario_domingo_cierre = models.TimeField()
    telefono_contacto = models.CharField(max_length=20)
    link_whatsapp_chat = models.URLField()

    def __str__(self):
        return self.nombre_sede

class Plan(models.Model):
    nombre_plan = models.CharField(max_length=100, unique=True)
    precio_inscripcion = models.DecimalField(max_digits=10, decimal_places=2)
    precio_mensualidad = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion_plan = models.TextField()
    incluye_alimentacion = models.BooleanField(default=False)
    incluye_entrenamiento_personalizado = models.BooleanField(default=False)
    acceso_todas_sedes = models.BooleanField(default=False)
    incluye_estacionamiento = models.BooleanField(default=False)
    incluye_pases_web = models.BooleanField(default=False)
    incluye_lockers = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_plan

class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre_rol

class Usuario(AbstractUser):
    firebase_uid = models.CharField(max_length=128, unique=True, null=True, blank=True)
    cedula_identidad = models.CharField(max_length=20, unique=True, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    
    GENEROS = [('Papeado', 'Papeado'), ('Papeada', 'Papeada')]
    genero = models.CharField(max_length=15, choices=GENEROS, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) # kg
    estatura = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True) # metros
    fecha_registro = models.DateTimeField(auto_now_add=True)
    id_sede_preferida = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True, blank=True)
    url_foto_perfil = models.URLField(null=True, blank=True)
    roles_sistema = models.ManyToManyField(Rol, through='UsuarioRol', related_name='usuarios')

class UsuarioRol(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

class GaleriaSede(models.Model):
    id_sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='galerias')
    url_imagen = models.URLField()
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    orden = models.IntegerField(default=0)

class Testimonio(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_cliente = models.CharField(max_length=100)
    texto_testimonio = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)

class UsuarioPlan(models.Model):
    ESTADOS = [('Activo', 'Activo'), ('Vencido', 'Vencido'), ('Suspendido', 'Suspendido')]
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='planes')
    id_plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    fecha_inicio_plan = models.DateField()
    fecha_fin_plan = models.DateField()
    fecha_pago_inscripcion = models.DateField(null=True, blank=True)
    estado_plan = models.CharField(max_length=20, choices=ESTADOS, default='Activo')
    fecha_ultima_actualizacion = models.DateTimeField(auto_now=True)

class Pago(models.Model):
    TIPOS = [('Inscripcion', 'Inscripcion'), ('Mensualidad', 'Mensualidad')]
    METODOS = [('Pago movil', 'Pago movil'), ('Zelle', 'Zelle'), ('Efectivo', 'Efectivo'), ('Transferencia', 'Transferencia')]
    ESTADOS = [('Pendiente', 'Pendiente'), ('Aprobado', 'Aprobado'), ('Rechazado', 'Rechazado')]
    
    BANCOS_VE = [
        ('0102', '0102 - Banco de Venezuela'),
        ('0104', '0104 - Banco Venezolano de Crédito'),
        ('0105', '0105 - Banco Mercantil'),
        ('0108', '0108 - BBVA Provincial'),
        ('0114', '0114 - Bancaribe'),
        ('0115', '0115 - Banco Exterior'),
        ('0128', '0128 - Banco Caronf'),
        ('0134', '0134 - Banesco'),
        ('0137', '0137 - Banco Sofitasa'),
        ('0138', '0138 - Banco Plaza'),
        ('0151', '0151 - BFC Banco Fondo Común'),
        ('0156', '0156 - 100% Banco'),
        ('0157', '0157 - Delsur Banco Universal'),
        ('0163', '0163 - Banco del Tesoro'),
        ('0166', '0166 - Banco Agrícola'),
        ('0168', '0168 - Bancrecer'),
        ('0171', '0171 - Banco Activo'),
        ('0172', '0172 - Bancamiga'),
        ('0174', '0174 - Banplus'),
        ('0175', '0175 - Banco Digital de los Trabajadores'),
        ('0177', '0177 - BANFANB'),
        ('0191', '0191 - BNC'),
    ]

    id_usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='pagos')
    tipo_pago = models.CharField(max_length=20, choices=TIPOS)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=METODOS)
    banco_origen = models.CharField(max_length=4, choices=BANCOS_VE, null=True, blank=True)
    telefono_origen = models.CharField(max_length=20, null=True, blank=True)  # Ej: 4141234567
    ultimos_6_digitos_ref = models.CharField(max_length=6, null=True, blank=True)
    numero_referencia = models.CharField(max_length=50, unique=True, null=True, blank=True)
    monto_efectivo_divisa = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    codigo_unico_confirmacion = models.CharField(max_length=12, unique=True, null=True, blank=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    id_administrador_verificador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='pagos_verificados')
    fecha_verificacion = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

class PreInscripcion(models.Model):
    ESTADOS = [('Pendiente', 'Pendiente'), ('Aprobada', 'Aprobada'), ('Rechazada', 'Rechazada'), ('Convertida_a_Usuario', 'Convertida_a_Usuario')]
    
    cedula_identidad = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    id_plan_interes = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado_pre_inscripcion = models.CharField(max_length=30, choices=ESTADOS, default='Pendiente')
    id_pago_inscripcion = models.OneToOneField(Pago, on_delete=models.SET_NULL, null=True, blank=True)
    id_administrador_gestor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

class TipoEntrenamiento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    url_icono = models.URLField(null=True, blank=True)

class Comodidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    url_icono = models.URLField(null=True, blank=True)

class SedeComodidad(models.Model):
    id_sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    id_comodidad = models.ForeignKey(Comodidad, on_delete=models.CASCADE)

class Ejercicio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    url_video_demostracion = models.URLField(null=True, blank=True)
    url_imagen_demostracion = models.URLField(null=True, blank=True)
    tipo_fuerza = models.CharField(max_length=50, null=True, blank=True)
    dificultad = models.CharField(max_length=50, null=True, blank=True)

class Rutina(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    id_creador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

class RutinaEjercicio(models.Model):
    id_rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    id_ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    series = models.IntegerField(null=True, blank=True)
    repeticiones = models.CharField(max_length=50, null=True, blank=True)
    descanso_segundos = models.IntegerField(null=True, blank=True)
    orden = models.IntegerField()

class UsuarioRutina(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField(auto_now_add=True)
    fecha_fin = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)

class Alimento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    calorias_por_100g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    proteinas_por_100g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    carbohidratos_por_100g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    grasas_por_100g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

class Dieta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    id_creador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    min_estatura_cm = models.IntegerField(null=True, blank=True)
    max_estatura_cm = models.IntegerField(null=True, blank=True)
    min_peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    max_peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    min_edad = models.IntegerField(null=True, blank=True)
    max_edad = models.IntegerField(null=True, blank=True)
    tipo_dieta = models.CharField(max_length=50, null=True, blank=True)

class DietaAlimento(models.Model):
    id_dieta = models.ForeignKey(Dieta, on_delete=models.CASCADE)
    id_alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE)
    cantidad_gramos = models.DecimalField(max_digits=6, decimal_places=2)
    momento_dia = models.CharField(max_length=50)
    orden = models.IntegerField()

class UsuarioDieta(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_dieta = models.ForeignKey(Dieta, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField(auto_now_add=True)
    fecha_fin = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)
