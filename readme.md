# 🔍 Talent Scout AI

**Fast + Dynamic AI Talent Scouting & Engagement Agent**

**Deccan AI Catalyst Hackathon Submission**  
**By: Shalem Raju Pobbathi**

---

### 🚀 Live Demo
**Project Site URL**: [https://huggingface.co/spaces/Shalem35/talent-scout-ai]

---

### 📋 Project Description
This AI agent takes any Job Description as input, **automatically detects the required location and requirements**, matches candidates intelligently, simulates realistic conversational outreach, calculates Match Score + Interest Score, and delivers a clean ranked shortlist with one-click CSV download.

**Just paste any Job Description and click the button** — the agent does the rest.

---

### ✨ Key Features
- Dynamic location detection (Bangalore, Hyderabad, Remote, etc.)
- Strict but fair candidate matching with detailed explanations
- Simulated natural recruiter-candidate conversations
- Combined scoring (Match Score 65% + Interest Score 35%)
- Fast response time
- One-click CSV download for immediate action

---

### 🏗️ Architecture
```mermaid
flowchart TD
    A[Job Description] --> B[Dynamic Location & Requirements Analyzer]
    B --> C[Candidate Matching Engine]
    C --> D[Top Candidates Selection]
    D --> E[Simulated Conversation Generator]
    E --> F[Final Scoring & Ranking]
    F --> G[Ranked Shortlist + CSV Download]