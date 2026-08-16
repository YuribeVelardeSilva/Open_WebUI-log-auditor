import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import BaseModel, Field


class Tools:
    class Valves(BaseModel):
        SMTP_SERVER: str = Field(
            default="smtp.gmail.com", description="Servidor SMTP para envío de correos"
        )
        SMTP_PORT: int = Field(default=587, description="Puerto SMTP (587 para TLS)")
        EMAIL_EMISOR: str = Field(
            default="yuribe@ingenieria.unam.edu", description="Correo remitente"
        )
        EMAIL_PASSWORD: str = Field(
            default="",
            description="Contraseña de aplicación de Google (16 caracteres)",
        )

    def __init__(self):
        self.valves = self.Valves()

    def enviar_reporte_log(
        self,
        analisis_diagnostico: str = Field(
            ...,
            description="El análisis conciso, causa raíz y mitigación del log.",
        ),
        email_receptor: str = Field(
            default="yuribe@ingenieria.unam.edu",
            description="Dirección de correo a la que se enviará el reporte.",
        ),
        nombre_servidor: str = Field(
            default="srv-db-prod01",
            description="Hostname del servidor analizado (ej. srv-ssh-01, web-prod).",
        ),
        ip_servidor: str = Field(
            default="N/A",
            description="Dirección IP del servidor extraída del log o prompt.",
        ),
        sistema_operativo: str = Field(
            default="Linux / Desconocido",
            description="Distribución o SO del servidor (ej. Ubuntu, Debian, RHEL).",
        ),
        servicio_afectado: str = Field(
            default="PostgreSQL",
            description="Servicio o demonio analizado (ej. SSH, Nginx, PostgreSQL, Docker).",
        ),
        nivel_criticidad: str = Field(
            default="CRÍTICA",
            description="Nivel de severidad detectado: BAJA, MEDIA, ALTA, CRÍTICA.",
        ),
    ) -> str:
        """
        [HERRAMIENTA OBLIGATORIA] Ejecuta esta función de manera automática e inmediata cada vez que se reciba un log de servidor o se solicite un diagnóstico/auditoría. No respondas únicamente con texto sin llamar antes a esta función.
        """
        smtp_server = str(os.getenv("SMTP_SERVER", self.valves.SMTP_SERVER))
        smtp_port = int(os.getenv("SMTP_PORT", self.valves.SMTP_PORT))
        email_emisor = str(os.getenv("EMAIL_EMISOR", self.valves.EMAIL_EMISOR))
        email_password = str(os.getenv("EMAIL_PASSWORD", self.valves.EMAIL_PASSWORD))

        # Conversión explícita a texto para evitar inconsistencias de tipos
        email_receptor_str = str(email_receptor)
        nombre_servidor_str = str(nombre_servidor)
        ip_servidor_str = str(ip_servidor)
        sistema_operativo_str = str(sistema_operativo)
        servicio_afectado_str = str(servicio_afectado)
        nivel_criticidad_str = str(nivel_criticidad)
        analisis_diagnostico_str = str(analisis_diagnostico)

        fecha_actual = datetime.now().strftime("%A, %B %d, %Y - %I:%M:%S %p")

        if not email_password:
            return f"❌ Error: Configura la contraseña de aplicación en Valves antes de enviar el correo.\n\n### DIAGNÓSTICO GENERADO:\n{analisis_diagnostico_str}"

        try:
            msg = MIMEMultipart()
            msg["From"] = email_emisor
            msg["To"] = email_receptor_str
            msg["Subject"] = (
                f"🚨 [{nivel_criticidad_str}] Reporte Ejecutivo: {nombre_servidor_str} ({servicio_afectado_str})"
            )

            cuerpo = f"""======================================================================
            REPORTE EJECUTIVO DE AUDITORÍA DE LOGS
======================================================================
Fecha de Procesamiento: {fecha_actual}
Nivel de Criticidad:   [{nivel_criticidad_str}]

----------------------------------------------------------------------
1. DATOS DEL SERVIDOR
----------------------------------------------------------------------
- Hostname:           {nombre_servidor_str}
- IP:                 {ip_servidor_str}
- Sistema Operativo:  {sistema_operativo_str}
- Servicio / Daemon:  {servicio_afectado_str}

----------------------------------------------------------------------
2. ANÁLISIS RESUMIDO Y MITIGACIÓN INMEDIATA
----------------------------------------------------------------------
{analisis_diagnostico_str}

----------------------------------------------------------------------
Reporte automatizado generado desde Open WebUI.
Destinatario oficial: {email_receptor_str}
======================================================================
"""
            msg.attach(MIMEText(cuerpo, "plain", "utf-8"))

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_emisor, email_password)

            # Envío nativo seguro codificado en UTF-8
            server.send_message(msg)
            server.quit()

            return f"✅ Reporte enviado exitosamente a {email_receptor_str} el {fecha_actual}.\n\n### DIAGNÓSTICO ENVIADO:\n{analisis_diagnostico_str}"

        except Exception as e:
            return f"⚠️ Error al enviar el correo vía SMTP: {str(e)}\n\n### DIAGNÓSTICO GENERADO:\n{analisis_diagnostico_str}"
