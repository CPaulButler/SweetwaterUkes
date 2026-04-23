---
name: update-upcoming-events
description: "Use when adding, removing, or updating upcoming events on the Sweetwater Ukes site. Triggers: 'add event', 'remove event', 'update event', 'upcoming event', 'practice at', 'event on', 'no longer happening'."
---

# Update Upcoming Events

## When to Use
- Adding a new upcoming event (practice session, gig, meeting, etc.)
- Removing a past or cancelled event
- Changing the date, time, location, or name of an existing event

## Key Rules
- **Always edit `HTMLheader.txt`** — this is the source of truth for events. Do NOT edit `site/index.html` directly unless also asked.
- **Remove past events**, including any event scheduled for today's date (today is considered past).
- Events live inside `<ul class="events-list">` in `HTMLheader.txt`.

## Event HTML Structure

Each event is an `<li>` block:

```html
<li class="event-item">
  <div class="event-name">EVENT NAME</div>
  <div class="event-details">DAY, MONTH DATE<br>H:MM AM/PM</div>
</li>
```

- Apostrophes must be HTML-encoded as `&#x27;` (e.g., `Sarah&#x27;s`).
- Day of week should be spelled out (e.g., `Thursday`).
- Use 12-hour time with AM/PM (e.g., `2:00 PM`).

## Procedure

1. Read the `<ul class="events-list">` section of `HTMLheader.txt`.
2. Identify and **remove** any `<li class="event-item">` blocks whose date is today or in the past (compare against today's date).
3. Add or update events as requested by the user.
4. Use `replace_string_in_file` with at least 3 lines of context before and after the changed block.
5. Confirm the change with a brief summary and a link to the file.
