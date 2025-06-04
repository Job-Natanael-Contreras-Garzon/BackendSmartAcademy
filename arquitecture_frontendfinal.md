# Arquitectura Frontend Smart Academy (React + TSX)

Este documento define la arquitectura, estructura de navegación y especificaciones para el desarrollo del frontend de Smart Academy utilizando React con TypeScript (TSX), basado en los endpoints y modelos disponibles en el backend actual.

## Índice

1. [Introducción y Objetivos](#1-introducción-y-objetivos)
2. [Arquitectura General](#2-arquitectura-general)
   - 2.1. [Tecnologías Principales](#21-tecnologías-principales)
   - 2.2. [Estructura de Carpetas Recomendada](#22-estructura-de-carpetas-recomendada)
   - 2.3. [Principios de Diseño](#23-principios-de-diseño)
3. [Configuración del Proyecto](#3-configuración-del-proyecto)
   - 3.1. [Inicialización con Create React App (TypeScript)](#31-inicialización-con-create-react-app-typescript)
   - 3.2. [Dependencias Esenciales](#32-dependencias-esenciales)
   - 3.3. [Configuración de ESLint, Prettier y Husky](#33-configuración-de-eslint-prettier-y-husky)
4. [Componentes y Servicios Base](#4-componentes-y-servicios-base)
   - 4.1. [Servicio API (Axios Wrapper)](#41-servicio-api-axios-wrapper)
   - 4.2. [Gestión de Estado Global (Context API / Zustand / Redux Toolkit)](#42-gestión-de-estado-global)
   - 4.3. [Sistema de Enrutamiento (React Router DOM)](#43-sistema-de-enrutamiento)
   - 4.4. [Componentes UI Reutilizables](#44-componentes-ui-reutilizables)
   - 4.5. [Layouts Principales](#45-layouts-principales)
5. [Módulos y Vistas Principales (Alineados con Casos de Uso del Backend)](#5-módulos-y-vistas-principales)
   - 5.1. [Autenticación (CU13)](#51-autenticación-cu13)
   - 5.2. [Dashboard (Rol Específico)](#52-dashboard-rol-específico)
   - 5.3. [Gestión de Usuarios (Admin - CU1)](#53-gestión-de-usuarios-admin---cu1)
   - 5.4. [Gestión de Roles y Permisos (Admin - CU2)](#54-gestión-de-roles-y-permisos-admin---cu2)
   - 5.5. [Gestión de Periodos Académicos (Admin - CU14)](#55-gestión-de-periodos-académicos-admin---cu14)
   - 5.6. [Gestión de Cursos (Admin, Profesor, Estudiante - CU3)](#56-gestión-de-cursos-admin-profesor-estudiante---cu3)
   - 5.7. [Gestión de Asignaturas y Criterios (Admin - CU4)](#57-gestión-de-asignaturas-y-criterios-admin---cu4)
   - 5.8. [Gestión de Calificaciones (Profesor, Estudiante - CU5)](#58-gestión-de-calificaciones-profesor-estudiante---cu5)
   - 5.9. [Gestión de Asistencia (Profesor, Estudiante - CU6)](#59-gestión-de-asistencia-profesor-estudiante---cu6)
   - 5.10. [Gestión de Tutores (Admin, Estudiante - CU8)](#510-gestión-de-tutores-admin-estudiante---cu8)
   - 5.11. [Predicciones de Rendimiento IA (Estudiante, Profesor/Admin - CU9)](#511-predicciones-de-rendimiento-ia)
   - 5.12. [Reportes Académicos (CU10)](#512-reportes-académicos-cu10)
   - 5.13. [Sistema de Notificaciones (CU11, CU12)](#513-sistema-de-notificaciones-cu11-cu12)
   - 5.14. [Configuración de Cuenta](#514-configuración-de-cuenta)
6. [Tipos y Interfaces (TypeScript)](#6-tipos-y-interfaces-typescript)
   - 6.1. [Basados en `ejemplosjson.md` y Schemas Pydantic del Backend](#61-basados-en-ejemplosjsonmd-y-schemas-pydantic-del-backend)
7. [Consideraciones Técnicas Adicionales](#7-consideraciones-técnicas-adicionales)
   - 7.1. [Manejo de Errores y Feedback al Usuario](#71-manejo-de-errores-y-feedback-al-usuario)
   - 7.2. [Seguridad en el Frontend](#72-seguridad-en-el-frontend)
   - 7.3. [Optimización del Rendimiento](#73-optimización-del-rendimiento)
   - 7.4. [Pruebas](#74-pruebas)
   - 7.5. [Accesibilidad (a11y)](#75-accesibilidad-a11y)
   - 7.6. [Despliegue](#76-despliegue)

## 1. Introducción y Objetivos

El objetivo de este documento es proporcionar una guía detallada y exhaustiva para el desarrollo del frontend de la aplicación Smart Academy. Esta guía se enfoca en la implementación utilizando React con TypeScript (TSX), asegurando una integración fluida con el backend existente, promoviendo las mejores prácticas de desarrollo, mantenibilidad y escalabilidad del código.

Se tomará como referencia principal el `README.md` del backend para entender los Casos de Uso (CU) y la estructura de la API, así como `ejemplosjson.md` para definir las interfaces de datos y los payloads/respuestas esperados.

## 2. Arquitectura General

### 2.1. Tecnologías Principales

Para el desarrollo del frontend de Smart Academy, se utilizará el siguiente stack tecnológico:

- **Framework UI**: [React.js](https://reactjs.org/) (versión 18+)
  - Utilizaremos la sintaxis **TSX** para los componentes, aprovechando al máximo las capacidades de TypeScript.
- **Lenguaje**: [TypeScript](https://www.typescriptlang.org/)
  - Para un tipado estático robusto, mejorando la calidad del código y la detección temprana de errores.
- **Gestión de Estado**: Se recomienda [Zustand](https://zustand-demo.pmnd.rs/) o [React Context API](https://reactjs.org/docs/context.html) para la gestión de estado global. La elección dependerá de la complejidad y las necesidades específicas de cada feature. Para estados más complejos o compartidos globalmente, Zustand ofrece una solución ligera y potente. Redux Toolkit es una alternativa viable si el equipo tiene experiencia previa o si se anticipa una gran complejidad en el estado global.
- **Enrutamiento**: [React Router DOM](https://reactrouter.com/) (versión 6+)
  - Para la gestión de rutas y navegación dentro de la aplicación.
- **Componentes UI**: Se recomienda una librería de componentes como [Material-UI (MUI)](https://mui.com/) o [Ant Design](https://ant.design/). Estas librerías ofrecen un conjunto completo de componentes personalizables y accesibles.
  - Alternativamente, [Tailwind CSS](https://tailwindcss.com/) puede ser utilizado para un enfoque más utilitario si se prefiere un mayor control sobre el diseño desde cero.
- **Peticiones HTTP**: [Axios](https://axios-http.com/)
  - Para realizar peticiones a la API del backend. Se creará un wrapper para centralizar la configuración (URL base, interceptores para tokens JWT, manejo de errores comunes).
- **Validación de Formularios**: [React Hook Form](https://react-hook-form.com/) en conjunto con [Zod](https://zod.dev/) para la validación de esquemas.
  - Esto proporciona una forma eficiente y declarativa de manejar formularios y su validación.
- **Notificaciones en Tiempo Real**: Si se requiere (basado en CU11, CU12), se utilizarán [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) (preferiblemente con [Socket.IO-Client](https://socket.io/docs/v4/client-installation/)) para la comunicación bidireccional con el backend.
- **Estilo de Código y Formateo**: [ESLint](https://eslint.org/) y [Prettier](https://prettier.io/)
  - Para mantener un código limpio, consistente y libre de errores comunes.
- **Utilidades**: [date-fns](https://date-fns.org/) o [Day.js](https://day.js.org/) para la manipulación de fechas.

### 2.2. Estructura de Carpetas Recomendada

Se propone una estructura de carpetas modular y escalable, inspirada en el enfoque de "feature-based" o "atomic design" adaptado. Esta estructura busca mejorar la organización, cohesión y mantenibilidad del código.

```
src/
├── App.tsx                 # Componente raíz, configuración de Router y Providers globales
├── main.tsx                # Punto de entrada de la aplicación React
├── vite-env.d.ts           # Tipos para Vite (si se usa Vite en lugar de CRA)
|
├── @types/                 # Definiciones de tipos globales y de librerías sin tipos
│   └── index.d.ts
│   └── environment.d.ts    # Tipos para variables de entorno
|
├── assets/                 # Archivos estáticos (imágenes, fuentes, etc.)
│   ├── images/
│   └── fonts/
|
├── components/             # Componentes UI globales, reutilizables y agnósticos al dominio
│   ├── common/             # Componentes muy genéricos (Button, Input, Modal, Card, etc.)
│   │   ├── Button.tsx
│   │   └── ...
│   ├── layout/             # Componentes de estructura (Header, Sidebar, Footer, PageLayout)
│   │   ├── Header.tsx
│   │   └── ...
│   └── feedback/           # Componentes para feedback al usuario (Alert, Spinner, Skeleton)
│       ├── Alert.tsx
│       └── ...
|
├── config/                 # Configuración de la aplicación
│   ├── api.config.ts       # URL base de la API, timeouts, etc.
│   ├── constants.ts        # Constantes globales de la aplicación
│   └── routes.config.ts    # Definición de rutas y paths
|
├── contexts/               # (Si se usa Context API para estado global)
│   ├── AuthContext.tsx
│   └── ThemeContext.tsx
|
├── features/               # Módulos de funcionalidad principal (alineados con Casos de Uso)
│   ├── auth/               # Ejemplo: Módulo de Autenticación (CU13)
│   │   ├── api/            # Funciones específicas para llamar a los endpoints de autenticación
│   │   │   └── auth.api.ts
│   │   ├── components/     # Componentes específicos del feature (LoginForm, RegisterForm)
│   │   │   ├── LoginForm.tsx
│   │   │   └── UserProfileCard.tsx
│   │   ├── hooks/          # Hooks personalizados específicos del feature
│   │   │   └── useAuth.ts
│   │   ├── pages/          # Páginas/Vistas del feature ( ensamblan componentes)
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterAdminPage.tsx
│   │   │   └── ProfilePage.tsx
│   │   ├── routes/         # Definición de rutas específicas del feature
│   │   │   └── index.ts
│   │   ├── services/       # Lógica de negocio y orquestación (raramente necesario si se usan hooks y api bien)
│   │   ├── store/          # (Si se usa Zustand/Redux slice para estado del feature)
│   │   │   └── auth.store.ts
│   │   ├── types/          # Tipos y interfaces TypeScript específicos del feature
│   │   │   └── auth.types.ts
│   │   └── utils/          # Funciones de utilidad específicas del feature
│   │       └── auth.utils.ts
│   ├── users/              # Ejemplo: Módulo de Gestión de Usuarios (CU1)
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── routes/
│   │   ├── store/
│   │   └── types/
│   ├── courses/            # (CU3)
│   ├── periods/            # (CU14)
│   ├── grades/             # (CU5)
│   ├── attendance/         # (CU6)
│   ├── predictions/        # (CU9)
│   └── ...                 # Otros módulos basados en Casos de Uso
|
├── hooks/                  # Hooks personalizados globales y reutilizables en varios features
│   ├── useDebounce.ts
│   └── useLocalStorage.ts
|
├── layouts/                # Layouts principales de la aplicación (AppLayout, AuthLayout, DashboardLayout)
│   ├── AppLayout.tsx       # Layout para rutas autenticadas (con Sidebar, Header)
│   └── AuthLayout.tsx      # Layout para rutas de autenticación (centrado, simple)
|
├── lib/                    # Instancias configuradas de librerías externas
│   ├── axios.instance.ts   # Instancia de Axios configurada (baseURL, interceptors)
│   └── queryClient.ts      # (Si se usa React Query) Instancia de QueryClient
|
├── services/               # (Alternativa a `features/**/api/`) Servicios API más genéricos si no se opta por api por feature
│                           # Se prefiere `features/**/api/` para mayor cohesión.
|
├── store/                  # Configuración de estado global (si se usa Zustand o Redux Toolkit)
│   ├── index.ts            # Punto de entrada para el store global
│   └── (slices o stores individuales por feature, si se centralizan aquí)
|
├── styles/                 # Estilos globales, temas, variables CSS/SCSS
│   ├── global.css          # Estilos globales (reset, base styles)
│   ├── theme.ts            # Configuración del tema para la librería UI (ej. MUI Theme)
│   └── variables.scss      # Variables SASS/CSS
|
├── utils/                  # Funciones de utilidad generales y helpers
│   ├── date.utils.ts
│   ├── formatters.ts
│   └── validators.ts       # Validadores genéricos (pueden usarse con Zod)
```

**Principios de la Estructura de Carpetas:**

- **Modularidad por Feature**: Cada funcionalidad principal (feature) reside en su propia carpeta dentro de `src/features/`. Esto facilita la localización del código relacionado con una funcionalidad específica y promueve la encapsulación.
- **Cohesión**: Los componentes, hooks, tipos, servicios/API y páginas relacionados con un feature específico se encuentran juntos dentro de la carpeta del feature.
- **Bajo Acoplamiento**: Los features deben ser lo más independientes posible entre sí. La comunicación entre features se debe realizar a través de props, estado global o eventos, evitando importaciones directas complejas.
- **Reusabilidad**: Los componentes y hooks verdaderamente genéricos y reutilizables en múltiples features se colocan en `src/components/common/` y `src/hooks/` respectivamente.
- **Claridad**: La estructura debe ser intuitiva y fácil de entender para los nuevos desarrolladores que se unan al proyecto.

### 2.3. Principios de Diseño

- **Component-Based Architecture**: Construir la UI como una composición de componentes reutilizables e independientes.
- **Single Responsibility Principle (SRP)**: Cada componente, hook o función debe tener una única responsabilidad bien definida.
- **Don't Repeat Yourself (DRY)**: Evitar la duplicación de código mediante la creación de abstracciones y utilidades reutilizables.
- **Separation of Concerns**: Separar la lógica de presentación (componentes), la lógica de negocio (hooks, servicios) y la gestión de estado.
- **TypeScript First**: Aprovechar al máximo las capacidades de TypeScript para definir interfaces claras, tipos de datos y asegurar la corrección del tipado en todo el proyecto.
- **Atomic Design (Inspiración)**: Pensar en componentes en diferentes niveles de abstracción (átomos, moléculas, organismos, plantillas, páginas), aunque no se siga estrictamente la nomenclatura, el concepto de construir UIs complejas a partir de piezas más pequeñas es fundamental.
- **Manejo de Estado predecible**: Utilizar patrones claros para la gestión del estado, ya sea local (useState, useReducer) o global (Context, Zustand, Redux).
- **Inmutabilidad**: Preferir la inmutabilidad al trabajar con estados y props para evitar efectos secundarios inesperados y facilitar el seguimiento de cambios.
- **Código Limpio y Legible**: Escribir código que sea fácil de entender, mantener y depurar. Seguir las guías de estilo (ESLint, Prettier).
- **Pruebas**: Implementar pruebas unitarias y de integración para asegurar la calidad y estabilidad del código.

## 3. Configuración del Proyecto

Esta sección cubre los pasos iniciales para configurar un nuevo proyecto de frontend para Smart Academy utilizando React con TypeScript.

### 3.1. Inicialización del Proyecto (React + TypeScript)

Se recomienda utilizar [Vite](https://vitejs.dev/) para la creación de proyectos React con TypeScript debido a su rapidez en el entorno de desarrollo y su eficiente sistema de construcción. Alternativamente, [Create React App (CRA)](https://create-react-app.dev/) sigue siendo una opción válida.

**Opción 1: Usando Vite (Recomendado)**

```bash
# NPM
npm create vite@latest smart-academy-frontend -- --template react-ts

# Yarn
yarn create vite smart-academy-frontend --template react-ts

# PNPM
pnpm create vite smart-academy-frontend --template react-ts

cd smart-academy-frontend
```

**Opción 2: Usando Create React App**

```bash
npx create-react-app smart-academy-frontend --template typescript

cd smart-academy-frontend
```

### 3.2. Dependencias Esenciales

Una vez creado el proyecto, instala las siguientes dependencias esenciales:

```bash
# NPM
npm install axios react-router-dom@6 zustand react-hook-form zod @emotion/react @emotion/styled @mui/material date-fns
# Opcional para iconos de Material-UI
npm install @mui/icons-material

# Yarn
yarn add axios react-router-dom@6 zustand react-hook-form zod @emotion/react @emotion/styled @mui/material date-fns
# Opcional para iconos de Material-UI
yarn add @mui/icons-material
```

**Desglose de dependencias:**

- `axios`: Para peticiones HTTP.
- `react-router-dom@6`: Para enrutamiento.
- `zustand`: Para gestión de estado global (alternativa ligera a Redux).
- `react-hook-form`: Para manejo de formularios.
- `zod`: Para validación de esquemas (funciona bien con TypeScript y React Hook Form).
- `@mui/material`, `@emotion/react`, `@emotion/styled`: Para la librería de componentes Material-UI (si se elige esta opción). Si se opta por Ant Design o Tailwind CSS, se instalarían sus respectivas dependencias.
  - `@mui/icons-material`: Iconos para Material-UI.
- `date-fns`: Para manipulación de fechas (o `dayjs`).

**Dependencias de Desarrollo:**

Estas suelen venir preinstaladas con Vite/CRA, pero es bueno asegurarse y configurar:

```bash
# NPM
npm install -D eslint prettier eslint-config-prettier eslint-plugin-prettier eslint-plugin-react eslint-plugin-react-hooks @typescript-eslint/eslint-plugin @typescript-eslint/parser husky lint-staged

# Yarn
yarn add -D eslint prettier eslint-config-prettier eslint-plugin-prettier eslint-plugin-react eslint-plugin-react-hooks @typescript-eslint/eslint-plugin @typescript-eslint/parser husky lint-staged
```

### 3.3. Configuración de ESLint, Prettier y Husky

Para mantener la calidad y consistencia del código, es crucial configurar ESLint, Prettier y Husky.

**1. ESLint (`.eslintrc.js` o `.eslintrc.json`):**
   Configura ESLint para TypeScript y React. Un ejemplo de configuración (`.eslintrc.js`):

   ```javascript
   module.exports = {
     parser: '@typescript-eslint/parser',
     extends: [
       'plugin:react/recommended',
       'plugin:@typescript-eslint/recommended',
       'plugin:prettier/recommended',
       'plugin:react-hooks/recommended',
     ],
     parserOptions: {
       ecmaVersion: 2020,
       sourceType: 'module',
       ecmaFeatures: {
         jsx: true,
       },
     },
     settings: {
       react: {
         version: 'detect',
       },
     },
     rules: {
       // Aquí puedes añadir o sobrescribir reglas específicas
       'react/prop-types': 'off', // No necesario con TypeScript
       'react/react-in-jsx-scope': 'off', // No necesario con React 17+
       '@typescript-eslint/explicit-function-return-type': 'off',
       'prettier/prettier': ['error', { endOfLine: 'auto' }],
     },
   };
   ```

**2. Prettier (`.prettierrc.js` o `.prettierrc.json`):**
   Define tus reglas de formateo. Ejemplo (`.prettierrc.js`):

   ```javascript
   module.exports = {
     semi: true,
     trailingComma: 'es5',
     singleQuote: true,
     printWidth: 80,
     tabWidth: 2,
     endOfLine: 'lf',
   };
   ```

   Añade un archivo `.prettierignore` para excluir archivos del formateo:

   ```
   node_modules
   build
   dist
   coverage
   ```

**3. Husky y lint-staged (Hooks de Git):**
   Husky permite ejecutar scripts en diferentes etapas de Git (ej. pre-commit). `lint-staged` permite ejecutar linters solo en los archivos modificados.

   - Instala Husky:
     ```bash
     npx husky-init && npm install # o yarn
     ```
     Esto creará una carpeta `.husky`.

   - Modifica el hook `pre-commit` en `.husky/pre-commit`:
     ```bash
     #!/bin/sh
     . "$(dirname "$0")/_/husky.sh"

     npx lint-staged
     ```

   - Configura `lint-staged` en tu `package.json`:
     ```json
     {
       // ... otras configuraciones
       "lint-staged": {
         "*.{js,jsx,ts,tsx}": [
           "eslint --fix",
           "prettier --write"
         ],
         "*.{json,md,css,scss}": [
           "prettier --write"
         ]
       }
     }
     ```

**4. Scripts en `package.json`:**
   Añade scripts para linting y formateo:

   ```json
   {
     "scripts": {
       // ... otros scripts (dev, build, etc.)
       "lint": "eslint . --ext .ts,.tsx --report-unused-disable-directives --max-warnings 0",
       "format": "prettier --write \"src/**/*.{ts,tsx,json,css,md}\""
     }
   }
   ```

Con esta configuración, cada vez que intentes hacer un commit, ESLint y Prettier se ejecutarán automáticamente sobre los archivos modificados, asegurando que el código cumpla con los estándares definidos antes de ser subido al repositorio.

## 4. Componentes y Servicios Base

Esta sección detalla los componentes y servicios fundamentales que servirán como base para el desarrollo de las funcionalidades de la aplicación.

### 4.1. Servicio API (Axios Wrapper)

Es esencial centralizar la lógica de las peticiones HTTP para interactuar con el backend. Crearemos una instancia de Axios configurada (`src/lib/axios.instance.ts`) que maneje la URL base, los headers comunes (como `Content-Type`), y los interceptores para la gestión de tokens JWT y errores globales.

**`src/lib/axios.instance.ts` (Ejemplo):**

```typescript
import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig, AxiosResponse } from 'axios';
import { API_BASE_URL } from '@/config/api.config'; // Asumiendo que tienes este archivo
import { useAuthStore } from '@/features/auth/store/auth.store'; // Ejemplo de store de autenticación con Zustand

const axiosInstance: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor de Peticiones
axiosInstance.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = useAuthStore.getState().accessToken; // Obtener token del store
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Interceptor de Respuestas
axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Manejar error de autenticación (ej. token expirado)
      // Podrías intentar refrescar el token o redirigir al login
      useAuthStore.getState().logout(); // Ejemplo de acción de logout
      // Opcionalmente, podrías redirigir:
      // window.location.href = '/login';
      console.error('Unauthorized access - 401. Logging out.');
    }
    // Aquí puedes añadir manejo para otros errores comunes (500, 403, etc.)
    // Por ejemplo, mostrar una notificación global de error.
    return Promise.reject(error);
  }
);

export default axiosInstance;
```

**Uso en los `features`:**
Cada `feature` tendrá su propio archivo `api` (ej. `src/features/auth/api/auth.api.ts`) que importará `axiosInstance` para realizar las llamadas específicas a sus endpoints.

**Ejemplo (`src/features/auth/api/auth.api.ts`):**

```typescript
import axiosInstance from '@/lib/axios.instance';
import { LoginCredentials, LoginResponse, UserProfile } from '../types/auth.types'; // Tipos específicos del feature

export const loginUser = async (credentials: LoginCredentials): Promise<LoginResponse> => {
  const response = await axiosInstance.post<LoginResponse>('/auth/login', credentials);
  return response.data;
};

export const getMe = async (): Promise<UserProfile> => {
  const response = await axiosInstance.get<UserProfile>('/auth/users/me');
  return response.data;
};

// ...otras funciones API para autenticación
```

### 4.2. Gestión de Estado Global

Como se mencionó en las tecnologías, [Zustand](https://zustand-demo.pmnd.rs/) es la opción recomendada para la gestión de estado global debido a su simplicidad y rendimiento. React Context API puede usarse para estados más localizados o temáticos (como el tema de la UI).

**Ejemplo de un Store de Autenticación con Zustand (`src/features/auth/store/auth.store.ts`):**

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { UserProfile } from '../types/auth.types'; // Asumiendo que tienes este tipo

interface AuthState {
  accessToken: string | null;
  user: UserProfile | null;
  isAuthenticated: boolean;
  setAuthData: (token: string, userData: UserProfile) => void;
  logout: () => void;
  // Podrías añadir isLoading, error, etc.
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      accessToken: null,
      user: null,
      isAuthenticated: false,
      setAuthData: (token, userData) => {
        set({
          accessToken: token,
          user: userData,
          isAuthenticated: true,
        });
      },
      logout: () => {
        set({
          accessToken: null,
          user: null,
          isAuthenticated: false,
        });
        // Opcionalmente, limpiar otros stores o caches aquí
      },
    }),
    {
      name: 'auth-storage', // Nombre de la clave en localStorage/sessionStorage
      storage: createJSONStorage(() => localStorage), // Puedes usar sessionStorage si prefieres
      // Opcionalmente, puedes elegir qué partes del estado persistir:
      // partialize: (state) => ({ accessToken: state.accessToken, user: state.user }),
    }
  )
);
```

**Uso en componentes:**

```tsx
import { useAuthStore } from '@/features/auth/store/auth.store';

const MyComponent = () => {
  const { user, isAuthenticated, logout } = useAuthStore();

  if (!isAuthenticated) {
    return <p>Por favor, inicia sesión.</p>;
  }

  return (
    <div>
      <p>Bienvenido, {user?.full_name}</p>
      <button onClick={logout}>Cerrar Sesión</button>
    </div>
  );
};
```

### 4.3. Sistema de Enrutamiento (React Router DOM v6)

React Router DOM v6 se utilizará para manejar la navegación. Las rutas se definirán de forma centralizada y por feature.

**Configuración Principal de Rutas (`src/App.tsx` o un archivo dedicado `src/routes/index.tsx`):**

```tsx
// src/App.tsx (ejemplo simplificado)
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppLayout } from '@/layouts/AppLayout';
import { AuthLayout } from '@/layouts/AuthLayout';
import { LoginPage } from '@/features/auth/pages/LoginPage';
import { DashboardPage } from '@/features/dashboard/pages/DashboardPage'; // Asumiendo que existe
import { useAuthStore } from '@/features/auth/store/auth.store';

// Componente para rutas protegidas
const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rutas de Autenticación */}
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<LoginPage />} />
          {/* Otras rutas de autenticación como /register, /forgot-password */}
        </Route>

        {/* Rutas Protegidas (Aplicación Principal) */}
        <Route 
          path="/app" 
          element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="dashboard" replace />} /> {/* Redirige /app a /app/dashboard */}
          <Route path="dashboard" element={<DashboardPage />} />
          {/* Aquí se anidarían las rutas de otros features (usuarios, cursos, etc.) */}
          {/* Ejemplo: <Route path="users/*" element={<UserRoutes />} /> */}
        </Route>
        
        {/* Ruta raíz, redirige según autenticación */}
        <Route 
          path="/" 
          element={
            useAuthStore.getState().isAuthenticated ? (
              <Navigate to="/app/dashboard" replace />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        
        {/* Ruta para Not Found (404) */}
        <Route path="*" element={<div><h1>404 - Página No Encontrada</h1></div>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

**Rutas por Feature (`src/features/users/routes/index.tsx`):**

```tsx
import { Routes, Route } from 'react-router-dom';
import { UserListPage } from '../pages/UserListPage';
import { UserDetailPage } from '../pages/UserDetailPage';
import { CreateUserPage } from '../pages/CreateUserPage';

export const UserRoutes = () => {
  return (
    <Routes>
      <Route path="" element={<UserListPage />} />
      <Route path="new" element={<CreateUserPage />} />
      <Route path=":userId" element={<UserDetailPage />} />
      {/* Más rutas específicas de usuarios */}
    </Routes>
  );
};
```
Estas `UserRoutes` se importarían y usarían en `App.tsx`.

### 4.4. Componentes UI Reutilizables

Se crearán componentes genéricos en `src/components/common/` y `src/components/layout/`.

- **`src/components/common/`**: Botones, Inputs, Modales, Cards, Spinners, Alertas, etc. Estos componentes deben ser altamente reutilizables y personalizables mediante props.
  - Ejemplo: `Button.tsx`, `InputField.tsx`, `ModalWrapper.tsx`.
  - Deberían encapsular la lógica de la librería UI elegida (ej. MUI) o ser componentes personalizados.
- **`src/components/layout/`**: Componentes para la estructura de la página como `Header.tsx`, `Sidebar.tsx`, `Footer.tsx`, `PageLayout.tsx` (que podría combinar los anteriores).

**Principios para Componentes Reutilizables:**
- **Agnósticos al Dominio**: No deben contener lógica de negocio específica de un feature.
- **Personalizables**: A través de props (incluyendo `className`, `style`, y props específicas de la librería UI).
- **Bien Tipados**: Con TypeScript para definir claramente sus props y comportamiento.
- **Accesibles**: Siguiendo las pautas de accesibilidad (WAI-ARIA).

### 4.5. Layouts Principales

Los layouts definen la estructura general de diferentes secciones de la aplicación. Se ubicarán en `src/layouts/`.

- **`AuthLayout.tsx`**: Layout para páginas de autenticación (login, registro). Suele ser simple, centrado y sin navegación principal.
  ```tsx
  // src/layouts/AuthLayout.tsx
  import { Outlet } from 'react-router-dom';
  import { Container, Box } from '@mui/material'; // Ejemplo con MUI

  export const AuthLayout = () => {
    return (
      <Container component="main" maxWidth="xs">
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          {/* Aquí podría ir un logo o título general */}
          <Outlet /> {/* Aquí se renderizarán las páginas de login, registro, etc. */}
        </Box>
      </Container>
    );
  };
  ```

- **`AppLayout.tsx`**: Layout para las páginas principales de la aplicación una vez que el usuario está autenticado. Incluirá elementos como `Header`, `Sidebar`, y el área de contenido principal donde se renderizan las vistas de los features.
  ```tsx
  // src/layouts/AppLayout.tsx
  import { Outlet } from 'react-router-dom';
  import { Box, CssBaseline } from '@mui/material'; // Ejemplo con MUI
  import { Header } from '@/components/layout/Header'; // Asumiendo que existen
  import { Sidebar } from '@/components/layout/Sidebar';

  const DRAWER_WIDTH = 240;

  export const AppLayout = () => {
    // Lógica para manejar el estado del sidebar (abierto/cerrado) si es necesario
    return (
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <Header drawerWidth={DRAWER_WIDTH} />
        <Sidebar drawerWidth={DRAWER_WIDTH} />
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3,
            width: { sm: `calc(100% - ${DRAWER_WIDTH}px)` },
            mt: '64px', // Altura del Header
          }}
        >
          <Outlet /> {/* Aquí se renderizarán las páginas de los features */}
        </Box>
      </Box>
    );
  };
  ```

Estos layouts se utilizan en la configuración de rutas para envolver grupos de páginas que comparten una estructura común.

## 5. Módulos y Vistas Principales (Alineados con Casos de Uso)

Esta sección describe la organización del frontend en módulos funcionales, cada uno correspondiendo a un conjunto de Casos de Uso (CU) definidos en el backend (`README.md`). Cada módulo encapsulará sus propias vistas (páginas), componentes específicos, lógica de estado, servicios API y tipos de datos.

La estructura de carpetas `src/features/[nombre-del-modulo]/` se utilizará para cada uno de estos módulos.

### 5.1. Módulo de Autenticación (CU13)

Este módulo maneja todos los aspectos relacionados con la autenticación y seguridad de los usuarios.

- **Caso de Uso Backend Asociado:** CU13: Gestión de autenticación y seguridad (web/mobile).
- **Ubicación:** `src/features/auth/`

**Vistas Principales:**

1.  **`LoginPage.tsx` (`/login`)**
    -   **Propósito:** Permitir a los usuarios iniciar sesión.
    -   **Componentes Clave:** Formulario de inicio de sesión (`LoginForm.tsx` con campos para email/usuario y contraseña), manejo de errores de validación y de la API.
    -   **Endpoints Consumidos:**
        -   `POST /api/v1/auth/login` (para obtener el token de acceso).
    -   **Estado Local/Global:**
        -   Estado del formulario (manejado por React Hook Form).
        -   Estado de carga (loading) durante la petición.
        -   Errores de la API.
        -   Al éxito, actualiza el `authStore` (Zustand) con el token y datos del usuario.
    -   **Flujo:**
        1.  Usuario ingresa credenciales.
        2.  Validación de formulario (cliente).
        3.  Envío de credenciales al backend.
        4.  Si éxito: almacena token y datos del usuario en `authStore`, redirige al dashboard (`/app/dashboard`).
        5.  Si error: muestra mensaje de error.

2.  **`RegisterPage.tsx` (`/register`) (Opcional, si aplica)**
    -   **Propósito:** Permitir a nuevos usuarios registrarse (si el sistema lo requiere y no es solo por invitación/admin).
    -   **Componentes Clave:** Formulario de registro.
    -   **Endpoints Consumidos:**
        -   `POST /api/v1/auth/users/` (o el endpoint específico para creación de usuarios si es diferente para auto-registro).
    -   **Estado Local/Global:** Similar a `LoginPage`.

3.  **`ForgotPasswordPage.tsx` (`/forgot-password`) (Opcional, si aplica)**
    -   **Propósito:** Permitir a los usuarios solicitar un reseteo de contraseña.
    -   **Endpoints Consumidos:** Endpoint para solicitar reseteo de contraseña (ej. `POST /api/v1/auth/password-recovery/{email}`).

4.  **`ResetPasswordPage.tsx` (`/reset-password/:token`) (Opcional, si aplica)**
    -   **Propósito:** Permitir a los usuarios establecer una nueva contraseña usando un token de reseteo.
    -   **Endpoints Consumidos:** Endpoint para confirmar nueva contraseña (ej. `POST /api/v1/auth/reset-password/`).

**Componentes Específicos del Módulo (`src/features/auth/components/`):**

-   `LoginForm.tsx`: Formulario reutilizable para el inicio de sesión.
-   `RegisterForm.tsx`: Formulario reutilizable para el registro.

**Servicios API (`src/features/auth/api/auth.api.ts`):**

-   `loginUser(credentials)`: Envía petición de login.
-   `registerUser(data)`: Envía petición de registro.
-   `getMe()`: Obtiene el perfil del usuario autenticado (usado después del login o al cargar la app para verificar sesión).
    -   Consume `GET /api/v1/auth/users/me`.
-   `logoutUser()`: (Podría no ser una llamada API si el logout es solo limpiar el estado del cliente, o podría llamar a un endpoint `POST /api/v1/auth/logout` si el backend invalida tokens).

**Gestión de Estado (`src/features/auth/store/auth.store.ts`):**

-   Utiliza `useAuthStore` (Zustand) para almacenar:
    -   `accessToken: string | null`
    -   `user: UserProfile | null` (perfil del usuario autenticado, obtenido de `ejemplosjson.md` para `UserRead`)
    -   `isAuthenticated: boolean`
    -   `isLoading: boolean`
    -   `error: string | null`
-   Acciones como `setAuthData`, `logout`, `setLoading`, `setError`.

**Tipos de Datos (`src/features/auth/types/auth.types.ts`):**

-   `LoginCredentials`, `LoginResponse`, `UserProfile` (basado en `UserRead` de `ejemplosjson.md`), `RegisterPayload`, etc.

**Consideraciones Adicionales:**

-   **Protección de Rutas:** Se usará un componente `ProtectedRoute.tsx` (como se definió en la sección 4.3) que verificará `isAuthenticated` del `authStore` para restringir el acceso a rutas protegidas.
-   **Manejo de Token:** El token JWT se almacenará de forma segura (ej. `localStorage` a través de `zustand/persist`) y se enviará en los encabezados de las peticiones API mediante el interceptor de Axios.
-   **Refresco de Token (Opcional Avanzado):** Si el backend implementa tokens de refresco, el interceptor de Axios podría manejar la lógica para refrescar un token de acceso expirado automáticamente.

### 5.2. Módulo de Gestión de Usuarios (Admin - CU1, CU2, CU3, CU4, CU5)

Este módulo proporciona las funcionalidades para que los administradores gestionen las cuentas de usuario del sistema.

- **Casos de Uso Backend Asociados:**
    - CU1: Creación de usuarios.
    - CU2: Lectura de usuarios.
    - CU3: Actualización de usuarios.
    - CU4: Eliminación de usuarios.
    - CU5: Asignación/revocación de roles a usuarios.
- **Ubicación:** `src/features/users/`
- **Acceso Principal:** Rol Administrador.

**Vistas Principales:**

1.  **`UserListPage.tsx` (`/app/users`)**
    -   **Propósito:** Mostrar una lista paginada y filtrable de todos los usuarios del sistema. Permitir acciones rápidas como editar, eliminar o ver detalles.
    -   **Componentes Clave:** Tabla de usuarios (`UserDataGrid.tsx` o similar), filtros de búsqueda (por nombre, email, rol), paginación, botón para crear nuevo usuario.
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/users/` (con parámetros de paginación y filtros).
        -   `DELETE /api/v1/users/{user_id}` (para eliminación rápida desde la lista).
    -   **Estado Local/Global:**
        -   Lista de usuarios.
        -   Parámetros de paginación y filtros.
        -   Estado de carga y errores.
        -   Estado de confirmación para eliminación.
    -   **Flujo:**
        1.  Al cargar, obtiene la lista de usuarios.
        2.  Permite al admin filtrar y paginar la lista.
        3.  Permite navegar a la página de creación de usuario.
        4.  Permite navegar a la página de edición/detalle de un usuario.
        5.  Permite eliminar usuarios (con confirmación).

2.  **`CreateUserPage.tsx` (`/app/users/new`)**
    -   **Propósito:** Permitir al administrador crear un nuevo usuario.
    -   **Componentes Clave:** Formulario de creación de usuario (`UserForm.tsx` con campos para nombre completo, email, contraseña inicial, roles, etc.).
    -   **Endpoints Consumidos:**
        -   `POST /api/v1/users/` (Payload: `UserCreate` de `ejemplosjson.md`).
        -   (Opcional) `GET /api/v1/roles/` para obtener la lista de roles disponibles para asignar.
    -   **Estado Local/Global:**
        -   Estado del formulario.
        -   Lista de roles disponibles (si se cargan dinámicamente).
        -   Estado de carga y errores.
    -   **Flujo:**
        1.  Admin completa el formulario.
        2.  Validación cliente.
        3.  Envío de datos al backend.
        4.  Si éxito, redirige a la lista de usuarios o al detalle del nuevo usuario, muestra notificación de éxito.
        5.  Si error, muestra mensaje de error.

3.  **`EditUserPage.tsx` (`/app/users/:userId/edit`)**
    -   **Propósito:** Permitir al administrador editar los datos de un usuario existente, incluyendo sus roles.
    -   **Componentes Clave:** Formulario de edición de usuario (`UserForm.tsx` precargado con datos del usuario), selector de roles.
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/users/{user_id}` (para obtener los datos actuales del usuario).
        -   `PUT /api/v1/users/{user_id}` (Payload: `UserUpdate` de `ejemplosjson.md`).
        -   `POST /api/v1/users/{user_id}/roles` (Payload: `RoleAssignment` de `ejemplosjson.md`) o un endpoint PUT que actualice roles junto con otros datos del usuario.
        -   (Opcional) `GET /api/v1/roles/` para obtener la lista de roles disponibles.
    -   **Estado Local/Global:**
        -   Datos del usuario a editar.
        -   Estado del formulario.
        -   Lista de roles disponibles.
        -   Estado de carga y errores.
    -   **Flujo:**
        1.  Carga datos del usuario.
        2.  Admin modifica el formulario.
        3.  Validación cliente.
        4.  Envío de datos actualizados al backend.
        5.  Si éxito, redirige a la lista de usuarios o al detalle del usuario, muestra notificación de éxito.
        6.  Si error, muestra mensaje de error.

4.  **`UserDetailPage.tsx` (`/app/users/:userId`) (Opcional, si no se combina con EditUserPage)**
    -   **Propósito:** Mostrar información detallada de un usuario.
    -   **Componentes Clave:** Visualización de datos del usuario, roles asignados, quizás actividad reciente.
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/users/{user_id}`.
    -   **Estado Local/Global:** Datos del usuario, estado de carga.

**Componentes Específicos del Módulo (`src/features/users/components/`):**

-   `UserForm.tsx`: Formulario reutilizable para crear y editar usuarios. Incluye validación con Zod.
-   `UserDataGrid.tsx` o `UserTable.tsx`: Componente para mostrar la lista de usuarios con funcionalidades de ordenamiento, filtrado y paginación (podría usar MUI DataGrid).
-   `RoleSelector.tsx`: Componente para seleccionar uno o varios roles para un usuario.

**Servicios API (`src/features/users/api/user.api.ts`):**

-   `getUsers(params)`: Obtiene la lista de usuarios.
-   `getUserById(userId)`: Obtiene un usuario específico.
-   `createUser(userData)`: Crea un nuevo usuario.
-   `updateUser(userId, userData)`: Actualiza un usuario.
-   `deleteUser(userId)`: Elimina un usuario.
-   `assignRolesToUser(userId, roleIds)`: Asigna roles a un usuario.
-   (Opcional) `getRoles()`: Obtiene la lista de todos los roles disponibles.

**Gestión de Estado (`src/features/users/store/user.store.ts`) (Opcional):**

-   Aunque muchas operaciones pueden ser manejadas con estado local en las vistas/componentes (usando React Query, SWR, o estado local simple para formularios), podría haber un store de Zustand si se necesita compartir estado complejo de usuarios o filtros entre múltiples componentes no relacionados directamente.
-   Por ejemplo, para mantener los filtros de la `UserListPage` si el usuario navega fuera y vuelve.

**Tipos de Datos (`src/features/users/types/user.types.ts`):**

-   `User`, `UserCreate`, `UserUpdate` (basados en `UserRead`, `UserCreate`, `UserUpdate` de `ejemplosjson.md`).
-   `Role` (basado en `RoleRead` de `ejemplosjson.md`).
-   `RoleAssignment` (basado en `RoleAssignment` de `ejemplosjson.md`).
-   Tipos para parámetros de paginación y filtros.

**Consideraciones Adicionales:**

-   **Seguridad:** Asegurar que solo los usuarios con rol de administrador puedan acceder a estas funcionalidades. Esto se maneja a nivel de rutas y, crucialmente, a nivel de API backend.
-   **Experiencia de Usuario (UX):** Proveer feedback claro durante las operaciones (carga, éxito, error). Usar modales de confirmación para acciones destructivas como la eliminación.
-   **Validación:** Implementar validación robusta tanto en el cliente (React Hook Form + Zod) como en el backend.

### 5.3. Módulo de Gestión de Roles (Admin - CU6)

Este módulo permite a los administradores gestionar los roles del sistema, que definen los permisos y accesos de los usuarios.

- **Caso de Uso Backend Asociado:** CU6: Gestión de Roles (CRUD).
- **Ubicación:** `src/features/roles/`
- **Acceso Principal:** Rol Administrador.

**Vistas Principales:**

1.  **`RoleListPage.tsx` (`/app/roles`)**
    -   **Propósito:** Mostrar una lista de todos los roles del sistema. Permitir acciones como editar, eliminar o ver detalles.
    -   **Componentes Clave:** Tabla de roles (`RoleDataGrid.tsx` o similar), botón para crear nuevo rol.
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/roles/`
        -   `DELETE /api/v1/roles/{role_id}` (para eliminación desde la lista).
    -   **Estado Local/Global:**
        -   Lista de roles.
        -   Estado de carga y errores.
        -   Estado de confirmación para eliminación.
    -   **Flujo:**
        1.  Al cargar, obtiene la lista de roles.
        2.  Permite navegar a la página de creación de rol.
        3.  Permite navegar a la página de edición de un rol.
        4.  Permite eliminar roles (con confirmación, y considerando implicaciones si hay usuarios con ese rol).

2.  **`CreateRolePage.tsx` (`/app/roles/new`)**
    -   **Propósito:** Permitir al administrador crear un nuevo rol.
    -   **Componentes Clave:** Formulario de creación de rol (`RoleForm.tsx` con campos para nombre del rol, descripción, y posiblemente permisos asociados si la granularidad es fina).
    -   **Endpoints Consumidos:**
        -   `POST /api/v1/roles/` (Payload: `RoleCreate` de `ejemplosjson.md`).
    -   **Estado Local/Global:**
        -   Estado del formulario.
        -   Estado de carga y errores.
    -   **Flujo:**
        1.  Admin completa el formulario.
        2.  Validación cliente.
        3.  Envío de datos al backend.
        4.  Si éxito, redirige a la lista de roles, muestra notificación de éxito.
        5.  Si error, muestra mensaje de error.

3.  **`EditRolePage.tsx` (`/app/roles/:roleId/edit`)**
    -   **Propósito:** Permitir al administrador editar los datos de un rol existente.
    -   **Componentes Clave:** Formulario de edición de rol (`RoleForm.tsx` precargado con datos del rol).
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/roles/{role_id}` (para obtener los datos actuales del rol).
        -   `PUT /api/v1/roles/{role_id}` (Payload: `RoleUpdate` de `ejemplosjson.md`).
    -   **Estado Local/Global:**
        -   Datos del rol a editar.
        -   Estado del formulario.
        -   Estado de carga y errores.
    -   **Flujo:**
        1.  Carga datos del rol.
        2.  Admin modifica el formulario.
        3.  Validación cliente.
        4.  Envío de datos actualizados al backend.
        5.  Si éxito, redirige a la lista de roles, muestra notificación de éxito.
        6.  Si error, muestra mensaje de error.

**Componentes Específicos del Módulo (`src/features/roles/components/`):**

-   `RoleForm.tsx`: Formulario reutilizable para crear y editar roles. Incluye validación.
-   `RoleDataGrid.tsx` o `RoleTable.tsx`: Componente para mostrar la lista de roles.

**Servicios API (`src/features/roles/api/role.api.ts`):**

-   `getRoles()`: Obtiene la lista de roles.
-   `getRoleById(roleId)`: Obtiene un rol específico.
-   `createRole(roleData)`: Crea un nuevo rol.
-   `updateRole(roleId, roleData)`: Actualiza un rol.
-   `deleteRole(roleId)`: Elimina un rol.

**Gestión de Estado (`src/features/roles/store/role.store.ts`) (Probablemente no necesario):**

-   La gestión de estado para roles puede manejarse principalmente con estado local en los componentes/vistas o mediante librerías de fetching de datos como React Query/SWR, que proporcionan cache y re-fetching.

**Tipos de Datos (`src/features/roles/types/role.types.ts`):**

-   `Role`, `RoleCreate`, `RoleUpdate` (basados en `RoleRead`, `RoleCreate`, `RoleUpdate` de `ejemplosjson.md`).

**Consideraciones Adicionales:**

-   **Dependencias:** Considerar las implicaciones de eliminar un rol que está asignado a usuarios. El backend debería manejar esto (ej. impidiendo la eliminación o requiriendo la reasignación de usuarios), y el frontend debería informar al usuario.
-   **Permisos Granulares (Opcional):** Si el sistema requiere una gestión de permisos más fina (asignar permisos específicos a roles), este módulo podría expandirse para incluir dicha funcionalidad, lo que implicaría más endpoints y complejidad en la UI.
-   **UX:** Feedback claro para todas las operaciones CRUD.

### 5.4. Módulo de Gestión de Períodos Académicos (Admin - CU7)

Este módulo es utilizado por los administradores para crear, visualizar, actualizar y eliminar los períodos académicos (ej. "2023-I", "2023-II", "Verano 2024").

- **Caso de Uso Backend Asociado:** CU7: Gestión de Periodos Académicos (CRUD).
- **Ubicación:** `src/features/academic-periods/`
- **Acceso Principal:** Rol Administrador.

**Vistas Principales:**

1.  **`AcademicPeriodListPage.tsx` (`/app/academic-periods`)**
    -   **Propósito:** Mostrar una lista de todos los períodos académicos. Permitir acciones como editar, eliminar.
    -   **Componentes Clave:** Tabla de períodos (`AcademicPeriodDataGrid.tsx`), botón para crear nuevo período.
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/academic-periods/`
        -   `DELETE /api/v1/academic-periods/{period_id}`.
    -   **Estado Local/Global:**
        -   Lista de períodos académicos.
        -   Estado de carga y errores.
        -   Confirmación para eliminación.
    -   **Flujo:**
        1.  Carga la lista de períodos.
        2.  Permite navegar a la creación o edición de períodos.
        3.  Permite eliminar períodos (con confirmación y considerando dependencias, ej. cursos asociados).

2.  **`CreateAcademicPeriodPage.tsx` (`/app/academic-periods/new`)**
    -   **Propósito:** Crear un nuevo período académico.
    -   **Componentes Clave:** Formulario (`AcademicPeriodForm.tsx`) con campos para nombre (ej. "2024-I"), fecha de inicio y fecha de fin.
    -   **Endpoints Consumidos:**
        -   `POST /api/v1/academic-periods/` (Payload: `AcademicPeriodCreate` de `ejemplosjson.md`).
    -   **Estado Local/Global:** Estado del formulario, carga, errores.
    -   **Flujo:**
        1.  Admin completa el formulario.
        2.  Validación cliente.
        3.  Envío al backend.
        4.  Si éxito, redirige a la lista y notifica.
        5.  Si error, muestra mensaje.

3.  **`EditAcademicPeriodPage.tsx` (`/app/academic-periods/:periodId/edit`)**
    -   **Propósito:** Editar un período académico existente.
    -   **Componentes Clave:** Formulario (`AcademicPeriodForm.tsx`) precargado.
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/academic-periods/{period_id}`.
        -   `PUT /api/v1/academic-periods/{period_id}` (Payload: `AcademicPeriodUpdate` de `ejemplosjson.md`).
    -   **Estado Local/Global:** Datos del período, estado del formulario, carga, errores.
    -   **Flujo:**
        1.  Carga datos del período.
        2.  Admin modifica.
        3.  Validación y envío.
        4.  Si éxito, redirige y notifica.
        5.  Si error, muestra mensaje.

**Componentes Específicos del Módulo (`src/features/academic-periods/components/`):**

-   `AcademicPeriodForm.tsx`: Formulario para crear/editar períodos.
-   `AcademicPeriodDataGrid.tsx`: Tabla para listar períodos.

**Servicios API (`src/features/academic-periods/api/academicPeriod.api.ts`):**

-   `getAcademicPeriods()`
-   `getAcademicPeriodById(periodId)`
-   `createAcademicPeriod(data)`
-   `updateAcademicPeriod(periodId, data)`
-   `deleteAcademicPeriod(periodId)`

**Gestión de Estado:**

-   Principalmente estado local y cache de SWR/React Query.

**Tipos de Datos (`src/features/academic-periods/types/academicPeriod.types.ts`):**

-   `AcademicPeriod`, `AcademicPeriodCreate`, `AcademicPeriodUpdate` (basados en `AcademicPeriodRead`, `AcademicPeriodCreate`, `AcademicPeriodUpdate` de `ejemplosjson.md`).

**Consideraciones Adicionales:**

-   **Validación de Fechas:** Asegurar que la fecha de inicio sea anterior a la fecha de fin. Manejar superposición de fechas si es una restricción del negocio.
-   **Dependencias:** Considerar cómo afecta la eliminación de un período a entidades asociadas (cursos, calificaciones, etc.). El backend debe manejar la lógica de restricción o cascada, y el frontend debe informar adecuadamente.

### 5.5. Módulo de Gestión de Cursos (Admin, Docente - CU8)

Este módulo permite a los administradores y docentes gestionar los cursos, incluyendo su creación, asignación de docentes, inscripción de estudiantes y detalles del curso.

- **Caso de Uso Backend Asociado:** CU8: Gestión de Cursos (CRUD y gestión de estudiantes en cursos).
- **Ubicación:** `src/features/courses/`
- **Acceso Principal:** Administrador (CRUD completo), Docente (Read, Update para sus cursos, gestión de estudiantes en sus cursos).

**Vistas Principales:**

1.  **`CourseListPage.tsx` (`/app/courses`)**
    -   **Propósito:** Mostrar una lista paginada y filtrable de todos los cursos. Para administradores, todos los cursos. Para docentes, los cursos que imparten.
    -   **Componentes Clave:** Tabla de cursos (`CourseDataGrid.tsx`), filtros (por nombre, período académico, docente), paginación, botón para crear nuevo curso (Admin).
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/courses/` (con parámetros de filtro y paginación. El backend debería filtrar por docente si el usuario es docente).
        -   `DELETE /api/v1/courses/{course_id}` (Admin).
    -   **Estado Local/Global:** Lista de cursos, filtros, paginación, carga, errores.
    -   **Flujo:**
        1.  Carga lista de cursos según rol.
        2.  Permite filtrar y paginar.
        3.  Admin: puede navegar a crear curso o editar/eliminar cualquier curso.
        4.  Docente: puede navegar a ver/editar detalles de sus cursos.

2.  **`CreateCoursePage.tsx` (`/app/courses/new`) (Admin)**
    -   **Propósito:** Permitir al administrador crear un nuevo curso.
    -   **Componentes Clave:** Formulario (`CourseForm.tsx`) con campos para nombre, descripción, período académico, docente asignado.
    -   **Endpoints Consumidos:**
        -   `POST /api/v1/courses/` (Payload: `CourseCreate` de `ejemplosjson.md`).
        -   `GET /api/v1/academic-periods/` (para selector de período).
        -   `GET /api/v1/users/?role=docente` (para selector de docentes).
    -   **Estado Local/Global:** Estado del formulario, listas de períodos y docentes, carga, errores.
    -   **Flujo:** Admin completa, valida, envía. Redirige y notifica.

3.  **`EditCoursePage.tsx` (`/app/courses/:courseId/edit`) (Admin, Docente)**
    -   **Propósito:** Editar un curso existente. Admin puede editar todo. Docente puede editar detalles de sus cursos (ej. descripción, materiales, pero no período o docente asignado, según reglas de negocio).
    -   **Componentes Clave:** Formulario (`CourseForm.tsx`) precargado. Campos editables pueden variar según rol.
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/courses/{course_id}`.
        -   `PUT /api/v1/courses/{course_id}` (Payload: `CourseUpdate` de `ejemplosjson.md`).
        -   (Opcional) Selectores para período/docente si el admin edita.
    -   **Estado Local/Global:** Datos del curso, estado del formulario, carga, errores.
    -   **Flujo:** Carga datos, modifica, valida, envía. Redirige y notifica.

4.  **`CourseDetailPage.tsx` (`/app/courses/:courseId`) (Admin, Docente, Estudiante)**
    -   **Propósito:** Mostrar información detallada de un curso, incluyendo estudiantes inscritos, materiales, etc. Las acciones disponibles varían por rol.
    -   **Componentes Clave:** Información del curso, lista de estudiantes inscritos (`StudentListInCourse.tsx`), sección de materiales, etc.
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/courses/{course_id}`.
        -   `GET /api/v1/courses/{course_id}/students` (Admin, Docente).
        -   `POST /api/v1/courses/{course_id}/students` (Admin, Docente - para inscribir).
        -   `DELETE /api/v1/courses/{course_id}/students/{student_id}` (Admin, Docente - para desinscribir).
    -   **Estado Local/Global:** Datos del curso, lista de estudiantes, carga, errores.
    -   **Flujo (Admin/Docente):**
        1.  Ver detalles del curso.
        2.  Ver/Gestionar estudiantes inscritos (añadir/eliminar).
        3.  (Futuro) Gestionar materiales, tareas, etc.

**Componentes Específicos del Módulo (`src/features/courses/components/`):**

-   `CourseForm.tsx`: Formulario para crear/editar cursos.
-   `CourseDataGrid.tsx`: Tabla para listar cursos.
-   `StudentListInCourse.tsx`: Componente para mostrar y gestionar estudiantes en un curso (con buscador para añadir estudiantes no inscritos).
-   `AcademicPeriodSelector.tsx`, `TeacherSelector.tsx`: Selectores reutilizables.

**Servicios API (`src/features/courses/api/course.api.ts`):**

-   `getCourses(params)`
-   `getCourseById(courseId)`
-   `createCourse(data)` (Admin)
-   `updateCourse(courseId, data)` (Admin, Docente para sus cursos)
-   `deleteCourse(courseId)` (Admin)
-   `getStudentsInCourse(courseId)`
-   `addStudentToCourse(courseId, studentId)`
-   `removeStudentFromCourse(courseId, studentId)`

**Gestión de Estado (`src/features/courses/store/course.store.ts`) (Opcional):**

-   Podría usarse para el estado de filtros complejos o para compartir datos del curso seleccionado entre vistas/componentes si no se usa React Query/SWR de forma extensiva.

**Tipos de Datos (`src/features/courses/types/course.types.ts`):**

-   `Course`, `CourseCreate`, `CourseUpdate` (basados en `CourseRead`, `CourseCreate`, `CourseUpdate` de `ejemplosjson.md`).
-   `StudentInCourse` (podría ser un `UserRead` simplificado o un tipo específico).
-   `AcademicPeriodBasic` (para selectores, ej. `id`, `name`).
-   `TeacherBasic` (para selectores, ej. `id`, `full_name`).

**Consideraciones Adicionales:**

-   **Roles y Permisos:** La UI debe adaptarse dinámicamente según el rol del usuario (Admin vs Docente). Los botones de acción (crear, editar, eliminar, inscribir) deben mostrarse/ocultarse condicionalmente.
-   **Inscripción de Estudiantes:** La UI para inscribir estudiantes podría incluir una búsqueda/selector de estudiantes existentes en el sistema.
-   **Dependencias:** La eliminación de cursos con estudiantes inscritos o con datos asociados (calificaciones, asistencia) debe manejarse con cuidado, preferiblemente con archivado o restricciones en el backend.

### 5.6. Módulo de Gestión de Calificaciones (Docente, Estudiante - CU9)

Este módulo permite a los docentes registrar, actualizar y eliminar calificaciones para los estudiantes en sus cursos. Los estudiantes pueden ver sus propias calificaciones.

- **Caso de Uso Backend Asociado:** CU9: Gestión de Calificaciones.
- **Ubicación:** `src/features/grades/`
- **Acceso Principal:** Docente (CRUD para calificaciones en sus cursos), Estudiante (Read para sus propias calificaciones).

**Vistas Principales:**

1.  **`CourseGradesPage.tsx` (`/app/courses/:courseId/grades`) (Docente)**
    -   **Propósito:** Permitir a los docentes ver y gestionar las calificaciones de todos los estudiantes inscritos en un curso específico. Mostrar una tabla editable de calificaciones.
    -   **Componentes Clave:** Tabla de estudiantes del curso con sus calificaciones (`GradesTable.tsx`), campos de entrada para calificaciones, botones para guardar/actualizar, selector de tipo de evaluación (parcial, final, tarea, etc.).
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/courses/{course_id}/students` (para listar estudiantes).
        -   `GET /api/v1/courses/{course_id}/students/{student_id}/grades` (para obtener calificaciones existentes de un estudiante en ese curso).
        -   `POST /api/v1/grades/` (para crear nuevas calificaciones).
        -   `PUT /api/v1/grades/{grade_id}` (para actualizar calificaciones existentes).
        -   `DELETE /api/v1/grades/{grade_id}` (para eliminar calificaciones).
    -   **Estado Local/Global:**
        -   Lista de estudiantes en el curso.
        -   Calificaciones de los estudiantes (posiblemente en un estado editable).
        -   Estado de carga, guardado y errores.
    -   **Flujo:**
        1.  Carga la lista de estudiantes del curso.
        2.  Para cada estudiante, carga sus calificaciones existentes o prepara campos para nuevas calificaciones.
        3.  Docente ingresa/modifica calificaciones.
        4.  Al guardar, se envían las peticiones POST/PUT correspondientes.
        5.  Feedback visual sobre el estado de guardado.

2.  **`MyGradesPage.tsx` (`/app/my-grades`) (Estudiante)**
    -   **Propósito:** Permitir a los estudiantes ver un resumen de sus calificaciones en todos los cursos en los que están inscritos, posiblemente filtrado por período académico.
    -   **Componentes Clave:** Lista/tabla de cursos con sus respectivas calificaciones (`MyGradesSummary.tsx`), selector de período académico.
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/grades/` (filtrado por el `student_id` del usuario autenticado, backend se encarga de esto).
        -   Opcionalmente: `GET /api/v1/students/{student_id}/grades-summary` (si este endpoint provee una vista más conveniente para el estudiante).
    -   **Estado Local/Global:**
        -   Lista de calificaciones/resumen de calificaciones.
        -   Filtro de período académico.
        -   Estado de carga y errores.
    -   **Flujo:**
        1.  Al cargar, obtiene las calificaciones del estudiante.
        2.  Permite filtrar por período académico.
        3.  Muestra las calificaciones de forma clara.

3.  **`StudentGradesDetailPage.tsx` (`/app/courses/:courseId/student/:studentId/grades`) (Docente, Estudiante - si es su propia info)**
    -   **Propósito:** Vista detallada de todas las calificaciones de un estudiante específico en un curso particular. Podría ser parte de `CourseGradesPage` o una vista separada si hay muchos detalles por calificación (ej. comentarios, historial).
    -   **Componentes Clave:** Lista detallada de calificaciones, con fechas, tipos de evaluación, valores, comentarios.
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/courses/{course_id}/students/{student_id}/grades`.
    -   **Estado Local/Global:** Calificaciones del estudiante, carga, errores.

**Componentes Específicos del Módulo (`src/features/grades/components/`):**

-   `GradesTable.tsx`: Tabla editable para que los docentes gestionen calificaciones de múltiples estudiantes en un curso.
-   `GradeInput.tsx`: Componente de entrada para una calificación individual, manejando validación y estado.
-   `MyGradesSummary.tsx`: Componente para mostrar el resumen de calificaciones de un estudiante.
-   `EvaluationTypeSelector.tsx`: Selector para tipos de evaluación (ej. Examen Parcial, Tarea, Participación).

**Servicios API (`src/features/grades/api/grade.api.ts`):**

-   `getGradesForCourseStudent(courseId, studentId)`
-   `createGrade(gradeData)` (Payload: `GradeCreate`)
-   `updateGrade(gradeId, gradeData)` (Payload: `GradeUpdate`)
-   `deleteGrade(gradeId)`
-   `getMyGrades(params)` (para estudiantes)
-   `getStudentGradesSummary(studentId)` (opcional)

**Gestión de Estado:**

-   Para la `CourseGradesPage` (Docente), el estado de las calificaciones que se están editando será local al componente o a la página, con lógica para manejar múltiples entradas y guardado masivo o individual.
-   Para `MyGradesPage` (Estudiante), SWR/React Query es ideal para cargar y cachear las calificaciones.

**Tipos de Datos (`src/features/grades/types/grade.types.ts`):**

-   `Grade`, `GradeCreate`, `GradeUpdate` (basados en `GradeRead`, `GradeCreate`, `GradeUpdate` de `ejemplosjson.md`).
-   `GradeSummaryItem` (si se usa un endpoint de resumen).
-   `EvaluationType` (enum o tipo string para los tipos de evaluación).

**Consideraciones Adicionales:**

-   **Cálculo de Promedios:** Si el frontend necesita mostrar promedios, decidir si se calculan en el cliente o si el backend los provee.
-   **Validación de Calificaciones:** Asegurar que las calificaciones estén dentro de un rango válido (ej. 0-20, 0-100). La validación debe estar en el frontend y backend.
-   **Feedback en Tiempo Real:** Para docentes, al editar calificaciones, considerar si el guardado es por cada cambio, por fila, o un guardado general de la tabla. Proveer feedback claro.
-   **Escalabilidad:** Si un curso tiene muchos estudiantes y muchas calificaciones por estudiante, la `CourseGradesPage` debe ser performante (virtualización de listas/tablas).

### 5.7. Módulo de Gestión de Asistencia (Docente, Estudiante - CU10)

Este módulo se encarga del registro y consulta de la asistencia de los estudiantes a los cursos.

- **Caso de Uso Backend Asociado:** CU10: Gestión de Asistencia.
- **Ubicación:** `src/features/attendance/`
- **Acceso Principal:** Docente (CRUD para asistencia en sus cursos), Estudiante (Read para su propia asistencia).

**Vistas Principales:**

1.  **`CourseAttendancePage.tsx` (`/app/courses/:courseId/attendance`) (Docente)**
    -   **Propósito:** Permitir a los docentes registrar y modificar la asistencia de los estudiantes para fechas específicas en un curso.
    -   **Componentes Clave:** Selector de fecha (`DatePicker`), tabla de estudiantes del curso (`AttendanceTable.tsx`) con opciones para marcar asistencia (Presente, Ausente, Justificado, Tarde).
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/courses/{course_id}/students` (para listar estudiantes).
        -   `GET /api/v1/courses/{course_id}/attendance?date=YYYY-MM-DD` (para obtener la asistencia de una fecha específica).
        -   `POST /api/v1/attendance/` (para registrar nueva asistencia, posiblemente en batch para una fecha).
        -   `PUT /api/v1/attendance/{attendance_id}` (para actualizar un registro de asistencia específico).
        -   `DELETE /api/v1/attendance/{attendance_id}` (raro, pero posible para corregir errores).
    -   **Estado Local/Global:**
        -   Fecha seleccionada.
        -   Lista de estudiantes y su estado de asistencia para esa fecha.
        -   Estado de carga, guardado y errores.
    -   **Flujo:**
        1.  Docente selecciona un curso y una fecha.
        2.  Carga la lista de estudiantes y su asistencia para esa fecha (si existe).
        3.  Docente marca/modifica la asistencia.
        4.  Al guardar, se envían las peticiones POST/PUT.
        5.  Feedback visual.

2.  **`MyAttendancePage.tsx` (`/app/my-attendance`) (Estudiante)**
    -   **Propósito:** Permitir a los estudiantes ver su registro de asistencia para los cursos en los que están inscritos, filtrado por curso y/o período.
    -   **Componentes Clave:** Selector de curso, selector de período académico, calendario o lista que muestra el historial de asistencia (`MyAttendanceRecord.tsx`).
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/attendance/` (filtrado por `student_id` del usuario autenticado, y posiblemente `course_id` o `academic_period_id`).
        -   Opcional: `GET /api/v1/students/{student_id}/attendance-summary?course_id=X`.
    -   **Estado Local/Global:**
        -   Registros de asistencia del estudiante.
        -   Filtros seleccionados.
        -   Estado de carga y errores.
    -   **Flujo:**
        1.  Estudiante selecciona filtros (opcional).
        2.  Carga y muestra el historial de asistencia.

**Componentes Específicos del Módulo (`src/features/attendance/components/`):**

-   `AttendanceTable.tsx`: Tabla para que los docentes gestionen la asistencia de estudiantes para una fecha.
-   `AttendanceStatusSelector.tsx`: Componente para seleccionar el estado de asistencia (Presente, Ausente, etc.).
-   `MyAttendanceRecord.tsx`: Componente para mostrar el historial de asistencia de un estudiante.

**Servicios API (`src/features/attendance/api/attendance.api.ts`):**

-   `getAttendanceForCourseDate(courseId, date)`
-   `createOrUpdateAttendanceBatch(attendanceDataList)` (Payload: `List[AttendanceCreate]` o `List[AttendanceUpdate]`)
-   `deleteAttendanceRecord(attendanceId)`
-   `getMyAttendance(params)` (para estudiantes)

**Gestión de Estado:**

-   Para `CourseAttendancePage` (Docente), el estado de la asistencia para la fecha seleccionada será local a la página/componente.
-   Para `MyAttendancePage` (Estudiante), SWR/React Query para cargar datos.

**Tipos de Datos (`src/features/attendance/types/attendance.types.ts`):**

-   `AttendanceRecord`, `AttendanceCreate`, `AttendanceUpdate` (basados en `AttendanceRead`, `AttendanceCreate`, `AttendanceUpdate` de `ejemplosjson.md`).
-   `AttendanceStatus` (enum: `'present'`, `'absent'`, `'justified'`, `'late'`).

**Consideraciones Adicionales:**

-   **Registro en Batch:** Para facilitar el trabajo del docente, permitir el registro/actualización de asistencia para todos los estudiantes de un curso en una fecha dada con una sola acción de guardado.
-   **Visualización:** Considerar el uso de un calendario para que los estudiantes vean su asistencia, marcando los días con colores según el estado.
-   **Justificaciones:** Si se manejan justificaciones, podría haber un flujo adicional para que los estudiantes las suban y los docentes las aprueben.

### 5.8. Módulo de Gestión de Tutores (Admin - CU11)

Este módulo permite a los administradores asignar estudiantes a tutores (docentes con rol de tutor) y gestionar estas asignaciones.

- **Caso de Uso Backend Asociado:** CU11: Gestión de Tutores y Tutorados.
- **Ubicación:** `src/features/tutoring/`
- **Acceso Principal:** Administrador.

**Vistas Principales:**

1.  **`TutorListPage.tsx` (`/app/tutors`) (Admin)**
    -   **Propósito:** Mostrar una lista de todos los usuarios con rol de 'docente' que pueden actuar como tutores. Permitir ver los estudiantes asignados a cada tutor y navegar para gestionar asignaciones.
    -   **Componentes Clave:** Tabla de tutores (`TutorDataGrid.tsx`), con información del tutor y número de estudiantes asignados. Botón para ir a la gestión de asignaciones de un tutor.
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/users/?role=docente` (o un endpoint específico si los tutores son una subcategoría especial, ej. `GET /api/v1/tutors/`).
        -   (Opcional) Un endpoint que devuelva tutores con el conteo de sus tutorados.
    -   **Estado Local/Global:** Lista de tutores, estado de carga, errores.
    -   **Flujo:**
        1.  Carga la lista de docentes/tutores.
        2.  Muestra información relevante (nombre, contacto, nº de tutorados).
        3.  Permite seleccionar un tutor para ver/gestionar sus estudiantes asignados.

2.  **`TutorAssignmentPage.tsx` (`/app/tutors/:tutorId/assign-students`) (Admin)**
    -   **Propósito:** Permitir a los administradores asignar o desasignar estudiantes a un tutor específico.
    -   **Componentes Clave:** Información del tutor seleccionado. Dos listas/tablas: una con estudiantes asignados actualmente al tutor (`AssignedStudentsList.tsx`) y otra con estudiantes disponibles para asignar (`AvailableStudentsList.tsx`) que no tengan tutor o puedan ser reasignados. Funcionalidad de búsqueda y selección múltiple en la lista de disponibles.
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/users/{tutor_id}` (para obtener detalles del tutor).
        -   `GET /api/v1/tutors/{tutor_id}/students` (para obtener estudiantes actualmente asignados).
        -   `GET /api/v1/students/?unassigned=true` (o similar, para obtener estudiantes sin tutor o disponibles).
        -   `POST /api/v1/tutors/{tutor_id}/students` (Payload: `List[student_id]` para asignar).
        -   `DELETE /api/v1/tutors/{tutor_id}/students` (Payload: `List[student_id]` para desasignar, o un endpoint individual `DELETE /api/v1/tutors/{tutor_id}/students/{student_id}`).
    -   **Estado Local/Global:**
        -   Datos del tutor.
        -   Lista de estudiantes asignados.
        -   Lista de estudiantes disponibles.
        -   Selección de estudiantes para asignar/desasignar.
        -   Estado de carga, guardado y errores.
    -   **Flujo:**
        1.  Carga datos del tutor y sus estudiantes asignados.
        2.  Carga lista de estudiantes disponibles.
        3.  Admin selecciona estudiantes de la lista de disponibles y los mueve a asignados, o viceversa.
        4.  Al guardar, se envían las peticiones POST/DELETE correspondientes.
        5.  Feedback visual.

3.  **`StudentTutorInfoPage.tsx` (`/app/students/:studentId/tutor`) (Admin, Estudiante, Docente/Tutor)**
    -   **Propósito:** Mostrar la información del tutor asignado a un estudiante específico. El estudiante ve a su tutor. El admin/docente puede ver esta info como parte del perfil del estudiante.
    -   **Componentes Clave:** Tarjeta o sección con los detalles del tutor asignado.
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/students/{student_id}/tutor` (devuelve la info del tutor asignado al estudiante).
    -   **Estado Local/Global:** Información del tutor, carga, errores.

**Componentes Específicos del Módulo (`src/features/tutoring/components/`):**

-   `TutorDataGrid.tsx`: Tabla para listar tutores.
-   `AssignedStudentsList.tsx`: Lista de estudiantes asignados a un tutor.
-   `AvailableStudentsList.tsx`: Lista de estudiantes disponibles para ser asignados, con filtros y búsqueda.
-   `TutorProfileCard.tsx`: Componente para mostrar la información de un tutor.

**Servicios API (`src/features/tutoring/api/tutoring.api.ts`):**

-   `getTutors(params)`
-   `getTutorById(tutorId)`
-   `getAssignedStudents(tutorId)`
-   `getAvailableStudents(params)`
-   `assignStudentsToTutor(tutorId, studentIds)`
-   `unassignStudentsFromTutor(tutorId, studentIds)`
-   `getStudentTutor(studentId)`

**Gestión de Estado:**

-   Principalmente estado local para las páginas de asignación. SWR/React Query para cargar listas.

**Tipos de Datos (`src/features/tutoring/types/tutoring.types.ts`):**

-   `Tutor` (probablemente `UserRead` con un filtro de rol o un tipo específico si hay datos adicionales para tutores).
-   `StudentAssigned` (probablemente `UserRead` simplificado).
-   `AssignStudentsPayload` (ej. `{ student_ids: string[] }`).

**Consideraciones Adicionales:**

-   **Lógica de Asignación:** El backend debe manejar la lógica de que un estudiante solo puede tener un tutor a la vez (si es el caso).
-   **UI para Selección Masiva:** La `TutorAssignmentPage` debe ser intuitiva para asignar/desasignar múltiples estudiantes.
-   **Notificaciones:** Considerar notificar al estudiante y/o al tutor cuando se realiza una nueva asignación o cambio.
-   **Visibilidad:** Los estudiantes deberían poder ver quién es su tutor asignado en su perfil o dashboard.

### 5.9. Módulo de Predicciones de Rendimiento (Admin, Docente - CU12)

Este módulo permite a administradores y docentes visualizar las predicciones de rendimiento de los estudiantes, identificar estudiantes en riesgo y, potencialmente, ver los factores que influyen en estas predicciones.

- **Caso de Uso Backend Asociado:** CU12: Gestión de Predicciones de Rendimiento.
- **Ubicación:** `src/features/predictions/`
- **Acceso Principal:** Administrador, Docente.

**Vistas Principales:**

1.  **`StudentPredictionDashboardPage.tsx` (`/app/predictions/students`) (Admin, Docente)**
    -   **Propósito:** Mostrar un dashboard con una lista de estudiantes y sus predicciones de rendimiento (ej. riesgo de reprobar, predicción de calificación final). Permitir filtros por curso, período académico, nivel de riesgo.
    -   **Componentes Clave:** Tabla/lista de estudiantes con predicciones (`StudentPredictionList.tsx`), filtros, gráficos de resumen (ej. distribución de niveles de riesgo).
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/predictions/students/` (con parámetros de filtro: `course_id`, `academic_period_id`, `risk_level`). El backend debe filtrar por los cursos del docente si el usuario es docente.
    -   **Estado Local/Global:**
        -   Lista de predicciones de estudiantes.
        -   Filtros aplicados.
        -   Estado de carga y errores.
    -   **Flujo:**
        1.  Carga las predicciones según los filtros (o todos los estudiantes accesibles por el rol).
        2.  Muestra la información de forma clara, destacando estudiantes en riesgo.
        3.  Permite navegar a la vista detallada de predicción de un estudiante.

2.  **`StudentPredictionDetailPage.tsx` (`/app/predictions/students/:studentId`) (Admin, Docente)**
    -   **Propósito:** Mostrar un análisis detallado de la predicción de rendimiento para un estudiante específico. Podría incluir factores influyentes, historial de predicciones, comparación con el rendimiento actual.
    -   **Componentes Clave:** Gráficos de tendencias, lista de factores contribuyentes (`PredictionFactors.tsx`), comparación de predicción vs. realidad (si aplica).
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/predictions/students/{student_id}` (podría requerir `course_id` o `academic_period_id` como query param para contexto).
        -   `GET /api/v1/predictions/students/{student_id}/factors` (si los factores se obtienen por separado).
    -   **Estado Local/Global:**
        -   Detalles de la predicción del estudiante.
        -   Factores influyentes.
        -   Estado de carga y errores.
    -   **Flujo:**
        1.  Carga los detalles de la predicción para el estudiante seleccionado.
        2.  Visualiza la información de manera comprensible para el docente/admin.

3.  **`PredictionModelManagementPage.tsx` (`/app/admin/predictions/models`) (Admin - Opcional Avanzado)**
    -   **Propósito:** (Si aplica) Permitir a los administradores ver el estado de los modelos de predicción, re-entrenarlos, o ver métricas de su rendimiento.
    -   **Componentes Clave:** Lista de modelos, botón para re-entrenar, visualización de métricas (accuracy, F1-score, etc.).
    -   **Endpoints Consumidos:**
        -   `GET /api/v1/predictions/models/status`
        -   `POST /api/v1/predictions/models/retrain`
    -   **Estado Local/Global:** Estado de los modelos, métricas, estado de re-entrenamiento.

**Componentes Específicos del Módulo (`src/features/predictions/components/`):**

-   `StudentPredictionList.tsx`: Componente para listar estudiantes con sus predicciones.
-   `PredictionFactors.tsx`: Componente para mostrar los factores que influyen en una predicción.
-   `RiskLevelIndicator.tsx`: Componente visual para mostrar el nivel de riesgo (ej. color-coded).
-   `PredictionChart.tsx`: Gráficos para visualizar tendencias o distribuciones de predicciones.

**Servicios API (`src/features/predictions/api/prediction.api.ts`):**

-   `getStudentPredictions(params)`
-   `getStudentPredictionDetail(studentId, params)`
-   `getPredictionFactors(studentId, params)`
-   (Opcional) `getModelStatus()`, `retrainModel()`

**Gestión de Estado:**

-   SWR/React Query para la carga de datos de predicciones.
-   Estado local para filtros y UI.

**Tipos de Datos (`src/features/predictions/types/prediction.types.ts`):**

-   `StudentPrediction` (ej. `{ student_id: string, student_name: string, course_id: string, predicted_grade: number, risk_level: 'low' | 'medium' | 'high', prediction_date: string }`). Este tipo debe definirse según lo que retorne el backend.
-   `PredictionFactor` (ej. `{ factor_name: string, contribution: number, details: string }`).
-   `ModelStatus` (si se implementa la gestión de modelos).

**Consideraciones Adicionales:**

-   **Interpretabilidad:** Es crucial que las predicciones sean presentadas de forma que los docentes puedan entenderlas y actuar sobre ellas. Mostrar los factores más influyentes es clave.
-   **Actualización de Datos:** Definir con qué frecuencia se actualizan las predicciones y cómo se notifica esto en la UI.
-   **UX para Riesgo:** Usar indicadores visuales claros (colores, iconos) para los niveles de riesgo.
-   **Acciones Sugeridas:** (Futuro) El sistema podría sugerir intervenciones para estudiantes en riesgo basadas en las predicciones.
-   **Privacidad y Ética:** Asegurar que el uso de predicciones se maneje de forma ética y respetando la privacidad del estudiante. La UI no debería ser determinista ni estigmatizante.

### 5.10. Módulo de Reportes y Estadísticas (Admin, Docente, Estudiante - CU14)

Este módulo proporciona herramientas para generar, visualizar y exportar reportes y estadísticas sobre diversos aspectos del sistema académico.

- **Caso de Uso Backend Asociado:** CU14: Generación de reportes y estadísticas.
- **Ubicación:** `src/features/reports/`
- **Acceso Principal:** Administrador (acceso a todos los reportes), Docente (reportes de sus cursos y estudiantes), Estudiante (reportes sobre su propio rendimiento).

**Vistas Principales:**

1.  **`ReportDashboardPage.tsx` (`/app/reports`) (Admin, Docente, Estudiante)**
    -   **Propósito:** Página principal del módulo de reportes. Muestra una lista de los reportes disponibles según el rol del usuario. Permite seleccionar un tipo de reporte para generar.
    -   **Componentes Clave:** Lista de tipos de reportes disponibles (`ReportTypeList.tsx`), breve descripción de cada reporte.
    -   **Endpoints Consumidos:** (Potencialmente ninguno directamente, la lógica de qué reportes mostrar puede ser frontend basada en rol, o un endpoint `GET /api/v1/reports/available` que liste reportes según rol).
    -   **Estado Local/Global:** Lista de reportes disponibles para el usuario.
    -   **Flujo:**
        1.  Usuario navega a la sección de reportes.
        2.  Se muestra una lista de reportes que puede generar (ej. "Progreso Académico del Estudiante", "Rendimiento del Curso", "Resumen de Riesgo Estudiantil").
        3.  Usuario selecciona un tipo de reporte para ir a la página de configuración/generación.

2.  **`GenerateReportPage.tsx` (`/app/reports/:reportType/generate`) (Admin, Docente, Estudiante)**
    -   **Propósito:** Permitir al usuario configurar los parámetros para un tipo de reporte específico y solicitar su generación.
    -   **Componentes Clave:** Formulario dinámico (`ReportConfigForm.tsx`) basado en el `reportType`. Selectores para `student_id`, `course_id`, `academic_period_id`, rangos de fechas, etc., según el reporte.
    -   **Endpoints Consumidos:** (Varía según el reporte)
        -   `GET /api/v1/reports/academic-progress` (con params: `student_id`, `course_id`, `period_id`)
        -   `GET /api/v1/reports/course-performance` (con params: `course_id`, `period_id`)
        -   `GET /api/v1/reports/student-risk-summary` (con params: `period_id`)
        -   (Otros endpoints de reportes que se definan)
    -   **Estado Local/Global:**
        -   Parámetros del formulario de configuración.
        -   Datos del reporte generado.
        -   Estado de carga y errores.
    -   **Flujo:**
        1.  Usuario selecciona los parámetros del reporte.
        2.  Al enviar, se realiza la petición al endpoint correspondiente del backend.
        3.  Una vez recibido, los datos se muestran en la `ViewReportPage` o directamente en esta página.

3.  **`ViewReportPage.tsx` (`/app/reports/:reportType/view/:reportId`) (Admin, Docente, Estudiante)**
    -   **Propósito:** Mostrar el contenido de un reporte generado. Podría ser una tabla, gráficos, o una combinación. Permitir opciones de exportación (PDF, CSV).
    -   **Componentes Clave:** Visualizador de reportes (`ReportViewer.tsx` - que puede renderizar tablas, gráficos usando bibliotecas como Chart.js o Recharts), botones de exportación.
    -   **Endpoints Consumidos:** (Si los reportes se guardan y tienen un ID, o si se pasan los datos directamente desde `GenerateReportPage`).
        -   `GET /api/v1/reports/generated/{reportId}` (si los reportes generados se almacenan).
    -   **Estado Local/Global:** Datos del reporte a visualizar.

**Componentes Específicos del Módulo (`src/features/reports/components/`):**

-   `ReportTypeList.tsx`: Lista los tipos de reportes disponibles.
-   `ReportConfigForm.tsx`: Formulario genérico o específico para configurar parámetros de reportes.
-   `ReportViewer.tsx`: Componente para renderizar el contenido del reporte (tablas, gráficos).
-   `ExportButtons.tsx`: Botones para exportar el reporte (PDF, CSV).
-   Selectores reutilizables para estudiantes, cursos, períodos académicos.

**Servicios API (`src/features/reports/api/report.api.ts`):**

-   `getAcademicProgressReport(params)`
-   `getCoursePerformanceReport(params)`
-   `getStudentRiskSummaryReport(params)`
-   (Otros servicios para reportes específicos)

**Gestión de Estado:**

-   SWR/React Query para la carga de datos de los reportes.
-   Estado local para los formularios de configuración y la UI de visualización.

**Tipos de Datos (`src/features/reports/types/report.types.ts`):**

-   Definir tipos para los parámetros de cada reporte y para la estructura de datos que devuelve cada endpoint de reporte. Ejemplos:
    -   `AcademicProgressReportData`
    -   `CoursePerformanceReportData`
    -   `StudentRiskSummaryData`
-   Los tipos exactos dependerán de la estructura de respuesta definida en el backend para cada reporte.

**Consideraciones Adicionales:**

-   **Tipos de Reportes:** El sistema puede expandirse para incluir muchos tipos de reportes. La arquitectura debe ser flexible.
-   **Personalización:** Considerar si los usuarios pueden personalizar los reportes (ej. seleccionar columnas en una tabla, cambiar tipo de gráfico).
-   **Exportación:** La exportación a PDF y CSV es una funcionalidad común y útil. Se pueden usar bibliotecas como `jspdf`, `papaparse`.
-   **Rendimiento:** Reportes que procesan grandes cantidades de datos deben ser manejados eficientemente por el backend. El frontend debe mostrar indicadores de carga y manejar timeouts si es necesario.
-   **Visualización de Datos:** Usar gráficos apropiados para representar los datos de manera efectiva (barras, líneas, pie charts, etc.).
-   **Acceso y Permisos:** Asegurar que los usuarios solo puedan acceder y generar reportes para los datos a los que tienen permiso según su rol.

## 6. Definición de Tipos TypeScript

Una de las piedras angulares de este proyecto frontend es el uso de TypeScript para garantizar un desarrollo más seguro, mantenible y escalable. La definición explícita de tipos para las estructuras de datos, props de componentes, estado de la aplicación y payloads de API es fundamental.

**Principios Generales:**

1.  **Fuente de Verdad:** Los esquemas Pydantic del backend y los `ejemplosjson.md` son la principal fuente de verdad para definir los tipos de datos que se intercambian con la API.
2.  **Ubicación de Tipos:**
    -   **Tipos Globales:** Tipos que son utilizados en múltiples módulos o que son muy genéricos (ej. `ApiResponse`, `UserRole`) pueden residir en `src/types/global.types.ts` o en un directorio `src/types/` organizado por dominio.
    -   **Tipos Específicos de Módulo:** Cada módulo dentro de `src/features/` debe tener su propio archivo de tipos (ej. `src/features/users/types/user.types.ts`, `src/features/courses/types/course.types.ts`). Esto promueve la modularidad y facilita la localización de definiciones.
    -   **Tipos de Componentes:** Los props para componentes reutilizables deben definirse junto al componente o en un archivo `.types.ts` hermano.
3.  **Interfaces vs. Types:**
    -   Usar `interface` para definir la forma de los objetos (ej. datos de API, props de componentes).
    -   Usar `type` para uniones, intersecciones, tipos primitivos con alias, o tipos más complejos que no pueden ser representados por una interfaz.
4.  **Nomenclatura:**
    -   Interfaces: Usar PascalCase (ej. `UserProfile`, `CourseDetails`).
    -   Tipos: Usar PascalCase (ej. `UserId`, `NotificationStatus`).
    -   Enums: Usar PascalCase para el nombre del enum y para sus miembros (ej. `enum UserRole { Admin = 'admin', Student = 'student' }`).
5.  **Reutilización y Composición:**
    -   Evitar la duplicación definiendo tipos base y extendiéndolos o componiéndolos usando `&` (intersección) o `|` (unión).
    -   Utilizar tipos de utilidad de TypeScript como `Partial<T>`, `Required<T>`, `Pick<T, K>`, `Omit<T, K>` para crear variaciones de tipos existentes de manera concisa (ej. para payloads de creación vs. actualización).

**Ejemplo General (basado en `ejemplosjson.md`):**

Si el backend para crear un usuario (`POST /api/v1/users/`) espera un JSON como:

```json
// Ejemplo de ejemplosjson.md para UserCreate
{
  "email": "user@example.com",
  "password": "stringstrong",
  "full_name": "John Doe",
  "role_id": 1
}
```

Y para leer un usuario (`UserRead`) devuelve:

```json
{
  "id": "c7a4c5e8-3d8a-4b1e-bf2a-6b9c8f7d2e1a",
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "role": {
    "id": 1,
    "name": "Estudiante",
    "description": "Rol para estudiantes"
  }
}
```

Los tipos en `src/features/users/types/user.types.ts` podrían definirse así:

```typescript
// src/features/users/types/user.types.ts

import { Role } from '@/features/roles/types/role.types.ts'; // Asumiendo que Role está definido

export interface UserCreate {
  email: string;
  password?: string; // Password puede ser opcional si se genera o se maneja de otra forma en creación
  full_name?: string;
  role_id: number;
  // Otros campos necesarios para la creación que no están en UserRead
  // por ejemplo, si el backend espera otros campos específicos para la creación
}

export interface UserUpdate extends Partial<UserCreate> {
  // Campos específicos que solo se pueden actualizar y no crear
  // O simplemente heredar de Partial<UserCreate> si los campos son los mismos
  is_active?: boolean;
}

export interface User {
  id: string; // UUID
  email: string;
  full_name: string | null;
  is_active: boolean;
  role: Role; // Reutilizando la interfaz Role
  // Otros campos que devuelve el API para un usuario leído
}

// Ejemplo de un tipo para el estado de la store de usuarios si se usa Zustand/Redux
export interface UsersState {
  users: User[];
  selectedUser: User | null;
  isLoading: boolean;
  error: string | null;
}
```

**Próximos Pasos en esta Sección:**

Aunque ya hemos esbozado los tipos de datos específicos dentro de cada subsección del "Módulo 5: Módulos y Vistas Principales", esta sección sirve como un recordatorio y guía general. Se anima a los desarrolladores a referirse constantemente a `ejemplosjson.md` y a coordinarse con el equipo de backend para mantener la sincronización de los tipos a medida que la API evoluciona.

En las siguientes secciones, se detallarán consideraciones técnicas avanzadas que también pueden influir en cómo se estructuran y utilizan estos tipos.

## 7. Consideraciones Técnicas Avanzadas

Esta sección aborda aspectos cruciales para la calidad, robustez y mantenibilidad de la aplicación frontend.

### 7.1. Manejo Avanzado de Errores

Un sistema robusto de manejo de errores es vital para la experiencia del usuario y la depuración.

-   **Centralización en Axios Wrapper:**
    -   Como se definió en la Sección 4.1, el wrapper de Axios es el punto central para interceptar y manejar errores de API (HTTP 4xx, 5xx).
    -   Los interceptores deben normalizar los errores de API a un formato consistente, por ejemplo:
        ```typescript
        interface ApiErrorFormat {
          status: number;
          message: string; // Mensaje general del error
          errors?: Record<string, string[]>; // Errores específicos por campo (para 422)
          errorCode?: string; // Código de error interno del backend (opcional)
        }
        ```
    -   Se recomienda una función global `handleApiError(error: any): ApiErrorFormat` que pueda ser invocada desde los servicios o hooks para procesar el error antes de pasarlo a la UI.

-   **Categorización y Estrategias de Manejo:**
    -   **Errores de Red/Servidor (ej. `Network Error`, timeouts, 5xx):**
        -   **UI:** Mostrar un mensaje genérico (ej. "Error de conexión. Inténtalo de nuevo más tarde.") y, si es aplicable, un botón para reintentar la acción.
        -   **Logging:** Registrar estos errores con detalle en el sistema de logging.
    -   **Errores de Validación (HTTP 422 Unprocessable Entity):**
        -   **Backend:** Debe devolver un objeto JSON con los errores por campo (ej. `{ "email": ["Este email ya está registrado."], "password": ["La contraseña es muy corta."] }`).
        -   **UI:** Mapear estos errores a los campos correspondientes en los formularios (React Hook Form facilita esto mostrando el error debajo del input).
    -   **Errores de Autenticación (HTTP 401 Unauthorized):**
        -   **Acción:** El interceptor de Axios debe manejar esto globalmente. Limpiar el estado de autenticación (token, perfil de usuario en Zustand) y redirigir al usuario a la página de login.
        -   **UI:** La redirección es la principal indicación.
    -   **Errores de Permisos (HTTP 403 Forbidden):**
        -   **UI:** Mostrar un mensaje claro de "Acceso Denegado" o una página específica de "403 Forbidden". No redirigir automáticamente al login si el usuario ya está autenticado, para que entienda que el problema es de permisos y no de sesión.
    -   **Errores de No Encontrado (HTTP 404 Not Found):**
        -   **UI:** Mostrar una página/componente de "404 No Encontrado" amigable, con opciones para volver al inicio o buscar.
    -   **Errores Inesperados del Cliente (JavaScript):**
        -   **Mecanismo:** Utilizar Error Boundaries de React.

-   **Error Boundaries en React:**
    -   Implementar Error Boundaries a nivel de componentes principales, rutas o secciones críticas de la aplicación.
    -   **Propósito:** Capturan errores de JavaScript en sus componentes hijos durante el renderizado, en métodos de ciclo de vida y en constructores.
    -   **Fallback UI:** Deben renderizar una UI de fallback (ej. "Algo salió mal. Por favor, recarga la página.") en lugar de que toda la aplicación se rompa.
    -   **Logging:** El método `componentDidCatch` del Error Boundary debe enviar el error y el `errorInfo` al servicio de logging.
    -   **Ejemplo de estructura:**
        ```tsx
        // src/components/base/ErrorBoundary.tsx
        import React, { Component, ErrorInfo, ReactNode } from 'react';

        interface Props {
          children: ReactNode;
          fallbackUI?: ReactNode; // UI personalizada de fallback
        }

        interface State {
          hasError: boolean;
        }

        class ErrorBoundary extends Component<Props, State> {
          public state: State = {
            hasError: false,
          };

          public static getDerivedStateFromError(_: Error): State {
            return { hasError: true };
          }

          public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
            console.error("Uncaught error:", error, errorInfo);
            // TODO: Send to logging service (Sentry, LogRocket, etc.)
            // logErrorToMyService(error, errorInfo);
          }

          public render() {
            if (this.state.hasError) {
              return this.props.fallbackUI || <h1>Lo sentimos... algo salió mal.</h1>;
            }
            return this.props.children;
          }
        }
        export default ErrorBoundary;
        ```

-   **Notificaciones de Errores (Toasts/Snackbars):**
    -   Utilizar un sistema de notificaciones (ej. Material-UI Snackbar, react-toastify) para errores no críticos que no interrumpen el flujo principal, o para confirmar acciones fallidas (ej. "No se pudo guardar el curso").
    -   Evitar el uso de `window.alert()` para una mejor UX.

-   **Logging de Errores en Frontend:**
    -   **Servicio Externo:** Integrar un servicio de logging de errores robusto como Sentry, LogRocket, o Datadog RUM.
    -   **Información a Registrar:**
        -   Mensaje de error y stack trace.
        -   Contexto del usuario (ID, rol, si está disponible y es pertinente).
        -   Ruta actual y acción que se intentaba realizar.
        -   Versión de la aplicación.
        -   Información del navegador y OS.
        -   Breadcrumbs (secuencia de acciones del usuario previas al error, si el servicio lo soporta).
    -   **Configuración:** Configurar `source maps` para que los stack traces en producción sean legibles.

-   **Estado de Error en Componentes y Stores:**
    -   Los hooks de fetching de datos (como los que se usarían con React Query/SWR o en servicios API customizados) deben devolver un estado de error.
    -   Las stores de Zustand deben incluir campos para `isLoading` y `error` para las operaciones asíncronas.
    -   Los componentes deben consumir estos estados para renderizar UI adecuada (indicadores de carga, mensajes de error específicos, botones de reintento).

-   **Mensajes de Error Amigables para el Usuario:**
    -   **Claridad:** Evitar mostrar mensajes técnicos o códigos de error crípticos directamente al usuario.
    -   **Traducción:** Si los mensajes de error del backend no son amigables, traducirlos o mapearlos a mensajes más comprensibles en el frontend.
    -   **Contexto y Soluciones:** Cuando sea posible, proporcionar contexto sobre por qué ocurrió el error y qué puede hacer el usuario (ej. "El archivo es demasiado grande. Intenta con un archivo menor a 5MB.").
    -   **Consistencia:** Mantener un tono y estilo consistentes para todos los mensajes de error.

    ### 7.2. Seguridad en el Frontend

Aunque la mayor parte de la lógica de seguridad reside en el backend, el frontend juega un papel crucial en mantener un entorno seguro.

-   **Gestión Segura de JWT:**
    -   **Almacenamiento:** Los JWT deben almacenarse de forma segura.
        -   **`HttpOnly` Cookies:** Es la opción más segura si el backend puede configurarlas, ya que no son accesibles mediante JavaScript, previniendo ataques XSS que intenten robar el token. Esto requiere que el backend y frontend estén en el mismo dominio o subdominios configurados adecuadamente para compartir cookies.
        -   **`localStorage` / `sessionStorage`:** Menos seguro que `HttpOnly` cookies porque son accesibles por JavaScript (vulnerables a XSS). Si se usan, se deben tomar precauciones adicionales contra XSS. `sessionStorage` es ligeramente mejor que `localStorage` porque se borra cuando se cierra la pestaña/navegador.
        -   **Memoria de JavaScript (ej. Zustand/Redux store):** El token se mantiene en memoria y se pierde al recargar. Requiere obtener un nuevo token (posiblemente con un refresh token) al iniciar la aplicación. Puede ser una opción si se combina con un refresh token almacenado en una cookie `HttpOnly`.
    -   **Transmisión:** Siempre transmitir JWTs sobre HTTPS.
    -   **Refresh Tokens:** Implementar un sistema de refresh tokens. El access token (JWT) debe tener una vida corta (ej. 15-60 minutos). El refresh token, con una vida más larga (ej. días o semanas), se almacena de forma más segura (idealmente en una cookie `HttpOnly`) y se usa para obtener nuevos access tokens sin que el usuario tenga que re-loguearse.
    -   **Interceptor de Axios:** El interceptor de Axios (Sección 4.1) debe:
        -   Adjuntar el access token a las cabeceras `Authorization` (`Bearer <token>`) de las peticiones salientes.
        -   Manejar errores 401 (Unauthorized) para intentar renovar el token usando el refresh token. Si la renovación falla o no hay refresh token, desloguear al usuario.

-   **Prevención de Cross-Site Scripting (XSS):**
    -   **React y Escapado Automático:** React escapa por defecto el contenido renderizado en JSX, lo que previene muchos ataques XSS.
    -   **`dangerouslySetInnerHTML`:** Evitar su uso. Si es absolutamente necesario, asegurarse de que el HTML que se inserta sea sanitizado previamente usando una librería como DOMPurify.
    -   **Atributos `href` y `src`:** Validar y sanitizar URLs antes de usarlas en `<a>` o `<img>` tags, especialmente si provienen de contenido generado por el usuario.
    -   **Librerías de Terceros:** Evaluar la seguridad de las librerías de terceros, ya que podrían introducir vulnerabilidades XSS.

-   **Prevención de Cross-Site Request Forgery (CSRF):**
    -   Si se usan cookies para la gestión de sesión (incluyendo `HttpOnly` cookies para JWTs), el backend debe implementar protección CSRF (ej. tokens anti-CSRF, SameSite cookies).
    -   **Tokens Anti-CSRF:** El backend genera un token único que el frontend debe incluir en las cabeceras de las peticiones que modifican estado (POST, PUT, DELETE).
    -   **`SameSite` Cookies:** Configurar las cookies de sesión con `SameSite=Lax` o `SameSite=Strict` para mitigar ataques CSRF.

-   **Protección de Rutas (Route Guarding):**
    -   Como se detalló en la Sección 4.3, usar componentes `ProtectedRoute` para restringir el acceso a rutas basado en el estado de autenticación y/o roles del usuario.
    -   La lógica de roles debe obtenerse del token JWT o de un endpoint de perfil de usuario seguro, y no debe ser fácilmente manipulable en el cliente.

-   **Validación de Entradas:**
    -   Validar todas las entradas del usuario en el frontend (con Zod, como se mencionó en Sección 3.2) para una mejor UX y para reducir la carga en el backend.
    -   **Importante:** La validación del frontend es para UX, no para seguridad. El backend DEBE re-validar todas las entradas.

-   **Content Security Policy (CSP):**
    -   Implementar cabeceras CSP (a través del servidor web o meta tags) para restringir los orígenes desde los cuales se pueden cargar recursos (scripts, estilos, imágenes, etc.). Esto ayuda a mitigar XSS y otros ataques de inyección.
    -   Ejemplo de política restrictiva:
        `Content-Security-Policy: default-src 'self'; script-src 'self' https://apis.google.com; img-src 'self' https://cdn.example.com; style-src 'self' 'unsafe-inline';`

-   **Cabeceras de Seguridad HTTP:**
    -   Asegurarse de que el servidor web que sirve el frontend esté configurado con cabeceras de seguridad adicionales:
        -   `X-Content-Type-Options: nosniff`
        -   `X-Frame-Options: DENY` (o `SAMEORIGIN`)
        -   `Strict-Transport-Security (HSTS)`
        -   `Referrer-Policy`

-   **Manejo de Secretos:**
    -   **NUNCA** incrustar claves de API, secretos o credenciales directamente en el código frontend.
    -   Usar variables de entorno (ej. `VITE_API_URL`) para configuración, pero recordar que estas son accesibles en el navegador. Para secretos verdaderos, se necesita una capa de backend (ej. un endpoint proxy que use el secreto).

-   **Dependencias Seguras:**
    -   Mantener las dependencias actualizadas (usar `npm audit` o `yarn audit` para identificar vulnerabilidades conocidas).
    -   Usar un `lockfile` (`package-lock.json` o `yarn.lock`) para asegurar instalaciones consistentes y predecibles.

-   **Desactivar Autocompletado en Campos Sensibles (si es necesario):**
    -   Para campos como contraseñas o información muy sensible, se puede usar `autoComplete="off"` o valores más específicos como `autoComplete="new-password"`, aunque el soporte de los navegadores puede variar.
    
    ### 7.3. Optimización del Rendimiento

Un rendimiento óptimo es crucial para la usabilidad y la satisfacción del usuario, especialmente en aplicaciones ricas en datos como Smart Academy.

-   **Code Splitting (División de Código):**
    -   **Propósito:** Reducir el tamaño inicial del bundle de JavaScript cargando solo el código necesario para la vista actual.
    -   **Implementación:**
        -   **React.lazy() y Suspense:** Para cargar componentes de forma diferida a nivel de ruta o para componentes grandes que no son visibles inicialmente.
            ```tsx
            // Ejemplo de carga diferida de una ruta
            const AdminDashboard = React.lazy(() => import('@/features/dashboard/AdminDashboard'));

            <Route path="/admin" element={
              <React.Suspense fallback={<PageLoader />}>
                <AdminDashboard />
              </React.Suspense>
            }/>
            ```
        -   **Configuración de Vite/Webpack:** Asegurar que el bundler esté configurado para generar chunks separados. Vite lo hace automáticamente para importaciones dinámicas.

-   **Memoización:**
    -   **React.memo():** Para componentes funcionales, evita re-renderizados si los props no han cambiado. Útil para componentes puros y componentes en listas largas.
    -   **useMemo():** Para memoizar valores calculados costosos, evitando que se recalculen en cada renderizado.
    -   **useCallback():** Para memoizar funciones (especialmente las pasadas como props a componentes hijos optimizados con `React.memo()`), evitando que los hijos se re-rendericen innecesariamente.
    -   **Precaución:** No memoizar todo indiscriminadamente, ya que la memoización en sí misma tiene un costo. Aplicar donde se identifiquen cuellos de botella de rendimiento.

-   **Virtualización de Listas y Tablas (Windowing):**
    -   **Problema:** Renderizar listas o tablas muy largas (cientos o miles de filas) puede ser muy costoso.
    -   **Solución:** Usar librerías como `react-window` o `react-virtualized` (o las capacidades integradas de componentes de UI como Material-UI DataGrid Pro si se usa) para renderizar solo los elementos visibles en la ventana gráfica.
    -   **Aplicación:** Indispensable para vistas como listados de usuarios, cursos, calificaciones, etc., que pueden crecer mucho.

-   **Optimización de Imágenes:**
    -   **Formatos Modernos:** Usar formatos de imagen eficientes como WebP (con fallback a JPEG/PNG para navegadores no compatibles).
    -   **Compresión:** Comprimir imágenes sin pérdida significativa de calidad.
    -   **Responsive Images:** Usar el tag `<picture>` o el atributo `srcset` en `<img>` para servir imágenes de diferentes tamaños según la resolución del dispositivo.
    -   **Lazy Loading de Imágenes:** Cargar imágenes solo cuando están a punto de entrar en la ventana gráfica (usar `loading="lazy"` en `<img>` o librerías de terceros).

-   **Reducción del Tamaño del Bundle:**
    -   **Tree Shaking:** Asegurar que el bundler (Vite/Webpack) esté configurado para eliminar código no utilizado.
    -   **Análisis del Bundle:** Usar herramientas como `vite-plugin-visualizer` (para Vite) o `webpack-bundle-analyzer` para identificar qué dependencias están ocupando más espacio y buscar alternativas más ligeras si es posible.
    -   **Importaciones Selectivas:** Importar solo los módulos necesarios de las librerías (ej. `import Button from '@mui/material/Button';` en lugar de `import { Button } from '@mui/material';` si solo se necesita Button y el tree-shaking no es perfecto).

-   **Caching:**
    -   **Caching del Navegador:** Configurar cabeceras HTTP de caching (`Cache-Control`, `ETag`, `Expires`) en el servidor para los assets estáticos (JS, CSS, imágenes).
    -   **Service Workers:** Para caching avanzado y capacidades offline (considerar para PWA).
    -   **Data Caching (React Query/SWR):** Como se mencionó en la Sección 3.3, estas librerías manejan el caching de datos de API, reduciendo peticiones redundantes.

-   **Debouncing y Throttling:**
    -   **Debouncing:** Para eventos que se disparan frecuentemente (ej. input de búsqueda, redimensionamiento de ventana), agrupa múltiples llamadas en una sola después de un periodo de inactividad.
    -   **Throttling:** Para eventos frecuentes (ej. scroll, mouse move), asegura que la función se ejecute como máximo una vez cada X milisegundos.
    -   **Implementación:** Usar utilidades de librerías como Lodash (`_.debounce`, `_.throttle`) o implementaciones custom.

-   **Minimización de Reflows y Repaints:**
    -   Evitar cambios frecuentes de estilos que afecten la geometría de los elementos (layout thrashing).
    -   Usar `transform` y `opacity` para animaciones siempre que sea posible, ya que suelen ser manejadas por la GPU y no causan reflows.
    -   Usar herramientas de desarrollo del navegador (Performance tab) para identificar cuellos de botella de renderizado.

-   **Carga Asíncrona de Scripts de Terceros:**
    -   Cargar scripts de terceros (analíticas, widgets, etc.) de forma asíncrona (`async` o `defer` en el tag `<script>`) para que no bloqueen el renderizado principal de la página.

-   **Preloading, Prefetching, Preconnect:**
    -   **`<link rel="preload">`:** Para recursos críticos que se necesitarán pronto en la carga de la página actual.
    -   **`<link rel="prefetch">`:** Para recursos que probablemente se necesitarán en la siguiente navegación.
    -   **`<link rel="preconnect">`:** Para establecer conexiones tempranas con dominios de terceros de donde se cargarán recursos importantes (ej. API, CDN de fuentes).

-   **Web Workers:**
    -   Para tareas computacionalmente intensivas que podrían bloquear el hilo principal (ej. procesamiento de datos complejos en el cliente, aunque esto debería ser raro si el backend maneja la mayoría de la lógica pesada).

-   ### 7.4. Pruebas (Testing)

Un conjunto completo de pruebas es esencial para garantizar la calidad del software, facilitar las refactorizaciones y prevenir regresiones. Se adoptará una estrategia de pruebas mixta.

-   **Herramientas Recomendadas:**
    -   **Framework de Pruebas:** [Vitest](https://vitest.dev/) (preferido por su integración con Vite) o [Jest](https://jestjs.io/).
    -   **Librería de Pruebas de Componentes:** [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) (RTL), enfocada en probar el comportamiento del componente desde la perspectiva del usuario.
    -   **Pruebas End-to-End (E2E):** [Cypress](https://www.cypress.io/) o [Playwright](https://playwright.dev/).
    -   **Mocks de API:**
        -   Para pruebas unitarias/integración: `msw` (Mock Service Worker) para interceptar peticiones a nivel de red.
        -   Para E2E: Cypress tiene capacidades de mockeo integradas.
    -   **Cobertura de Código:** Vitest/Jest generan reportes de cobertura (ej. con `istanbul`).

-   **Tipos de Pruebas:**
    -   **Pruebas Unitarias:**
        -   **Objetivo:** Probar la unidad más pequeña de código de forma aislada (funciones de utilidad, hooks customizados, lógica de estado en Zustand).
        -   **Características:** Rápidas, granulares.
        -   **Ejemplo (Vitest/Jest + RTL para un hook):**
            ```typescript
            // src/hooks/useCounter.test.ts
            import { renderHook, act } from '@testing-library/react';
            import { useCounter } from './useCounter';

            describe('useCounter hook', () => {
              it('should increment counter', () => {
                const { result } = renderHook(() => useCounter(0));
                act(() => {
                  result.current.increment();
                });
                expect(result.current.count).toBe(1);
              });
            });
            ```

    -   **Pruebas de Componentes (Integración Ligera):**
        -   **Objetivo:** Probar componentes individuales o pequeños grupos de componentes interactuando, incluyendo su renderizado, interacciones del usuario y cómo responden a cambios de props/estado.
        -   **Herramienta:** React Testing Library.
        -   **Enfoque:** Simular eventos de usuario (`fireEvent`, `userEvent` de RTL) y verificar que el DOM se actualiza como se espera. No probar detalles de implementación.
        -   **Ejemplo (Vitest/Jest + RTL):**
            ```tsx
            // src/components/MyButton.test.tsx
            import { render, screen, fireEvent } from '@testing-library/react';
            import userEvent from '@testing-library/user-event';
            import MyButton from './MyButton';

            describe('MyButton component', () => {
              it('renders with correct text', () => {
                render(<MyButton>Click Me</MyButton>);
                expect(screen.getByRole('button', { name: /Click Me/i })).toBeInTheDocument();
              });

              it('calls onClick prop when clicked', async () => {
                const handleClick = vi.fn(); // o jest.fn()
                render(<MyButton onClick={handleClick}>Click Me</MyButton>);
                await userEvent.click(screen.getByRole('button', { name: /Click Me/i }));
                expect(handleClick).toHaveBeenCalledTimes(1);
              });
            });
            ```

    -   **Pruebas End-to-End (E2E):**
        -   **Objetivo:** Probar flujos completos de la aplicación desde la perspectiva del usuario, simulando interacciones reales en un navegador.
        -   **Herramientas:** Cypress o Playwright.
        -   **Características:** Más lentas y costosas de mantener, pero cruciales para validar la integración de todas las partes (frontend, backend, API).
        -   **Ejemplo de Escenario (conceptual):**
            1.  Navegar a la página de login.
            2.  Ingresar credenciales válidas.
            3.  Verificar redirección al dashboard.
            4.  Navegar a la gestión de cursos.
            5.  Crear un nuevo curso.
            6.  Verificar que el curso aparece en la lista.
        -   **Mocking de API en E2E:** Para flujos críticos, se pueden mockear respuestas de API para hacer las pruebas más deterministas y rápidas, y para probar estados de error específicos.

-   **Estrategia de Pruebas:**
    -   **Pirámide de Pruebas:** Enfocarse en tener una base sólida de pruebas unitarias y de componentes, complementada por un conjunto más pequeño pero significativo de pruebas E2E para los flujos críticos.
    -   **Cobertura:** Apuntar a una alta cobertura de código (ej. >80%), pero priorizar la calidad y relevancia de las pruebas sobre el simple porcentaje.
    -   **Integración Continua (CI):** Ejecutar todas las pruebas automáticamente en cada push/pull request a través de un pipeline de CI (ej. GitHub Actions, GitLab CI).

-   **Mocking y Spying:**
    -   Usar `vi.mock` (Vitest) o `jest.mock` para mockear módulos o dependencias externas (ej. servicios API, librerías de terceros).
    -   Usar `vi.spyOn` o `jest.spyOn` para espiar llamadas a métodos específicos sin modificar su implementación original.

-   **Accesibilidad (a11y) en Pruebas:**
    -   Integrar herramientas como `jest-axe` con React Testing Library para verificar problemas básicos de accesibilidad en los componentes renderizados durante las pruebas.
        ```tsx
        // Ejemplo con jest-axe
        import { render } from '@testing-library/react';
        import { axe, toHaveNoViolations } from 'jest-axe';
        import MyComponent from './MyComponent';

        expect.extend(toHaveNoViolations);

        it('should have no a11y violations', async () => {
          const { container } = render(<MyComponent />);
          const results = await axe(container);
          expect(results).toHaveNoViolations();
        });
        ```

-   **Pruebas de Regresión Visual (Opcional):**
    -   Para proyectos donde la consistencia visual es crítica, se pueden usar herramientas como Percy o Applitools para tomar snapshots de UI y compararlos entre builds para detectar cambios visuales inesperados.


Estas consideraciones técnicas avanzadas —manejo de errores, seguridad, rendimiento y pruebas— son fundamentales para desarrollar una aplicación frontend de alta calidad, robusta, segura y mantenible. La adherencia a estas prácticas no solo mejorará la experiencia del usuario final, sino que también facilitará la escalabilidad y la colaboración a largo plazo en el proyecto Smart Academy. Es crucial que el equipo de desarrollo revise y aplique estos principios de manera continua a lo largo del ciclo de vida del proyecto.

## 8. Conclusión y Próximos Pasos

Esta guía de arquitectura frontend ha establecido un marco de trabajo detallado para el desarrollo de la interfaz de usuario de la plataforma Smart Academy. Se ha enfocado en la creación de una aplicación moderna, modular, mantenible, escalable y de alto rendimiento utilizando React, TypeScript, Material-UI y otras herramientas y patrones contemporáneos.

**Resumen de Principios Clave:**

-   **Tecnologías Base:** React (con Hooks y Context API/Zustand para estado global), TypeScript para tipado estático, Vite como herramienta de build, React Router para enrutamiento, Axios para llamadas API, y Material-UI para componentes de UI.
-   **Modularidad:** Organización del código en `features` o módulos funcionales, cada uno con sus propios componentes, servicios, tipos y opcionalmente estado.
-   **Componentización:** Énfasis en componentes reutilizables, bien definidos y con APIs claras.
-   **Estado:** Gestión de estado local con hooks de React, estado global con Zustand (o React Query/SWR para estado de servidor), y React Hook Form para formularios.
-   **Tipado Fuerte:** Uso extensivo de TypeScript, con tipos e interfaces alineados con los modelos de datos del backend (Pydantic) y los `ejemplosjson.md`.
-   **Calidad y Mantenibilidad:** A través de linters (ESLint), formateadores (Prettier), manejo avanzado de errores, logging, y una estrategia de pruebas robusta (unitaria, componentes, E2E).
-   **Seguridad:** Implementación de prácticas de seguridad frontend como gestión segura de JWT, prevención de XSS/CSRF, y protección de rutas.
-   **Rendimiento:** Optimización mediante code splitting, memoización, virtualización de listas, optimización de imágenes y otras técnicas.
-   **Flujo de Desarrollo:** Adopción de GitFlow simplificado, revisiones de código mediante Pull Requests, y mensajes de commit convencionales.

**Próximos Pasos Recomendados:**

1.  **Configuración Inicial del Proyecto:**
    -   Crear el repositorio Git.
    -   Inicializar el proyecto React + TypeScript con Vite.
    -   Instalar dependencias base (React Router, Axios, Material-UI, Zustand, Zod, ESLint, Prettier, Vitest, React Testing Library, etc.).
    -   Configurar ESLint, Prettier, y los scripts de `package.json` para linting, formateo, pruebas y build.
    -   Establecer la estructura de directorios base (`src/components`, `src/hooks`, `src/services`, `src/features`, `src/types`, `src/utils`, etc.).

2.  **Desarrollo del Módulo de Autenticación (CU1, CU2, CU3, CU4):**
    -   Implementar las vistas de Login, Registro (si aplica), Olvido/Recuperación de Contraseña.
    -   Crear el servicio API para autenticación (`authService.ts`) usando el wrapper de Axios.
    -   Configurar el store de Zustand para el estado de autenticación (usuario, token, estado de carga).
    -   Implementar los `ProtectedRoute` y la lógica de redirección.
    -   Definir los tipos TypeScript para `AuthPayload`, `UserAuth`, `TokenResponse`.

3.  **Implementación de Componentes Base y Layout:**
    -   Desarrollar el layout principal de la aplicación (Navbar, Sidebar, Footer, Contenedor de contenido).
    -   Crear componentes UI reutilizables genéricos (ej. `Button`, `Input`, `Modal`, `TableWrapper`, `PageLoader`) si los de Material-UI no son suficientes o requieren personalización extensa.

4.  **Desarrollo Iterativo de Módulos (Features):**
    -   Priorizar los módulos según las necesidades del proyecto (ej. Gestión de Usuarios, Roles, Cursos).
    -   Para cada módulo:
        -   Definir rutas.
        -   Crear tipos TypeScript basados en `ejemplosjson.md`.
        -   Desarrollar servicios API.
        -   Implementar componentes de UI y vistas.
        -   Gestionar estado local y/o global.
        -   Escribir pruebas unitarias y de componentes.

5.  **Configuración de CI/CD (Paralelo):**
    -   Configurar el pipeline de Integración Continua (ej. GitHub Actions) para ejecutar linters, formateadores y pruebas en cada PR.
    -   Establecer el pipeline de Despliegue Continuo para los entornos de Staging y Producción.

6.  **Revisiones y Refinamiento Continuo:**
    -   Realizar revisiones de código periódicas.
    -   Refinar la arquitectura y las implementaciones basándose en la retroalimentación y los nuevos requisitos.
    -   Mantener actualizada la documentación (esta guía y JSDoc/TSDoc en el código).

7.  **Capacitación del Equipo:**
    -   Asegurar que todos los miembros del equipo frontend comprendan y sigan las directrices establecidas en este documento.

Esta guía de arquitectura es un documento vivo y debe ser actualizado a medida que el proyecto evoluciona y se toman nuevas decisiones técnicas. La colaboración y comunicación constante entre los equipos de frontend, backend, y diseño serán clave para el éxito de Smart Academy.