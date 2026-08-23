import firebase_admin
from firebase_admin import credentials, auth
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Rol, UsuarioRol, Sede

Usuario = get_user_model()
import os

try:
    if not firebase_admin._apps:
        cert_path = os.path.join(settings.BASE_DIR, 'firebase-adminsdk.json')
        if os.path.exists(cert_path):
            cred = credentials.Certificate(cert_path)
            firebase_admin.initialize_app(cred)
        else:
            print(f"ATENCION: No se encontro {cert_path}. El Login backend hacia Firebase fallara hasta que añadas la llave maestra.")
except Exception as e:
    print(f"ERROR inicializando Firebase Admin: {e}")

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        
        id_token = auth_header.split(' ').pop()

        try:
            decoded_token = auth.verify_id_token(id_token)
            firebase_uid = decoded_token.get('uid')
            email = decoded_token.get('email')
        except Exception as e:
            raise AuthenticationFailed(f'Auth Token Firebase Invalido o Expirado: {str(e)}')

        try:
            # 1. Intentar por firebase_uid (el camino más rápido)
            user = Usuario.objects.get(firebase_uid=firebase_uid)
        except Usuario.DoesNotExist:
            # 2. Si no hay UID, intentar vincular por email (Link-by-Email)
            user = Usuario.objects.filter(email=email).first()
            
            if user:
                # Ya existe por email, vincular UID de Firebase
                user.firebase_uid = firebase_uid
                if not user.url_foto_perfil:
                    user.url_foto_perfil = decoded_token.get('picture', '')
                user.save()
            else:
                # 3. No existe usuario, crear uno nuevo (JIT Registration)
                with transaction.atomic():
                    raw_name = decoded_token.get('name', email.split('@')[0] if email else "Rockero")
                    name_parts = raw_name.split()
                    fname = name_parts[0]
                    lname = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
                    
                    # Generar username único basado en email
                    username = email if email else firebase_uid
                    if Usuario.objects.filter(username=username).exists():
                        import uuid
                        username = f"{username.split('@')[0]}_{str(uuid.uuid4())[:4]}"

                    user = Usuario.objects.create(
                        username=username,
                        firebase_uid=firebase_uid,
                        email=email,
                        first_name=fname,
                        last_name=lname,
                        url_foto_perfil=decoded_token.get('picture', '')
                    )

                    # Asignar Rol 'Miembro' por defecto
                    rol_miembro, _ = Rol.objects.get_or_create(nombre_rol='Miembro')
                    UsuarioRol.objects.create(id_usuario=user, id_rol=rol_miembro)

                    # Asignar Sede por defecto si no tiene ninguna
                    if not user.id_sede_preferida:
                        sede, _ = Sede.objects.get_or_create(
                            nombre_sede='Sede Central Caracas',
                            defaults={
                                'direccion': 'Av. Principal de Las Mercedes, Caracas',
                                'horario_lunes_viernes_apertura': '06:00:00',
                                'horario_lunes_viernes_cierre': '21:00:00',
                                'horario_sabado_apertura': '08:00:00',
                                'horario_sabado_cierre': '14:00:00',
                                'horario_domingo_apertura': '08:00:00',
                                'horario_domingo_cierre': '12:00:00',
                                'telefono_contacto': '+58 212-0000000',
                                'link_whatsapp_chat': 'https://wa.me/584240000000'
                            }
                        )
                        user.id_sede_preferida = sede
                        user.save()

        return (user, None)
