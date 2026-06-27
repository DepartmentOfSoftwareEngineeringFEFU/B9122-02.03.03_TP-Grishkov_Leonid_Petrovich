import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from './api';

function Dashboard() {
  const [activeTab, setActiveTab] = useState('requests');
  const [requests, setRequests] = useState([]);
  const [orders, setOrders] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editReq, setEditReq] = useState(null);
  const navigate = useNavigate();

  const fetchRequests = async () => {
    try {
      const resp = await api.get('requests/?my=true');
      setRequests(resp.data.filter(r => r.status !== 'deleted'));
    } catch (e) {
      console.error(e);
    }
  };

  const fetchOrders = async () => {
    try {
      const resp = await api.get('orders/?my=true');
      setOrders(resp.data);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchRequests();
    fetchOrders();
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  const handleDelete = async (id) => {
    if (window.confirm('Удалить заявку?')) {
      await api.patch(`requests/${id}/`, { status: 'deleted' });
      fetchRequests();
    }
  };

  const statusLabels = {
    new: 'Новая', in_review: 'На согласовании', approved: 'Согласована',
    rejected: 'Отклонена', deleted: 'Удалена',
    pending: 'В очереди', in_progress: 'В производстве', completed: 'Завершён',
    closed: 'Закрыт', cancelled: 'Отменён',
  };

  return (
    
    

    <div style={styles.container}>
      <div style={{ backgroundColor: '#0067B8', color: '#fff', padding: '12px 24px', marginBottom: '20px', borderRadius: '8px' }}>
        <h1 style={{ fontSize: '20px', margin: 0 }}>ООО «Экструзионное оборудование»</h1>
        <p style={{ fontSize: '14px', margin: '5px 0 0', opacity: 0.8 }}>Портал клиента</p>
      </div>

      <div style={styles.header}>
        <h2>Личный кабинет</h2>
        <button onClick={handleLogout} style={styles.logoutBtn}>Выйти</button>
      </div>

      

      <div style={styles.tabs}>
        <button
          style={activeTab === 'requests' ? styles.activeTab : styles.tab}
          onClick={() => setActiveTab('requests')}
        >
          Мои заявки
        </button>
        <button
          style={activeTab === 'orders' ? styles.activeTab : styles.tab}
          onClick={() => setActiveTab('orders')}
        >
          Мои заказы
        </button>
      </div>

      {activeTab === 'requests' && (
        <div>
          <button onClick={() => { setEditReq(null); setShowForm(true); }} style={styles.addBtn}>
            + Новая заявка
          </button>
          <table style={styles.table}>
            <thead>
              <tr>
                <th>№</th><th>Изделие</th><th>Кол-во</th><th>Срок</th><th>Статус</th><th></th>
              </tr>
            </thead>
            <tbody>
              {  requests.length === 0 ? (
                <tr><td colSpan={6} style={{ textAlign: 'center', color: '#999' }}>Нет данных</td></tr>
              ) : (           
              requests.map(r => (
                <tr key={r.id}>
                  <td>{r.id}</td>
                  <td>{r.product_name || '—'}</td>
                  <td>{r.quantity || '—'}</td>
                  <td>{r.desired_deadline || '—'}</td>
                  <td>{statusLabels[r.status] || r.status}</td>
                  <td>
                    {(r.status === 'new' || r.status === 'in_review') && (
                      <>
                        <button
                          onClick={() => { setEditReq(r); setShowForm(true); }}
                          style={{ padding: '4px 10px', marginRight: '5px', backgroundColor: '#0067B8', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '13px' }}
                        >
                          Ред.
                        </button>
                        <button
                          onClick={() => handleDelete(r.id)}
                          style={{ padding: '4px 10px', backgroundColor: '#dc3545', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '13px' }}
                        >
                          Удал.
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              )))}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === 'orders' && (
        <table style={styles.table}>
          <thead>
            <tr>
              <th>№</th><th>Изделие</th><th>Кол-во</th><th>Сумма</th><th>Статус</th><th>Дата</th>
            </tr>
          </thead>
          <tbody>
            {orders.length === 0 ? (
                <tr><td colSpan={6} style={{ textAlign: 'center', color: '#999' }}>Нет данных</td></tr>
              ) : (
            orders.map(o => (
              <tr key={o.id}>
                <td>{o.id}</td>
                <td>{o.product_name || '—'}</td>
                <td>{o.quantity}</td>
                <td>{o.total_price}</td>
                <td>{statusLabels[o.status] || o.status}</td>
                <td>{o.accepted_date}</td>
              </tr>
            )))}
          </tbody>
        </table>
      )}

      {showForm && (
        <RequestForm
          req={editReq}
          onClose={() => { setShowForm(false); setEditReq(null); }}
          onSave={() => { setShowForm(false); setEditReq(null); fetchRequests(); }}
        />
      )}
    </div>
  );
}

function RequestForm({ req, onClose, onSave }) {
  const [form, setForm] = useState({
    description: req?.description || '',
    product_name: req?.product_name || '',
    quantity: req?.quantity || 1,
    desired_deadline: req?.desired_deadline || '',
  });
  const [error, setError] = useState('');

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      if (req) {
        await api.put(`requests/${req.id}/`, form);
      } else {
        await api.post('requests/', form);
      }
      onSave();
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка сохранения');
    }
  };

  return (
    <div style={styles.modal}>
      <div style={styles.modalContent}>
        <h3>{req ? 'Редактировать заявку' : 'Новая заявка'}</h3>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <form onSubmit={handleSubmit}>
          <textarea style={styles.input} name="description" placeholder="Описание" value={form.description} onChange={handleChange} required rows={3} />
          <input style={styles.input} name="product_name" placeholder="Наименование изделия" value={form.product_name} onChange={handleChange} />
          <input style={styles.input} name="quantity" type="number" placeholder="Количество" value={form.quantity} onChange={handleChange} />
          <input style={styles.input} name="desired_deadline" type="date" value={form.desired_deadline} onChange={handleChange} />
          <div style={{ display: 'flex', gap: '10px' }}>
            <button style={styles.button} type="submit">Сохранить</button>
            <button style={{ ...styles.button, backgroundColor: '#999' }} type="button" onClick={onClose}>Отмена</button>
          </div>
        </form>
      </div>
    </div>
  );
}

const styles = {
  container: { maxWidth: '900px', margin: '0 auto', padding: '20px' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  logoutBtn: { padding: '8px 16px', backgroundColor: '#dc3545', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  tabs: { display: 'flex', gap: '0', marginBottom: '20px', borderBottom: '2px solid #ddd' },
  tab: { padding: '10px 20px', border: 'none', backgroundColor: 'transparent', cursor: 'pointer', fontSize: '16px', color: '#666' },
  activeTab: { padding: '10px 20px', border: 'none', borderBottom: '3px solid #0067B8', backgroundColor: 'transparent', cursor: 'pointer', fontSize: '16px', color: '#0067B8', fontWeight: 'bold' },
  addBtn: { padding: '8px 16px', marginBottom: '15px', backgroundColor: '#0067B8', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  table: { width: '100%', borderCollapse: 'collapse' },
  input: { width: '100%', padding: '8px', marginBottom: '10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '14px', boxSizing: 'border-box' },
  button: { padding: '10px 20px', backgroundColor: '#0067B8', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '14px' },
  modal: { position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center' },
  modalContent: { backgroundColor: '#fff', padding: '25px', borderRadius: '8px', width: '450px' },
};

export default Dashboard;