import streamlit as st
import subprocess
import sys
import os
import json
import time
import smtplib
from email.message import EmailMessage

# =====================================================
# SEND REGISTRATION EMAIL
# =====================================================

def send_registration_email(user_email, user_name):

    try:

        sender_email = st.secrets["EMAIL_ADDRESS"]
        sender_password = st.secrets["EMAIL_APP_PASSWORD"]

        msg = EmailMessage()

        msg["Subject"] = "🎉 Registration Successful - AI Interview Analyzer"
        msg["From"] = sender_email
        msg["To"] = user_email

        msg.set_content(
            f"""
Hello {user_name},

🎉 Congratulations!

Your registration for AI Interview Analyzer was successful.

Your account has been created successfully.

You can now login and start your AI interview.

Thank you,
AI Interview Analyzer Team
"""
        )

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                sender_email,
                sender_password
            )

            smtp.send_message(msg)

        return True

    except Exception as e:

        print("Email sending error:", e)

        return False

from database.db import (
    save_interview,
    get_interview_history,
    register_user,
    login_user
)

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from ml.predict import predict_interview_score
from modules.career_coach.coach import generate_career_coaching
from modules.analytics.insights import generate_insights
from components.security.security import security_monitor
from modules.questions import (
    get_questions,
    get_resume_questions,
    get_adaptive_question
)
from speech.speech_analysis import get_voice_answer

from modules.analyzer import analyze_answer
from modules.ai_interviewer import AIInterviewer

from resume.parser import extract_resume_text
from resume.skill_extractor import extract_skills
from resume.matcher import match_skills




st.set_page_config(
    page_title="AI Interview Analyzer",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 AI Interview Analyzer")
st.write("AI-powered mock interview system")


# -------------------------
# SESSION STATE
# -------------------------

if "interviewer" not in st.session_state:
    st.session_state.interviewer = None

if "started" not in st.session_state:
    st.session_state.started = False

if "security_violation" not in st.session_state:
    st.session_state.security_violation = False    

if "answers" not in st.session_state:
    st.session_state.answers = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "vision_process" not in st.session_state:
    st.session_state.vision_process = None

if "vision_result" not in st.session_state:
    st.session_state.vision_result = None 

if "interview_terminated" not in st.session_state:
    st.session_state.interview_terminated = False   

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "user_email" not in st.session_state:
    st.session_state.user_email = None

# =====================================================
# REGISTRATION SUCCESS POPUP
# =====================================================

@st.dialog("🎉 Registration Successful")
def registration_success_popup():

    st.success(
        "Your account has been created successfully!"
    )

    st.write(
        "You can now login to your account."
    )

    if st.button(
        "OK",
        type="primary",
        key="registration_success_ok"
    ):
        st.rerun()


# =====================================================
# LOGIN / REGISTER
# =====================================================

if not st.session_state.logged_in:

    st.header("🔐 Welcome to AI Interview Analyzer")

    login_tab, register_tab = st.tabs(
        ["🔑 Login", "📝 Register"]
    )

    # =================================================
    # LOGIN
    # =================================================

    with login_tab:

        st.subheader("🔑 Login")

        login_email = st.text_input(
            "Email",
            key="login_email"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🔐 Login",
            type="primary",
            key="login_button"
        ):

            # -----------------------------------------
            # Check empty fields
            # -----------------------------------------

            if not login_email or not login_password:

                st.warning(
                    "⚠️ Please enter email and password."
                )

            else:

                # -------------------------------------
                # Login user
                # -------------------------------------

                user = login_user(
                    login_email,
                    login_password
                )

                # -------------------------------------
                # Login successful
                # -------------------------------------

                if user:

                    st.session_state.logged_in = True

                    st.session_state.user_id = user[0]

                    st.session_state.user_name = user[1]

                    st.session_state.user_email = user[2]

                    st.success(
                        f"Welcome, {user[1]}! 🎉"
                    )

                    st.rerun()

                # -------------------------------------
                # Login failed
                # -------------------------------------

                else:

                    st.error(
                        "❌ Invalid email or password."
                    )


    # =================================================
    # REGISTER
    # =================================================

    with register_tab:

        st.subheader("📝 Create Account")

        register_name = st.text_input(
            "Full Name",
            key="register_name"
        )

        register_email = st.text_input(
            "Email",
            key="register_email"
        )

        register_password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        register_confirm = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm"
        )

        if st.button(
            "📝 Create Account",
            type="primary",
            key="register_button"
        ):

            # -----------------------------------------
            # Name validation
            # -----------------------------------------

            if not register_name.strip():

                st.warning(
                    "⚠️ Please enter your name."
                )

            # -----------------------------------------
            # Email validation
            # -----------------------------------------

            elif not register_email.strip():

                st.warning(
                    "⚠️ Please enter your email."
                )

            # -----------------------------------------
            # Password validation
            # -----------------------------------------

            elif not register_password:

                st.warning(
                    "⚠️ Please enter a password."
                )

            # -----------------------------------------
            # Confirm password validation
            # -----------------------------------------

            elif register_password != register_confirm:

                st.error(
                    "❌ Passwords do not match."
                )

            # -----------------------------------------
            # Registration
            # -----------------------------------------

            else:

                created = register_user(
                    register_name.strip(),
                    register_email.strip(),
                    register_password
                )

                # -------------------------------------
                # Registration successful
                # -------------------------------------

                if created:

                 # Send confirmation email
                  email_sent = send_registration_email(
                    register_email.strip(),
                    register_name.strip()
    )

    # Show registration popup
                  registration_success_popup()

                # -------------------------------------
                # Email already exists
                # -------------------------------------

                else:

                    st.error(
                        "❌ This email is already registered."
                    )


    # =================================================
    # STOP LOGIN / REGISTER PAGE
    # =================================================

    st.stop()


