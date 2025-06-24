import React from 'react'
import { Link, NavLink } from "react-router-dom";

function Navbar() {
  return (
     <nav className="h-screen w-48 bg-gray-800 text-white p-4">
      <h1 className="text-xl font-bold mb-8">My App</h1>
      <ul className="space-y-4">
        <li>
          <NavLink to="/todo" className={({isActive}) =>`rounded-2xl delay-100 hover:text-gray-300 block px-4 py-2 ${isActive ? "bg-blue-700": "bg-gray-800"}`}>ToDo</NavLink>
        </li>
        <li>
          <NavLink to="/notes" className={({isActive}) =>`rounded-2xl delay-100 hover:text-gray-300 block px-4 py-2 ${isActive ? "bg-blue-700": "bg-gray-800"}`}>Notes</NavLink>
        </li>
      </ul>
    </nav>
  )
}

export default Navbar