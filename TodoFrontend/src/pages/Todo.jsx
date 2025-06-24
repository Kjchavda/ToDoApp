import React , {useState, useEffect} from 'react'
import TodoItem from '../components/TodoItem';
import { useAuth } from '../context/AuthContext';
import axios from '../api/axios';

export default function TodoPage() {
  const { token } = useAuth();
  const [todos, setTodos] = useState([]); // initialized as array
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [availableTags, setAvailableTags] = useState([]);
  const [selectedTagIds, setSelectedTagIds] = useState([]);

  const fetchTodos = async () => {
      try {
        const res = await axios.get("/todos", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        console.log("Fetched todos:", res.data); //test
        setTodos(res.data);
      } catch (err) {
        console.error("Fetch error:", err);
        setError("Failed to load todos.");
      } finally {
        setLoading(false);
      }
    };
    
    const handleCreateTodo = async (e) => {
  e.preventDefault();

  try {
    await axios.post("/todos/create", {
      title: newTitle,
      content: newContent,
      tag_ids: selectedTagIds // you can handle tag selection later
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    setSelectedTagIds([]);

    setShowModal(false);
    setNewTitle("");
    setNewContent("");
    fetchTodos(); // refresh list
  } catch (err) {
    console.error("Error creating todo:", err.response?.data || err.message);
  }
};

  const fetchTags = async () => {
  try {
    const res = await axios.get("/tags/", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    setAvailableTags(res.data);
  } catch (err) {
    console.error("Error fetching tags:", err);
  }
};

  useEffect(() => {
    
    fetchTags();
    fetchTodos();
  }, [token]);

  const [newTitle, setNewTitle] = useState("");
  const [newContent, setNewContent] = useState("");

  


  return (
    <div className="p-6">
      <div className='flex justify-between align-middle p-4'>
      <h2 className="text-2xl font-semibold mb-1 mt-2">My Todos</h2>
      <button
  className="bg-blue-600 text-white px-5 py-2 my-1 rounded-2xl hover:bg-blue-700 border-2 border-blue-700 cursor-pointer"
  onClick={() => setShowModal(true)}
>
  + Create Todo
</button>
{showModal && (
  <div className="fixed inset-0 flex items-center justify-center z-50">
    <div className="bg-gray-800 text-black p-6 rounded shadow-lg w-full max-w-md">
      <h2 className="text-xl font-bold mb-4 mt-0">Create New Todo</h2>
      
      <form
        onSubmit={handleCreateTodo}
        className="space-y-4"
      >
        <input
          type="text"
          placeholder="Title"
          className="w-full px-4 py-2 border rounded bg-gray-700"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          required
        />
        <textarea
          placeholder="Content"
          className="w-full px-4 py-2 border rounded bg-gray-700"
          value={newContent}
          onChange={(e) => setNewContent(e.target.value)}
          required
        />
        <div>
  <label className="block font-semibold mb-1">Tags:</label>
  <div className="flex flex-wrap gap-2">
    {availableTags.map((tag) => (
      <label key={tag.id} className="flex items-center space-x-2">
        <input
          type="checkbox"
          checked={selectedTagIds.includes(tag.id)}
          onChange={(e) => {
            const checked = e.target.checked;
            setSelectedTagIds((prev) =>
              checked ? [...prev, tag.id] : prev.filter((id) => id !== tag.id)
            );
          }}
        />
        <span>{tag.name}</span>
      </label>
    ))}
  </div>
</div>

        <div className="flex justify-end space-x-2 mt-4">
          <button
            type="button"
            className="px-4 py-2 border rounded cursor-pointer bg-amber-50"
            onClick={() => setShowModal(false)}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded cursor-pointer hover:bg-blue-700"
          >
            Create
          </button>
        </div>
      </form>
    </div>
  </div>
)}
      </div>
      {loading && <p className="text-gray-500">Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {!loading && Array.isArray(todos) && todos.length === 0 && (
        <p className="text-gray-500">No todos found.</p>
      )}

      {!loading && Array.isArray(todos) &&
        todos.toReversed().map((todo) => <TodoItem key={todo.id} todo={todo} onUpdate={fetchTodos}  />)}
    </div>
  );
}


