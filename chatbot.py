import random
from models import db, Student

def get_response(user_input, role=None, user_id=None):
    user_input = user_input.lower().strip()
    responses = {
        "greeting": {
            "response": random.choice([
                """
                <div class="welcome-message">
                    <h3>Hello! 👋</h3>
                    <p>Welcome to <strong>ACE Engineering College</strong> Assistant. I'm here to provide all the information you need about our college in Hyderabad.</p>
                    <div class="quick-links">
                        <p>Try asking about:</p>
                        <ul>
                            <li>About ACE</li>
                            <li>Admission process</li>
                            <li>Courses offered</li>
                            <li>Fee structure</li>
                            <li>Placements</li>
                            <li>Campus facilities</li>
                            <li>Scholarships</li>
                            <li>Contact details</li>
                        </ul>
                    </div>
                </div>
                """,
                """
                <div class="welcome-message">
                    <h3>Hi there! 😊</h3>
                    <p>I'm your assistant for <strong>ACE Engineering College</strong>, Hyderabad. Ask me anything about our programs, facilities, or admissions!</p>
                </div>
                """
            ]),
            "keywords": ["hi", "hello", "hey", "greetings"]
        },
        "about": {
            "response": """
            <div class="info-card">
                <div class="info-header">
                    <i class="fas fa-university"></i>
                    <h3>About ACE Engineering College</h3>
                </div>
                <div class="info-content">
                    <p><strong>Established</strong>: 2007 by Yadala Satyanarayana Memorial Educational Society.</p>
                    <p><strong>Location</strong>: Ankushapur, Ghatkesar, Hyderabad, Telangana, on Hyderabad-Warangal National Highway (20 km from Uppal, 28 km from Secunderabad).</p>
                    <p><strong>Affiliation</strong>: Jawaharlal Nehru Technological University (JNTUH), autonomous since 2020-21.</p>
                    <p><strong>Accreditation</strong>: Approved by AICTE, accredited by NAAC-A and NBA for CE, EEE, ME, ECE, CSE.</p>
                    <p><strong>Vision</strong>: To be a leading technical institute preparing globally competent engineers with ethical values.</p>
                    <p><strong>Campus</strong>: 10-acre main campus, 2.7 acres for hostels, 4 acres for sports facilities, surrounded by lush greenery.</p>
                    <p><strong>Leadership</strong>: Guided by Prof. Y.V. Gopala Krishna Murthy, founder of ACE Engineering Academy.</p>
                    <p>Ranked 1st among top 50 engineering colleges in Telangana and 116th by TOI (2019). Known for quality education and strong placements.</p>
                    <div class="quick-links">
                        <p>Want to know more? Ask about:</p>
                        <ul>
                            <li>Courses offered</li>
                            <li>Admissions</li>
                            <li>Placements</li>
                        </ul>
                    </div>
                </div>
            </div>
            """,
            "keywords": ["about", "ace", "college", "overview", "history", "information"]
        },
        "admissions": {
            "response": """
            <div class="info-card">
                <div class="info-header">
                    <i class="fas fa-user-graduate"></i>
                    <h3>Admissions 2025</h3>
                </div>
                <div class="info-content">
                    <div class="admission-step">
                        <div class="step-number">1</div>
                        <div class="step-content">
                            <h4>Eligibility</h4>
                            <p>10+2 with 45% in Physics, Chemistry, Mathematics (PCM).</p>
                        </div>
                    </div>
                    <div class="admission-step">
                        <div class="step-number">2</div>
                        <div class="step-content">
                            <h4>Entrance Exams</h4>
                            <p>TS EAMCET or JEE Main with valid scores.</p>
                        </div>
                    </div>
                    <div class="admission-step">
                        <div class="step-number">3</div>
                        <div class="step-content">
                            <h4>Categories</h4>
                            <p><strong>Category A</strong>: Convener quota via TS EAMCET counseling.<br><strong>Category B</strong>: Management quota based on academic merit.</p>
                        </div>
                    </div>
                    <div class="admission-step">
                        <div class="step-number">4</div>
                        <div class="step-content">
                            <h4>Apply Online</h4>
                            <p>Visit <a href="https://www.aceec.ac.in" target="_blank">www.aceec.ac.in</a> for application forms.</p>
                        </div>
                    </div>
                    <div class="admission-step">
                        <div class="step-number">5</div>
                        <div class="step-content">
                            <h4>Key Dates</h4>
                            <p>Application Deadline: August 15, 2025 (tentative).<br>Counseling: August 20-30, 2025 (tentative).</p>
                        </div>
                    </div>
                    <div class="contact-box">
                        <p><i class="fas fa-phone-alt"></i> +91-8712225044</p>
                        <p><i class="fas fa-envelope"></i> admissions@aceec.ac.in</p>
                    </div>
                    <div class="quick-links">
                        <p>Related queries:</p>
                        <ul>
                            <li>Fee structure</li>
                            <li>Scholarships</li>
                            <li>Courses offered</li>
                        </ul>
                    </div>
                </div>
            </div>
            """,
            "keywords": ["admission", "admissions", "process", "apply", "eligibility", "entrance", "how to join"]
        },
        "courses": {
            "response": """
            <div class="info-card">
                <div class="info-header">
                    <i class="fas fa-graduation-cap"></i>
                    <h3>Courses Offered</h3>
                </div>
                <div class="dept-grid">
                    <div class="dept-card" style="border-color: #4361ee;">
                        <h4><i class="fas fa-laptop-code"></i> CSE (Computer Science)</h4>
                        <p>420 seats | NBA accredited</p>
                    </div>
                    <div class="dept-card" style="border-color: #4361ee;">
                        <h4><i class="fas fa-robot"></i> CSE (AI & ML)</h4>
                        <p>180 seats | 4 labs</p>
                    </div>
                    <div class="dept-card" style="border-color: #4361ee;">
                        <h4><i class="fas fa-database"></i> CSE (Data Science)</h4>
                        <p>60 seats | Industry-focused</p>
                    </div>
                    <div class="dept-card" style="border-color: #4361ee;">
                        <h4><i class="fas fa-network-wired"></i> CSE (IoT)</h4>
                        <p>60 seats | Emerging tech</p>
                    </div>
                    <div class="dept-card" style="border-color: #7209b7;">
                        <h4><i class="fas fa-microchip"></i> ECE</h4>
                        <p>120 seats | 3 labs | NBA accredited</p>
                    </div>
                    <div class="dept-card" style="border-color: #4cc9f0;">
                        <h4><i class="fas fa-building"></i> Civil Engineering</h4>
                        <p>60 seats | 2 labs | NBA accredited</p>
                    </div>
                    <div class="dept-card" style="border-color: #f72585;">
                        <h4><i class="fas fa-cogs"></i> Mechanical Engineering</h4>
                        <p>120 seats | 5 labs | NBA accredited</p>
                    </div>
                    <div class="dept-card" style="border-color: #ffba08;">
                        <h4><i class="fas fa-bolt"></i> EEE</h4>
                        <p>30 seats | NBA accredited</p>
                    </div>
                    <div class="dept-card" style="border-color: #06d6a0;">
                        <h4><i class="fas fa-code"></i> Information Technology</h4>
                        <p>60 seats | Modern IT labs</p>
                    </div>
                </div>
                <p><strong>Duration</strong>: 4 years | Affiliated with JNTUH</p>
                <p><strong>Add-ons</strong>: Data Analytics, Line Apps Development.</p>
                <div class="quick-links">
                    <p>Explore more:</p>
                    <ul>
                        <li>Admissions</li>
                        <li>Fees</li>
                        <li>Faculty</li>
                    </ul>
                </div>
            </div>
            """,
            "keywords": ["department", "departments", "courses", "programs", "btech", "branches", "specializations"]
        },
        "fees": {
            "response": """
            <div class="info-card">
                <h3>Fee Structure (2025-26)</h3>
                <div class="fee-structure">
                    <div class="fee-card">
                        <h4>B.Tech (Convener Quota)</h4>
                        <div class="fee-amount">₹1,20,000</div>
                        <p>per year (~₹4.8 lakh total)</p>
                    </div>
                    <div class="fee-card">
                        <h4>B.Tech (Management Quota)</h4>
                        <div class="fee-amount">₹1,50,000</div>
                        <p>per year</p>
                    </div>
                    <div class="fee-card">
                        <h4>Hostel</h4>
                        <div class="fee-amount">₹60,000</div>
                        <p>per year</p>
                    </div>
                    <div class="fee-card">
                        <h4>Transport</h4>
                        <div class="fee-amount">₹25,000</div>
                        <p>per year</p>
                    </div>
                </div>
                <p><strong>Note</strong>: Fees vary by quota. Scholarships available for TS EAMCET rank holders.</p>
                <div class="quick-links">
                    <p>Related queries:</p>
                    <ul>
                        <li>Scholarships</li>
                        <li>My fees (student login required)</li>
                        <li>Admissions</li>
                    </ul>
                </div>
            </div>
            """,
            "keywords": ["fee", "fees", "cost", "tuition", "structure"]
        },
        "placements": {
            "response": """
            <div class="info-card">
                <h3>Placements 2025</h3>
                <div class="placement-stats">
                    <div class="stat-card">
                        <h4>Highest Package</h4>
                        <p>₹16 LPA</p>
                    </div>
                    <div class="stat-card">
                        <h4>Average Package</h4>
                        <p>₹4.5 LPA</p>
                    </div>
                    <div class="stat-card">
                        <h4>Placement Rate</h4>
                        <p>85%</p>
                    </div>
                </div>
                <div class="recruiters">
                    <h4>Top Recruiters</h4>
                    <div class="recruiter-logos">
                        <img src="/static/images/tcs.png" alt="TCS">
                        <img src="/static/images/infosys.png" alt="Infosys">
                        <img src="/static/images/wipro.png" alt="Wipro">
                        <img src="/static/images/cisco.png" alt="Cisco">
                    </div>
                </div>
                <p><strong>Training</strong>: Microsoft Innovation Centre, TCS Ion, Talent Sprint.</p>
                <div class="quick-links">
                    <p>Explore more:</p>
                    <ul>
                        <li>Courses</li>
                        <li>Faculty</li>
                        <li>Campus facilities</li>
                    </ul>
                </div>
            </div>
            """,
            "keywords": ["placement", "placements", "jobs", "recruiters", "package", "training"]
        },
        "my fees": {
            "response": lambda: get_my_fees(user_id),
            "keywords": ["my fees", "my balance", "fee status"],
            "role": "student"
        },
        "facilities": {
            "response": """
            <div class="info-card">
                <h3>Campus Facilities</h3>
                <div class="facility-grid">
                    <div class="facility-card">
                        <i class="fas fa-book"></i>
                        <h4>Library</h4>
                        <p>42,800 books, 108 journals, digital library with IEEE access.</p>
                    </div>
                    <div class="facility-card">
                        <i class="fas fa-laptop"></i>
                        <h4>Labs</h4>
                        <p>State-of-the-art labs for all disciplines, Wi-Fi enabled.</p>
                    </div>
                    <div class="facility-card">
                        <i class="fas fa-home"></i>
                        <h4>Hostels</h4>
                        <p>Separate for boys and girls, 2.7-acre facility.</p>
                    </div>
                    <div class="facility-card">
                        <i class="fas fa-futbol"></i>
                        <h4>Sports</h4>
                        <p>4-acre sports ground, gym, and recreational areas.</p>
                    </div>
                    <div class="facility-card">
                        <i class="fas fa-utensils"></i>
                        <h4>Canteen</h4>
                        <p>Hygienic, vegetarian food.</p>
                    </div>
                    <div class="facility-card">
                        <i class="fas fa-bus"></i>
                        <h4>Transport</h4>
                        <p>Buses from all parts of Hyderabad.</p>
                    </div>
                    <div class="facility-card">
                        <i class="fas fa-building"></i>
                        <h4>Auditorium</h4>
                        <p>State-of-the-art facility for events and seminars.</p>
                    </div>
                </div>
                <p><strong>Other</strong>: Wi-Fi campus, CCTV, seminar halls (500+ seats), water treatment plant.</p>
                <div class="quick-links">
                    <p>Explore more:</p>
                    <ul>
                        <li>Hostels</li>
                        <li>Campus life</li>
                        <li>Fees</li>
                    </ul>
                </div>
            </div>
            """,
            "keywords": ["facilities", "campus", "infrastructure", "hostel", "library", "sports", "labs"]
        },
        "scholarships": {
            "response": """
            <div class="info-card">
                <h3>Scholarships</h3>
                <div class="info-content">
                    <p><strong>Merit-Based</strong>: 50%-100% tuition fee waiver based on TS EAMCET rank.</p>
                    <p><strong>Fee Reimbursement</strong>: ₹35,000/year for eligible students (economically weaker sections).</p>
                    <p><strong>Additional</strong>: 40%-100% concession on hostel/transport fees, free GATE coaching for ranks 1500-20,000.</p>
                    <p><strong>Eligibility</strong>: Contact the financial aid office for criteria and application.</p>
                    <div class="contact-box">
                        <p><i class="fas fa-phone-alt"></i> +91-9133308460</p>
                        <p><i class="fas fa-envelope"></i> deanadmin@aceec.ac.in</p>
                    </div>
                    <div class="quick-links">
                        <p>Related queries:</p>
                        <ul>
                            <li>Fees</li>
                            <li>Admissions</li>
                            <li>My fees (student login)</li>
                        </ul>
                    </div>
                </div>
            </div>
            """,
            "keywords": ["scholarship", "financial aid", "merit", "reimbursement"]
        },
        "faculty": {
            "response": """
            <div class="info-card">
                <h3>Faculty</h3>
                <div class="info-content">
                    <p><strong>Qualifications</strong>: Most faculty hold M.Tech. or Ph.D. degrees from reputed institutions.</p>
                    <p><strong>Experience</strong>: Dedicated professors with industry and research expertise.</p>
                    <p><strong>Guest Lecturers</strong>: Regular sessions by industry experts for career insights.</p>
                    <p><strong>Key Faculty</strong>:</p>
                    <ul>
                        <li>Dr. Khaleel Ur Rahman Khan (Dean, CSE)</li>
                        <li>Mrs. K. Sravani (Asst. Prof., IT)</li>
                    </ul>
                    <p><strong>Approach</strong>: Focus on real-time case studies, practical learning, and mentorship.</p>
                    <div class="quick-links">
                        <p>Explore more:</p>
                        <ul>
                            <li>Courses</li>
                            <li>Placements</li>
                            <li>Campus life</li>
                        </ul>
                    </div>
                </div>
            </div>
            """,
            "keywords": ["faculty", "professors", "teachers", "staff"]
        },
        "campus_life": {
            "response": """
            <div class="info-card">
                <h3>Campus Life</h3>
                <div class="info-content">
                    <p><strong>Student Clubs</strong>: SAE India, NSS, tech societies, and cultural groups.</p>
                    <p><strong>Events</strong>: ENLITE (tech fest), sports tournaments, cultural programs.</p>
                    <p><strong>Skill Development</strong>: Workshops, seminars, and industry certifications.</p>
                    <p><strong>Community</strong>: Vibrant, inclusive environment with peer counseling.</p>
                    <p><strong>Recreation</strong>: Green lawns, sports facilities, and relaxation areas.</p>
                    <div class="quick-links">
                        <p>Explore more:</p>
                        <ul>
                            <li>Facilities</li>
                            <li>Student clubs</li>
                            <li>Events</li>
                        </ul>
                    </div>
                </div>
            </div>
            """,
            "keywords": ["campus life", "student life", "clubs", "events", "activities"]
        },
        "contact": {
            "response": """
            <div class="info-card">
                <h3>Contact Details</h3>
                <div class="info-content">
                    <p><strong>Address</strong>: Ankushapur, Ghatkesar Mandal, Medchal District, Telangana - 501 301.</p>
                    <p><strong>Admissions</strong>: +91-8712225044 | admissions@aceec.ac.in</p>
                    <p><strong>Administration</strong>: +91-9133308460 | deanadmin@aceec.ac.in</p>
                    <p><strong>Principal</strong>: +91-9490941200 | principal@aceec.ac.in</p>
                    <p><strong>Website</strong>: <a href="https://www.aceec.ac.in" target="_blank">www.aceec.ac.in</a></p>
                    <p><strong>Location</strong>: 1.3 km from Ankushapur Bus Stop, 6.9 km from Ghatkesar Railway Station, 58.6 km from Rajiv Gandhi International Airport.</p>
                    <div class="quick-links">
                        <p>Explore more:</p>
                        <ul>
                            <li>About</li>
                            <li>Admissions</li>
                            <li>Facilities</li>
                        </ul>
                    </div>
                </div>
            </div>
            """,
            "keywords": ["contact", "address", "phone", "email", "location"]
        },
        "thanks": {
            "response": random.choice([
                """
                <div class="thanks-message">
                    <h3>You're welcome! 😊</h3>
                    <p>Happy to help with <strong>ACE Engineering College</strong> info. Ask more about courses, campus, or anything else!</p>
                </div>
                """,
                """
                <div class="thanks-message">
                    <h3>Glad I could assist! 😄</h3>
                    <p>Feel free to explore more about <strong>ACE Engineering College</strong>.</p>
                </div>
                """
            ]),
            "keywords": ["thank", "thanks", "thank you"]
        }
    }

    def get_my_fees(user_id):
        if user_id is None:
            return """
            <div class="error-message">
                <h3>Oops!</h3>
                <p>Please log in as a student to view your fee status.</p>
            </div>
            """
        student = Student.query.filter_by(user_id=user_id).first()
        if not student:
            return """
            <div class="error-message">
                <h3>Error!</h3>
                <p>No student record found. Contact support.</p>
            </div>
            """
        return """
        <div class="info-card">
            <h3>Your Fee Status</h3>
            <p><strong>Roll No</strong>: {student.roll_no}</p>
            <p><strong>Balance</strong>: ₹{student.balance}</p>
            <p>Check your dashboard for payment options or contact <a href="mailto:support@aceec.ac.in">support@aceec.ac.in</a>.</p>
        </div>
        """.format(student=student)

    for key, data in responses.items():
        if any(keyword in user_input for keyword in data['keywords']):
            if 'role' in data and role != data['role']:
                return """
                <div class="error-message">
                    <h3>Oops!</h3>
                    <p>This query is only available for {}s. Please log in with the appropriate account.</p>
                </div>
                """.format(data['role'])
            response = data['response']
            if isinstance(response, str):
                return response
            else:
                return response()

    return """
    <div class="error-message">
        <h3>Sorry, I didn't understand that.</h3>
        <p>Try asking about ACE College, admissions, fees, placements, or facilities. For example, say 'about ACE' or 'fee structure'.</p>
        <div class="quick-links">
            <p>Suggestions:</p>
            <ul>
                <li>About College</li>
                <li>Admissions</li>
                <li>Courses</li>
                <li>Fees</li>
                <li>Placements</li>
            </ul>
        </div>
    </div>
    """