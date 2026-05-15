import React from 'react';

export default function Card({ title, children, className = '' }) {
  return (
    <section className={`card ${className}`}>
      <h3>{title}</h3>
      {children}
    </section>
  );
}
