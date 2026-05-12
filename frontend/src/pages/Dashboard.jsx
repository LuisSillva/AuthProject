import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <div style={{ maxWidth: 400, margin: '100px auto', padding: 24 }}>
      <h2>Dashboard</h2>
      <p>Logged in as: <strong>{user?.email}</strong></p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}