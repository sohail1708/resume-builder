import streamlit as st
import requests


# Backend URL
BACKEND_URL = "https://q6xdqysotl.execute-api.us-east-2.amazonaws.com/prod/generate-resume"  # Replace with your backend API endpoint

# Initialize session state
if "nav_tabs" not in st.session_state:
    st.session_state.nav_tabs = ["Profile", "Job Description"]
if "current_page" not in st.session_state:
    st.session_state.current_page = "Profile"

# Sidebar for navigation
st.sidebar.title("Navigation")
st.session_state.current_page = st.sidebar.selectbox(
    "Go to", st.session_state.nav_tabs, index=st.session_state.nav_tabs.index(st.session_state.current_page)
)


full_name = None
email = None
phone = None
linkedin = None
github = None
website = None
education_list = None
work_experience_list = None
certifications_list = None
projects_list = None
skills = None

# Profile Page
if st.session_state.current_page == "Profile":
    st.title("Resume Builder")

    # Basic Information
    st.header("Personal Information")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    linkedin = st.text_input("LinkedIn Profile")
    github = st.text_input("GitHub Profile")
    website = st.text_input("Personal Website")

    # Initialize session state for dynamic sections
    if "education" not in st.session_state:
        st.session_state.education = [{}]

    if "work_experience" not in st.session_state:
        st.session_state.work_experience = [{}]

    if "certifications" not in st.session_state:
        st.session_state.certifications = [{}]

    if "projects" not in st.session_state:
        st.session_state.projects = [{}]

    # Dynamic Education Section
    st.header("Education")
    education_list = []
    for i, edu in enumerate(st.session_state.education):
        degree = st.text_input(f"Degree {i+1}", key=f"degree_{i}")
        university = st.text_input(f"University/Institution {i+1}", key=f"university_{i}")
        grad_year = st.text_input(f"Graduation Year {i+1}", key=f"grad_year_{i}")
        if degree and university and grad_year:
            education_list.append({"degree": degree, "university": university, "grad_year": grad_year})
    if st.button("Add Education"):
        st.session_state.education.append({})

    # Dynamic Work Experience Section
    st.header("Work Experience")
    work_experience_list = []
    for i, work in enumerate(st.session_state.work_experience):
        job_title = st.text_input(f"Job Title {i+1}", key=f"job_title_{i}")
        company = st.text_input(f"Company Name {i+1}", key=f"company_{i}")
        start_date = st.date_input(f"Start Date {i+1}", key=f"work_start_date_{i}")
        end_date = st.date_input(f"End Date {i+1}", key=f"work_end_date_{i}")
        description = st.text_area(f"Description {i+1}", key=f"work_description_{i}")
        if job_title and company and start_date and end_date and description:
            work_experience_list.append({
                "job_title": job_title,
                "company": company,
                "start_date": str(start_date),
                "end_date": str(end_date),
                "description": description,
            })
    if st.button("Add Work Experience"):
        st.session_state.work_experience.append({})

    # Dynamic Certifications Section
    st.header("Certifications")
    certifications_list = []
    for i, cert in enumerate(st.session_state.certifications):
        cert_name = st.text_input(f"Certification Name {i+1}", key=f"cert_name_{i}")
        cert_authority = st.text_input(f"Certifying Authority {i+1}", key=f"cert_authority_{i}")
        cert_year = st.text_input(f"Year of Certification {i+1}", key=f"cert_year_{i}")
        if cert_name and cert_authority and cert_year:
            certifications_list.append({
                "cert_name": cert_name,
                "cert_authority": cert_authority,
                "cert_year": cert_year,
            })
    if st.button("Add Certification"):
        st.session_state.certifications.append({})

    # Dynamic Projects Section
    st.header("Projects")
    projects_list = []
    for i, proj in enumerate(st.session_state.projects):
        proj_name = st.text_input(f"Project Name {i+1}", key=f"proj_name_{i}")
        proj_description = st.text_area(f"Project Description {i+1}", key=f"proj_description_{i}")
        proj_tech_stack = st.text_area(f"Technologies Used {i+1}", key=f"proj_tech_stack_{i}")
        if proj_name and proj_description and proj_tech_stack:
            projects_list.append({
                "proj_name": proj_name,
                "proj_description": proj_description,
                "proj_tech_stack": proj_tech_stack,
            })
    if st.button("Add Project"):
        st.session_state.projects.append({})

    # Skills Section
    st.header("Skills")
    skills = st.text_area("List your skills (separated by commas)")

    # Submit Button
    if st.button("Submit"):
        # Uncomment below lines when backend is ready to handle the resume submission

        # Navigate to "Job Description" page directly for now
        if "Job Description" not in st.session_state.nav_tabs:
            st.session_state.nav_tabs.append("Job Description")
        st.session_state.current_page = "Job Description"
        st.rerun()

# Job Description Page
elif st.session_state.current_page == "Job Description":
    st.title("Job Description")
    job_description = st.text_area("Paste the job description here")
    st.write("You can now analyze the job description against your resume.")

    st.markdown(
        """
        <style>
        .center-btn {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 50vh;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("""<style>div.stButton {text-align:center}</style>""", unsafe_allow_html=True)
    if st.button("Generate Your Resume"):
        payload = {
            "personal_info": {
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "linkedin": linkedin,
                "github": github,
                "website": website,
            },
            "education": education_list,
            "work_experience": work_experience_list,
            "certifications": certifications_list,
            "projects": projects_list,
            "skills": skills.split(",") if skills else [],
        }

        try:
            response = requests.post(BACKEND_URL, json=payload)
            if response.status_code == 200:
                st.success("Resume submitted successfully!")
                if "Job Description" not in st.session_state.nav_tabs:
                    st.session_state.nav_tabs.append("Job Description")
                st.session_state.current_page = "Job Description"
                st.rerun()
            else:
                st.error(f"Failed to submit resume: {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")


    st.markdown("</div>", unsafe_allow_html=True)
