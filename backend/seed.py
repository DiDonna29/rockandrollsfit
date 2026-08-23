import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import Usuario, Plan, Sede, UsuarioPlan

print("--- Iniciando Populacion de Datos (Seed) ---")

sede, _ = Sede.objects.get_or_create(
    nombre_sede="Base Principal Caracas",
    defaults={
        "direccion": "Av Libertador",
        "horario_lunes_viernes_apertura": "06:00:00",
        "horario_lunes_viernes_cierre": "22:00:00",
        "horario_sabado_apertura": "08:00:00",
        "horario_sabado_cierre": "18:00:00",
        "horario_domingo_apertura": "08:00:00",
        "horario_domingo_cierre": "13:00:00"
    }
)

plan, _ = Plan.objects.get_or_create(
    nombre_plan="Plan VIP Rock",
    defaults={
        "precio_inscripcion": 30.00,
        "precio_mensualidad": 60.00,
        "descripcion_plan": "El plan definitivo para tu entrenamiento"
    }
)

usuarios = Usuario.objects.all()

if not usuarios.exists():
    print("No hay usuarios logueados aun. El seed detendra la aplicacion de membresias automaticas.")
else:
    for u in usuarios:
        if not UsuarioPlan.objects.filter(id_usuario=u).exists():
            fecha_inicio = timezone.now() - timedelta(days=12)
            UsuarioPlan.objects.create(
                id_usuario=u,
                id_plan=plan,
                fecha_inicio_plan=fecha_inicio,
                fecha_fin_plan=fecha_inicio + timedelta(days=30),
                fecha_pago_inscripcion=fecha_inicio,
                estado_plan="Activo",
                dias_restantes_mensualidad=18
            )
            print(f"-> Plan VIP simulado asignado a {u.email}")
        else:
            print(f"-> El usuario {u.email} ya posee membresia.")

print("--- Seed Completado ---")