def create_pdf_report(
    file_path,
    candidate_name,
    role,
    experience,
    difficulty,
    final_score,
    answer_score,
    vision_score,
    eye_contact,
    posture,
    strengths,
    weaknesses,
    insights
):

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(
        Paragraph(
            "AI Interview Analyzer - Final Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    # Candidate Information
    story.append(
        Paragraph(
            "<b>Candidate Information</b>",
            styles["Heading2"]
        )
    )

    candidate_data = [
        ["Candidate Name", candidate_name],
        ["Role", role],
        ["Experience", experience],
        ["Difficulty", difficulty]
    ]

    table = Table(candidate_data)

    table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(table)

    story.append(Spacer(1, 20))

    # Scores
    story.append(
        Paragraph(
            "<b>Interview Scores</b>",
            styles["Heading2"]
        )
    )

    score_data = [
        ["Overall Score", f"{final_score:.1f}/100"],
        ["Answer Score", f"{answer_score:.1f}/100"],
        ["Vision Score", f"{vision_score:.1f}/100"],
        ["Eye Contact", f"{eye_contact:.1f}%"],
        ["Posture", f"{posture:.1f}%"]
    ]

    score_table = Table(score_data)

    score_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(score_table)

    story.append(Spacer(1, 20))

    # Strengths
    story.append(
        Paragraph(
            "<b>Strengths</b>",
            styles["Heading2"]
        )
    )

    if strengths:

        for strength in strengths:

            story.append(
                Paragraph(
                    f"• {strength}",
                    styles["BodyText"]
                )
            )

    else:

        story.append(
            Paragraph(
                "No major strengths detected.",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 15))

    # Weaknesses
    story.append(
        Paragraph(
            "<b>Areas to Improve</b>",
            styles["Heading2"]
        )
    )

    if weaknesses:

        for weakness in weaknesses:

            story.append(
                Paragraph(
                    f"• {weakness}",
                    styles["BodyText"]
                )
            )

    else:

        story.append(
            Paragraph(
                "No major improvement areas detected.",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 15))

    # Insights
    story.append(
        Paragraph(
            "<b>Interview Insights</b>",
            styles["Heading2"]
        )
    )

    if insights:

        for insight in insights:

            story.append(
                Paragraph(
                    f"• {insight}",
                    styles["BodyText"]
                )
            )

    else:

        story.append(
            Paragraph(
                "No additional insights available.",
                styles["BodyText"]
            )
        )

    doc.build(story)    

def start_vision():

    try:

        process = subprocess.Popen(
            [
                sys.executable,
                os.path.join(
                    "vision",
                    "vision_engine.py"
                )
            ]
        )

        return process

    except Exception as e:

        st.error(
            f"Vision system could not start: {e}"
        )

        return None


def terminate_interview():

    # Stop interview
    st.session_state.started = False

    # Stop vision process
    process = st.session_state.get("vision_process")

    if process is not None:

        try:

            if process.poll() is None:
                process.terminate()

        except Exception:
            pass

    # Clear vision process
    st.session_state.vision_process = None

    # Clear interviewer
    st.session_state.interviewer = None

    # Mark interview as terminated
    st.session_state.interview_terminated = True





# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("⚙️ Interview Settings")
# ==============================
# USER PROFILE + LOGOUT
# ==============================

if st.session_state.logged_in:

    st.sidebar.success(
        f"👤 {st.session_state.user_name}"
    )

    st.sidebar.caption(
        st.session_state.user_email
    )

    if st.sidebar.button(
        "🚪 Logout",
        key="logout_button"
    ):

        # Stop active interview
        if st.session_state.started:
            terminate_interview()

        # Clear login session
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.session_state.user_email = None

        st.rerun()


name = st.sidebar.text_input(
    "Candidate Name"
)

role = st.sidebar.selectbox(
    "Select Role",
    [
        "Python Developer",
        "Data Analyst",
        "Machine Learning Engineer",
        "Software Engineer"
    ]
)
# -------------------------
# REQUIRED SKILLS
# -------------------------

ROLE_SKILLS = {

    "Python Developer": [
        "Python",
        "SQL",
        "Git",
        "Docker"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Power BI",
        "Excel"
    ],

    "Machine Learning Engineer": [
        "Python",
        "NumPy",
        "Pandas",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "Git"
    ],

    "Software Engineer": [
        "Python",
        "Java",
        "C++",
        "SQL",
        "Git",
        "Docker"
    ]
}

experience = st.sidebar.selectbox(
    "Experience",
    [
        "Fresher",
        "0-2 Years",
        "2-5 Years",
        "5+ Years"
    ]
)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    [
        "Easy",
        "Medium",
        "Hard"
    ]
)

# -------------------------
# RESUME INTELLIGENCE
# -------------------------

st.sidebar.divider()

st.sidebar.subheader("📄 Resume Intelligence")

resume_file = st.sidebar.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if resume_file:

    if st.sidebar.button("🔍 Analyze Resume"):

        resume_text = extract_resume_text(
            resume_file
        )

        if resume_text:

            skills = extract_skills(
                resume_text
            )

            st.session_state.resume_text = resume_text
            st.session_state.resume_skills = skills

            st.success(
                "Resume analyzed successfully!"
            )

        else:

            st.error(
                "Could not extract text from this PDF."
            )

# -------------------------
# START INTERVIEW
# -------------------------

if st.sidebar.button(
    "🚀 Start Interview",
    type="primary"
):



    # Clear old security violation
    st.query_params.pop("interview_violation", None)

    # ==========================================
    # RESET OLD VISION RESULT
    # ==========================================

    vision_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "vision_result.json"
    )

    if os.path.exists(vision_file):
        os.remove(vision_file)

    # ==========================================
    # CREATE FRESH VISION SESSION
    # ==========================================

    initial_vision = {
        "vision_score": 0,
        "eye_contact": 0,
        "head_stability": 0,
        "posture": 0,
        "face_presence": 0,
        "feedback": [
            "🎥 Starting live vision analysis..."
        ]
    }

    with open(
        vision_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            initial_vision,
            file,
            indent=4
        )

    # ==========================================
    # LOAD QUESTIONS
    # ==========================================

    if "resume_skills" in st.session_state:

        questions = get_resume_questions(
            role,
            st.session_state.resume_skills
        )

    else:

        questions = get_questions(role)

    # ==========================================
    # CHECK QUESTIONS
    # ==========================================

    if not questions:

        st.error(
            f"No questions found for {role}"
        )

    else:

        # ==========================================
        # CREATE INTERVIEWER
        # ==========================================

        st.session_state.interviewer = AIInterviewer(
            questions
        )

        st.session_state.started = True

        st.session_state.answers = []

        st.session_state.last_result = None

        # ==========================================
        # START VISION ONLY ONCE
        # ==========================================

        if (
            st.session_state.vision_process is None
            or st.session_state.vision_process.poll() is not None
        ):

            st.session_state.vision_process = start_vision()

        # ==========================================
        # CLEAR OLD VOICE ANSWER
        # ==========================================

        if "voice_answer" in st.session_state:

            del st.session_state["voice_answer"]

        st.success(
            f"Interview started for {name or 'Candidate'}!"
        )

        st.rerun()






