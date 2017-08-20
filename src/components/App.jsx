import React from 'react';
import Moment from 'moment';
import { CSSTransitionGroup } from 'react-transition-group';

import BookingEvent from './App/BookingEvent';
import ReadyState from './App/ReadyState';

import './App/App.scss';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      webhookReadyState: 0,
      bookings: window.initialData.bookings,
    };
    this.handleWebSocketReceive.bind(this);
    this.startWSConnection.bind(this);
  }

  componentDidMount() {
    this.startWSConnection();
  }

  startWSConnection() {
    const isLocal = (location.hostname === 'localhost' || location.hostname === '127.0.0.1');

    const socket = isLocal ? new WebSocket(`ws://${window.location.host}`) : new WebSocket(`wss://${window.location.host}`);
    socket.addEventListener('open', () => {
      this.setState({ webhookReadyState: socket.readyState });
    });
    socket.addEventListener('message', (event) => {
      this.handleWebSocketReceive(event.data);
    });
    socket.addEventListener('close', () => {
      this.setState({ webhookReadyState: socket.readyState });
      setTimeout(() => { this.startWSConnection(); }, 5000);
    });
  }

  handleWebSocketReceive(data) {
    const result = JSON.parse(data);
    this.setState(
        { bookings: [...this.state.bookings, result.new_booking] },
    );
  }

  render() {
    return (
      <div className="site-wrapper">
        <h1><strong>Room Bookings Live</strong></h1>
        <ReadyState
          webhookReadyState={this.state.webhookReadyState}
        />
        <div className="booking-events">
          <CSSTransitionGroup
            transitionName="newBooking"
            transitionEnterTimeout={500}
            transitionLeaveTimeout={300}
          >
            {this.state.bookings
              .sort((a, b) => {
                if (new Moment(a.created) > new Moment(b.created)) {
                  return -1;
                }
                return 1;
              })
              .map(booking => (
                <BookingEvent
                  key={`${booking.slotid}W${booking.weeknumber}`}
                  {...booking}
                />
            ))}
          </CSSTransitionGroup>
        </div>
      </div>
    );
  }
}

export default App;
