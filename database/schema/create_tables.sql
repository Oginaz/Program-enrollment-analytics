CREATE DATABASE IF NOT EXISTS pwani_teknowgalz
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE pwani_teknowgalz;

-- 1. Lookup: counties
CREATE TABLE counties (
    county_id     INT AUTO_INCREMENT PRIMARY KEY,
    county_name   VARCHAR(100) NOT NULL,
    region  VARCHAR(20)  NOT NULL  
);

-- 2. Lookup: application channels
CREATE TABLE application_channels (
    channel_id    INT AUTO_INCREMENT PRIMARY KEY,
    channel_name  VARCHAR(50) NOT NULL  
);

-- 3. Lookup: exit reasons
CREATE TABLE exit_reasons (
    exit_reason_id      INT AUTO_INCREMENT PRIMARY KEY,
    reason_description  VARCHAR(150) NOT NULL,
    funnel_stage        VARCHAR(50)
);

-- 4. Catalog: resources
CREATE TABLE resources (
    resource_id        INT AUTO_INCREMENT PRIMARY KEY,
    resource_name      VARCHAR(100) NOT NULL,
    resource_category  VARCHAR(50),
    unit_cost          DECIMAL(10,2),
    descriptcion        VARCHAR(255)
);

-- 5. Programs catalog
CREATE TABLE programs (
    program_id            INT AUTO_INCREMENT PRIMARY KEY,
    program_name          VARCHAR(150) NOT NULL,
    skill_area            VARCHAR(100),
    duration_months       INT,
    delivery_mode         VARCHAR(20) DEFAULT 'physical',  
    cost_per_participant  DECIMAL(10,2)
);

-- 6. Applicants
CREATE TABLE applicants (
    applicant_id      INT AUTO_INCREMENT PRIMARY KEY,
    full_name         VARCHAR(150) NOT NULL,
    gender            VARCHAR(20) DEFAULT 'female',
    dob               DATE,
    county_id         INT,
    education_level   VARCHAR(100),
    income_level      VARCHAR(50),
    device_ownership  BOOLEAN,
    channel_id        INT,
    program_id        INT,
    registered_at     DATE,
    FOREIGN KEY (county_id)  REFERENCES counties(county_id),
    FOREIGN KEY (channel_id) REFERENCES application_channels(channel_id),
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);

-- 7. Cohorts 
CREATE TABLE cohorts (
    cohort_id       INT AUTO_INCREMENT PRIMARY KEY,
    program_id      INT NOT NULL,
    county_id       INT NOT NULL,
    cohort_name     VARCHAR(150),
    start_date      DATE,
    end_date        DATE,
    capacity        INT,
    funding_source  VARCHAR(150),
    FOREIGN KEY (program_id) REFERENCES programs(program_id),
    FOREIGN KEY (county_id)  REFERENCES counties(county_id)
);

-- 8. Applications (funnel backbone)
CREATE TABLE applications (
    application_id      INT AUTO_INCREMENT PRIMARY KEY,
    applicant_id        INT NOT NULL,
    cohort_id           INT NOT NULL,
    application_date    DATE,
    stage               VARCHAR(30),   -- applied / screened / interviewed / offered / rejected
    eligibility_status  VARCHAR(30),
    interview_result    VARCHAR(30),
    offer_status        VARCHAR(30),
    exit_reason_id      INT,
    exit_date           DATE,
    FOREIGN KEY (applicant_id)   REFERENCES applicants(applicant_id),
    FOREIGN KEY (cohort_id)      REFERENCES cohorts(cohort_id),
    FOREIGN KEY (exit_reason_id) REFERENCES exit_reasons(exit_reason_id)
);

-- 9. Enrollments (post-enrollment lifecycle)
CREATE TABLE enrollments (
    enrollment_id      INT AUTO_INCREMENT PRIMARY KEY,
    application_id     INT NOT NULL UNIQUE,
    enrollment_date    DATE,
    retained_30_day    BOOLEAN,
    retained_90_day    BOOLEAN,
    retained_180_day   BOOLEAN,
    completion_status  VARCHAR(30),
    completion_date    DATE,
    FOREIGN KEY (application_id) REFERENCES applications(application_id)
);

-- 10. Resource allocations 
CREATE TABLE resource_allocations (
    allocation_id       INT AUTO_INCREMENT PRIMARY KEY,
    cohort_id           INT NOT NULL,
    resource_id         INT NOT NULL,
    quantity_available  INT,
    quantity_needed     INT,
    allocation_date     DATE,
    FOREIGN KEY (cohort_id)   REFERENCES cohorts(cohort_id),
    FOREIGN KEY (resource_id) REFERENCES resources(resource_id)
);