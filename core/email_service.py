import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from config.settings import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS

class EmailService:
    def __init__(self):
        self.smtp_host = SMTP_HOST
        self.smtp_port = SMTP_PORT
        self.smtp_user = SMTP_USER
        self.smtp_pass = SMTP_PASS
    
    def _load_template(self, template_name: str, **kwargs) -> str:
        """Load and render email template"""
        # print("kwargs>>>>>>>>>",kwargs)
        try:
            template_path = os.path.join("templates", template_name)
            with open(template_path, 'r', encoding='utf-8') as file:
                template = file.read()
            
            # Simple template rendering
            for key, value in kwargs.items():
                template = template.replace(f"{{{{{key}}}}}", str(value))
            
            return template
        except Exception as e:
            return f"<p>Welcome! Your registration was successful.</p>"
    
    async def send_welcome_otp_email(self, email: str, full_name: str, user_id: str, otp: str):
        """Send welcome email with OTP verification"""
        try:
            html_content = self._load_template(
                "welcome_otp_email.html",
                full_name=full_name,
                email=email,
                user_id=user_id,
                otp=otp,
                registration_date=datetime.now().strftime("%B %d, %Y")
            )
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Welcome & Email Verification - College Management System"
            msg['From'] = self.smtp_user
            msg['To'] = email
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            return False
    
    async def send_verification_success_email(self, email: str, full_name: str):
        """Send verification success email"""
        try:
            html_content = self._load_template(
                "verification_success_email.html",
                full_name=full_name,
                email=email
            )
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Email Verified Successfully - College Management System"
            msg['From'] = self.smtp_user
            msg['To'] = email
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            return False
    
    async def send_forgot_password_email(self, email: str, full_name: str, otp: str):
        """Send forgot password email with OTP"""
        try:
            html_content = self._load_template(
                "forgot_password_email.html",
                full_name=full_name,
                email=email,
                otp=otp
            )
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Password Reset Request - College Management System"
            msg['From'] = self.smtp_user
            msg['To'] = email
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            return False
    
    async def send_password_reset_success_email(self, email: str, full_name: str):
        """Send password reset success email"""
        try:
            html_content = self._load_template(
                "password_reset_success_email.html",
                full_name=full_name,
                email=email
            )
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Password Reset Successful - College Management System"
            msg['From'] = self.smtp_user
            msg['To'] = email
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            return False