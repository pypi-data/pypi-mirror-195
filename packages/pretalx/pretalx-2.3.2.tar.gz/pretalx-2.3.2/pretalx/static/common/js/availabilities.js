document.addEventListener("DOMContentLoaded", function() {
  "use strict"

  $("input.availabilities-editor-data").each(function() {
    var data_field = $(this)
    var data = JSON.parse(data_field.attr("value"))

    var editor = $('<div class="availabilities-editor">')
    editor.attr("data-name", data_field.attr("name"))
    data_field.after(editor)
    editor.before($(`<div class="availabilities-tz-hint">${data.event.timezone}</div>`))

    function save_events() {
      data = {
        availabilities: editor.fullCalendar("clientEvents").map(function(e) {
          if (e.allDay) {
            return {
              start: e.start.format("YYYY-MM-DD HH:mm:ss"),
              end: e.end.format("YYYY-MM-DD HH:mm:ss"),
            }
          } else {
            return {
              start: e.start.toISOString(),
              end: e.end.toISOString(),
            }
          }
        }),
      }
      data_field.attr("value", JSON.stringify(data))
    }

    var editable = !Boolean(data_field.attr("disabled"))

    let slotDuration = data_field.attr("resolution")
    slotDuration = slotDuration || "00:30:00"
    var events = data.availabilities.map(function(e) {
      e.start = moment(e.start).tz(data.event.timezone)
      e.end = moment(e.end).tz(data.event.timezone)

      if (e.start.format("HHmmss") == 0 && e.end.format("HHmmss") == 0) {
        e.allDay = true
      }

      return e
    })
    let localeData = document.querySelector("#calendar-locale")
    const locale = localeData ? localeData.dataset.locale : "en"
    editor.fullCalendar({
      views: {
        agendaVariableDays: {
          type: "agenda",
          duration: {
            days:
              moment(data.event.date_to).diff(
                moment(data.event.date_from),
                "days"
              ) + 1,
          },
        },
      },
      defaultView: "agendaVariableDays",
      defaultDate: data.event.date_from,
      visibleRange: {
        start: data.event.date_from,
        end: data.event.date_to,
      },
      events: events,
      nowIndicator: false,
      navLinks: false,
      header: false,
      timeFormat: "H:mm",
      slotDuration: slotDuration,
      slotLabelFormat: "H:mm",
      scrollTime: "09:00:00",
      selectable: editable,
      locale: locale,
      selectHelper: true,
      select: function(start, end) {
        var wasInDeleteMode = false
        editor.fullCalendar("clientEvents").forEach(function(e) {
          if (e.className.indexOf("delete") >= 0) {
            wasInDeleteMode = true
          }
          e.className = ""
          editor.fullCalendar("updateEvent", e)
        })

        if (wasInDeleteMode) {
          editor.fullCalendar("unselect")
          return
        }

        var eventData = {
          start: start,
          end: end,
        }
        editor.fullCalendar("renderEvent", eventData, true)
        editor.fullCalendar("unselect")
        save_events()
      },
      eventResize: save_events,
      eventDrop: save_events,
      editable: editable,
      selectOverlap: false,
      eventOverlap: false,
      eventColor: "#00DD00",
      eventClick: function(calEvent, jsEvent, view) {
        if (!editable) {
          return
        }

        if (calEvent.className.indexOf("delete") >= 0) {
          editor.fullCalendar("removeEvents", function(searchEvent) {
            return searchEvent._id === calEvent._id
          })
          save_events()
        } else {
          editor.fullCalendar("clientEvents").forEach(function(e) {
            if (e._id == calEvent._id) {
              e.className = "delete"
            } else {
              e.className = ""
            }
            editor.fullCalendar("updateEvent", e)
          })
        }
      },
    })
  })
})
