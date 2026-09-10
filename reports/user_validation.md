# User & Stakeholder Validation Protocol — Rural Microgrid Intelligence Platform

> [!IMPORTANT]
> **Status: Validation Pending Field Trial**  
> As per project requirements, since live field trial testing with human stakeholders is scheduled for the upcoming pilot phase, results below outline the formal validation protocol. No fake or simulated user survey numbers have been fabricated.

---

### **1. Target Stakeholder Personas**

| Persona Role | Target Representative User | Primary Testing Focus |
|---|---|---|
| **Operations Staff** | Microgrid Operator | Real-time alarm handling, load shifting recommendations, and equipment controls. |
| **Microgrid Manager** | Campus Facility Director | Financial ROI, monthly bill savings, baseline vs. verified energy reduction. |
| **Technician** | Electrical / Sensor Technician | Sensor health monitoring, telemetry freshness, flatline stuck sensor diagnosis. |
| **Resident / Non-Technical User** | Student / Campus Resident | Plain-language disaggregation breakdown, simple energy conservation tips. |

---

### **2. Validation Task Protocol**

| Task # | Task Description | Target Metric / Benchmark | Expected Completion Time |
|---|---|---|---|
| **Task 1** | Identify the highest energy waste issue currently occurring on the microgrid. | Operator locates Water Pump peak tariff issue. | < 30 seconds |
| **Task 2** | Explain *why* energy usage is higher than expected between 5 PM and 7 PM. | User reads non-technical root cause description (WHAT, WHY, EVIDENCE). | < 45 seconds |
| **Task 3** | Locate and apply the recommended operational action for the water pump. | User clicks "Apply Action" on recommendation REC_WP_01. | < 30 seconds |
| **Task 4** | Check whether data feeds are current or stale. | User identifies Freshness Banner status (LIVE / STALE). | < 15 seconds |
| **Task 5** | Determine total verified monthly financial savings. | Manager locates verified cost savings (₹30,019). | < 20 seconds |

---

### **3. Evaluation Metrics & Success Criteria**
1. **Task Completion Rate**: Target ≥ 90% task success without assist.
2. **System Usability Scale (SUS)**: Target SUS score ≥ 80 / 100.
3. **Information Clarity & Trust**: Rated on 5-point Likert scale (Target ≥ 4.2 / 5.0).
4. **Accessibility Checks**: Keyboard navigation and screen-reader labels verified (formal third-party WCAG audit pending field trial).

---

### **4. Execution Plan for Field Trial**
1. Conduct 30-minute observational user sessions with 3 representatives per persona (12 total participants).
2. Record task completion time, error rates, and qualitative verbal feedback.
3. Update `reports/user_validation.md` with post-trial empirical findings upon trial completion.
