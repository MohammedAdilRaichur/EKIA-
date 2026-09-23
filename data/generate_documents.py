import os
from fpdf import FPDF

# Ensure directories exist
base_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(base_dir, "documents")
departments = ["HR", "IT", "Finance", "Engineering", "Company"]

for dept in departments:
    os.makedirs(os.path.join(docs_dir, dept), exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'NovaTech Solutions Enterprise Knowledge', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def create_pdf(department, filename, title, sections):
    pdf = PDF()
    pdf.add_page()
    pdf.set_title(title)
    
    # Metadata as text for RAG (normally we'd use actual PDF metadata, but this is simpler for MVP)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, f"Document: {title} | Department: {department} | Classification: Internal", 0, 1)
    pdf.ln(5)
    
    for section_title, content in sections.items():
        pdf.chapter_title(section_title)
        pdf.chapter_body(content)
        
    filepath = os.path.join(docs_dir, department, filename)
    pdf.output(filepath, 'F')
    print(f"Generated: {filepath}")

# --- HR Documents ---
create_pdf("HR", "employee_handbook.pdf", "Employee Handbook", {
    "1. Introduction": "Welcome to NovaTech Solutions. Our core values include innovation, integrity, and collaboration.",
    "2. Working Hours": "Standard working hours are from 9:00 AM to 5:00 PM, Monday to Friday.",
    "3. Code of Conduct": "All employees are expected to treat colleagues with respect and adhere to our zero-tolerance policy for harassment."
})

create_pdf("HR", "leave_policy.pdf", "Leave Policy", {
    "1. Annual Leave": "Employees are entitled to 20 days of paid annual leave per calendar year. Up to 5 days can be carried over to the next year.",
    "2. Sick Leave": "Employees receive 10 days of paid sick leave. Medical certificates are required for sick leave exceeding 3 consecutive days.",
    "3. Parental Leave": "NovaTech offers 16 weeks of fully paid parental leave for primary caregivers and 6 weeks for secondary caregivers."
})

create_pdf("HR", "remote_work_policy.pdf", "Remote Work Policy", {
    "1. Eligibility": "Employees may work remotely under the conditions specified by their department manager. Generally, up to 2 days a week is permitted.",
    "2. Core Hours": "When working remotely, employees must be online and available during core hours (10:00 AM to 3:00 PM).",
    "3. Equipment": "NovaTech provides a standard work laptop. Additional remote equipment is subject to department budget."
})

create_pdf("HR", "benefits_policy.pdf", "Benefits Policy", {
    "1. Health Insurance": "Comprehensive health insurance is provided through NovaHealth Partners for all full-time employees.",
    "2. Retirement": "NovaTech matches up to 5% of employee contributions to their 401k or equivalent retirement plan.",
    "3. Wellness": "Employees receive a wellness stipend of Rs. 2,500 per month for gym memberships or mental health apps."
})

# --- IT Documents ---
create_pdf("IT", "password_policy.pdf", "Password Policy", {
    "1. Complexity": "Passwords must be at least 14 characters long and include uppercase, lowercase, numbers, and special characters.",
    "2. Rotation": "Passwords must be changed every 90 days. You cannot reuse any of your last 5 passwords.",
    "3. MFA": "Multi-Factor Authentication (MFA) is mandatory for all enterprise applications."
})

create_pdf("IT", "vpn_guide.pdf", "VPN Guide", {
    "1. Installation": "Download the NovaTech Cisco AnyConnect client from the IT self-service portal.",
    "2. Connection": "Connect using your SSO credentials and approve the push notification on your mobile device.",
    "3. Troubleshooting": "If the VPN disconnects, restart your machine. If the issue persists, contact IT Support at extension 4004."
})

create_pdf("IT", "device_security.pdf", "Device Security Policy", {
    "1. Disk Encryption": "All company-issued laptops must have full disk encryption (FileVault for Mac, BitLocker for Windows) enabled at all times.",
    "2. Lost Devices": "If your company laptop is compromised or lost, you must immediately report it to the IT Security Operations Center (SOC) at security@novatech.com.",
    "3. Unauthorized Software": "Employees are strictly prohibited from installing unapproved software on company devices."
})

create_pdf("IT", "incident_response.pdf", "Incident Response", {
    "1. Definition": "A security incident includes unauthorized access, data breaches, or malware infections.",
    "2. Reporting": "Report incidents to the IT Helpdesk immediately. Do not attempt to investigate the issue yourself.",
    "3. Containment": "If you suspect malware, disconnect the device from the network but DO NOT power it off."
})

# --- Finance Documents ---
create_pdf("Finance", "travel_policy.pdf", "Travel Policy", {
    "1. Approval": "All business travel must be approved by a department manager at least 14 days in advance.",
    "2. Flights": "Employees must book economy class for flights under 6 hours. Business class is allowed for flights exceeding 6 hours.",
    "3. Accommodation": "The accommodation limit is Rs. 4,000 per day. For international travel, the limit varies by city tier."
})

create_pdf("Finance", "reimbursement_policy.pdf", "Reimbursement Policy", {
    "1. Submission": "Expense claims must be submitted within 30 days of incurring the expense through the Expensify portal.",
    "2. Documentation": "Employees must provide original receipts, hotel invoices, proof of payment, and an approved travel request for any claim exceeding Rs. 500.",
    "3. Processing": "Approved reimbursements are processed on the 15th and 30th of each month."
})

create_pdf("Finance", "expense_policy.pdf", "Expense Policy", {
    "1. Meals": "The daily meal allowance during business travel is Rs. 1,500.",
    "2. Non-Reimbursable": "Alcohol, personal entertainment, and traffic fines are strictly non-reimbursable.",
    "3. Client Entertainment": "Client dinners require prior VP approval and are capped at Rs. 3,000 per head."
})

# --- Engineering Documents ---
create_pdf("Engineering", "coding_standards.pdf", "Coding Standards", {
    "1. Formatting": "We use Black for Python code formatting and Prettier for JavaScript. Maximum line length is 100 characters.",
    "2. Code Reviews": "All pull requests require at least two approvals from senior engineers before merging to the main branch.",
    "3. Testing": "New features must include unit tests with a minimum code coverage of 80%."
})

create_pdf("Engineering", "git_guidelines.pdf", "Git Guidelines", {
    "1. Branching": "Use the feature branch workflow (e.g., feature/JIRA-123-add-login). Never commit directly to main.",
    "2. Commits": "Commit messages must follow the Conventional Commits specification (e.g., feat: add login endpoint).",
    "3. Rebasing": "Always rebase against main before creating a pull request to maintain a clean history."
})

create_pdf("Engineering", "deployment_guide.pdf", "Deployment Guide", {
    "1. Payment Service": "The deployment procedure for the payment service requires running the database migration script first, followed by the Kubernetes rolling update.",
    "2. CI/CD": "Deployments to production are fully automated via GitHub Actions upon tagging a release.",
    "3. Rollback": "To rollback, trigger the 'Revert Deployment' action in GitHub and select the previous stable tag."
})

create_pdf("Engineering", "incident_management.pdf", "Incident Management", {
    "1. Severity Levels": "SEV-1 (Critical System Outage), SEV-2 (Major Feature Broken), SEV-3 (Minor Bug).",
    "2. On-Call": "The on-call engineer must acknowledge PagerDuty alerts within 5 minutes for SEV-1 incidents.",
    "3. Post-Mortem": "A blameless post-mortem document must be completed within 48 hours of resolving any SEV-1 or SEV-2 incident."
})

# --- Company Documents ---
create_pdf("Company", "company_handbook.pdf", "Company Handbook", {
    "1. Mission": "NovaTech Solutions aims to build scalable, AI-driven enterprise software that empowers businesses worldwide.",
    "2. History": "Founded in 2018, NovaTech has grown from a 5-person startup to a global team of over 500 professionals.",
    "3. Culture": "We believe in transparency, continuous learning, and fostering a diverse and inclusive workplace."
})

create_pdf("Company", "organizational_structure.pdf", "Organizational Structure", {
    "1. Executive Team": "The CEO is Jane Doe, CTO is John Smith, and CFO is Alice Johnson.",
    "2. Departments": "NovaTech is organized into Engineering, Product, Sales, Marketing, Finance, HR, and IT.",
    "3. Reporting": "We operate in a matrix structure. Project managers handle delivery, while engineering managers handle people growth."
})

create_pdf("Company", "communication_policy.pdf", "Communication Policy", {
    "1. Slack": "Slack is used for day-to-day informal communication. Use public channels over direct messages when possible.",
    "2. Email": "Email is reserved for formal announcements, client communication, and HR updates.",
    "3. Meetings": "Always include an agenda in meeting invites. If a meeting can be an email or Slack thread, cancel it."
})

print("All documents generated successfully.")
