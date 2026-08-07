# Project Brief

*This document explains what the project is, why it exists, how we solve the problem, and what success looks like.*

## Contents

1. Project Overview
2. Executive Summary
3. Background
4. Business Problem
5. Project Objectives
6. Project Scope
7. Stakeholders
8. Business Questions
9. Success Metrics
10. Deliverables
11. Assumptions/Risks
12. Timeline
13. Team Roles

---

## 1. Project Overview

| | |
|---|---|
| **Project Title** | Program Enrollment Analytics |
| **Organization** | Pwani Teknowgalz |
| **Team Members** | Sammy Shoka & Sunday Layefa |
| **Date** | 04/08/2026 |

## 2. Executive Summary

**The organization's challenge**

The organization experiences a significant gap between the number of applicants and the number of applicants who successfully enroll in its programs. Despite receiving considerable interest, only approximately **15% of applicants complete the enrollment process**, falling well short of the organization's target of **50% enrollment**. Limited visibility into the applicant journey, resource constraints, and fragmented reporting make it difficult to identify bottlenecks, understand the causes of applicant drop-off, and implement targeted interventions that improve enrollment outcomes.

**Proposed analytics solution:**

- Design a relational database schema covering applicants, programs, counties, cohorts, application stages, and resource constraints.
- Generate a realistic synthetic dataset calibrated to the funnel numbers in the brief (20,000+ applications → 12,000 qualifying → 6,000 interviewed → 3,000 enrolled), with reasonable variation by county, age group, and program.
- Clean and validate the dataset, then perform EDA to identify where and why drop-off happens, and which segments (county/age/program) are underrepresented relative to the applicant pool.
- Build an interactive dashboard tracking the funnel, KPIs, and progress toward the 50%-reach goal.

## 3. Background

**What the organization does**

The organization is a registered technology-focused non-governmental organization (NGO) committed to equipping girls and young women aged **15 to 28** from marginalized communities across Kenya's coastal region with market-relevant digital and technology skills. Through its training programs, the organization seeks to improve participants' employability, foster economic independence, and increase their participation in the growing digital economy by providing sustainable pathways to livelihood and career opportunities.

**Their mission:**

To equip young Kenyan women in marginalized communities with employable technology skills, with the aim of empowering them to have a financially stable future and contribute to the digital economy.

## 4. Business Problem

**Current pain points:**

The organization receives a substantial number of applications for its programs, but only a small proportion of applicants successfully progress through the entire enrollment process. Although there is strong interest in the programs, the organization lacks visibility into where applicants disengage, why they fail to complete the process, and which operational factors contribute to low enrollment. This makes it difficult to identify bottlenecks, allocate resources effectively, and implement targeted interventions that improve enrollment outcomes.

**Why the problem matters:**

Low enrollment limits the organization's ability to fulfill its mission of reaching and supporting more beneficiaries. Without clear insights into the applicant journey, leadership cannot make evidence-based decisions to improve conversion rates, justify funding requests, or optimize the use of available resources. Improving enrollment performance is therefore essential to increasing program impact, operational efficiency, and accountability.

**Strategic impact:**

- Reduced ability to achieve the target enrollment rate of 50%.
- Lower overall program reach and social impact.
- Difficulty demonstrating measurable outcomes to donors and funding partners.
- Reduced confidence in strategic planning due to limited data-driven insights.
- Missed opportunities to optimize program expansion and resource investment.
- Limited evidence to support future funding proposals and organizational growth.

## 5. Project Objectives

**Specific Objectives**

1. Analyze applicant funnel
2. Identify bottlenecks
3. Evaluate resource allocation
4. Improve enrollment visibility
5. Support decision making

## 6. Project Scope

**In Scope**

1. Database Design
2. Synthetic Dataset
3. SQL Database
4. Power BI Dashboard
5. KPI Development

**Out of Scope**

1. Live production system
2. Real-time integration

## 7. Stakeholders

| Internal | External |
|---|---|
| Executive Director | Donors |
| Operations Team | Funding Partners |
| Program Managers | Government |

## 8. Business Questions

1. Where do applicants drop off?
2. What factors contribute to drop off at each funnel stage?
3. What factors are most strongly associated with successful enrollment?
4. Which counties perform best?
5. Which programs have the highest enrollment?
6. Does resource availability affect enrollment?
7. Which stage of the enrollment funnel offers the greatest opportunity for improvement?
8. What operational changes could most effectively increase enrollment toward the 50% target?

## 9. Success Metrics

1. Enrollment Rate
2. Conversion Rate
3. Capacity Utilization
4. Device Allocation
5. Program Completion

## 10. Deliverables

1. Database Schema
2. Synthetic Dataset
3. SQL Scripts
4. Power BI Dashboard
5. Documentation
6. Presentation

## 11. Assumptions/Risks

1. Data is synthetic
2. Counties remain unchanged
3. Enrollment process is uncertain
4. Missing business rules

## 12. Timeline

Planning
↓
Database Schema Design/Creation
↓
Data Generation
↓
Dashboard
↓
Presentation

## 13. Team Roles

**Sunday Layefa:**
Leads on KPI definition, funnel/segmentation logic, business narrative and insights framing, stakeholder-style documentation.

**Sammy Shoka:**
Leads on database schema design, synthetic dataset generation, data cleaning pipeline, and dashboard build.

**Joint Responsibilities:**
Joint review of whether the dataset "feels" realistic against the brief's figures, and joint preparation of the final presentation.
