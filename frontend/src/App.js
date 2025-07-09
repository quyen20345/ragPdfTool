import './App.css';
import axios from 'axios';
import { useState, useEffect } from 'react'; // la 2 React Hooks: quan ly state(trang thai du lieu) trong component va xu ly side effects(goi api, dk su kien,...)

function App() {
  const [people, setPeople] = useState([]); 
  useEffect(()=> {
    axios.get('/api').then(res => setPeople(res.data));
  }, [])

  return people.map((p, index) => {
    return <p key={index}>{p.id} - {p.name} - {p.age}</p>
  });
  
}

export default App;