# -------------------------
# LAST ANSWER ANALYSIS
# -------------------------

if st.session_state.last_result is not None:

    st.divider()

    st.subheader("📊 Answer Analysis")

    result = st.session_state.last_result

    st.success(
        f"🎯 Score: {result['score']}/100"
    )

    st.info(
        f"💬 Feedback: {result['feedback']}"
    )

# ==============================
# NORMAL INTERVIEW + SECURITY
# ==============================

if st.session_state.started:

    # -------------------------
    # INTERVIEW SECURITY
    # -------------------------

    security_event = security_monitor(
        key="interview_security"
    )
    st.write("🔐 Security Event:", security_event)
    
    if (
        security_event is not None
        and security_event.get("violation") is True
    ):

        terminate_interview()

        st.error(
            "🚫 Interview terminated!"
        )

        st.warning(
            "⚠️ You left the interview page."
        )

        st.stop()




    # ==============================
    # NORMAL INTERVIEW
    # ==============================


    interviewer = st.session_state.interviewer

    question = interviewer.get_current_question()

    

    if question is not None:

        st.divider()

        st.subheader(
            f"Question {interviewer.current_index + 1}"
        )

        # -------------------------
        # QUESTION TEXT
        # -------------------------

        if isinstance(question, dict):

            question_text = (
                question.get("question")
                or question.get("text")
                or str(question)
            )

        else:

            question_text = str(question)

        st.info(question_text)


        # -------------------------
        # TEXT ANSWER
        # -------------------------

        answer = st.text_area(
            "Your Answer",
            height=180,
            key=f"answer_{interviewer.current_index}"
        )


        # -------------------------
        # VOICE ANSWER
        # -------------------------

        st.write("### 🎤 Or Answer Using Voice")

        if st.button(
            "🎙️ Record Voice Answer",
            key=f"voice_{interviewer.current_index}"
        ):

            with st.spinner(
                "🎤 Listening... Please speak for 8 seconds"
            ):

               voice_result = get_voice_answer(
                  duration=8
)

            st.session_state["voice_answer"] = voice_result["text"]
            st.session_state["speech_analysis"] = voice_result
            st.success(
                "✅ Voice captured successfully!"
            )

            st.write("### 📝 Voice Answer")

            st.write(voice_result["text"])

            st.write("### 📊 Speech Analysis")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                   "Words",
                    voice_result["word_count"]
    )

            with col2:
               st.metric(
                "Speaking Speed",
                 f"{voice_result['wpm']} WPM"
    )

            with col3:
             st.metric(
              "Filler Words",
                voice_result["filler_words"]
    )

            with col4:
             st.metric(
              "Speech Score",
              f"{voice_result['speech_score']}/100"
    )
             # -------------------------
        # SHOW SAVED VOICE ANSWER
        # -------------------------

    if "voice_answer" in st.session_state:

            st.write("### 🎤 Recorded Answer")

            st.info(
                st.session_state["voice_answer"]
            )


        # -------------------------
        # SUBMIT ANSWER
        # -------------------------

    if st.button(
            "✅ Submit Answer",
            type="primary",
            key=f"submit_{interviewer.current_index}"
        ):

            # Get text answer
            final_answer = answer.strip()


            # If text empty, use voice answer
            if (
                not final_answer
                and "voice_answer" in st.session_state
            ):

                final_answer = (
                    st.session_state["voice_answer"].strip()
                )


            # -------------------------
            # CHECK ANSWER
            # -------------------------

            if not final_answer:

                st.warning(
                    "Please write your answer or record your voice."
                )

            else:

                # -------------------------
                # ANALYZE ANSWER
                # -------------------------

                result = analyze_answer(
                    question_text,
                    final_answer
                )


                # -------------------------
                # SAVE ANSWER
                # -------------------------

                st.session_state.answers.append(
                    {
                        "question": question_text,
                        "answer": final_answer,
                        "score": result["score"],
                        "feedback": result["feedback"]
                    }
                )


                # -------------------------
                # SAVE RESULT
                # -------------------------

                st.session_state.last_result = result


                # -------------------------
                # CLEAR VOICE
                # -------------------------

                if "voice_answer" in st.session_state:

                    del st.session_state["voice_answer"]


                # -------------------------
                # MOVE TO NEXT QUESTION
                # -------------------------

                next_question = interviewer.next_question(
                    result["score"]
                )
            
                


                # -------------------------
                # NEXT QUESTION EXISTS
                # -------------------------

                if next_question is not None:

                    st.success(
                        "➡️ Moving to next question..."
                    )

                    st.rerun()


                # -------------------------
                # INTERVIEW COMPLETED
                # -------------------------

                else:

                    st.session_state.started = False

