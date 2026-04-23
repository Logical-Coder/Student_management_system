import { useEffect, useState } from "react";
import axios from "axios";
import ApiTester from "./ApiTester";

export default function App() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const [formData, setFormData] = useState({
    student_name: "",
    roll_number: "",
    date_of_birth: "",
    gender: "male",
    class_room: "",
  });

  const API_BASE_URL = "http://127.0.0.1:8000/api";

  const fetchStudents = async () => {
    try {
      setLoading(true);
      setMessage("");
      const response = await axios.get(`${API_BASE_URL}/Students/`);
      setStudents(response.data.data || response.data);
      setMessage("Students fetched successfully");
    } catch (error) {
      console.error(error);
      setMessage("Failed to fetch students");
    } finally {
      setLoading(false);
    }
  };

  const createStudent = async (e) => {
    e.preventDefault();

    try {
      setMessage("");

      const payload = {
        student_name: formData.student_name,
        roll_number: formData.roll_number,
        date_of_birth: formData.date_of_birth,
        gender: formData.gender,
        class_room: Number(formData.class_room),
      };

      const response = await axios.post(`${API_BASE_URL}/Students/`, payload, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      console.log(response.data);
      setMessage("Student created successfully");

      setFormData({
        student_name: "",
        roll_number: "",
        date_of_birth: "",
        gender: "male",
        class_room: "",
      });

      fetchStudents();
    } catch (error) {
      console.error(error.response?.data || error.message);
      setMessage("Failed to create student");
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  const [activeTab, setActiveTab] = useState("students");

  return (
    <div style={styles.page}>
      {/* Tab Navigation */}
      <div style={styles.tabBar}>
        <button
          id="tab-students"
          onClick={() => setActiveTab("students")}
          style={{
            ...styles.tabBtn,
            ...(activeTab === "students" ? styles.tabBtnActive : {}),
          }}
        >
          🎓 Student Management
        </button>
        <button
          id="tab-api-tester"
          onClick={() => setActiveTab("api-tester")}
          style={{
            ...styles.tabBtn,
            ...(activeTab === "api-tester" ? styles.tabBtnActive : {}),
          }}
        >
          ⚡ API Tester
        </button>
      </div>

      {/* API Tester Tab */}
      {activeTab === "api-tester" && <ApiTester />}

      {/* Students Tab */}
      {activeTab === "students" && (
        <div style={styles.studentsTab}>
          <h1 style={{ color: "#e2e8f0", marginTop: 0 }}>Student Management</h1>

          <div style={styles.message}>{message}</div>

          <div style={styles.container}>
            <div style={styles.formSection}>
              <h2>Add Student</h2>

              <form onSubmit={createStudent} style={styles.form}>
                <input
                  type="text"
                  name="student_name"
                  placeholder="Student Name"
                  value={formData.student_name}
                  onChange={handleChange}
                  required
                  style={styles.input}
                />

                <input
                  type="text"
                  name="roll_number"
                  placeholder="Roll Number"
                  value={formData.roll_number}
                  onChange={handleChange}
                  required
                  style={styles.input}
                />

                <input
                  type="date"
                  name="date_of_birth"
                  value={formData.date_of_birth}
                  onChange={handleChange}
                  style={styles.input}
                />

                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  style={styles.input}
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>

                <input
                  type="number"
                  name="class_room"
                  placeholder="Class Room ID"
                  value={formData.class_room}
                  onChange={handleChange}
                  required
                  style={styles.input}
                />

                <button type="submit" style={styles.button}>
                  Create Student
                </button>
              </form>
            </div>

            <div style={styles.listSection}>
              <div style={styles.listHeader}>
                <h2>Students List</h2>
                <button onClick={fetchStudents} style={styles.button}>
                  Refresh
                </button>
              </div>

              {loading ? (
                <p>Loading...</p>
              ) : (
                <table style={styles.table}>
                  <thead>
                    <tr>
                      <th style={styles.th}>ID</th>
                      <th style={styles.th}>Name</th>
                      <th style={styles.th}>Roll Number</th>
                      <th style={styles.th}>DOB</th>
                      <th style={styles.th}>Gender</th>
                    </tr>
                  </thead>
                  <tbody>
                    {students.map((student) => (
                      <tr key={student.id}>
                        <td style={styles.td}>{student.id}</td>
                        <td style={styles.td}>{student.student_name}</td>
                        <td style={styles.td}>{student.roll_number}</td>
                        <td style={styles.td}>{student.date_of_birth}</td>
                        <td style={styles.td}>{student.gender}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  page: {
    padding: "0",
    fontFamily: "'Inter', 'Segoe UI', Arial, sans-serif",
    background: "#0f172a",
    minHeight: "100vh",
    color: "#e2e8f0",
  },
  tabBar: {
    display: "flex",
    gap: "4px",
    padding: "16px 20px 0",
    background: "#0f172a",
    borderBottom: "1px solid #1e293b",
  },
  tabBtn: {
    padding: "10px 22px",
    border: "none",
    borderRadius: "8px 8px 0 0",
    background: "transparent",
    color: "#64748b",
    fontWeight: "600",
    fontSize: "14px",
    cursor: "pointer",
    transition: "all 0.2s",
    letterSpacing: "0.3px",
  },
  tabBtnActive: {
    background: "#1e293b",
    color: "#38bdf8",
    borderBottom: "2px solid #38bdf8",
  },
  message: {
    marginBottom: "15px",
    color: "green",
    fontWeight: "bold",
  },
  container: {
    display: "flex",
    gap: "20px",
    alignItems: "flex-start",
  },
  formSection: {
    width: "30%",
    border: "1px solid #ccc",
    padding: "16px",
    borderRadius: "8px",
  },
  listSection: {
    width: "70%",
    border: "1px solid #ccc",
    padding: "16px",
    borderRadius: "8px",
    overflowX: "auto",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  input: {
    padding: "10px",
    fontSize: "14px",
  },
  button: {
    padding: "10px 14px",
    fontSize: "14px",
    cursor: "pointer",
  },
  listHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "10px",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
  },
  th: {
    border: "1px solid #ccc",
    padding: "10px",
    textAlign: "left",
    backgroundColor: "#f5f5f5",
  },
  td: {
    border: "1px solid #ccc",
    padding: "10px",
  },
};