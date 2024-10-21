# Job Crawler

**Job Crawler** is a web application designed to list remote job opportunities for job seekers. It allows companies to post jobs and job seekers to apply for them. Additionally, it includes admin roles for managing jobs and users. This project was built to enhance my backend engineering skills, especially in Python, Flask, and database management.

## Features

- **User Authentication**: Sign up and log in as a job seeker or company.
- **User Authorization**: Different permissions based on user roles (job seekers, companies, admins, super admins).
- **Responsive Design**: Optimized for various devices.
- **Job Listing**: Companies can post job listings.
- **Application Management**: Job seekers can apply for jobs, save listings, and manage their applications.
- **Admin Privileges**:
  - **Super Admin**: Manages users and jobs, can create and delete ordinary admins.
  - **Admins**: Can manage jobs, job seekers, and companies.

## Technologies Used

- **Frontend**: Jinja2, HTML, CSS
- **Backend**: Flask, Python
- **Database**: MongoDB using MongoEngine
- **Other Tools**: AWS, Nginx, Docker

## Installation and Setup

### Prerequisites

- **Python** (>= 3.9)
- **MongoDB**

### Step-by-Step Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/job-crawler.git
   cd job-crawler
   ```

2. **Set up environment variables**:
   - Copy the sample `.env` file and fill in the necessary variables.
   ```bash
   cp .env.sample .env
   ```

3. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the project**:
   ```bash
   python job_crawler.py
   # OR
   ./job_crawler.py
   ```

## Usage

### For Job Seekers:
- **Sign up** as a Job Seeker.
- **Log in** and set up your profile by updating your bio, skills, and uploading a resume.
- **Search for Jobs** by keywords (job title, skill, location, or description).
- **Save jobs** for later and apply to preferred jobs.
- **Manage your saved and applied jobs** on your dashboard.
- **Track your applications** through your dashboard.

### For Companies:
- **Sign up** as a Company.
- **Log in** and upload job listings.
- **Manage applications** and jobs via your company dashboard.

### For Admins:
- **Manage jobs** posted by companies and view job seeker applications.
- Super Admins can create or delete ordinary admins.

## Demo

_Demo coming soon.._

## Screenshots

![Job Listing Screenshot](path/to/job-listing-screenshot.png)
![Company Dashboard Screenshot](path/to/company-dashboard-screenshot.png)

## Future Features

- **Web scraping** of job postings from external job boards.
- **API integration** with popular job APIs for a broader selection of listings.

## License

This project is licensed under the **Apache License, Version 2.0**. You may obtain a copy of the License at:

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

## Contact

- **Email**: [daniell.olaitan@gmail.com](mailto:daniell.olaitan@gmail.com)
- **Website**: [daniell-olaitan.com](https://daniell-olaitan.com)
- **LinkedIn**: [Daniell Olaitan](https://www.linkedin.com/in/daniell-olaitan)
