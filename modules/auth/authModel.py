from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

class LoginModel(BaseModel):
    email: EmailStr
    password: str

class RegisterModel(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=8, max_length=100)

class EducationModel(BaseModel):
    board: Optional[str] = ""
    percentage: Optional[str] = ""
    year: Optional[str] = ""

class PreviousCollegeModel(BaseModel):
    name: Optional[str] = ""
    degree: Optional[str] = ""
    percentage: Optional[str] = ""
    year: Optional[str] = ""

class AcademicDetailsModel(BaseModel):
    tenth: Optional[EducationModel] = None
    twelfth: Optional[EducationModel] = None
    previousCollege: Optional[PreviousCollegeModel] = None

class CourseSelectionModel(BaseModel):
    program: Optional[str] = None
    course: Optional[str] = None

class PersonalDetailsModel(BaseModel):
    full_name: Optional[str] = None
    father_name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    phone_number: Optional[str] = None
    alt_number: Optional[str] = None

class CompleteProfileModel(BaseModel):
    personalDetails: Optional[PersonalDetailsModel] = None
    academicDetails: Optional[AcademicDetailsModel] = None
    courseSelection: Optional[CourseSelectionModel] = None
    photo: Optional[dict] = None
    id_proof: Optional[dict] = None