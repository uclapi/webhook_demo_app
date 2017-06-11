import React, { Component } from 'react';
import { Paper } from 'material-ui';
import Moment from 'moment';

import './BookingEvent/styles.scss';


class BookingEvent extends Component {
  render() {
    const creationTime = new Moment(this.props.created);
    const bookingStart = new Moment(this.props.start_time);
    const bookingEnd = new Moment(this.props.end_time);
    const bookingDay = bookingStart.format('ddd, DD/MM/YYYY');
    return (
      <Paper className="booking-event">
        <p>{this.props.roomname}</p>
        <p>{this.props.description}</p>
        <Choose>
          <When condition={this.props.added}>
            <p style={{ color: 'green' }}>Added</p>
          </When>
          <Otherwise>
            <p style={{ color: 'red' }}>Removed</p>
          </Otherwise>
        </Choose>
        <p>
          <span>{bookingDay}</span>
          <br />
          <span>{`${bookingStart.format('HH:mm')}-${bookingEnd.format('HH:mm')}`}</span>
        </p>
        <p>{this.props.contact}</p>
        <p>{creationTime.fromNow()}</p>
      </Paper>
    );
  }
}


export default BookingEvent;
