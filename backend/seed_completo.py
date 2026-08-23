"""
Seed Completo - Rock And Rolls Fit
Crea: 1 Sede, 3 Planes, 4 Roles, 6 Usuarios con Roles distintos, Planes activos y Pagos históricos.
Uso:
    cd backend
    source venv/Scripts/activate  (Windows: venv\\Scripts\\activate)
    python seed_completo.py
"""
import os
import django
from datetime import date, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import firebase_admin
from firebase_admin import auth as fb_auth, credentials
from core.models import (
    Usuario, Plan, Sede, UsuarioPlan, Rol, UsuarioRol, Pago
)

print("\n🎸  Iniciando Seed Completo Rock And Rolls Fit...\n")

# --- Firebase Admin Init ---
try:
    cred = credentials.Certificate("firebase-adminsdk.json")
    firebase_admin.initialize_app(cred)
except ValueError:
    pass  # ya está inicializada

# =====================
# 1. SEDE
# =====================
sede, _ = Sede.objects.get_or_create(
    nombre_sede="Sede Central Caracas",
    defaults={
        "direccion": "Av. Libertador, CCCT, Caracas",
        "horario_lunes_viernes_apertura": "06:00",
        "horario_lunes_viernes_cierre": "22:00",
        "horario_sabado_apertura": "07:00",
        "horario_sabado_cierre": "20:00",
        "horario_domingo_apertura": "08:00",
        "horario_domingo_cierre": "14:00",
        "telefono_contacto": "+58 412 000 0000",
        "link_whatsapp_chat": "https://wa.me/584120000000"
    }
)
print(f"  ✅ Sede: {sede.nombre_sede}")

# =====================
# 2. PLANES
# =====================
plan_rock, _ = Plan.objects.get_or_create(
    nombre_plan="ROCK",
    defaults={
        "precio_inscripcion": 5, "precio_mensualidad": 25,
        "descripcion_plan": "Plan base con alimentación y entrenamiento personalizado.",
        "incluye_alimentacion": True, "incluye_entrenamiento_personalizado": True,
        "acceso_todas_sedes": False, "incluye_estacionamiento": False,
        "incluye_pases_web": False, "incluye_lockers": False
    }
)
plan_multi, _ = Plan.objects.get_or_create(
    nombre_plan="MULTI ROCK",
    defaults={
        "precio_inscripcion": 5, "precio_mensualidad": 35,
        "descripcion_plan": "Todo el paquete Rock + Acceso multisede total + Pases web.",
        "incluye_alimentacion": True, "incluye_entrenamiento_personalizado": True,
        "acceso_todas_sedes": True, "incluye_estacionamiento": False,
        "incluye_pases_web": True, "incluye_lockers": False
    }
)
plan_parking, _ = Plan.objects.get_or_create(
    nombre_plan="PARKING ROCK",
    defaults={
        "precio_inscripcion": 5, "precio_mensualidad": 35,
        "descripcion_plan": "Paquete Rock base + Estacionamiento VIP + Lockers seguros.",
        "incluye_alimentacion": True, "incluye_entrenamiento_personalizado": True,
        "acceso_todas_sedes": False, "incluye_estacionamiento": True,
        "incluye_pases_web": False, "incluye_lockers": True
    }
)
print(f"  ✅ Planes creados: ROCK / MULTI ROCK / PARKING ROCK")

# =====================
# 3. ROLES
# =====================
roles_data = ["Miembro", "Administrador", "Entrenador", "Nutricionista"]
roles = {}
for rn in roles_data:
    r, _ = Rol.objects.get_or_create(nombre_rol=rn)
    roles[rn] = r
print(f"  ✅ Roles: {', '.join(roles_data)}")

# =====================
# 4. USUARIOS
# =====================
today = date.today()
users_config = [
    {
        "email": "pepe@rock.com",
        "pass": "Rock2026!",
        "first_name": "José",
        "last_name": "Rodríguez",
        "cedula": "V-12345678",
        "telefono": "+58 414 111 1111",
        "rol": "Miembro",
        "plan": plan_multi,
        "peso": 78.5, "estatura": 1.75,
        "fecha_inicio": date(2026, 4, 1),
        "genero": "Papeado"
    },
    {
        "email": "maria@rock.com",
        "pass": "Rock2026!",
        "first_name": "María",
        "last_name": "Pérez",
        "cedula": "V-23456789",
        "telefono": "+58 424 222 2222",
        "rol": "Miembro",
        "plan": plan_rock,
        "peso": 62.0, "estatura": 1.62,
        "fecha_inicio": date(2026, 3, 15),
        "genero": "Papeada"
    },
    {
        "email": "carlos@rock.com",
        "pass": "Rock2026!",
        "first_name": "Carlos",
        "last_name": "Martínez",
        "cedula": "V-34567890",
        "telefono": "+58 412 333 3333",
        "rol": "Miembro",
        "plan": plan_parking,
        "peso": 90.0, "estatura": 1.82,
        "fecha_inicio": date(2026, 2, 1),
        "genero": "Papeado"
    },
    {
        "email": "luisa@rock.com",
        "pass": "Rock2026!",
        "first_name": "Luisa",
        "last_name": "González",
        "cedula": "V-45678901",
        "telefono": "+58 416 444 4444",
        "rol": "Entrenador",
        "plan": None,
        "peso": 58.0, "estatura": 1.67,
        "fecha_inicio": None,
        "genero": "Papeada"
    },
    {
        "email": "nutricion@rock.com",
        "pass": "Rock2026!",
        "first_name": "Andrés",
        "last_name": "Nutrici",
        "cedula": "V-56789012",
        "telefono": "+58 412 555 5555",
        "rol": "Nutricionista",
        "plan": None,
        "peso": 75.0, "estatura": 1.78,
        "fecha_inicio": None,
        "genero": "Papeado"
    },
    {
        "email": "admin@rock.com",
        "pass": "RockAdmin2026!",
        "first_name": "Admin",
        "last_name": "Rock",
        "cedula": "V-99999999",
        "telefono": "+58 412 999 9999",
        "rol": "Administrador",
        "plan": None,
        "peso": None, "estatura": None,
        "fecha_inicio": None,
        "genero": "Papeado"
    }
]

