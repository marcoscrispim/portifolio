import logo from './logo.svg';
import './App.css';
import axios from "axios";
import {useEffect,useState} from "react";
function App() {
  const [ boby, setbody] = useState('');
  useEffect(() => {
    axios.get('http://localhost:8000/get_data/')
    .then((response) => {
      console.log(response);
    })
  }, []);
  return (
    <div >
      tomate
    </div>
  );
}

export default App;
