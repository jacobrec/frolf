import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import Login from './views/login'
import Home from './views/main'

export default class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      tok: null
    }
  }
  
  render() {
    if (this.state.tok) {
      return <Home />
    }
    return <Login />
  }
}
