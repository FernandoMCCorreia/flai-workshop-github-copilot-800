import React, { useState, useEffect } from 'react';

function Users() {
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;
  const teamsApiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;

  useEffect(() => {
    console.log('Users Component - Fetching from API:', apiUrl);
    
    // Fetch teams first to map team_id to team names
    Promise.all([
      fetch(apiUrl).then(response => {
        console.log('Users Component - Response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      }),
      fetch(teamsApiUrl).then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
    ])
      .then(([usersData, teamsData]) => {
        console.log('Users Component - Raw data received:', usersData);
        // Handle both paginated (.results) and plain array responses
        const usersArray = usersData.results || usersData;
        const teamsArray = teamsData.results || teamsData;
        
        // Create a map of team_id to team name
        const teamsMap = {};
        teamsArray.forEach(team => {
          teamsMap[team._id] = team.name;
        });
        
        console.log('Users Component - Processed users:', usersArray);
        console.log('Users Component - Teams map:', teamsMap);
        
        setUsers(Array.isArray(usersArray) ? usersArray : []);
        setTeams(teamsMap);
        setLoading(false);
      })
      .catch(error => {
        console.error('Users Component - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [apiUrl, teamsApiUrl]);

  if (loading) return <div className="container mt-4"><p>Loading users...</p></div>;
  if (error) return <div className="container mt-4"><p className="text-danger">Error: {error}</p></div>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Users</h2>
      <div className="table-responsive">
        {users.length === 0 ? (
          <p className="text-muted">No users found.</p>
        ) : (
          <table className="table table-striped table-hover">
            <thead className="table-dark">
              <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Team</th>
                <th>Created At</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user._id}>
                  <td><strong>{user.username}</strong></td>
                  <td>{user.email}</td>
                  <td>
                    {user.team_id ? (
                      <span className="badge bg-primary">{teams[user.team_id] || 'Unknown Team'}</span>
                    ) : (
                      <span className="badge bg-secondary">No Team</span>
                    )}
                  </td>
                  <td>{user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default Users;
