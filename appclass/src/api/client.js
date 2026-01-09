const API_BASE_URL = (process.env.REACT_APP_API_URL || 'http://localhost:8000/api').replace(/\/$/, '');

export async function getCourses(signal) {
  const response = await fetch(`${API_BASE_URL}/courses/`, { signal });

  if (!response.ok) {
    throw new Error('No fue posible cargar los cursos.');
  }

  return response.json();
}

export async function signIn(credentials) {
  const response = await fetch(`${API_BASE_URL}/token/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  });
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'No fue posible iniciar sesión.');
  }

  return data;
}
