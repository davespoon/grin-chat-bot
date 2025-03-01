# repositories.py
from sqlalchemy.orm import Session
from typing import List, Optional

from models.PersonProfile import PersonProfile
from models.DbProfile import DbProfile


class ProfileRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_profile(self, profile: PersonProfile) -> int:
        """Add a new profile using the hybrid model and return its generated ID."""
        new_profile = DbProfile(
            name=profile.name,
            phone=profile.phone,
            email=profile.email,
            summary=profile.summary,
            extra_data={
                "skills": profile.skills,
                "experience": profile.experience,
                "education": profile.education,
                "another_info": profile.another_info
            }
        )
        self.session.add(new_profile)
        self.session.commit()
        self.session.refresh(new_profile)
        return new_profile.id

    def get_profile(self, profile_id: int) -> Optional[PersonProfile]:
        """Retrieve a profile by ID and convert it into a Pydantic model."""
        profile = self.session.query(DbProfile).filter(DbProfile.id == profile_id).first()
        if profile:
            # Merge the two parts into one dict for the Pydantic model.
            data = {
                "name": profile.name,
                "phone": profile.phone,
                "email": profile.email,
                "summary": profile.summary,
                **(profile.extra_data or {})  # unpack the JSON fields
            }
            try:
                return PersonProfile.model_validate(data)
            except Exception as e:
                print(f"Error parsing profile: {e}")
        return None

    def get_all_profiles(self) -> List[PersonProfile]:
        """Retrieve all profiles and return them as Pydantic models."""
        profiles = self.session.query(DbProfile).all()
        result = []
        for profile in profiles:
            data = {
                "id": profile.id,
                "name": profile.name,
                "phone": profile.phone,
                "email": profile.email,
                "summary": profile.summary,
                **(profile.extra_data or {})
            }
            try:
                result.append(PersonProfile.model_validate(data))
            except Exception as e:
                print(f"Error parsing profile: {e}")
        return result

    def update_profile(self, profile_id: int, profile: PersonProfile) -> bool:
        """Update an existing profile using a Pydantic model."""
        db_profile = self.session.query(DbProfile).filter(DbProfile.id == profile_id).first()
        if db_profile:
            db_profile.name = profile.name
            db_profile.phone = profile.phone
            db_profile.email = profile.email
            db_profile.summary = profile.summary
            db_profile.extra_data = {
                "skills": profile.skills,
                "experience": profile.experience,
                "education": profile.education,
                "another_info": profile.another_info
            }
            self.session.commit()
            return True
        return False

    def delete_profile(self, profile_id: int) -> bool:
        """Delete a profile."""
        profile = self.session.query(DbProfile).filter(DbProfile.id == profile_id).first()
        if profile:
            self.session.delete(profile)
            self.session.commit()
            return True
        return False
