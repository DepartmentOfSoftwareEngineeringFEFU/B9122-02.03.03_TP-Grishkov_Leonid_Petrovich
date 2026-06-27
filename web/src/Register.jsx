import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from './api';

function Register() {
  const [form, setForm] = useState({ username: '', password: '', name: '', phone: '', email: '' });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('register/', form);
      setSuccess('Регистрация успешна! Сейчас вы будете перенаправлены на страницу входа.');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError(err.response?.data?.error || 'Ошибка регистрации');
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2>Регистрация</h2>
        {error && <p style={styles.error}>{error}</p>}
        {success && <p style={styles.success}>{success}</p>}
        <form onSubmit={handleSubmit}>
          <input style={styles.input} name="username" placeholder="Логин" onChange={handleChange} required />
          <input style={styles.input} name="password" type="password" placeholder="Пароль" onChange={handleChange} required />
          <input style={styles.input} name="name" placeholder="ФИО или организация" onChange={handleChange} required />
          <input style={styles.input} name="phone" placeholder="Телефон" onChange={handleChange} />
          <input style={styles.input} name="email" placeholder="Email" onChange={handleChange} />
          <button style={styles.button} type="submit">Зарегистрироваться</button>
        </form>
        <p style={styles.link}>
          Уже есть аккаунт? <Link to="/login">Войти</Link>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: { display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#f0f2f5' },
  card: { backgroundColor: '#fff', padding: '30px', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)', width: '360px' },
  input: { width: '100%', padding: '10px', marginBottom: '12px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '14px', boxSizing: 'border-box' },
  button: { width: '100%', padding: '12px', backgroundColor: '#0067B8', color: '#fff', border: 'none', borderRadius: '4px', fontSize: '16px', cursor: 'pointer' },
  error: { color: 'red', marginBottom: '10px' },
  success: { color: 'green', marginBottom: '10px' },
  link: { textAlign: 'center', marginTop: '15px', fontSize: '14px' },
};

export default Register;