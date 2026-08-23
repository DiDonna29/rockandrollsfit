import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import firebase_admin
from firebase_admin import auth, credentials
from core.models import Usuario, Plan, Sede, UsuarioPlan

print("--- Iniciando Creacion de Usuarios de Prueba (Firebase + Django) ---")

try:
    cred = credentials.Certificate("firebase-adminsdk.json")
    firebase_admin.initialize_app(cred)
except ValueError:
    pass # App already initialized

sede = Sede.objects.first()
plan = Plan.objects.first()

if not sede:
    print("Por favor crear una Sede y un Plan VIP primero (corre seed.py original).")
    sede = Sede.objects.create(nombre_sede="Base Principal Caracas", direccion="Av Libertador")
    plan = Plan.objects.create(nombre_plan="Plan VIP Rock", precio_inscripcion=30)
    
test_users = [
    {"email": "pepe@rock.com", "pass": "Rock2026!", "name": "Pepe Rockero", "role": "Miembro"},
    {"email": "maria@rock.com", "pass": "Rock2026!", "name": "Maria Pesas", "role": "Miembro"}
]

for tu in test_users:
    try:
        user_record = auth.get_user_by_email(tu["email"])
        print(f"Usuario {tu['email']} ya existe en Firebase Auth.")
    except Exception:
        user_record = auth.create_user(
            email=tu["email"],
            email_verified=True,
            password=tu["pass"],
            display_name=tu["name"]
        )
        print(f"CREADO: {tu['email']} en Firebase Auth.")

    usuario, created = Usuario.objects.get_or_create(
        email=tu["email"],
        defaults={
            "username": tu["email"],
            "firebase_uid": user_record.uid,
            "cedula_identidad": str(user_record.uid)[:10],
            "first_name": tu["name"].split()[0],
            "last_name": tu["name"].split()[1] if len(tu["name"].split()) > 1 else "",
            "genero": "Papeado",
            "id_sede_preferida": sede
        }
    )
    
    if tu["role"] == "Miembro":
        fecha_ini = timezone.make_aware(timezone.datetime(2026, 4, 1))
        UsuarioPlan.objects.get_or_create(
            id_usuario=usuario,
            id_plan=plan,
            defaults={
                "fecha_inicio_plan": fecha_ini,
                "fecha_fin_plan": fecha_ini + timedelta(days=30),
                "fecha_pago_inscripcion": fecha_ini,
                "estado_plan": 'Activo'
            }
        )
    print(f"Sincronizado {tu['email']} de manera cruzada Firebase/Django.")

print("Listo! YA PUEDES INICIAR SESION CON LOS CORREOS.")
