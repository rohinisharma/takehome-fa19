import React, { Component } from 'react'

class Counter extends Component {
  // YOUR CODE GOES BELOW
  constructor(props) {
    super(props);
    this.state = {
      clicks: 0

    };
  }

  increment = ()  => {
    this.setState({clicks: this.state.clicks + 1});
  }
  decrement = ()  => {
    this.setState({clicks: this.state.clicks - 1});
  }

  render() {
    return (

      <div>
        <span>{this.state.clicks}</span>
        <button onClick={this.increment}>Increment</button>
        <button onClick={this.decrement}>Decrement</button>




      </div>
    )
  }
}

export default Counter
