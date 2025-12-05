# com7033-assignment-ituaehishenry
com7033-assignment-ituaehishenry created by GitHub Classroom 
My first assigment
System Planning, Architecture and Security Design of Stroke Management and Prediction Web Application Software

Goal: A web application design with the awareness of security and GDPR compliance to collect and manage data of stroke patients, provide clinician access and model-based risk of stroke predictions. The design is based on a defence-in-depth, zero-trust, and secure software best practices.

Note that there will be no prediction features built into this web application in the first instance. However, this will be a feature in the near future, and we will launch it into the cloud environment. 


Tabular explanation of users of the app.


Stakeholder	Responsibility	Data Managed/Accessed	Data/Information Sensitivity Intensity	Justification





Patient	Records and observes the health system of measurement, including sleep, calories, heart rate, and steps. This data can be shared with their GP.	


Personal information (name, 
email), consent preferences, health metrics	



Special Category	Data relating to health is qualified as a special category and needs enhanced protection under GDPR Article 9  
(European Union, 2016)


General Practitioner	Reviews information or data provided by the patient based on the patient's consent for treatment recommendations and advice	


Identifiers and health metrics shared by the patient	


Special Category	Accessing health-related data requires compliance with GDPR principles of confidentiality and integrity.


Developer	Designs, develops, deploys, and maintains the Health Track Application for patients.	

Anonymised test data, application code, bug, and reports	


Internal	They are not to access real user data in production. They should use anonymised datasets for testing and debugging.
System Administrator	
They manage user accounts, data back-ups, and updates.	
User credentials, access logs, and system configurations	
Confidential	They handle sensitive information, requiring strict authentication and debugging.
Data Protection Officer (DPO)	Ensures GDPR compliance and adherence, checks data and information handling, and assesses security practices.	


Data flow documentation, consent logs, and incident reports	



Confidential	They oversee data processing and breach reporting under GDPR Article 32 (European Union, 2016)
Database Administrator (DBA)	Preserves, secures databases, and enforces encryption and access control instruments.	
Encrypted health and personal data, system logs	
Confidential/ special Category	In charge of making sure data is encrypted both at rest and in transit using secure cryptographic protocols

The app development focuses on 3 main users – Clinicians, that is, medical practitioners. The administrative staff, which includes other users not mentioned, can be embedded within the patients. In the web application, clinicians and administrative staff have access to the admin dashboard and the login credentials for the admin dashboard.  They also have access to the record of the users(clients), while the client only has access to their own individual record.


Functional Requirements

Type 	Requirement Description	Implementation/Example
Functional Requirement 1	The system should allow authorised or required users to register and create a personal account	The registration form collects name, email and password; it validates input before account creation.
Functional Requirement 2	The system should be planned to allow users to log in and access a dashboard that is personal to them.	Authentication uses email and password via a secure HTTPS connection.
Functional Requirement 3	The system should record and store users’ daily data details	Mobile sensors synchronise data information to the cloud through the REST API.
Functional Requirement 4	The system shall allow users to share health information with clinicians upon explicit consent.	Permission management system logs data-sharing preferences and timestamps.
Functional Requirement 5	The system is designed to allow users to reset their passwords in a secure manner	The email reset link expires after some minutes – between 15 – 20 minutes.
Functional Requirement 6	Clinicians Portal Access	The system allows registered clinicians to securely access shared patient data through a dedicated web portal using role-based authentication.
Functional Requirement 7	Alerts and Notifications	The system notifies users via email or app alert regarding significant health trends, system updates, or data-sharing activities
Functional Requirement 8	Visualisation and Health Information	The system shall present recorded health data to users in an easy-to-read dashboard using charts and summaries of progress over time, with easy comprehension.
Functional Requirement 9	Data Export and Download	The software app shall allow users to export their health information/data in a standard file format.


Use Case
Use Case ID	Description	Actors	Preconditions	Outcome
User1 - UC1i	User registers a new account.
	End User	User provides valid details.	Account created and confirmation sent.
User1 - UC1ii	User logs into their account.	End User	User has already registered.	Secure session initiated.
User 2 - UC2i	User shares health data with GP.	End User       GP	User grants consent.	GP gains access to shared metrics.
User 2 - UC2ii	GP reviews patient data.	GP	GP authenticated via MFA to be sure that it is a registered and authorised medical professional.	GP views shared records only and gives advice based on the shared information.








Security Requirements:
Integrating security software into the software development process is fundamental to protecting from vulnerabilities and flaws (Manal J., Maha A., Dr. Onytra A. 2024).

Type	Requirement Description	Implementation/example
Security Requirement 1	All passwords are required to be stored using a salted SHA-256 hash	This aligns with the OWASP Password Storage Guidelines.
Security Requirement 2	All communications between clients and server shall be encrypted using TLS 1.3.	Ensures confidentiality and integrity of data in transit
Security Requirement 3	The system is designed to adopt and implement MFA for clinicians and administrative logins.	Ensuring a time-based one-time password and authentication for well-secured data
Security Requirement 4	Requires that sensitive health data information be encrypted at rest using AES.	In compliance with GDPR. Security of Processing 
Security Requirement 5	The system is designed to maintain audit logs of all data information entry and distribute events.	Ensure the logs record the timestamp, user ID, and action type for non-repudiation.
Security Requirement 6	The system shall enforce Role-Based Access Control to limit data visibility	There should be distinct responsibilities for the end user, GP, DPO, and administrator.


