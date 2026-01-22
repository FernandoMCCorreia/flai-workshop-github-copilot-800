import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;

  useEffect(() => {
    console.log('Workouts Component - Fetching from API:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        console.log('Workouts Component - Response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts Component - Raw data received:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Workouts Component - Processed workouts:', workoutsData);
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Workouts Component - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [apiUrl]);

  if (loading) return <div className="container mt-4"><p>Loading workouts...</p></div>;
  if (error) return <div className="container mt-4"><p className="text-danger">Error: {error}</p></div>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Workout Suggestions</h2>
      <div className="table-responsive">
        {workouts.length === 0 ? (
          <p className="text-muted">No workouts found.</p>
        ) : (
          <table className="table table-striped table-hover">
            <thead className="table-dark">
              <tr>
                <th>ID</th>
                <th>Workout Name</th>
                <th>Description</th>
                <th>User ID</th>
                <th>Duration (min)</th>
                <th>Difficulty</th>
                <th>Date Suggested</th>
              </tr>
            </thead>
            <tbody>
              {workouts.map((workout) => (
                <tr key={workout.id}>
                  <td>{workout.id}</td>
                  <td><strong>{workout.name}</strong></td>
                  <td>{workout.description}</td>
                  <td>{workout.user}</td>
                  <td>{workout.duration}</td>
                  <td><span className="badge bg-info">{workout.difficulty_level}</span></td>
                  <td>{new Date(workout.date_suggested).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default Workouts;