# -------------------------
    # STOP VISION
    # -------------------------

                    if st.session_state.vision_process is not None:

                       st.session_state.vision_process.terminate()

                       st.session_state.vision_process = None

                    st.session_state.started = False

                    st.success(
                        "🎉 Interview Completed!"
                    )

                    st.rerun()


# -------------------------
# SUMMARY
# -------------------------

if st.session_state.answers:

    st.divider()

    st.header("📊 Interview Progress")

    total = len(st.session_state.answers)

    # Prevent division by zero
    if total > 0:

        average = sum(
            answer["score"]
            for answer in st.session_state.answers
        ) / total

    else:

        average = 0

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Questions Attempted",
            total
        )

    with col2:

        st.metric(
            "Average Score",
            f"{average:.1f}/100"
        )


# -------------------------
# RESUME RESULTS
# -------------------------

if "resume_skills" in st.session_state:

    st.divider()

    st.header("📄 Resume Intelligence")

    skills = st.session_state.resume_skills

    required_skills = ROLE_SKILLS[role]

    match_result = match_skills(
        skills,
        required_skills
    )

    # -------------------------
    # DETECTED SKILLS
    # -------------------------

    st.subheader("Detected Skills")

    if skills:

        cols = st.columns(4)

        for i, skill in enumerate(skills):

            with cols[i % 4]:

                st.success(skill)

    else:

        st.warning(
            "No known skills detected."
        )


    # -------------------------
    # ROLE MATCHING
    # -------------------------

    st.subheader(
        f"🎯 {role} Skill Matching"
    )

    st.metric(
        "Resume Match",
        f"{match_result['match_percentage']}%"
    )

    col1, col2 = st.columns(2)

    # -------------------------
    # MATCHED SKILLS
    # -------------------------

    with col1:

        st.write("### ✅ Matched Skills")

        if match_result["matched"]:

            for skill in match_result["matched"]:

                st.success(skill)

        else:

            st.info("No matched skills found.")


    # -------------------------
    # MISSING SKILLS
    # -------------------------

    with col2:

        st.write("### ⚠️ Missing Skills")

        if match_result["missing"]:

            for skill in match_result["missing"]:

                st.warning(skill)

        else:

            st.success(
                "🎉 No missing skills!"
            )

