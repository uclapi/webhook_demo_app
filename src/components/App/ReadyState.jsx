import React, { Component } from 'react';
import { RefreshIndicator } from 'material-ui';

const styles = {
  container: {
    position: 'relative',
  },
  refresh: {
    display: 'inline-block',
    position: 'relative',
  },
};

class ReadyState extends Component {
  render() {
    return (
      <span style={styles.container}>
        <Choose>
          <When condition={this.props.webhookReadyState === 1}>
            <span>Connected</span>
          </When>
          <Otherwise>
            <RefreshIndicator
              size={20}
              left={-5}
              top={0}
              status="loading"
              style={styles.refresh}
            />
            <span>Connecting</span>
          </Otherwise>
        </Choose>
      </span>
    );
  }
}


export default ReadyState;
