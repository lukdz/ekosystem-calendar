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

**Syncing to Android (Google Calendar App):**
It is common for newly subscribed `.ics` calendars to be hidden and disabled by default on the mobile app, even after you've set them up on the web.

Here is how to force the calendar to sync and display on your Android device:

**1. Enable Sync in the App Settings**
1. Open the **Google Calendar app** on your Android phone.
2. Tap the **Menu** icon (three horizontal lines) in the top-left corner.
3. Scroll all the way to the bottom and tap **Settings** (the gear icon).
4. Find the Google Account where you added the `.ics` calendar.
5. If you do not see the new calendar listed under that account, tap **Show more** to reveal hidden calendars.
6. Tap the name of your newly added calendar.
7. Toggle the **Sync** switch to the **On** position. (You may also want to change the color or notifications here).

**2. Make the Calendar Visible**
1. Tap the back arrow twice to return to the main calendar view.
2. Tap the **Menu** icon (three horizontal lines) again.
3. Scroll down to your Google Account.
4. Locate the newly synced calendar and **tap the checkbox** next to it so it is filled in.
5. To force an immediate update, tap **Refresh** (often located at the top of the menu or triggered by pulling down on the main calendar screen).

*Note: Subscribed `.ics` calendars are updated by Google automatically, but they can sometimes take up to 24 hours to pull in changes made by the calendar owner.*

**Syncing to Desktop Apps:**
When you subscribe to an external `.ics` calendar via a URL, Google adds it to your web view under "Other Calendars," but **it does not automatically push that calendar to third-party apps** like Apple Calendar or Microsoft Outlook by default.

To fix this, you have to enable synchronization for that specific calendar in a somewhat hidden Google settings menu.

Here is how to force it to show up in your desktop apps:

**1. Enable Sync for the Specific Calendar**
1. Open your web browser and make sure you are logged into the Google Account that is connected to your Mac Calendar/Outlook.
2. Go to this exact, hidden Google Calendar sync settings page: **[calendar.google.com/calendar/syncselect](https://calendar.google.com/calendar/syncselect)**
3. Look under the **Shared Calendars** or **Other Calendars** section.
4. Find the `.ics` calendar you just added and **check the box** next to it.
5. Click **Save** in the bottom right corner.

**2. Refresh Your Desktop App**
Once you've told Google to actually broadcast the calendar, you need to prompt your desktop apps to fetch the new data.

**For Mac Calendar (Apple Calendar):**
* Open the Calendar app.
* Press `Command + R` on your keyboard, or go to **View > Refresh Calendars** in the top menu bar.
* *Note: It might take a minute or two for the new calendar to appear in your sidebar under your Google account.*

**For Microsoft Outlook (Mac):**
* Open Outlook and go to the Calendar view.
* Go to the **Tools** tab at the top and click **Sync** (or click the Send/Receive button).
* Alternatively, fully quit Outlook (`Command + Q`) and reopen it to force a fresh connection to Google's servers.

Once you complete these steps, the `.ics` calendar should populate right alongside your primary Google Calendar events!

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
