This summary is designed for a technical implementation agent (such as an LLM or developer) to build the automation. It outlines the logic, security requirements, and architectural decisions without including the specific code.

---

### **Project Brief: Waste Disposal iCal Generator**

**Objective:**  
Automate the extraction of a garbage collection schedule from a specific municipal API and convert it into a valid iCalendar (`.ics`) format for subscription via Google Calendar and iOS.

---

#### **1. Data Source (Ekosystem Wrocław API)**
*   **Endpoint:** `https://ekosystem.wroc.pl/wp-admin/admin-ajax.php`
*   **Method:** `POST`
*   **Payload (Data-Raw):**
    *   `action`: `waste_disposal_form_get_schedule_direct`
    *   `id_numeru`: `[SECRET_ID_NUMERU]`
    *   `id_ulicy`: `[SECRET_ID_ULICY]`
*   **Response Format:** JSON list containing dates (YYYY-MM-DD) and waste types in Polish (e.g., "Bio", "Szkło", "Tworzywa sztuczne i metale").

#### **2. Security & Privacy Architecture**
*   **Hosting:** The script should run on a headless runner (e.g., GitHub Actions) on a weekly schedule (Cron).
*   **Secrets Management:** The `id_numeru` and `id_ulicy` are PII (Personally Identifiable Information) as they pinpoint a home address. They must be stored as environment variables/secrets and never hardcoded.
*   **Integration Method:** **"The Pull Method."** 
    *   To avoid granting a script write-access to the primary Google Calendar, the script will generate an `.ics` file.
    *   The file will be hosted at a static, unguessable URL (e.g., a Secret Gist or a hashed filename in a private repo).
    *   The user will subscribe to this URL in Google Calendar/iOS. This "sandboxes" the automation.

#### **3. Functional Requirements**
*   **Parsing & Localization:**
    *   Map Polish waste types to friendly English equivalents with emojis (e.g., "Szkło" → "Garbage: Glass 🟢").
    *   Handle "All Day" event formatting.
*   **Notification Logic:**
    *   The script must inject a `VALARM` component into each event set for 2 hours before the event start.
    *   Events should be set to "All Day" to ensure they appear correctly at the top of the calendar.
*   **Consistency:**
    *   The script must ensure the generated UID for each event is stable (based on the date and waste type) so that calendar clients do not create duplicates when the file is refreshed.

#### **4. Workflow Execution**
1.  **Trigger:** Weekly automated run (e.g., Monday 05:00 AM).
2.  **Fetch:** Call the Ekosystem API using secrets.
3.  **Generate:** Process the JSON into a standardized iCalendar string.
4.  **Publish:** Overwrite the existing `garbage_schedule.ics` file at the hosted location.
5.  **Subscribe:** Provide the user with the "Raw" URL of the file for 1-time subscription in their calendar app.

#### **5. Key Parameters for Implementation**
*   **Language:** Python 3.x
*   **Primary Libraries:** `requests` (API calls), `ics` or `icalendar` (RFC 5545 compliance).
*   **Environment Variables needed:** `STREET_ID`, `HOUSE_ID`.