for uc in users_config:
    # -- Firebase --
    try:
        fb_user = fb_auth.get_user_by_email(uc["email"])
    except Exception:
        fb_user = fb_auth.create_user(
            email=uc["email"],
            email_verified=True,
            password=uc["pass"],
            display_name=f"{uc['first_name']} {uc['last_name']}"
        )
        print(f"  🔥 Firebase: creado {uc['email']}")

    # -- Django --
    usuario, created = Usuario.objects.get_or_create(
        email=uc["email"],
        defaults={
            "username": uc["email"],
            "firebase_uid": fb_user.uid,
            "cedula_identidad": uc["cedula"],
            "first_name": uc["first_name"],
            "last_name": uc["last_name"],
            "telefono": uc["telefono"],
            "peso": uc["peso"],
            "estatura": uc["estatura"],
            "genero": uc["genero"],
            "id_sede_preferida": sede,
            "is_staff": uc["rol"] == "Administrador"
        }
    )
    if not created:
        # Actualizar firebase_uid si faltaba
        if not usuario.firebase_uid:
            usuario.firebase_uid = fb_user.uid
            usuario.save()

    # -- Rol --
    UsuarioRol.objects.get_or_create(id_usuario=usuario, id_rol=roles[uc["rol"]])

    # -- Plan activo (solo miembros) --
    if uc["plan"] and uc["fecha_inicio"]:
        up, _ = UsuarioPlan.objects.get_or_create(
            id_usuario=usuario,
            id_plan=uc["plan"],
            defaults={
                "fecha_inicio_plan": uc["fecha_inicio"],
                "fecha_fin_plan": uc["fecha_inicio"] + timedelta(days=30),
                "fecha_pago_inscripcion": uc["fecha_inicio"],
                "estado_plan": "Activo"
            }
        )

        # -- Pagos históricos (solo miembros) --
        # Usamos email prefix para unicidad garantizada en los códigos
        email_key = uc["email"].split("@")[0].upper()[:6]
        pagos_hist = [
            {"tipo": "Inscripcion",  "monto": uc["plan"].precio_inscripcion,   "metodo": "Zelle",      "ref": f"INS-{email_key}", "codigo": f"ROCK-{email_key}I", "estado": "Aprobado"},
            {"tipo": "Mensualidad",  "monto": uc["plan"].precio_mensualidad,    "metodo": "Pago movil", "ref": f"FEB-{email_key}", "codigo": f"ROCK-{email_key}F", "estado": "Aprobado"},
            {"tipo": "Mensualidad",  "monto": uc["plan"].precio_mensualidad,    "metodo": "Zelle",      "ref": f"MAR-{email_key}", "codigo": f"ROCK-{email_key}M", "estado": "Aprobado"},
            {"tipo": "Mensualidad",  "monto": uc["plan"].precio_mensualidad,    "metodo": "Efectivo",   "ref": f"ABR-{email_key}", "codigo": f"ROCK-{email_key}A", "estado": "Pendiente"},
        ]
        for ph in pagos_hist:
            try:
                Pago.objects.get_or_create(
                    numero_referencia=ph["ref"],
                    defaults={
                        "id_usuario": usuario,
                        "tipo_pago": ph["tipo"],
                        "monto": ph["monto"],
                        "metodo_pago": ph["metodo"],
                        "estado_pago": ph["estado"],
                        "codigo_unico_confirmacion": ph["codigo"]
                    }
                )
            except Exception as e:
                print(f"    ⚠️  Pago {ph['ref']} ya existe o colisión: {e}")

    estado = "NUEVO" if created else "existente"
    print(f"  👤 [{uc['rol']}] {uc['email']} ({estado})")

print("\n🎸  Seed completado exitosamente!")
print("\n📋  CREDENCIALES DE PRUEBA:")
print("  Miembro 1  : pepe@rock.com          / Rock2026!")
print("  Miembro 2  : maria@rock.com         / Rock2026!")
print("  Miembro 3  : carlos@rock.com        / Rock2026!")
print("  Entrenador : luisa@rock.com         / Rock2026!")
print("  Nutrición  : nutricion@rock.com     / Rock2026!")
print("  Admin      : admin@rock.com         / RockAdmin2026!")
print("\n  ℹ️  Todos los miembros tienen historial de pagos de prueba en la BD.")
