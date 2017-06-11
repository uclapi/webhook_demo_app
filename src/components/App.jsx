import React from 'react';
import Moment from 'moment';

import BookingEvent from './App/BookingEvent';

import './App/App.scss';

function App() {
  const bookings = window.initialData.bookings;
  return (
    <div className="site-wrapper">
      <h1><strong>Room Bookings Live</strong></h1>
      <div className="booking-events">
        {bookings
          .sort((a, b) => {
            if (new Moment(a.created) > new Moment(b.created)) {
              return -1;
            }
            return 1;
          })
          .map(booking => (
            <BookingEvent
              key={`${booking.slotid}W${bookings.weeknumber}`}
              {...booking}
            />
        ))}
      </div>
    </div>
  );
}

export default App;