System Architecture and Secure Design

The 7 Threat Modelling (STRIDE) is adopted, where key possible threats and mitigations are identified in the table below.

STRIDE	Possible Threat	Adopted Mitigations
Spoofing	An attacker steals credentials and uses them to access the web app.	Strong Password, account lockout, Multi-Factor Authenticator (MFA) for admin, and per-request token validation (JWT signed)
Tampering	Patient data or prediction is modified.	Input validation, database integrity checks, Parameterised queries, and Hash-Based Message Authentication Code (HMAC) for audit entries
Repudiation	When a user denies the request for the prediction/deletion of a record	Adopting an immutable audit log with signed-in entries, Hardware Security Module HSM or Key Management Service (KMS)
Information Disclosure	Breach of Data	Transport Layer standard 1.3 (TLS 1.3) or other level of layers for data in transit, Advanced Encryption Standard (AES-256) for data at rest, encryption for Personal Identifiable Information (PII), field level, and least privilege database roles
Denial of Service	Flood prediction endpoint	Web Application Firewall (WAF), rate limiting at API, and circuit breakers
Elevation of Privilege	When a regular user carried out admin actions	Step-up MFA + RBAC + secure objects ACLs





                                                        Structure of Threat Modelling

 
Figure 1

Source: Author’s own
                    


                                           Data Flow Diagram (DFD)

 Figure 2

Source: Author’s own




Trust Boundaries

1.	Client Access – edging the internet: Strict CORS, TLS 1.3 + HSTS.
2.	Edging the backend – WAF, API Gateway Validation, TLS, and Least-privilege DB accounts.
The images used in the web application were generated through brainstorming with ChatGPT (OpenAI, 2025)


                    

Flows Explanation

1.	Patients register or login as an existing client via the browser (frontend) and use the API Gateway. Patient is authenticated. Security – multi-factor authentication (MFA), Parameterised Queries, HTTPS, TLS 1.3, etc for data in transit, etc.

2.	 Clinicians/Amin login as an already existing client via the browser (frontend) and use the API Gateway. Patient is authenticated. Security – Multi-factor authentication (MFA), RBAC, TLS 1.3 for data in transit, etc.

3.	Browse: Patience wants to get access to the database through the server– API Gateway. Security: RBAC, TLS, CORS restricted access to frontend.

4.	Create, Read, Update and Delete (CRUD): browsing through the API patient service to the database, writing immutable Audit/logs to the database. Security: Parameterised queries, RBAC, etc. for authentication and authorisation


5.	Update from admin via admin portal- ensure audit/logs. Security, immutable logging, MFA setup, modification of approval workflows, and least privilege.

6.	Prediction: Browser via the API Gateway to the object store and return score to store the result. Security: AES 256 for data at rest, Audit trail, Input validation, and model version logging.

Security features implemented:
•	Secured Password hashing
•	Session Management
•	Input validation
•	Authentication and authorisation
•	SQL injection
•	Environmental variables for sensitive data dotenv
•	Secure MongoDB Connection
•	Amin user creation and user creation -RBAC
•	 Cross-Site Request Forgery attacks (CSRF)


DATABASE DESIGN

•	MongoDB:
1.	It used to manage all patient records
2.	Flexibility and Scalability for handling structured and unstructured data


•	SQLite:
1.	Managing small-scale users' data
2.	Users' authentication details database



 PROFESSIONAL AND ETHICAL PRACTICES

Professional Practices:
•	Clean Code Adherence
1.	Inline documentation and consistent naming conventions
2.	Modular design for scalability and maintainability


Ethical Considerations:
•	Data Privacy:
1.	Security handling of data and storage of sensitive patient information.
2.	Compliance with data privacy and data protection standards (GDPR)
 
Transparency:

1.	Clarity in users' communication regarding usage policies.
Testing and Quality Assurance:
•	Unit and Integration testing were implemented for system reliability
 



 



References:

•	Murugiah, S., Karen s., & Donna D. (2022). Secure Software Development Framework (SSDF) Version 1.1: Recommendations for Mitigating the Risk of Software Vulnerabilities. National Institute of Standards and Technology (NIST). Special Publication 800-218 Natl. Inst. Stand. Technol. Spec. Publ. 800-218, 36 pages (February 2022). https://doi.org/10.6028/NIST.SP.800-218
•	Manal J., Maha A., Dr. Onytra A. (2024). Secure Software Development: Problems and Solutions. International Journal of Intelligent Systems and Applications in Engineering. IJISAE, 2024, 12(4), 4769 - 4776 |4770
•	 OWASP Secure-By-Design Framework Draft Version 0.5.0 – Initial Community Review (August 2025)  OWASP Secure by Design Framework | OWASP Foundation
•	OpenAI. (2025). ChatGPT (GPT-5.1) [Large language model]. https//chat.openai.com






