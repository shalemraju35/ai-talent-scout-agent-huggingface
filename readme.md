# 🔍 Talent Scout AI

**Fast + Dynamic Location Version**

**AI-Powered Talent Scouting & Engagement Agent**  
**Deccan AI Catalyst Hackathon Submission**  
**By: Shalem Raju Pobbathi**

---

### 📋 One-Page Write-up

**Problem Solved**  
Recruiters spend hours manually screening profiles and chasing candidates for interest. This agent automates the entire process — from Job Description input to candidate matching, simulated conversational outreach, and delivering a ready-to-use ranked shortlist.

**Approach**  
- Fully dynamic location detection from the JD (Bangalore, Hyderabad, Remote, etc.)
- Strict but fair candidate scoring with explainability
- Simulated natural conversations (only for top 5 candidates for speed)
- Combined Match Score + Interest Score system
- Optimized for fast response time

**Key Features**
- Dynamic location awareness
- Simulated conversational outreach
- Ranked shortlist with detailed explanations
- One-click CSV download
- Clean and fast Gradio interface

**Scoring Logic**
- **Match Score (65%)**: Location match, experience fit, skills alignment
- **Interest Score (35%)**: Generated from realistic simulated conversation
- **Final Score** = 0.65 × Match Score + 0.35 × Interest Score

---

### 🏗️ Architecture

```mermaid
flowchart TD
    A[Job Description Input] --> B[Dynamic Location Analyzer]
    B --> C[Candidate Matching Engine]
    C --> D[Top 5 Selection]
    D --> E[Simulated Conversation Generator]
    E --> F[Final Scoring & Ranking]
    F --> G[Ranked Shortlist + CSV Download]