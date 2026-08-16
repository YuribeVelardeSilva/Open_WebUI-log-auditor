import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import BaseModel, Field


class Tools:
    class Valves(BaseModel):
        FROM_EMAIL: str = Field(
            default="yuribe@ingenieria.unam.edu",
            description="Correo emisor (ej. tu dirección de Gmail o Google Workspace)",
        )
        PASSWORD: str = Field(
            default="", description="Contraseña de aplicación de Google (16 caracteres)"
        )
        SMTP_SERVER: str = Field(
            default="smtp.gmail.com",
            description="Servidor SMTP (smtp.gmail.com para Gmail)",
        )
        SMTP_PORT: int = Field(default=587, description="Puerto SMTP (587 para TLS)")

    def __init__(self):
        self.valves = self.Valves()

    def send_email(
        self,
        to: str = Field(..., description="Email del destinatario."),
        subject: str = Field(..., description="Asunto del correo."),
        body: str = Field(..., description="Cuerpo o contenido del correo."),
    ) -> str:
        """
        Envía un email usando SMTP de manera segura. Usar siempre que el usuario pida enviar un correo.
        """
        # Validación de inputs
        if not to or not subject or not body:
            return "❌ Error: Faltan parámetros obligatorios (to, subject, body)."

        if not self.valves.FROM_EMAIL or not self.valves.PASSWORD:
            return "❌ Error: Valves no configurados. Configura FROM_EMAIL y PASSWORD en los ajustes de la Tool."

        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = self.valves.FROM_EMAIL
            msg["To"] = to
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))

            server = smtplib.SMTP(self.valves.SMTP_SERVER, self.valves.SMTP_PORT)
            server.starttls()
            server.login(self.valves.FROM_EMAIL, self.valves.PASSWORD)
            server.send_message(msg)
            server.quit()

            return f"✅ Email enviado exitosamente a {to}. Asunto: '{subject}'"

        except smtplib.SMTPAuthenticationError:
            return "❌ Error de autenticación: Revisa que tu FROM_EMAIL y la contraseña de aplicación en Valves sean correctos."
        except smtplib.SMTPException as e:
            return f"❌ Error de protocolo SMTP: {str(e)}"
        except Exception as e:
            return f"❌ Error inesperado: {str(e)}"
