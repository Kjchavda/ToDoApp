import React from 'react'
import Navbar from './components/Navbar';
import { Outlet } from 'react-router-dom';

function Layout() {
  return (
    <>
        <div className='flex h-screen'>
          <aside><Navbar/></aside>
        <main className='flex-1 p-4 bg-gray-700 overflow-auto'><Outlet/></main>
        </div>
    </>
  )
}

export default Layout