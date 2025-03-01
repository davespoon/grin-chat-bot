from flask import render_template, request, jsonify, flash, redirect, url_for

import constants
from helpers import doc_helper
from models.entities.PersonProfile import PersonProfile
from repositories.ProfileRepository import ProfileRepository
from repositories.db import SessionLocal


def index():
    """
       Retrieves all profiles from the database, converts them into
       PersonProfile instances for validation/typing, and renders the
       profiles.html template.
       """
    session = SessionLocal()
    repo = ProfileRepository(session)

    # Retrieve stored profiles as list of dicts
    profiles_data = repo.get_all_profiles()
    profiles = []
    for data in profiles_data:
        try:
            # Validate and create a PersonProfile instance
            profile = PersonProfile.model_validate(data)
            profiles.append(profile)
        except Exception as e:
            print(f"Error parsing profile: {e}")
    session.close()
    return render_template("profiles.html", profiles=profiles)


def upload_profile():
    """
        Handles file uploads for profiles. The process is:
        1. Retrieve the uploaded file from the request.
        2. Save the file to disk via a helper function.
        3. Load the file(s) and extract profile/resume info using a prompt/template.
        4. Validate and construct a PersonProfile instance.
        5. Store the profile into the database via the ORM repository.
        6. Return a JSON response indicating success or error.
        """
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400

    # Save the file and get its filename
    filename = doc_helper.save_file(file)
    if not filename:
        return jsonify({"error": "File upload failed"}), 500

    # Load documents from the data directory (adjust DATA_PATH as needed)
    docs, modification_times = doc_helper.load_documents(constants.DATA_PATH)

    # Extract resume/profile information using a prompt template
    extracted_data = doc_helper.extract_resume_info(docs)

    # Validate extracted data using your Pydantic model
    try:
        profile = PersonProfile(
            name=extracted_data.name,
            email=extracted_data.email,
            phone=extracted_data.phone,
            experience=extracted_data.experience,
            education=extracted_data.education,
            skills=extracted_data.skills,
            summary=extracted_data.summary,
            another_info=extracted_data.another_info
        )
    except Exception as e:
        return jsonify({"error": f"Profile data validation failed: {str(e)}"}), 500

    # Insert the new profile into the database
    session = SessionLocal()
    repo = ProfileRepository(session)
    profile_id = repo.add_profile(profile)
    session.close()

    flash(f"File uploaded successfully!", category="success")
    return redirect(url_for("profiles"))


def delete_profile(profile_id):
    """
    Deletes a profile identified by profile_id and redirects back to the profiles page.
    """
    session = SessionLocal()
    repo = ProfileRepository(session)
    success = repo.delete_profile(profile_id)
    session.close()
    if success:
        flash("Profile deleted successfully.", "success")
    else:
        flash("Profile not found.", "danger")
    return redirect(url_for("profiles"))


def edit_profile(profile_id):
    """
    Handles editing a profile.
      - GET: Retrieves the profile and renders the edit form.
      - POST: Validates the submitted form data and updates the profile.
    """
    session = SessionLocal()
    repo = ProfileRepository(session)

    if request.method == 'POST':
        # Retrieve updated data from the form
        # For simplicity, we expect comma-separated lists for skills, experience, and education.
        updated_data = {
            "name": request.form.get("name"),
            "phone": request.form.get("phone"),
            "email": request.form.get("email"),
            "summary": request.form.get("summary"),
            "skills": [s.strip() for s in request.form.get("skills", "").split(",") if s.strip()],
            "experience": [e.strip() for e in request.form.get("experience", "").split(",") if e.strip()],
            "education": [ed.strip() for ed in request.form.get("education", "").split(",") if ed.strip()],
            "another_info": request.form.get("another_info")
        }
        try:
            # Validate using the Pydantic model
            updated_profile = PersonProfile.model_validate(updated_data)
        except Exception as e:
            session.close()
            flash("Profile update failed: " + str(e), "danger")
            return redirect(url_for("edit_profile", profile_id=profile_id))

        # Update the profile in the database
        success = repo.update_profile(profile_id, updated_profile)
        session.close()
        if success:
            flash("Profile updated successfully.", "success")
        else:
            flash("Profile update failed. Profile not found.", "danger")
        return redirect(url_for("profiles"))
    else:
        # GET request: Retrieve the profile and render the edit form.
        profile = repo.get_profile(profile_id)
        session.close()
        if profile is None:
            flash("Profile not found.", "danger")
            return redirect(url_for("profiles"))
        return render_template("edit_profile.html", profile=profile)
