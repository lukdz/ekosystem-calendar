# ♻️ Ekosystem Wrocław Calendar (Privacy-Focused)

This project automatically scrapes the garbage collection schedule from [Ekosystem Wrocław](https://ekosystem.wroc.pl/gospodarowanie-odpadami/harmonogram-wywozu-odpadow/) and generates subscribable `.ics` (iCalendar) files for your calendar apps (Google Calendar, Apple Calendar, Outlook, etc.).

It is designed to run entirely via **GitHub Actions** and publish the calendars via **GitHub Pages**, completely free and fully automated.

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
   The script will print out a message like: `This location is assigned to key: a8f39c1b`. **Remember this identifier!** Your final calendar URL will be `calendar_a8f39c1b.ics`.

### Step 3: Add the GitHub Variable
1. Go to your forked repository on GitHub.
2. Navigate to **Settings** > **Secrets and variables** > **Actions** > **Variables**.
3. Click **New repository variable**.
4. Set the Name to `LOCATIONS_JSON`.
5. Open your locally generated `locations.json` file, copy all of its contents, and paste it into the value box. Click Add.

### Step 4: Enable GitHub Pages & Actions
1. Go to **Settings** > **Pages**.
2. Under "Build and deployment", change the Source to **GitHub Actions**.
3. Go to the **Actions** tab in your repository and click **"I understand my workflows, go ahead and enable them"**.

### Step 5: Run the Workflow
1. Still in the **Actions** tab, select the **Generate Calendar** workflow on the left.
2. Click the **Run workflow** dropdown on the right, and click **Run workflow**.
3. Wait a minute or two for the action to finish and deploy your site to GitHub Pages.

### Step 6: Subscribe to your Calendar!
Find your specific calendar using the identifier assigned to you in Step 2.

The URL will look like this:
`https://<your-github-username>.github.io/<repository-name>/calendar_<your_identifier>.ics`

*Example: `https://lukdz.github.io/ekosystem-calendar/calendar_a8f39c1b.ics`*

Now, add this URL to your preferred calendar app as a "Subscribed Calendar". Because it is a subscription, it will automatically stay up-to-date as the GitHub Action runs every week!

#### 📅 Google Calendar
1. Open [calendar.google.com](https://calendar.google.com) on a computer.
2. On the left side, next to "Other calendars", click the **+** button.
3. Select **From URL**.
4. Paste your calendar URL and click **Add calendar**. *(It will automatically sync to the Google Calendar app on your phone).*

#### 🍏 Apple Calendar (iPhone/iPad)
1. Open the **Settings** app on your device.
2. Scroll down and tap **Calendar** > **Accounts** > **Add Account**.
3. Tap **Other** > **Add Subscribed Calendar**.
4. Paste your calendar URL, tap **Next**, and then **Save**.

#### 🍏 Apple Calendar (Mac)
1. Open the **Calendar** app.
2. In the menu bar, click **File** > **New Calendar Subscription...**
3. Paste your calendar URL and click **Subscribe**.
4. *Recommended:* Set the "Auto-refresh" option to **Every day**.

#### ✉️ Microsoft Outlook (Web)
1. Open Outlook Calendar on the web.
2. Click **Add calendar** in the left sidebar.
3. Select **Subscribe from web**.
4. Paste your calendar URL, give it a name, and click **Import**.

---

## 🛠️ Modifying the Script
If you want to change the notification behavior, look inside `generate_ical.py` at the `create_calendar` function. By default, it creates an "All Day" event and sets an alarm/reminder for **18:00 the evening before** collection day.

## 📜 License
This project is open-source. Feel free to use and modify it!
