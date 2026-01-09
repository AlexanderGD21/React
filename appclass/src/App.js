import { useEffect, useState } from 'react';
import { getCourses, signIn } from './api/client';
import './App.css';

function App() {
  const [courses, setCourses] = useState([]);
  const [status, setStatus] = useState('loading');
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [authStatus, setAuthStatus] = useState('idle');
  const [user, setUser] = useState('');

  useEffect(() => {
    const controller = new AbortController();

    getCourses(controller.signal)
      .then((data) => {
        setCourses(data);
        setStatus('ready');
      })
      .catch((error) => {
        if (error.name !== 'AbortError') setStatus('error');
      });

    return () => controller.abort();
  }, []);

  async function handleSignIn(event) {
    event.preventDefault();
    setAuthStatus('loading');

    try {
      const session = await signIn(credentials);
      window.sessionStorage.setItem('digitaleducas_access_token', session.access);
      window.sessionStorage.setItem('digitaleducas_refresh_token', session.refresh);
      setUser(session.username || credentials.username);
      setAuthStatus('ready');
      setIsLoginOpen(false);
      setCredentials({ username: '', password: '' });
    } catch (error) {
      setAuthStatus('error');
    }
  }

  return (
    <main className="app-shell">
      <header className="hero">
        <div className="hero-topbar">
          <p className="eyebrow">Plataforma de aprendizaje</p>
          {user ? (
            <span className="welcome">Hola, {user}</span>
          ) : (
            <button className="button-secondary" type="button" onClick={() => setIsLoginOpen(true)}>
              Iniciar sesión
            </button>
          )}
        </div>
        <h1>DigitalEducas</h1>
        <p>Explora cursos y sigue construyendo tu aprendizaje.</p>
      </header>

      {isLoginOpen && (
        <section className="login-panel" aria-labelledby="login-heading">
          <div className="panel-heading">
            <h2 id="login-heading">Iniciar sesión</h2>
            <button className="close-button" type="button" onClick={() => setIsLoginOpen(false)} aria-label="Cerrar">
              ×
            </button>
          </div>
          <form onSubmit={handleSignIn}>
            <label htmlFor="username">Usuario</label>
            <input
              id="username"
              value={credentials.username}
              onChange={(event) => setCredentials({ ...credentials, username: event.target.value })}
              autoComplete="username"
              required
            />
            <label htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              value={credentials.password}
              onChange={(event) => setCredentials({ ...credentials, password: event.target.value })}
              autoComplete="current-password"
              required
            />
            {authStatus === 'error' && <p className="message-error" role="alert">Credenciales inválidas o cuenta sin verificar.</p>}
            <button className="button-primary" disabled={authStatus === 'loading'} type="submit">
              {authStatus === 'loading' ? 'Ingresando…' : 'Ingresar'}
            </button>
          </form>
        </section>
      )}

      <section aria-labelledby="courses-heading">
        <h2 id="courses-heading">Cursos disponibles</h2>
        {status === 'loading' && <p aria-live="polite">Cargando cursos…</p>}
        {status === 'error' && (
          <p className="message-error" role="alert">
            No se pudieron cargar los cursos. Verifica que la API esté disponible.
          </p>
        )}
        {status === 'ready' && courses.length === 0 && <p>Aún no hay cursos publicados.</p>}
        {status === 'ready' && courses.length > 0 && (
          <div className="course-grid">
            {courses.map((course) => (
              <article className="course-card" key={course.id}>
                {course.image && <img src={course.image} alt="" />}
                <div>
                  <h3>{course.title}</h3>
                  <p>{course.description}</p>
                  <span>{course.lessons?.length || 0} lecciones</span>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}

export default App;
