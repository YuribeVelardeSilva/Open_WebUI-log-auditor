# 🛡️ Agentic SysAdmin Log Auditor & SMTP Alert System

Sistema automatizado de ciberseguridad y administración de sistemas para la auditoría de logs de servidores, diagnóstico de causas raíz e inyección de alertas ejecutivas por correo electrónico utilizando un **LLM local** y **Tool Calling**.

---

## 🏗️ Arquitectura del Proyecto

* **Interfaz / Orquestador:** Open WebUI
* **Motor LLM Local:** Ollama con `qwen2.5:7b` (Soporte de Native Function Calling)
* **Custom Tool:** Script en Python (`tool_email.py`) utilizando `smtplib` y `pydantic`
* **Workflow:** Invocación por comando modal (`/auditar-log`) con análisis automático de adjuntos `.log` / `.txt`

---

## 🚀 Requisitos Previos

* [Docker](https://www.docker.com/) y Docker Compose instalados.
* [Ollama](https://ollama.com/) instalado en el sistema o corriendo en contenedor.
* Credenciales SMTP activas (ej. Contraseña de Aplicación de Gmail).

---

## 🛠️ Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone [https://github.com/tu-usuario/sysadmin-log-auditor.git](https://github.com/tu-usuario/sysadmin-log-auditor.git)
cd sysadmin-log-auditor