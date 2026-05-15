import React from 'react';
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart as RLineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

export default function Chart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={250}>
      <AreaChart data={data} margin={{ top: 16, right: 24, left: 12, bottom: 18 }}>
        <defs>
          <linearGradient id="p" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#7c3aed" stopOpacity={0.8} />
            <stop offset="95%" stopColor="#7c3aed" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid stroke="#1e293b" />
        <XAxis dataKey="date" stroke="#94a3b8" tickMargin={12} minTickGap={28} />
        <YAxis stroke="#94a3b8" tickMargin={12} width={55} />
        <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #334155' }} />
        <Area type="monotone" dataKey="value" stroke="#8b5cf6" fill="url(#p)" strokeWidth={2} />
      </AreaChart>
    </ResponsiveContainer>
  );
}

export function ComparisonChart({ strategy, benchmark }) {
  const merged = strategy.map((point, index) => ({
    date: point.date,
    strategy: point.value,
    benchmark: benchmark?.[index]?.value,
  }));

  return (
    <ResponsiveContainer width="100%" height={250}>
      <RLineChart data={merged} margin={{ top: 16, right: 24, left: 12, bottom: 18 }}>
        <CartesianGrid stroke="#1e293b" />
        <XAxis dataKey="date" stroke="#94a3b8" tickMargin={12} minTickGap={28} />
        <YAxis stroke="#94a3b8" tickMargin={12} width={55} />
        <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #334155' }} />
        <Line type="monotone" dataKey="strategy" stroke="#8b5cf6" dot={false} strokeWidth={2} />
        <Line type="monotone" dataKey="benchmark" stroke="#22c55e" dot={false} strokeWidth={2} />
      </RLineChart>
    </ResponsiveContainer>
  );
}

export function Bars({ data }) {
  return (
    <ResponsiveContainer width="100%" height={210}>
      <BarChart data={data} margin={{ top: 16, right: 24, left: 12, bottom: 18 }}>
        <CartesianGrid stroke="#1e293b" />
        <XAxis dataKey="month" stroke="#94a3b8" tickMargin={12} minTickGap={18} />
        <YAxis stroke="#94a3b8" tickMargin={12} width={50} />
        <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #334155' }} />
        <Bar dataKey="return">
          {data.map((d, i) => (
            <Cell key={i} fill={d.return >= 0 ? '#22c55e' : '#ef4444'} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

export function Drawdown({ data }) {
  return (
    <ResponsiveContainer width="100%" height={210}>
      <AreaChart data={data} margin={{ top: 16, right: 24, left: 12, bottom: 18 }}>
        <CartesianGrid stroke="#1e293b" />
        <XAxis dataKey="date" stroke="#94a3b8" tickMargin={12} minTickGap={28} />
        <YAxis stroke="#94a3b8" tickMargin={12} width={55} />
        <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #334155' }} />
        <Area type="monotone" dataKey="dd" stroke="#ef4444" fill="#7f1d1d" />
      </AreaChart>
    </ResponsiveContainer>
  );
}

export function SignalPreviewChart({ data }) {
  const sample = data?.[0] || {};
  const hasMALines = 'ma_short' in sample || 'ma_long' in sample;
  const hasPosition = 'position' in sample;

  return (
    <ResponsiveContainer width="100%" height={230}>
      <RLineChart data={data} margin={{ top: 16, right: 24, left: 12, bottom: 18 }}>
        <CartesianGrid stroke="#1e293b" />
        <XAxis dataKey="date" stroke="#94a3b8" tickMargin={12} minTickGap={28} />
        <YAxis stroke="#94a3b8" tickMargin={12} width={55} />
        {hasPosition && !hasMALines && (
          <YAxis yAxisId="signal" orientation="right" domain={[0, 1]} tickCount={2} stroke="#64748b" tickMargin={12} width={40} />
        )}
        <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #334155' }} />
        <Line type="monotone" dataKey="close" stroke="#8b5cf6" dot={false} />
        {hasMALines && <Line type="monotone" dataKey="ma_short" stroke="#22c55e" dot={false} />}
        {hasMALines && <Line type="monotone" dataKey="ma_long" stroke="#ef4444" dot={false} />}
        {hasPosition && !hasMALines && (
          <Line type="stepAfter" dataKey="position" yAxisId="signal" stroke="#22c55e" dot={false} strokeWidth={2} />
        )}
      </RLineChart>
    </ResponsiveContainer>
  );
}
