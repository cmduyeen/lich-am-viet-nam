import ICAL from './node_modules/ical.js/dist/ical.js';

export function readCalendar(raw) {
  const calendar = new ICAL.Component(ICAL.parse(raw));
  if (calendar.name !== 'vcalendar') throw new Error('Expected VCALENDAR');
  const seen = new Set();
  const events = calendar.getAllSubcomponents('vevent').map(component => {
    const event = new ICAL.Event(component);
    if (!event.startDate.isDate || !event.endDate.isDate) throw new Error('Expected all-day DATE');
    if (seen.has(event.uid)) throw new Error(`Duplicate UID: ${event.uid}`);
    seen.add(event.uid);
    const start = event.startDate.toString(), end = event.endDate.toString();
    if (Date.parse(end) - Date.parse(start) !== 86400000) throw new Error('Wrong event boundary');
    if (!event.summary) throw new Error('Empty summary');
    return {id:event.uid, title:event.summary, start, end, allDay:true,
      color:component.getFirstPropertyValue('color') || '#D94B3E',
      extendedProps:{description:event.description, identity:component.getFirstPropertyValue('x-lunar-event-id'),
        sequence:component.getFirstPropertyValue('sequence') || 0}};
  });
  return {name:calendar.getFirstPropertyValue('x-wr-calname'), events};
}
