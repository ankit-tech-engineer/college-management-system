import random
import hashlib
import hmac
from datetime import datetime, timedelta
from config.database import get_db
from typing import Optional

class OTPService:
    def __init__(self):
        self.otp_length = 6
        self.expiry_minutes = 10
        self.max_attempts = 3
        self.algorithm = "HMAC-SHA256"
        self.secret_key = "otp-secret-key"
        
    def _generate_otp(self) -> str:
        """Generate 6-digit OTP"""
        return str(random.randint(100000, 999999))
    
    def _hash_otp(self, otp: str) -> str:
        """Hash OTP using HMAC-SHA256"""
        return hmac.new(
            self.secret_key.encode(),
            otp.encode(),
            hashlib.sha256
        ).hexdigest()
    
    async def create_otp(self, user_identifier: str) -> str:
        """Create and store OTP for user"""
        try:
            db = await get_db()
            collection = db["otp_records"]
            
            # Generate OTP
            otp = self._generate_otp()
            hashed_otp = self._hash_otp(otp)
            
            # Create OTP record
            otp_record = {
                "user_identifier": user_identifier,
                "otp_hash": hashed_otp,
                "creation_timestamp": datetime.utcnow(),
                "expiry_time": datetime.utcnow() + timedelta(minutes=self.expiry_minutes),
                "otp_length": self.otp_length,
                "otp_algorithm": "TOTP",
                "hashing_algorithm": self.algorithm,
                "verification_attempts": 0,
                "verification_status": False,
                "locked_status": False,
                "secret_key_encoding": "base64",
                "version": 1,
                "is_deleted": False
            }
            
            # Soft delete existing OTP for user
            await collection.update_many(
                {"user_identifier": user_identifier, "is_deleted": False},
                {"$set": {"is_deleted": True}}
            )
            
            # Insert new OTP
            await collection.insert_one(otp_record)
            
            return otp
        except Exception as e:
            return None
    
    async def verify_otp(self, user_identifier: str, otp: str) -> dict:
        """Verify OTP for user"""
        try:
            db = await get_db()
            collection = db["otp_records"]
            
            # Find active OTP record
            record = await collection.find_one({
                "user_identifier": user_identifier,
                "is_deleted": False
            })
            
            if not record:
                return {"success": False, "message": "OTP not found"}
            
            # Check if locked
            if record.get("locked_status"):
                return {"success": False, "message": "OTP verification locked due to too many attempts"}
            
            # Check if expired
            if datetime.utcnow() > record["expiry_time"]:
                # Mark as expired (soft delete)
                await collection.update_one(
                    {"_id": record["_id"]},
                    {"$set": {"is_deleted": True, "expired_at": datetime.utcnow()}}
                )
                return {"success": False, "message": "OTP expired"}
            
            # Check if already verified
            if record.get("verification_status"):
                return {"success": False, "message": "OTP already verified"}
            
            # Increment attempts
            attempts = record.get("verification_attempts", 0) + 1
            
            # Hash provided OTP
            hashed_otp = self._hash_otp(otp)
            
            # Verify OTP
            if hashed_otp == record["otp_hash"]:
                # Mark as verified (soft delete)
                await collection.update_one(
                    {"_id": record["_id"]},
                    {"$set": {
                        "verification_status": True,
                        "verified_at": datetime.utcnow(),
                        "is_deleted": True
                    }}
                )
                return {"success": True, "message": "OTP verified successfully"}
            else:
                # Update attempts
                update_data = {"verification_attempts": attempts}
                
                # Lock if max attempts reached
                if attempts >= self.max_attempts:
                    update_data["locked_status"] = True
                
                await collection.update_one(
                    {"_id": record["_id"]},
                    {"$set": update_data}
                )
                
                remaining = self.max_attempts - attempts
                if remaining > 0:
                    return {"success": False, "message": f"Invalid OTP. {remaining} attempts remaining"}
                else:
                    return {"success": False, "message": "OTP verification locked due to too many attempts"}
                    
        except Exception as e:
            return {"success": False, "message": "OTP verification failed"}
    
    async def is_email_verified(self, user_identifier: str) -> bool:
        """Check if user email is verified"""
        try:
            db = await get_db()
            collection = db["otp_records"]
            
            # Check if there's a verified OTP record
            verified_record = await collection.find_one({
                "user_identifier": user_identifier,
                "verification_status": True
            })
            
            return verified_record is not None
        except:
            return False
    
    async def cleanup_expired_otps(self):
        """Soft delete expired OTP records"""
        try:
            db = await get_db()
            collection = db["otp_records"]
            await collection.update_many(
                {
                    "expiry_time": {"$lt": datetime.utcnow()},
                    "is_deleted": False
                },
                {"$set": {"is_deleted": True, "expired_at": datetime.utcnow()}}
            )
        except:
            pass