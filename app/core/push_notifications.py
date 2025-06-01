import firebase_admin
from firebase_admin import credentials, messaging
import json
import os
from typing import Dict, List, Optional, Union
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# Path relativo al certificado de Firebase
FIREBASE_CERTIFICATE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "firebase-credentials.json"
)

# Inicializar Firebase Admin SDK
try:
    if os.path.exists(FIREBASE_CERTIFICATE_PATH):
        cred = credentials.Certificate(FIREBASE_CERTIFICATE_PATH)
        firebase_admin.initialize_app(cred)
        logger.info("Firebase Admin SDK inicializado correctamente")
    else:
        logger.warning(
            f"No se encontró el certificado de Firebase en {FIREBASE_CERTIFICATE_PATH}. "
            "Las notificaciones push estarán desactivadas."
        )
except Exception as e:
    logger.error(f"Error al inicializar Firebase Admin SDK: {e}")


class PushNotificationService:
    """Servicio para enviar notificaciones push usando Firebase Cloud Messaging (FCM)"""

    @staticmethod
    async def send_to_device(
        token: str,
        title: str,
        body: str,
        data: Optional[Dict] = None,
        notification_type: str = "general",
        priority: str = "high",
    ) -> Dict:
        """
        Envía una notificación push a un dispositivo específico
        
        Args:
            token: Token FCM del dispositivo
            title: Título de la notificación
            body: Contenido de la notificación
            data: Datos adicionales para la notificación
            notification_type: Tipo de notificación (academic, payment, etc.)
            priority: Prioridad de la notificación (high, normal)
            
        Returns:
            Dict: Respuesta del servicio FCM
        """
        # Si Firebase no está inicializado, registrar y devolver error
        if not firebase_admin._apps:
            logger.error("Firebase Admin SDK no está inicializado. No se puede enviar notificación.")
            return {"error": "Firebase no inicializado", "success": False}
        
        try:
            # Configurar mensaje de notificación
            notification = messaging.Notification(
                title=title,
                body=body
            )
            
            # Datos adicionales (siempre incluir tipo)
            android_config = messaging.AndroidConfig(
                priority=priority,
                notification=messaging.AndroidNotification(
                    sound="default",
                    default_sound=True,
                    default_vibrate_timings=True,
                    default_light_settings=True,
                    icon="notification_icon",
                    color="#4285F4"
                )
            )
            
            apns_config = messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        sound="default",
                        badge=1,
                        content_available=True
                    )
                )
            )
            
            # Datos para la notificación
            push_data = data or {}
            push_data["type"] = notification_type
            
            # Crear mensaje
            message = messaging.Message(
                notification=notification,
                data=push_data,
                token=token,
                android=android_config,
                apns=apns_config
            )
            
            # Enviar mensaje
            response = messaging.send(message)
            logger.info(f"Notificación push enviada correctamente: {response}")
            return {"message_id": response, "success": True}
        
        except Exception as e:
            error_message = f"Error al enviar notificación push: {str(e)}"
            logger.error(error_message)
            return {"error": error_message, "success": False}

    @staticmethod
    async def send_to_multiple_devices(
        tokens: List[str],
        title: str,
        body: str,
        data: Optional[Dict] = None,
        notification_type: str = "general",
        priority: str = "high",
    ) -> Dict:
        """
        Envía una notificación push a múltiples dispositivos
        
        Args:
            tokens: Lista de tokens FCM
            title: Título de la notificación
            body: Contenido de la notificación
            data: Datos adicionales para la notificación
            notification_type: Tipo de notificación (academic, payment, etc.)
            priority: Prioridad de la notificación (high, normal)
            
        Returns:
            Dict: Respuesta del servicio FCM
        """
        # Si Firebase no está inicializado, registrar y devolver error
        if not firebase_admin._apps:
            logger.error("Firebase Admin SDK no está inicializado. No se puede enviar notificación.")
            return {"error": "Firebase no inicializado", "success": False}
        
        # Validar tokens
        if not tokens:
            return {"error": "No se proporcionaron tokens", "success": False}
        
        try:
            # Configurar mensaje de notificación
            notification = messaging.Notification(
                title=title,
                body=body
            )
            
            # Configuraciones específicas para Android y iOS
            android_config = messaging.AndroidConfig(
                priority=priority,
                notification=messaging.AndroidNotification(
                    sound="default",
                    default_sound=True,
                    default_vibrate_timings=True,
                    default_light_settings=True,
                    icon="notification_icon",
                    color="#4285F4"
                )
            )
            
            apns_config = messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        sound="default",
                        badge=1,
                        content_available=True
                    )
                )
            )
            
            # Datos para la notificación
            push_data = data or {}
            push_data["type"] = notification_type
            
            # Crear mensaje multicast
            multicast_message = messaging.MulticastMessage(
                notification=notification,
                data=push_data,
                tokens=tokens,
                android=android_config,
                apns=apns_config
            )
            
            # Enviar mensaje multicast
            response = messaging.send_multicast(multicast_message)
            
            logger.info(f"Notificación enviada a {response.success_count} de {response.failure_count} dispositivos")
            
            return {
                "success_count": response.success_count,
                "failure_count": response.failure_count,
                "success": response.success_count > 0
            }
        
        except Exception as e:
            error_message = f"Error al enviar notificación push multicast: {str(e)}"
            logger.error(error_message)
            return {"error": error_message, "success": False}


# Instancia singleton del servicio
push_service = PushNotificationService()