# -------------------------
# FINAL VISION REPORT
# -------------------------

VISION_FILE = "vision_result.json"

if os.path.isfile(VISION_FILE):

    try:

        with open(VISION_FILE, "r", encoding="utf-8") as file:
            vision = json.load(file)

        st.divider()

        st.header("🎥 Vision Interview Report")

        # Overall Vision Score
        st.subheader("🏆 Vision Score")

        st.metric(
            "Overall Vision Score",
            f"{vision.get('vision_score', 0)}/100"
        )

        # Vision Metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "👁️ Eye Contact",
                f"{vision.get('eye_contact', 0):.1f}%"
            )

        with col2:
            st.metric(
                "🧠 Head Stability",
                f"{vision.get('head_stability', 0):.1f}%"
            )

        with col3:
            st.metric(
                "🧍 Posture",
                f"{vision.get('posture', 0):.1f}%"
            )

        with col4:
            st.metric(
                "🙂 Face Presence",
                f"{vision.get('face_presence', 0):.1f}%"
            )

        # Feedback
        st.subheader("💬 Vision Feedback")

        feedback = vision.get(
            "feedback",
            []
        )

        if feedback:

            for item in feedback:
                st.info(item)

        else:

            st.info(
                "No vision feedback available."
            )

    except Exception as e:

        st.error(
            f"Could not load vision report: {e}"
        )

