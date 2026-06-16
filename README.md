# ♻️ Ekosystem Wrocław Calendar (Privacy-Focused)

This project automatically scrapes the garbage collection schedule from [Ekosystem Wrocław](https://ekosystem.wroc.pl/gospodarowanie-odpadami/harmonogram-wywozu-odpadow/) and generates subscribable `.ics` (iCalendar) files for your calendar apps (Google Calendar, Apple Calendar, Outlook, etc.).

It is designed to run entirely via **GitHub Actions**, keeping your main branch clean by publishing the calendars to an isolated data branch. It's completely free and fully automated.

---

## 🚀 How to Fork and Set Up Your Own

Follow these steps to set up your own automated, privacy-protected garbage collection calendar.

### Step 1: Fork the Repository
Click the **Fork** button at the top right of this page to copy this repository into your own GitHub account.

### Step 2: Generate your `LOCATIONS_JSON`
You need to populate a list of addresses.

1. Clone your forked repository to your local machine.
2. Go to [Ekosystem Wrocław](https://ekosystem.wroc.pl/gospodarowanie-odpadami/harmonogram-wywozu-odpadow/?), search for an address on the side panel, and check the schedule for that street.
3. Copy the URL from your browser's address bar once the schedule loads. It should look something like this:
   `https://ekosystem.wroc.pl/gospodarowanie-odpadami/harmonogram-wywozu-odpadow/?lokalizacja=27717&ulica=744`
4. Run the "add location" script, passing the copied URL as an argument in quotes:
   ```bash
   python add_location.py "https://ekosystem.wroc.pl/gospodarowanie-odpadami/harmonogram-wywozu-odpadow/?lokalizacja=27717&ulica=744"
   ```
   The script will print out a message like: `This location is assigned to key: a8f39c1b`. **Remember this identifier!** Your final calendar URL will contain `calendar_a8f39c1b.ics`.

### Step 3: Add the GitHub Secret
1. Go to your forked repository on GitHub.
2. Navigate to **Settings** > **Secrets and variables** > **Actions**.
3. Click **New repository secret**.
4. Set the Name to `LOCATIONS_JSON`.
5. Open your locally generated `locations.json` file, copy all of its contents, and paste it into the Secret value box. Click Add.

### Step 4: Enable GitHub Actions
1. Go to the **Actions** tab in your repository and click **"I understand my workflows, go ahead and enable them"**.

### Step 5: Run the Workflow
1. Still in the **Actions** tab, select the **Generate Calendar** workflow on the left.
2. Click the **Run workflow** dropdown on the right, and click **Run workflow**.
3. Wait a minute or two for the action to finish generating your calendars and pushing them to the `public` branch.

### Step 6: Subscribe to your Calendar!
Find your specific calendar using the identifier assigned to you in Step 2.

To get your calendar subscription URL:
1. Go to your repository homepage on GitHub.
2. Switch the branch from `master` to `public` using the branch dropdown menu at the top left.
3. Click on your specific calendar file (e.g., `calendar_a8f39c1b.ics`).
4. Click the **Raw** button at the top right of the file view.
5. Copy the URL from your browser's address bar. 

It will look something like this:
`https://raw.githubusercontent.com/<your-github-username>/<repository-name>/refs/heads/public/calendar_<your_identifier>.ics`

Now, add this URL to your preferred calendar app as a "Subscribed Calendar". Because it is a subscription, it will automatically stay up-to-date as the GitHub Action runs every week!

#### 📅 Google Calendar
1. Open [calendar.google.com](https://calendar.google.com) on a computer.
2. On the left side, next to "Other calendars", click the **+** button.
3. Select **From URL**.
4. Paste your calendar URL and click **Add calendar**. *(It will automatically sync to the Google Calendar app on your phone).*

**Notifications:**
* **The Default:** Google automatically blocks the `.ics` creator's reminders.
* **Best Fix:** Go to Google Calendar on a web browser, open **Settings**, select the subscribed calendar under "Settings for other calendars," and manually add your own custom **Event notifications**.

#### 🍏 Apple Calendar (iPhone/iPad)
1. Open the **Settings** app on your device.
2. Scroll down and tap **Calendar** > **Accounts** > **Add Account**.
3. Tap **Other** > **Add Subscribed Calendar**.
4. Paste your calendar URL, tap **Next**, and then **Save**.

**Notifications:**
* **The Default:** Apple silences the calendar creator's reminders by default.
* **Best Fix:** Force Apple to use the original reminders. On iOS, go to *Settings > Calendar > Accounts > Subscribed Calendars*, select the calendar, and toggle off **Remove Alarms**.

#### 🍏 Apple Calendar (Mac)
1. Open the **Calendar** app.
2. In the menu bar, click **File** > **New Calendar Subscription...**
3. Paste your calendar URL and click **Subscribe**.
4. *Recommended:* Set the "Auto-refresh" option to **Every day**.

**Notifications:**
* **The Default:** Apple silences the calendar creator's reminders by default.
* **Best Fix:** Right-click the calendar, click *Get Info*, and uncheck **Ignore alerts**.

#### ✉️ Microsoft Outlook (Web)
1. Open Outlook Calendar on the web.
2. Click **Add calendar** in the left sidebar.
3. Select **Subscribe from web**.
4. Paste your calendar URL, give it a name, and click **Import**.

**Notifications:**
* **The Default:** Outlook strips out the creator's reminders and provides no way to add custom rules specifically for that subscription.
* **Best Fix:** If you absolutely need reminders, don't use the URL subscription feature. Instead, **download the `.ics` file** and manually import it into Outlook (*File > Open & Export > Import/Export*). *Note: The calendar will no longer auto-update.*

---

## 🛠️ Modifying the Script
If you want to change the notification behavior, look inside `generate_ical.py` at the `create_calendar` function. By default, it creates an "All Day" event and sets an alarm/reminder for **18:00 the evening before** collection day.

## 📜 License
This project is open-source. Feel free to use and modify it!
