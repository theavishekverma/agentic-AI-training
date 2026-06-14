import { useState } from 'react'
import './App.css'

function App() {
  const [employees, setEmployees] = useState([])
  const [formData, setFormData] = useState({ name: '', age: '', department: '' })
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const API_URL = 'http://localhost:8000'

  // Fetch all employees
  const fetchEmployees = async () => {
    setLoading(true)
    setMessage('')
    try {
      const response = await fetch(`${API_URL}/employees/`)
      const data = await response.json()
      setEmployees(data.employees || [])
      setMessage('✓ Employees fetched successfully')
    } catch (error) {
      setMessage(`✗ Error fetching employees: ${error.message}`)
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  // Create new employee
  const createEmployee = async (e) => {
    e.preventDefault()
    if (!formData.name || !formData.age || !formData.department) {
      setMessage('✗ Please fill all fields')
      return
    }

    setLoading(true)
    setMessage('')
    try {
      const response = await fetch(`${API_URL}/employees/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: formData.name,
          age: parseInt(formData.age),
          department: formData.department,
        }),
      })

      const data = await response.json()
      if (response.ok) {
        setMessage('✓ Employee created successfully')
        setFormData({ name: '', age: '', department: '' })
        await fetchEmployees()
      } else {
        setMessage(`✗ Error: ${data.detail || 'Unknown error'}`)
      }
    } catch (error) {
      setMessage(`✗ Error creating employee: ${error.message}`)
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  // Get single employee
  const getEmployee = async (id) => {
    setLoading(true)
    setMessage('')
    try {
      const response = await fetch(`${API_URL}/employees/${id}`)
      const data = await response.json()
      if (response.ok) {
        setMessage(`✓ Employee: ${JSON.stringify(data.employee)}`)
      } else {
        setMessage(`✗ Error: ${data.detail || 'Employee not found'}`)
      }
    } catch (error) {
      setMessage(`✗ Error fetching employee: ${error.message}`)
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Employee Management System</h1>
      <p className="subtitle">Test CORS with FastAPI Backend</p>

      {/* Create Employee Form */}
      <div className="card">
        <h2>Create New Employee</h2>
        <form onSubmit={createEmployee}>
          <input
            type="text"
            placeholder="Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          />
          <input
            type="number"
            placeholder="Age"
            value={formData.age}
            onChange={(e) => setFormData({ ...formData, age: e.target.value })}
          />
          <input
            type="text"
            placeholder="Department"
            value={formData.department}
            onChange={(e) => setFormData({ ...formData, department: e.target.value })}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Creating...' : 'Create Employee'}
          </button>
        </form>
      </div>

      {/* Fetch Employees Button */}
      <div className="card">
        <h2>All Employees</h2>
        <button onClick={fetchEmployees} disabled={loading}>
          {loading ? 'Loading...' : 'Fetch Employees'}
        </button>
        {employees.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Age</th>
                <th>Department</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {employees.map((emp) => (
                <tr key={emp.id}>
                  <td>{emp.id}</td>
                  <td>{emp.name}</td>
                  <td>{emp.age}</td>
                  <td>{emp.department}</td>
                  <td>
                    <button onClick={() => getEmployee(emp.id)} disabled={loading}>
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Message Display */}
      {message && <div className={`message ${message.includes('✓') ? 'success' : 'error'}`}>{message}</div>}
    </div>
  )
}

export default App