else:

    st.info(
        "🎥 Vision report will appear after the vision analysis is completed."
    )

# =====================================================
# FINAL INTERVIEW SCORE + ADVANCED ANALYTICS
# =====================================================

vision_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "vision_result.json"
)
# =====================================================
# FINAL INTERVIEW SCORE + ADVANCED ANALYTICS
# =====================================================


if st.session_state.answers and os.path.exists(vision_file):

    try:

        # =================================================
        # LOAD VISION RESULT
        # =================================================

        with open(
            vision_file,
            "r",
            encoding="utf-8"
        ) as file:

            vision = json.load(file)

        # =================================================
        # ANSWER SCORE
        # =================================================

        answer_score = sum(
            answer["score"]
            for answer in st.session_state.answers
        ) / len(st.session_state.answers)

        # =================================================
        # VISION SCORE
        # =================================================

        vision_score = float(
            vision.get("vision_score", 0)
        )

        # =================================================
        # FINAL SCORE
        # =================================================

        final_score = (
            answer_score * 0.60
            + vision_score * 0.40
        )

         # =================================================
# SAVE INTERVIEW RESULT TO DATABASE
# =================================================

        resume_match = 0

        if "resume_skills" in st.session_state:

            required_skills = ROLE_SKILLS[role]

            match_result = match_skills(
              st.session_state.resume_skills,
              required_skills
    )

            resume_match = float(
               match_result.get("match_percentage", 0)
    )



            save_interview(
                user_id=st.session_state.user_id,
                candidate_name=name or "Candidate",
                role=role,
                experience=experience,
                difficulty=difficulty,
                answer_score=answer_score,
                vision_score=vision_score,
                ml_score=final_score,
                eye_contact=float(
                    vision.get("eye_contact", 0)
                ),
                posture=float(
                    vision.get("posture", 0)
                ),
                resume_match=resume_match
            )

        # =================================================
# ML PREDICTED INTERVIEW SCORE
# =================================================

        eye_contact_score = float(
           vision.get("eye_contact", 0)
)

        posture_score = float(
          vision.get("posture", 0)
)

