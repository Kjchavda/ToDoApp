import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css'
import Login from './pages/Login';
import Layout from './Layout';
import Todo from './pages/Todo';
import Notes from './pages/Notes';

function App() {

  return (
    <>
      <BrowserRouter>
        <Routes>
          
          <Route path="/login" element={<Login />} />
          <Route path='/' element={<Layout/>}>
            <Route path='/todo' element={<Todo />}/>
            <Route path='/notes' element={<Notes />}/>
          </Route>
      </Routes>
    </BrowserRouter>
  
    </>
  )
}

export default App
