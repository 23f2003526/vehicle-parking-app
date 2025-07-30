from datetime import datetime

def render_daily_reminder_html(user, new_lots_count=0):
    name = user.name or "there"
    lots_msg = (f"<p>We added <b>{new_lots_count}</b> new parking lot(s) today. "
                f"Check them out!</p>") if new_lots_count else ""
    return f"""
    <div style="font-family: Arial, sans-serif;">
      <h2>Hi {name},</h2>
      <p>Friendly reminder to book a parking spot if you need one today.</p>
      {lots_msg}
      <p><a href="http://localhost:5173">Open ParkEasy</a></p>
      <hr/>
      <small>This is an automated message sent at {datetime.now().strftime('%Y-%m-%d %H:%M')} IST.</small>
    </div>
    """

def render_monthly_report_html(user, stats):
    # total_bookings, total_spent, most_used_lot, month_label, breakdown_by_lot
    breakdown_rows = "".join(
        f"<tr><td>{row['lot']}</td><td style='text-align:right'>{row['count']}</td></tr>"
        for row in stats.get('breakdown_by_lot', [])
    )
    most_used = stats.get('most_used_lot') or '—'
    return f"""
    <div style="font-family: Arial, sans-serif;">
      <h2>Monthly Activity Report - {stats['month_label']}</h2>
      <p>Hello {user.name or 'there'}, here’s your parking activity summary.</p>
      <ul>
        <li><b>Total bookings:</b> {stats['total_bookings']}</li>
        <li><b>Total spent:</b> ₹{stats['total_spent']:.2f}</li>
        <li><b>Most used lot:</b> {most_used}</li>
      </ul>

      <h3>Bookings by Lot</h3>
      <table cellpadding="8" cellspacing="0" border="1" style="border-collapse:collapse;">
        <thead>
          <tr><th>Lot</th><th>Bookings</th></tr>
        </thead>
        <tbody>
          {breakdown_rows or '<tr><td colspan="2">No bookings this month</td></tr>'}
        </tbody>
      </table>

      <p style="margin-top:16px">Thanks for using ParkEasy!</p>
    </div>
    """