# If voice analysis is available, use speech score
# Otherwise use a neutral score
        speech_score = 70.0

        if "speech_analysis" in st.session_state:

          speech_score = float(
            st.session_state["speech_analysis"].get(
               "speech_score",
                70
        )
    )

        ml_score = predict_interview_score(
           answer_quality=answer_score,
           eye_contact=eye_contact_score,
           posture=posture_score,
           speech_score=speech_score
)
        st.divider()

        st.subheader("🤖 ML Interview Prediction")

        st.metric(
            "Predicted Interview Score",
            f"{ml_score:.1f}/100"
) 
    


    # =================================================
        # FINAL INTERVIEW REPORT
        # =================================================

        st.divider()

        st.header("🏆 Final Interview Report")

        st.metric(
            "Overall Interview Score",
            f"{final_score:.1f}/100"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "📝 Answer Score",
                f"{answer_score:.1f}/100"
            )

        with col2:

            st.metric(
                "🎥 Vision Score",
                f"{vision_score:.1f}/100"
            )
            

    

        # =================================================
        # STEP 18 — ADVANCED ANALYTICS
        # =================================================

        performance = {

            "answer_quality": answer_score,

            "vision_score": vision_score,

            "eye_contact": float(
                vision.get("eye_contact", 0)
            ),

            "posture": float(
                vision.get("posture", 0)
            )
        }

        # =================================================
        # PERFORMANCE GRAPH
        # =================================================

        st.subheader("📊 Performance Overview")

        chart_data = {
            "Metric": [
                "Answer Quality",
                "Vision",
                "Eye Contact",
                "Posture"
            ],

            "Score": [
                performance["answer_quality"],
                performance["vision_score"],
                performance["eye_contact"],
                performance["posture"]
            ]
        }

        st.bar_chart(
            chart_data,
            x="Metric",
            y="Score"
        )


    
        # =================================================
        # GENERATE INTERVIEW INSIGHTS
        # =================================================

        insights = generate_insights(
            performance
        )

        # =================================================
        # STEP 19 — DOWNLOAD INTERVIEW REPORT
        # =================================================

        report_data = {
            "Candidate Name": name or "Candidate",
            "Role": role,
            "Experience": experience,
            "Difficulty": difficulty,

            "Overall Interview Score": round(
                final_score, 1
            ),

            "Answer Score": round(
                answer_score, 1
            ),

            "Vision Score": round(
                vision_score, 1
            ),

            "Eye Contact": round(
                performance["eye_contact"], 1
            ),

            "Posture": round(
                performance["posture"], 1
            ),

            "Strengths": insights.get(
                "strengths", []
            ),

            "Areas to Improve": insights.get(
                "weaknesses", []
            ),

            "Interview Insights": insights.get(
                "insights", []
            )
        }

        report_json = json.dumps(
            report_data,
            indent=4,
            ensure_ascii=False
        )

        st.subheader("📥 Download Report")

        st.download_button(
            label="📥 Download Interview Report",
            data=report_json,
            file_name="AI_Interview_Report.json",
            mime="application/json"
        )


        # =================================================
        # STEP 20.4 — PDF DOWNLOAD
        # =================================================

        pdf_file = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            "AI_Interview_Report.pdf"
        )

        create_pdf_report(
            file_path=pdf_file,
            candidate_name=name or "Candidate",
            role=role,
            experience=experience,
            difficulty=difficulty,
            final_score=final_score,
            answer_score=answer_score,
            vision_score=vision_score,
            eye_contact=performance["eye_contact"],
            posture=performance["posture"],
            strengths=insights.get("strengths", []),
            weaknesses=insights.get("weaknesses", []),
            insights=insights.get("insights", [])
        )

        with open(
            pdf_file,
            "rb"
        ) as pdf:

            pdf_data = pdf.read()

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_data,
            file_name="AI_Interview_Report.pdf",
            mime="application/pdf"
        )
        # =================================================
        # INTERVIEW INSIGHTS
        # =================================================

        st.subheader("🧠 Interview Insights")

        if insights.get("insights"):

            for insight in insights["insights"]:

                st.info(
                    f"💡 {insight}"
                )

        else:

            st.info(
                "No additional insights available."
            )

        # =================================================
        # STRENGTHS
        # =================================================

        st.subheader("💪 Strengths")

        if insights.get("strengths"):

            for strength in insights["strengths"]:

                st.success(
                    f"✓ {strength}"
                )

        else:

            st.info(
                "No major strengths detected yet."
            )

        # =================================================
        # AREAS TO IMPROVE
        # =================================================

        st.subheader("⚠️ Areas to Improve")

        if insights.get("weaknesses"):

            for weakness in insights["weaknesses"]:

                st.warning(
                    f"⚠️ {weakness}"
                )

        else:

            st.success(
                "🎉 No major improvement areas detected."
            )

        # =================================================
        # RESUME SKILL MATCH
        # =================================================

        resume_match = 0

        missing_skills = []

        if "resume_skills" in st.session_state:

            required_skills = ROLE_SKILLS[role]

            match_result = match_skills(
                st.session_state.resume_skills,
                required_skills
            )

            resume_match = float(
                match_result["match_percentage"]
            )

            missing_skills = match_result.get(
                "missing",
                []
            )

    except Exception as e:

        st.error(
            f"Could not calculate final report: {e}"
        )

        

        # =================================================
        # AI CAREER COACH
        # =================================================

        career_coaching = generate_career_coaching(

            answer_score=answer_score,

            vision_score=vision_score,

            eye_contact=float(
                vision.get("eye_contact", 0)
            ),

            posture=float(
                vision.get("posture", 0)
            ),

            resume_match=resume_match,

            role=role,

            missing_skills=missing_skills
        )

        # =================================================
        # INTERVIEW INSIGHTS
        # =================================================

        st.subheader("🧠 Interview Insights")

        if insights["insights"]:

            for insight in insights["insights"]:

                st.info(
                    f"💡 {insight}"
                )

        else:

            st.info(
                "No additional insights available."
            )

        # =================================================
        # STRENGTHS
        # =================================================

        st.subheader("💪 Strengths")

        if insights["strengths"]:

            for strength in insights["strengths"]:

                st.success(
                    f"✓ {strength}"
                )

        else:

            st.info(
                "No major strengths detected yet."
            )

        # =================================================
        # AREAS TO IMPROVE
        # =================================================

        st.subheader(
            "⚠️ Areas to Improve"
        )

        if insights["weaknesses"]:

            for weakness in insights["weaknesses"]:

                st.warning(
                    f"⚠ {weakness}"
                )

        else:

            st.success(
                "No major improvement areas detected."
            )

        # =================================================
        # AI CAREER COACH DISPLAY
        # =================================================

        st.divider()

        st.header("🤖 AI Career Coach")

        st.write(
            f"Personalized career guidance for **{role}**"
        )

        # =================================================
        # CURRENT PERFORMANCE
        # =================================================

        st.subheader("📊 Current Performance")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Answer Performance",
                f"{answer_score:.1f}/100"
            )

        with col2:

            st.metric(
                "Vision Performance",
                f"{vision_score:.1f}/100"
            )

        with col3:

            st.metric(
                "Resume Match",
                f"{resume_match:.1f}%"
            )

        # =================================================
        # PRIORITY AREAS
        # =================================================

        st.subheader("🎯 Priority Areas")

        if career_coaching["priorities"]:

            for priority in career_coaching["priorities"]:

                st.warning(
                    f"⚠️ {priority}"
                )

        else:

            st.success(
                "🎉 No major priority areas detected."
            )

        # =================================================
        # RECOMMENDED ACTIONS
        # =================================================

        st.subheader(
            "📚 Recommended Actions"
        )

        if career_coaching["recommendations"]:

            for recommendation in career_coaching["recommendations"]:

                st.info(
                    f"💡 {recommendation}"
                )

        else:

            st.info(
                "Keep practicing regularly."
            )

        # =================================================
        # SKILLS TO IMPROVE
        # =================================================

        st.subheader("🛠️ Skills to Improve")

        if missing_skills:

            for skill in missing_skills:

                st.warning(
                    f"📌 {skill}"
                )

        else:

            st.success(
                "🎉 No major skill gaps detected!"
            )

        # =================================================
        # PERSONALIZED LEARNING ROADMAP
        # =================================================

        st.subheader(
            "🗺️ Personalized Learning Roadmap"
        )

        if career_coaching["learning_plan"]:

            for index, item in enumerate(
                career_coaching["learning_plan"],
                start=1
            ):

                st.write(
                    f"**{index}.** {item}"
                )

        else:

            st.info(
                "Keep practicing regularly."
            )

    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        st.error(
            f"Could not calculate final score: {e}"
        )

        # =====================================================
