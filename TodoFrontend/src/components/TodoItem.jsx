import React from 'react'
import axios from '../api/axios';
import { useState } from 'react';
import { useAuth } from "../context/AuthContext";

export default function TodoItem({ todo , onUpdate}) {
  const { token } = useAuth();

  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editContent, setEditContent] = useState(todo.content);
  const handleUpdate = async () => {
  try {
    await axios.put(`/todos/${todo.id}`, {
      title: editTitle,
      content: editContent,
      completed: todo.completed,
      tag_ids: todo.tags.map(tag => tag.id)  // if you're using tags
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    setIsEditing(false);
    onUpdate();  // Optional callback to refresh todos
  } catch (err) {
    console.error("Update failed:", err);
  }
};

  const handleDelete = async () => {
  if (!window.confirm("Are you sure you want to delete this todo?")) return;

  try {
    await axios.delete(`/todos/${todo.id}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    onUpdate(); // refresh list
  } catch (err) {
    console.error("Delete failed:", err.response?.data || err.message);
  }
};

  return (
    <div className="p-4 mb-4 border rounded bg-gray-800 shadow-sm hover:shadow-md transition">
      {isEditing ? (
    <>
      <input
        className="w-full mb-2 border px-2 py-1"
        value={editTitle}
        onChange={(e) => setEditTitle(e.target.value)}
      />
      <textarea
        className="w-full mb-2 border px-2 py-1"
        value={editContent}
        onChange={(e) => setEditContent(e.target.value)}
      />
      <div className="flex space-x-2">
        <button className="bg-blue-500 text-white px-3 py-1 rounded" onClick={handleUpdate}>Save</button>
        <button className="bg-gray-500 text-white px-3 py-1 rounded" onClick={() => setIsEditing(false)}>Cancel</button>
      </div>
    </>
  ) : (
    <>
      <h2 className="text-xl font-bold">{todo.title}</h2>
      <p className="text-gray-700">{todo.content}</p>
      <p className={`mt-2 font-semibold ${todo.completed ? "text-green-600" : "text-red-500"}`}>
        {todo.completed ? "✅ Completed" : "⏳ Not Completed"}
      </p>

      {todo.tags && todo.tags.length > 0 && (
  <div className="mt-2 flex flex-wrap gap-2 p-1">
    {todo.tags.map((tag) => (
      <span
        key={tag.id}
        className="text-sm bg-blue-200 text-blue-800 px-2 py-1 rounded"
      >
        {tag.name}
      </span>
    ))}
  </div>
)}

      <div className='py-2'>
        <button className="ml-2 px-2 py-1 text-sm bg-blue-400 text-white rounded hover:bg-blue-500" onClick={() => setIsEditing(true)}>
        Edit
      </button>
      <button
  onClick={handleDelete}
  className="ml-2 px-2 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600"
>
  Delete
</button>
      </div>
    </>
  )}
    </div>
  );
}

