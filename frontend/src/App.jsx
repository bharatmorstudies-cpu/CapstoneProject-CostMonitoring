import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { DollarSign, Cloud, Layers, Activity } from 'lucide-react';

function App() {
  const [summaryData, setSummaryData] = useState([]);
  const [timelineData, setTimelineData] = useState([]);
  const [activeFilter, setActiveFilter] = useState('ALL');
  const [loading, setLoading] = useState(true);

  const fetchTelemetryCanvas = async () => {
    setLoading(true);
    try {
      const summaryRes = await fetch('http://localhost:8000/api/costs/summary');
      const timelineRes = await fetch('http://localhost:8000/api/costs/timeline');
      
      const summaryResult = await summaryRes.json();
      const timelineResult = await timelineRes.json();

      setSummaryData(summaryResult.data || []);
      setTimelineData(timelineResult.data || []);
    } catch (err) {
      console.error("Presentation layer failed connecting with data paths:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTelemetryCanvas();
  }, []);

  // Compute calculated macro state attributes from operational data matrices
  const filteredSummary = summaryData.filter(item => activeFilter === 'ALL' || item.provider === activeFilter);
  const totalBurnUSD = filteredSummary.reduce((sum, item) => sum + item.total_spending, 0);
  const totalMonitoredServices = filteredSummary.length;

  return (
    <div style={{ padding: '24px', fontFamily: 'system-ui, sans-serif', backgroundColor: '#f8fafc', minHeight: '100vh', color: '#0f172a' }}>
      
      {/* Visual Navigation Header Layout Component */}
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px', borderBottom: '1px solid #e2e8f0', paddingBottom: '20px' }}>
        <div>
          <h1 style={{ fontSize: '26px', fontWeight: 'bold', margin: 0 }}>Multi-Cloud Infrastructure Cost Panel</h1>
          <p style={{ margin: '4px 0 0 0', color: '#64748b', fontSize: '14px' }}>Real-time full-stack resource expenditure management workspace</p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          {['ALL', 'AWS', 'GCP'].map(provider => (
            <button
              key={provider}
              onClick={() => setActiveFilter(provider)}
              style={{
                padding: '8px 16px',
                borderRadius: '6px',
                border: '1px solid #cbd5e1',
                cursor: 'pointer',
                fontWeight: '600',
                backgroundColor: activeFilter === provider ? '#2563eb' : 'white',
                color: activeFilter === provider ? 'white' : '#475569',
                transition: 'all 0.2s'
              }}
            >
              {provider} Metrics
            </button>
          ))}
        </div>
      </header>

      {/* Strategic Analytical Metric Grid Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '20px', marginBottom: '32px' }}>
        <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.05)', border: '1px solid #e2e8f0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#64748b', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>Calculated Monthly Burn <DollarSign size={18} color="#2563eb" /></div>
          <div style={{ fontSize: '28px', fontWeight: 'bold' }}>${totalBurnUSD.toFixed(2)}</div>
        </div>
        <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.05)', border: '1px solid #e2e8f0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#64748b', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>Active Cloud Tenants <Cloud size={18} color="#0284c7" /></div>
          <div style={{ fontSize: '28px', fontWeight: 'bold' }}>{activeFilter === 'ALL' ? '2 Providers' : `1 (${activeFilter})`}</div>
        </div>
        <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.05)', border: '1px solid #e2e8f0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#64748b', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>Tracked Services Count <Layers size={18} color="#16a34a" /></div>
          <div style={{ fontSize: '28px', fontWeight: 'bold' }}>{totalMonitoredServices} Services</div>
        </div>
      </div>

      {/* Core Graphical Visual Charts Layout blocks */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '32px' }}>
        
        {/* Chart 1: Expenditure By Node Category Groupings */}
        <div style={{ backgroundColor: 'white', padding: '24px', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
          <h3 style={{ margin: '0 0 20px 0', fontSize: '16px', fontWeight: '600' }}>Infrastructure Cost Outlays by Resource Type</h3>
          <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
              <BarChart data={filteredSummary}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="service" stroke="#94a3b8" fontSize={11} />
                <YAxis stroke="#94a3b8" fontSize={11} />
                <Tooltip />
                <Legend />
                <Bar dataKey="total_spending" name="Total Expenditure ($)" fill="#2563eb" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Cross Cloud Trend Timeline Lines */}
        <div style={{ backgroundColor: 'white', padding: '24px', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
          <h3 style={{ margin: '0 0 20px 0', fontSize: '16px', fontWeight: '600' }}>Daily Cross-Cloud Historical Spending Trend</h3>
          <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
              <LineChart data={timelineData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="date" stroke="#94a3b8" fontSize={11} />
                <YAxis stroke="#94a3b8" fontSize={11} />
                <Tooltip />
                <Legend />
                {(activeFilter === 'ALL' || activeFilter === 'AWS') && <Line type="monotone" dataKey="AWS" stroke="#2563eb" strokeWidth={2.5} dot={{ r: 4 }} />}
                {(activeFilter === 'ALL' || activeFilter === 'GCP') && <Line type="monotone" dataKey="GCP" stroke="#10b981" strokeWidth={2.5} dot={{ r: 4 }} />}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

      {/* Relational Analytical Ledger Data Grid View */}
      <div style={{ backgroundColor: 'white', padding: '24px', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
        <h3 style={{ margin: '0 0 16px 0', fontSize: '16px', fontWeight: '600' }}>Resource Asset Financial Ledger Logs</h3>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid #f1f5f9', color: '#64748b', fontSize: '13px' }}>
              <th style={{ padding: '12px' }}>Cloud Engine Provider</th>
              <th style={{ padding: '12px' }}>Resource Target Node Component</th>
              <th style={{ padding: '12px', textAlign: 'right' }}>Aggregated Outlays Allocation</th>
            </tr>
          </thead>
          <tbody>
            {filteredSummary.map((row, idx) => (
              <tr key={idx} style={{ borderBottom: '1px solid #f1f5f9', fontSize: '14px', color: '#334155' }}>
                <td style={{ padding: '12px' }}>
                  <span style={{
                    backgroundColor: row.provider === 'AWS' ? '#eff6ff' : '#ecfdf5',
                    color: row.provider === 'AWS' ? '#1e40af' : '#065f46',
                    padding: '4px 8px', borderRadius: '4px', fontSize: '11px', fontWeight: 'bold'
                  }}>{row.provider}</span>
                </td>
                <td style={{ padding: '12px', fontWeight: '500' }}>{row.service}</td>
                <td style={{ padding: '12px', fontWeight: 'bold', textAlign: 'right', color: '#0f172a' }}>${row.total_spending.toFixed(2)} {row.currency}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  );
}

export default App;