# INTERVIEW HISTORY
# =======================================================


st.divider()

st.header("📚 Interview History")

history = get_interview_history(
    
    st.session_state.user_id
)


if history:

    for interview in history:

        (
            candidate_name,
            interview_role,
            experience_level,
            difficulty_level,
            answer_score_history,
            vision_score_history,
            ml_score_history,
            eye_contact_history,
            posture_history,
            resume_match_history,
            interview_date
        ) = interview

        with st.expander(
            f"🎤 {interview_role} — "
            f"{ml_score_history:.1f}/100 — "
            f"{interview_date}"
        ):

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "📝 Answer",
                    f"{answer_score_history:.1f}/100"
                )

            with col2:
                st.metric(
                    "🎥 Vision",
                    f"{vision_score_history:.1f}/100"
                )

            with col3:
                st.metric(
                    "🤖 ML Score",
                    f"{ml_score_history:.1f}/100"
                )

            st.write(
                f"**Candidate:** {candidate_name}"
            )

            st.write(
                f"**Experience:** {experience_level}"
            )

            st.write(
                f"**Difficulty:** {difficulty_level}"
            )

            st.write(
                f"**Eye Contact:** "
                f"{eye_contact_history:.1f}%"
            )

            st.write(
                f"**Posture:** "
                f"{posture_history:.1f}%"
            )

            st.write(
                f"**Resume Match:** "
                f"{resume_match_history:.1f}%"
            )

else:

    st.info(
        "No previous interviews found."
    )