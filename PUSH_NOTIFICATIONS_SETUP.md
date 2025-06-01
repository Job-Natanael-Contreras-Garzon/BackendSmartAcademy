# Configuración de Notificaciones Push para Smart Academy

Este documento detalla los pasos necesarios para configurar las notificaciones push en el backend y la aplicación móvil de Smart Academy.

## 1. Configuración del Backend

### 1.1. Requisitos

- Certificado de Firebase Admin SDK
- Python 3.8+
- Paquete firebase-admin

### 1.2. Instalación de Dependencias

Añadir `firebase-admin` al archivo `requirements.txt`:

```
firebase-admin==5.3.0
```

Instalar la dependencia:

```bash
pip install -r requirements.txt
```

### 1.3. Configuración del Certificado Firebase

1. Acceder a la [Consola de Firebase](https://console.firebase.google.com/)
2. Crear un nuevo proyecto o usar uno existente
3. Ir a Configuración del Proyecto > Cuentas de servicio
4. Generar una nueva clave privada (descarga un archivo JSON)
5. Renombrar el archivo descargado como `firebase-credentials.json`
6. Colocar el archivo en la raíz del proyecto BackendSmartAcademy

### 1.4. Estructura de Tablas

Ejecutar el script de creación de tablas para generar las tablas necesarias:

```bash
python -m app.scripts.create_tables
```

Este script creará las siguientes tablas:
- `user_devices`: Almacena los tokens FCM de los dispositivos de los usuarios
- `user_notification_preferences`: Guarda las preferencias de notificaciones
- `notifications`: Almacena todas las notificaciones enviadas

## 2. Integración con Flutter

### 2.1. Requisitos Flutter

- Flutter 3.0+
- Firebase Core
- Firebase Messaging
- Flutter Local Notifications

### 2.2. Configurar Firebase en Flutter

1. Instalar Firebase CLI:
   ```bash
   npm install -g firebase-tools
   ```

2. Iniciar sesión en Firebase:
   ```bash
   firebase login
   ```

3. Configurar Flutter con Firebase:
   ```bash
   flutter pub add firebase_core firebase_messaging flutter_local_notifications
   flutter pub get
   flutterfire configure --project=tu-proyecto-firebase
   ```

4. Seguir las instrucciones del asistente de FlutterFire para configurar las plataformas (Android/iOS)

### 2.3. Implementación en Flutter

Ver el archivo `ejemplosjson_push.md` para ejemplos detallados de código Flutter para:
- Inicialización de Firebase
- Solicitud de permisos
- Registro de tokens FCM
- Manejo de notificaciones en primer y segundo plano

## 3. Flujo de Funcionamiento

1. **Registro de dispositivo**:
   - La app Flutter obtiene el token FCM
   - Envía el token al backend mediante el endpoint `/api/v1/devices/`
   - El backend almacena el token asociado al usuario

2. **Envío de notificaciones**:
   - Cuando se crea una notificación en el sistema, se activa el envío push
   - El sistema verifica las preferencias del usuario
   - Si las preferencias lo permiten, envía la notificación mediante FCM
   - Firebase entrega la notificación al dispositivo

3. **Recepción en dispositivo**:
   - La app Flutter muestra la notificación según su estado (primer o segundo plano)
   - Al hacer tap, navega a la pantalla correspondiente

## 4. Consideraciones de Seguridad

- Los tokens FCM son sensibles y no deben compartirse
- Solo el propio usuario puede gestionar sus dispositivos
- Las preferencias de notificaciones son privadas para cada usuario
- El sistema respeta la política de autenticación existente donde:
  - Solo administradores pueden registrar usuarios
  - El sistema usa login con JWT
  - No hay registro público

## 5. Solución de Problemas

### El dispositivo no recibe notificaciones

1. Verificar que el token esté correctamente registrado en la tabla `user_devices`
2. Comprobar las preferencias del usuario en `user_notification_preferences`
3. Revisar logs de Firebase en la consola de Firebase
4. Verificar que el certificado `firebase-credentials.json` sea válido
5. Comprobar que la app tiene permisos de notificaciones en el dispositivo

### Error de inicialización de Firebase

1. Verificar que el archivo `firebase-credentials.json` existe en la raíz
2. Comprobar que el formato del archivo es correcto
3. Revisar logs del servidor para mensajes de error específicos
